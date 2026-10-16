# Day 15 — Collections II: Set, Map, HashMap Internals, Queue/Deque/PriorityQueue, and Immutable Collections

**Phase:** Core Java  
**Primary theme:** Pick the right Set/Map/Queue, understand how hashing drives them, and expose state through immutable collections.  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-unique-normalize`, `task-02-frequency-map`, `task-03-priority-queue-lab`, `task-04-immutable-copy`  
**Instruction alignment:** Maps to the Day 15 entry of the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21 (no Spring today)

## Overview

Lists answer "what is at position i"; Sets and Maps answer "is it present, and what is associated with it" in (amortized) constant time. Almost every service uses a `Map` as a cache, index, counter, or lookup table, and a `Queue` to schedule work. Production bugs here are subtle: a mutable key that vanishes from a `HashMap`, a `HashSet` that keeps "duplicates" because `hashCode` was not overridden, a shared mutable list leaking out of a getter.

Today you build a mental model of hashing and trees, learn the idiomatic Map API, use heaps and deques, and finish with immutable collections - the safest way to share data. Interviews: *how does HashMap work*, *HashMap vs TreeMap vs LinkedHashMap*, *why must equals and hashCode agree*, *PriorityQueue complexity*, *List.of vs Collections.unmodifiableList*.

## Day roadmap

1. Set, Map, and how HashMap works
2. Queue, Deque, ArrayDeque, and PriorityQueue
3. Immutable collections, copies, and unmodifiable views
4. Interview angles
5. Common mistakes & debugging
6. Further reading, glossary, answers

### Set, Map, and how HashMap works

#### What it is

A `Set<E>` holds unique elements; a `Map<K,V>` associates unique keys with values (`Set<K>` is basically a `Map<K,Boolean>`). Implementations: **Hash*** (O(1) average, no order), **LinkedHash*** (O(1) with insertion or access order), **Tree*** (red-black tree, O(log n), sorted by `Comparable`/`Comparator`, navigation methods like `floor`, `ceiling`, `headMap`). **HashMap internals (conceptual):** `hash = key.hashCode()` is spread (`h ^ h>>>16`) and masked to a bucket index in a power-of-two table; the bucket holds a linked list (or, since Java 8, a red-black tree when a bucket exceeds 8 entries and the table has >= 64 slots); lookup compares hash then `equals`. When size exceeds `capacity * loadFactor` (default 0.75) the table doubles and entries are redistributed.

#### Why it exists / why it matters

Constant-time lookup is what makes caches, dedup, counting, joins, and indexing practical. Understanding the mechanics explains the contract: **equal objects must have equal hash codes**, hash codes of keys must not change while stored, and a poor `hashCode` collapses a map into O(n) (or O(log n) with treeification) behavior - also a denial-of-service vector with attacker-chosen keys.

#### Pros and cons

**Pros**

- `HashMap`/`HashSet`: O(1) average put/get/contains
- `LinkedHashMap`: predictable iteration (insertion/access order), LRU cache via `removeEldestEntry`
- `TreeMap`/`TreeSet`: sorted views and range queries
- Rich Map API (`merge`, `compute*`, `getOrDefault`) removes boilerplate

**Cons / tradeoffs**

- `HashMap` iteration order is unspecified and may change across runs/versions
- Mutable or poorly hashed keys break lookups
- `TreeMap` needs consistent ordering and rejects `null` keys; not thread-safe (`HashMap` too - use `ConcurrentHashMap`)

#### What happens without it / when misused

If you override `equals` but not `hashCode`, two equal objects usually land in different buckets: `set.contains(new Point(1,2))` returns false although an equal point is inside. If you **mutate a field used in `hashCode`** after inserting the object as a key, `map.get(key)` returns null and the entry is unreachable (a memory leak). Resizing under concurrent writes in a plain `HashMap` can corrupt it or lose data. A `TreeSet<String>` built with `String.CASE_INSENSITIVE_ORDER` treats `"A"` and `"a"` as the same element - by design. Iterating a `HashMap` and asserting an order in tests yields flaky tests.

#### Syntax and rules

- Contract: `a.equals(b)` => `a.hashCode() == b.hashCode()`; hashCode must be stable while in a hash structure.
- Defaults: initial capacity 16, load factor 0.75; presize with `new HashMap<>(expected * 4 / 3 + 1)` for big maps.
- `put` returns the previous value; `putIfAbsent`, `getOrDefault(k, d)`, `containsKey`.
- Counting idiom: `counts.merge(word, 1, Integer::sum);`
- Grouping idiom: `groups.computeIfAbsent(key, k -> new ArrayList<>()).add(item);`
- `HashSet.add` returns `false` when the element was already present - handy for duplicate detection.
- `TreeMap` navigation: `firstKey`, `floorKey(k)`, `ceilingEntry(k)`, `subMap`, `descendingMap`.
- Iterate entries with `for (Map.Entry<K,V> e : map.entrySet())` - not `keySet()` + `get`.

#### Examples

**Example 1.1 — Tiny — counting with merge, grouping with computeIfAbsent**

```java
Map<String, Integer> counts = new HashMap<>();
for (String w : "to be or not to be".split(" ")) counts.merge(w, 1, Integer::sum);
System.out.println(new TreeMap<>(counts));     // {be=2, not=1, or=1, to=2}

Map<Integer, List<String>> byLen = new TreeMap<>();
for (String w : List.of("a", "bb", "cc", "d")) byLen.computeIfAbsent(w.length(), k -> new ArrayList<>()).add(w);
System.out.println(byLen);                     // {1=[a, d], 2=[bb, cc]}
```

**Example 1.2 — Tiny — the mutable key disaster**

```java
class Key { int id; Key(int id) { this.id = id; }
    @Override public boolean equals(Object o) { return o instanceof Key k && k.id == id; }
    @Override public int hashCode() { return id; } }

Map<Key, String> m = new HashMap<>();
Key k = new Key(1);
m.put(k, "x");
k.id = 2;                                   // hashCode changed after insertion
System.out.println(m.get(k));               // null  (looks in bucket 2)
System.out.println(m.get(new Key(1)));      // null  (bucket 1 has it, but equals() now fails)
System.out.println(m.size());               // 1 - entry is orphaned
```

**Example 1.3 — Medium — a bounded LRU cache with LinkedHashMap**

```java
import java.util.*;

public class LruCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;

    public LruCache(int capacity) {
        super(16, 0.75f, true);           // true = access order
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }

    public static void main(String[] args) {
        LruCache<String, Integer> c = new LruCache<>(2);
        c.put("a", 1); c.put("b", 2);
        c.get("a");                       // a becomes most recent
        c.put("c", 3);                    // evicts b
        System.out.println(c.keySet());   // [a, c]
    }
}
```

#### Quick checks

1. What must hold between `equals` and `hashCode`?
2. What happens to `HashMap.get` if a key's hash-relevant field changes after insertion?
3. When does a HashMap bucket turn into a tree?
4. Which Map would you use for an LRU cache and why?

### Queue, Deque, ArrayDeque, and PriorityQueue

#### What it is

A `Queue<E>` models waiting work (`offer`/`poll`/`peek`; `add`/`remove`/`element` throw on failure). A `Deque<E>` (double-ended queue) adds `offerFirst/Last`, `pollFirst/Last`, `push/pop` and serves as both queue **and stack**. `ArrayDeque` is the fast resizable-array implementation (no nulls). `PriorityQueue` is a binary **min-heap**: `peek`/`poll` return the smallest element by natural order or the supplied `Comparator`; `offer`/`poll` are O(log n), `peek` O(1). Its iterator and `toString` are **not** sorted.

#### Why it exists / why it matters

Queues decouple producers from consumers (task scheduling, BFS, rate buffers); deques implement undo stacks, sliding windows, and palindromes; priority queues power schedulers, top-K, Dijkstra, and merge-K-sorted. `java.util.Stack` and `LinkedList` as a stack are legacy choices - use `ArrayDeque`.

#### Pros and cons

**Pros**

- `ArrayDeque`: fast, compact queue/stack
- `PriorityQueue`: O(log n) priority scheduling; top-K in O(n log k)
- Method pairs let you choose exceptions (`remove`) or special values (`poll`)
- `Deque` unifies stack and queue operations

**Cons / tradeoffs**

- `PriorityQueue` iteration order is not sorted; `contains`/`remove(Object)` are O(n)
- `ArrayDeque` and `PriorityQueue` reject `null`
- Neither is thread-safe (see `LinkedBlockingQueue`, `PriorityBlockingQueue`)

#### What happens without it / when misused

Using `java.util.Stack` (synchronized `Vector`) is slow and exposes list methods. Printing a `PriorityQueue` and expecting sorted output is a classic mistake; only repeated `poll()` yields order. A comparator with inconsistent ordering corrupts the heap property silently. Calling `remove()`/`element()` on an empty queue throws `NoSuchElementException`, while `poll()`/`peek()` return `null`. Using `PriorityQueue<int[]>` without a comparator throws `ClassCastException` (arrays are not `Comparable`).

#### Syntax and rules

- Prefer `offer/poll/peek` for bounded or possibly-empty queues; `add/remove/element` when emptiness is a bug.
- Stack idiom: `Deque<Integer> st = new ArrayDeque<>(); st.push(1); st.pop();` (push/pop work at the head).
- Queue idiom: `offer` at tail, `poll` from head.
- Max-heap: `new PriorityQueue<>(Comparator.reverseOrder())`.
- Top-K smallest: keep a **max**-heap of size K, evict the largest when it grows beyond K.
- `PriorityQueue(int initialCapacity, Comparator<? super E>)`; capacity 1+ required.

#### Examples

**Example 2.1 — Tiny — stack and queue on one ArrayDeque class**

```java
Deque<String> stack = new ArrayDeque<>();
stack.push("a"); stack.push("b");
System.out.println(stack.pop());     // b
Queue<String> q = new ArrayDeque<>();
q.offer("x"); q.offer("y");
System.out.println(q.poll());        // x
```

**Example 2.2 — Tiny — PriorityQueue is a heap, not a sorted list**

```java
PriorityQueue<Integer> pq = new PriorityQueue<>(List.of(5, 1, 4, 2, 3));
System.out.println(pq.peek());       // 1
StringBuilder sb = new StringBuilder();
while (!pq.isEmpty()) sb.append(pq.poll()).append(' ');
System.out.println(sb);              // 1 2 3 4 5   (only poll() order is sorted)
```

**Example 2.3 — Medium — balanced brackets with a Deque and top-K with a bounded heap**

```java
import java.util.*;

public class QueueDemo {
    static boolean balanced(String s) {
        Deque<Character> st = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            switch (c) {
                case '(', '[', '{' -> st.push(c);
                case ')', ']', '}' -> {
                    if (st.isEmpty()) return false;
                    char o = st.pop();
                    if ("([{".indexOf(o) != ")]}".indexOf(c)) return false;
                }
                default -> { }
            }
        }
        return st.isEmpty();
    }

    static List<Integer> kSmallest(List<Integer> xs, int k) {
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
        for (int x : xs) { maxHeap.offer(x); if (maxHeap.size() > k) maxHeap.poll(); }
        List<Integer> out = new ArrayList<>(maxHeap);
        Collections.sort(out);
        return out;
    }

    public static void main(String[] a) {
        System.out.println(balanced("{[()]}") + " " + balanced("(]"));   // true false
        System.out.println(kSmallest(List.of(9, 1, 8, 2, 7), 2));        // [1, 2]
    }
}
```

#### Quick checks

1. What is the complexity of `PriorityQueue.offer`, `poll`, `peek`, `contains`?
2. Why prefer `ArrayDeque` over `Stack`?
3. How do you get a max-heap from `PriorityQueue`?
4. Difference between `remove()` and `poll()` on a Queue?

### Immutable collections, copies, and unmodifiable views

#### What it is

Java offers three different things people call "read-only": (1) **immutable collections** created by `List.of`, `Set.of`, `Map.of`, `Map.ofEntries`, and the *copy* factories `List.copyOf`, `Set.copyOf`, `Map.copyOf` - they cannot change and reject `null`; (2) **unmodifiable views** from `Collections.unmodifiableList(x)` - they throw on mutation but **reflect later changes to the wrapped collection**; (3) **fixed-size** adapters like `Arrays.asList`. Immutable collections are shallow: the elements themselves may still be mutable.

#### Why it exists / why it matters

Shared mutable state is the root of many bugs: a getter that returns the internal list lets any caller corrupt your object (**representation exposure**), and a constructor that stores the caller's list lets the caller change it later. Immutable copies make objects safe to share across threads without locks and easy to reason about. Record-like domain objects (`Order`, `Money`, `Roster`) are typically built from defensive immutable copies.

#### Pros and cons

**Pros**

- Thread-safe by construction and easy to reason about
- `copyOf` is cheap when the source is already immutable (returns it)
- `List.of`/`Set.of`/`Map.of` are compact and null-hostile (fail fast)
- Clear API contract: callers cannot mutate your state

**Cons / tradeoffs**

- Mutation attempts fail at **runtime** with `UnsupportedOperationException`, not at compile time
- `Set.of`/`Map.of` iteration order is unspecified and randomized per JVM run; duplicates in `Set.of(...)`/`Map.of(...)` throw `IllegalArgumentException`
- Shallow immutability: contents may still be mutable objects

#### What happens without it / when misused

`Collections.unmodifiableList(internal)` returned from a getter looks safe, yet your own later `internal.add(...)` shows up in the caller's "read-only" list (and concurrent modification can throw CME in their iteration). Storing the constructor argument directly (`this.names = names`) lets the caller mutate your object. `List.of("a", null)` throws `NullPointerException`; `Set.of("a", "a")` throws `IllegalArgumentException`; `List.copyOf(listWithNull)` throws NPE. Assuming `Map.of` keeps insertion order causes flaky tests.

#### Syntax and rules

- Defensive copy in: `this.names = List.copyOf(names);` (NPE if `names` or an element is null).
- Defensive copy out: return the already-immutable field directly, or `List.copyOf(internalMutable)`.
- `Map.of(k1, v1, ...)` up to 10 pairs; use `Map.ofEntries(Map.entry(k, v), ...)` beyond that.
- `stream.toList()` (Java 16) returns an unmodifiable list (nulls allowed); `Collectors.toUnmodifiableList()` rejects nulls.
- Test with `assertThatThrownBy(() -> list.add(x)).isInstanceOf(UnsupportedOperationException.class)` - obtain the list *before* the lambda.
- Wither pattern: `public Roster withName(String n)` returns a new instance instead of mutating.

#### Examples

**Example 3.1 — Tiny — immutable vs view**

```java
List<String> base = new ArrayList<>(List.of("a"));
List<String> view = Collections.unmodifiableList(base);
List<String> copy = List.copyOf(base);
base.add("b");
System.out.println(view);   // [a, b]  - the view reflects the change
System.out.println(copy);   // [a]     - the copy does not
// view.add("c");           // UnsupportedOperationException
```

**Example 3.2 — Tiny — fail-fast factories**

```java
try { List.of("a", null); } catch (NullPointerException e) { System.out.println("NPE"); }
try { Set.of("a", "a"); }    catch (IllegalArgumentException e) { System.out.println("IAE"); }
try { Map.of("k", 1, "k", 2); } catch (IllegalArgumentException e) { System.out.println("IAE"); }
// NPE
// IAE
// IAE
```

**Example 3.3 — Medium — an immutable value object with defensive copies and a wither**

```java
import java.util.*;

public final class Team {
    private final String name;
    private final List<String> members;

    public Team(String name, Collection<String> members) {
        this.name = Objects.requireNonNull(name);
        this.members = List.copyOf(members);               // defensive copy in, immutable
    }

    public List<String> members() { return members; }       // safe to expose

    public Team withMember(String who) {
        List<String> next = new ArrayList<>(members);
        next.add(who);
        return new Team(name, next);                         // new instance, original untouched
    }

    public static void main(String[] args) {
        List<String> src = new ArrayList<>(List.of("ann"));
        Team t = new Team("core", src);
        src.add("mallory");                                  // does not leak in
        Team t2 = t.withMember("bob");
        System.out.println(t.members() + " " + t2.members()); // [ann] [ann, bob]
    }
}
```

#### Quick checks

1. What is the difference between `Collections.unmodifiableList(x)` and `List.copyOf(x)`?
2. Which factory call throws `IllegalArgumentException` and which throws `NullPointerException`: `Set.of(1, 1)` / `List.of(1, null)`?
3. Is a `List.of(new StringBuilder("a"))` deeply immutable?
4. Why return `List.copyOf(internal)` from a getter instead of `internal`?

## Interview angles

**Q: Explain how HashMap works internally.**

Key's `hashCode` is spread and masked to a bucket index; the bucket is a linked list (a red-black tree after 8 collisions at capacity >= 64). `get` finds the bucket then uses `equals`. When size exceeds capacity x 0.75 the table doubles and entries are rehashed. Average O(1), worst O(log n) with treeification.

**Q: HashMap vs LinkedHashMap vs TreeMap vs ConcurrentHashMap?**

Hash: fastest, unordered. LinkedHash: insertion/access order, LRU. Tree: sorted, O(log n), range queries. ConcurrentHashMap: thread-safe, no null keys/values, atomic compute/merge.

**Q: Why must equals and hashCode be overridden together?**

Hash collections locate by hash first; unequal hashes for equal objects make lookups fail and sets hold duplicates.

**Q: When would a PriorityQueue be the right tool?**

Task scheduling by priority, top-K, merging sorted streams, Dijkstra - anywhere you repeatedly need the min/max of a changing set.

**Q: How do you make a class's collection fields safe to expose?**

Defensive copy in the constructor with `List.copyOf`, return immutable fields (or copies), avoid exposing views over mutable internals.

**Q: What happens when two different keys have the same hashCode?**

They share a bucket; `equals` disambiguates; many collisions degrade performance (treeified buckets bound the damage to O(log n)).

## Common mistakes & debugging

- Overriding `equals` without `hashCode` (or the reverse) - `HashSet` shows duplicates, `contains` fails.
- Mutating an object after using it as a `HashMap` key or `HashSet` element.
- Asserting `HashMap`/`HashSet`/`Set.of` iteration order in tests (use `containsExactlyInAnyOrder`).
- Treating `PriorityQueue.toString()`/iteration as sorted.
- Exposing internal collections from getters or storing constructor arguments without copying.
- Using `Stack`/`LinkedList` instead of `ArrayDeque`, or `get(k) == null` checks where `merge`/`computeIfAbsent` is cleaner.

## Further reading

- Javadoc: `java.util.HashMap` (implementation notes), `LinkedHashMap`, `TreeMap`, `PriorityQueue`, `ArrayDeque`, `Collections`
- JEP 269 - *Convenience Factory Methods for Collections*
- Oracle Java Tutorials - *Collections*: Set, Map, Queue, Deque interfaces
- *Effective Java* (Bloch) items 10-11 (equals/hashCode), 50 (defensive copies), 17 (minimize mutability)

## Glossary

| Term | Meaning |
|------|---------|
| Bucket | A slot in a hash table holding entries whose hash maps to the same index |
| Load factor | Fill ratio (default 0.75) at which a HashMap resizes |
| Treeification | Converting a heavily collided bucket into a red-black tree (Java 8+) |
| Heap | Tree structure keeping the smallest (or largest) element at the root; backs `PriorityQueue` |
| Deque | Double-ended queue; also used as a stack |
| Unmodifiable view | Read-only wrapper over a collection that still reflects changes to the underlying one |
| Defensive copy | Copying mutable input/output to protect internal state |
| Representation exposure | Leaking a reference to internal mutable state |

## Answers

Answers to every **Quick check** above (numbered `section.question`).

- **1.1** — What must hold between `equals` and `hashCode`?  
  If `a.equals(b)` then `a.hashCode() == b.hashCode()`. The converse need not hold (collisions).

- **1.2** — What happens to `HashMap.get` if a key's hash-relevant field changes after insertion?  
  The map searches the wrong bucket (or equals fails), returns `null`, and the entry is unreachable.

- **1.3** — When does a HashMap bucket turn into a tree?  
  In Java 8+, when a bucket has more than 8 nodes and the table capacity is at least 64 (otherwise it resizes instead).

- **1.4** — Which Map would you use for an LRU cache and why?  
  `LinkedHashMap` with access order and `removeEldestEntry`.

- **2.1** — What is the complexity of `PriorityQueue.offer`, `poll`, `peek`, `contains`?  
  O(log n), O(log n), O(1), O(n).

- **2.2** — Why prefer `ArrayDeque` over `Stack`?  
  `Stack` extends synchronized `Vector` (slow, leaky API); `ArrayDeque` is faster and has a clean `Deque` API.

- **2.3** — How do you get a max-heap from `PriorityQueue`?  
  Pass `Comparator.reverseOrder()` (or a reversed custom comparator).

- **2.4** — Difference between `remove()` and `poll()` on a Queue?  
  `remove()` throws `NoSuchElementException` when empty; `poll()` returns `null`.

- **3.1** — What is the difference between `Collections.unmodifiableList(x)` and `List.copyOf(x)`?  
  The first is a read-only *view* that reflects later changes to `x`; the second is an independent immutable snapshot that rejects nulls.

- **3.2** — Which factory call throws `IllegalArgumentException` and which throws `NullPointerException`: `Set.of(1, 1)` / `List.of(1, null)`?  
  `Set.of(1, 1)` -> IAE (duplicate); `List.of(1, null)` -> NPE.

- **3.3** — Is a `List.of(new StringBuilder("a"))` deeply immutable?  
  No - the list is immutable but the `StringBuilder` element is mutable (shallow immutability).

- **3.4** — Why return `List.copyOf(internal)` from a getter instead of `internal`?  
  To prevent callers from mutating or holding live references to your internal state (representation exposure).
