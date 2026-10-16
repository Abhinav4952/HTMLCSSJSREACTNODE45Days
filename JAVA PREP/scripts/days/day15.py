from gen_helpers import sec, task

DAY = dict(
    num=15,
    title="Collections II: Set, Map, HashMap Internals, Queue/Deque/PriorityQueue, and Immutable Collections",
    theme="Pick the right Set/Map/Queue, understand how hashing drives them, and expose state through immutable collections.",
    objectives=[
        "Choose between `HashSet`, `LinkedHashSet`, `TreeSet` and between `HashMap`, `LinkedHashMap`, `TreeMap`",
        "Explain conceptually how `HashMap` works (hashCode, buckets, equals, load factor, resize, treeification)",
        "Write correct `equals`/`hashCode` and avoid mutable keys",
        "Use `merge`, `computeIfAbsent`, `getOrDefault`, and `entrySet` idiomatically",
        "Use `Queue`, `Deque`/`ArrayDeque`, and `PriorityQueue` (heap) for real problems",
        "Create defensive immutable copies with `List.copyOf`, `Map.copyOf`, `Set.copyOf` and understand unmodifiable *views*",
    ],
    prereqs=["Day 14 — List, Iterator, Comparable/Comparator", "Day 08–09 — `equals` and `hashCode` contract"],
    overview="""Lists answer \"what is at position i\"; Sets and Maps answer \"is it present, and what is associated with it\" in (amortized) constant time. Almost every service uses a `Map` as a cache, index, counter, or lookup table, and a `Queue` to schedule work. Production bugs here are subtle: a mutable key that vanishes from a `HashMap`, a `HashSet` that keeps \"duplicates\" because `hashCode` was not overridden, a shared mutable list leaking out of a getter.

Today you build a mental model of hashing and trees, learn the idiomatic Map API, use heaps and deques, and finish with immutable collections - the safest way to share data. Interviews: *how does HashMap work*, *HashMap vs TreeMap vs LinkedHashMap*, *why must equals and hashCode agree*, *PriorityQueue complexity*, *List.of vs Collections.unmodifiableList*.""",
    sections=[
        sec(
            "Set, Map, and how HashMap works",
            "A `Set<E>` holds unique elements; a `Map<K,V>` associates unique keys with values (`Set<K>` is basically a `Map<K,Boolean>`). Implementations: **Hash*** (O(1) average, no order), **LinkedHash*** (O(1) with insertion or access order), **Tree*** (red-black tree, O(log n), sorted by `Comparable`/`Comparator`, navigation methods like `floor`, `ceiling`, `headMap`). **HashMap internals (conceptual):** `hash = key.hashCode()` is spread (`h ^ h>>>16`) and masked to a bucket index in a power-of-two table; the bucket holds a linked list (or, since Java 8, a red-black tree when a bucket exceeds 8 entries and the table has >= 64 slots); lookup compares hash then `equals`. When size exceeds `capacity * loadFactor` (default 0.75) the table doubles and entries are redistributed.",
            "Constant-time lookup is what makes caches, dedup, counting, joins, and indexing practical. Understanding the mechanics explains the contract: **equal objects must have equal hash codes**, hash codes of keys must not change while stored, and a poor `hashCode` collapses a map into O(n) (or O(log n) with treeification) behavior - also a denial-of-service vector with attacker-chosen keys.",
            ["`HashMap`/`HashSet`: O(1) average put/get/contains", "`LinkedHashMap`: predictable iteration (insertion/access order), LRU cache via `removeEldestEntry`", "`TreeMap`/`TreeSet`: sorted views and range queries", "Rich Map API (`merge`, `compute*`, `getOrDefault`) removes boilerplate"],
            ["`HashMap` iteration order is unspecified and may change across runs/versions", "Mutable or poorly hashed keys break lookups", "`TreeMap` needs consistent ordering and rejects `null` keys; not thread-safe (`HashMap` too - use `ConcurrentHashMap`)"],
            "If you override `equals` but not `hashCode`, two equal objects usually land in different buckets: `set.contains(new Point(1,2))` returns false although an equal point is inside. If you **mutate a field used in `hashCode`** after inserting the object as a key, `map.get(key)` returns null and the entry is unreachable (a memory leak). Resizing under concurrent writes in a plain `HashMap` can corrupt it or lose data. A `TreeSet<String>` built with `String.CASE_INSENSITIVE_ORDER` treats `\"A\"` and `\"a\"` as the same element - by design. Iterating a `HashMap` and asserting an order in tests yields flaky tests.",
            """- Contract: `a.equals(b)` => `a.hashCode() == b.hashCode()`; hashCode must be stable while in a hash structure.
- Defaults: initial capacity 16, load factor 0.75; presize with `new HashMap<>(expected * 4 / 3 + 1)` for big maps.
- `put` returns the previous value; `putIfAbsent`, `getOrDefault(k, d)`, `containsKey`.
- Counting idiom: `counts.merge(word, 1, Integer::sum);`
- Grouping idiom: `groups.computeIfAbsent(key, k -> new ArrayList<>()).add(item);`
- `HashSet.add` returns `false` when the element was already present - handy for duplicate detection.
- `TreeMap` navigation: `firstKey`, `floorKey(k)`, `ceilingEntry(k)`, `subMap`, `descendingMap`.
- Iterate entries with `for (Map.Entry<K,V> e : map.entrySet())` - not `keySet()` + `get`.""",
            [
                ("Tiny — counting with merge, grouping with computeIfAbsent", """Map<String, Integer> counts = new HashMap<>();
for (String w : "to be or not to be".split(" ")) counts.merge(w, 1, Integer::sum);
System.out.println(new TreeMap<>(counts));     // {be=2, not=1, or=1, to=2}

Map<Integer, List<String>> byLen = new TreeMap<>();
for (String w : List.of("a", "bb", "cc", "d")) byLen.computeIfAbsent(w.length(), k -> new ArrayList<>()).add(w);
System.out.println(byLen);                     // {1=[a, d], 2=[bb, cc]}"""),
                ("Tiny — the mutable key disaster", """class Key { int id; Key(int id) { this.id = id; }
    @Override public boolean equals(Object o) { return o instanceof Key k && k.id == id; }
    @Override public int hashCode() { return id; } }

Map<Key, String> m = new HashMap<>();
Key k = new Key(1);
m.put(k, "x");
k.id = 2;                                   // hashCode changed after insertion
System.out.println(m.get(k));               // null  (looks in bucket 2)
System.out.println(m.get(new Key(1)));      // null  (bucket 1 has it, but equals() now fails)
System.out.println(m.size());               // 1 - entry is orphaned"""),
                ("Medium — a bounded LRU cache with LinkedHashMap", """import java.util.*;

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
}"""),
            ],
            [
                ("What must hold between `equals` and `hashCode`?", "If `a.equals(b)` then `a.hashCode() == b.hashCode()`. The converse need not hold (collisions)."),
                ("What happens to `HashMap.get` if a key's hash-relevant field changes after insertion?", "The map searches the wrong bucket (or equals fails), returns `null`, and the entry is unreachable."),
                ("When does a HashMap bucket turn into a tree?", "In Java 8+, when a bucket has more than 8 nodes and the table capacity is at least 64 (otherwise it resizes instead)."),
                ("Which Map would you use for an LRU cache and why?", "`LinkedHashMap` with access order and `removeEldestEntry`."),
            ],
        ),
        sec(
            "Queue, Deque, ArrayDeque, and PriorityQueue",
            "A `Queue<E>` models waiting work (`offer`/`poll`/`peek`; `add`/`remove`/`element` throw on failure). A `Deque<E>` (double-ended queue) adds `offerFirst/Last`, `pollFirst/Last`, `push/pop` and serves as both queue **and stack**. `ArrayDeque` is the fast resizable-array implementation (no nulls). `PriorityQueue` is a binary **min-heap**: `peek`/`poll` return the smallest element by natural order or the supplied `Comparator`; `offer`/`poll` are O(log n), `peek` O(1). Its iterator and `toString` are **not** sorted.",
            "Queues decouple producers from consumers (task scheduling, BFS, rate buffers); deques implement undo stacks, sliding windows, and palindromes; priority queues power schedulers, top-K, Dijkstra, and merge-K-sorted. `java.util.Stack` and `LinkedList` as a stack are legacy choices - use `ArrayDeque`.",
            ["`ArrayDeque`: fast, compact queue/stack", "`PriorityQueue`: O(log n) priority scheduling; top-K in O(n log k)", "Method pairs let you choose exceptions (`remove`) or special values (`poll`)", "`Deque` unifies stack and queue operations"],
            ["`PriorityQueue` iteration order is not sorted; `contains`/`remove(Object)` are O(n)", "`ArrayDeque` and `PriorityQueue` reject `null`", "Neither is thread-safe (see `LinkedBlockingQueue`, `PriorityBlockingQueue`)"],
            "Using `java.util.Stack` (synchronized `Vector`) is slow and exposes list methods. Printing a `PriorityQueue` and expecting sorted output is a classic mistake; only repeated `poll()` yields order. A comparator with inconsistent ordering corrupts the heap property silently. Calling `remove()`/`element()` on an empty queue throws `NoSuchElementException`, while `poll()`/`peek()` return `null`. Using `PriorityQueue<int[]>` without a comparator throws `ClassCastException` (arrays are not `Comparable`).",
            """- Prefer `offer/poll/peek` for bounded or possibly-empty queues; `add/remove/element` when emptiness is a bug.
- Stack idiom: `Deque<Integer> st = new ArrayDeque<>(); st.push(1); st.pop();` (push/pop work at the head).
- Queue idiom: `offer` at tail, `poll` from head.
- Max-heap: `new PriorityQueue<>(Comparator.reverseOrder())`.
- Top-K smallest: keep a **max**-heap of size K, evict the largest when it grows beyond K.
- `PriorityQueue(int initialCapacity, Comparator<? super E>)`; capacity 1+ required.""",
            [
                ("Tiny — stack and queue on one ArrayDeque class", """Deque<String> stack = new ArrayDeque<>();
stack.push("a"); stack.push("b");
System.out.println(stack.pop());     // b
Queue<String> q = new ArrayDeque<>();
q.offer("x"); q.offer("y");
System.out.println(q.poll());        // x"""),
                ("Tiny — PriorityQueue is a heap, not a sorted list", """PriorityQueue<Integer> pq = new PriorityQueue<>(List.of(5, 1, 4, 2, 3));
System.out.println(pq.peek());       // 1
StringBuilder sb = new StringBuilder();
while (!pq.isEmpty()) sb.append(pq.poll()).append(' ');
System.out.println(sb);              // 1 2 3 4 5   (only poll() order is sorted)"""),
                ("Medium — balanced brackets with a Deque and top-K with a bounded heap", """import java.util.*;

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
}"""),
            ],
            [
                ("What is the complexity of `PriorityQueue.offer`, `poll`, `peek`, `contains`?", "O(log n), O(log n), O(1), O(n)."),
                ("Why prefer `ArrayDeque` over `Stack`?", "`Stack` extends synchronized `Vector` (slow, leaky API); `ArrayDeque` is faster and has a clean `Deque` API."),
                ("How do you get a max-heap from `PriorityQueue`?", "Pass `Comparator.reverseOrder()` (or a reversed custom comparator)."),
                ("Difference between `remove()` and `poll()` on a Queue?", "`remove()` throws `NoSuchElementException` when empty; `poll()` returns `null`."),
            ],
        ),
        sec(
            "Immutable collections, copies, and unmodifiable views",
            "Java offers three different things people call \"read-only\": (1) **immutable collections** created by `List.of`, `Set.of`, `Map.of`, `Map.ofEntries`, and the *copy* factories `List.copyOf`, `Set.copyOf`, `Map.copyOf` - they cannot change and reject `null`; (2) **unmodifiable views** from `Collections.unmodifiableList(x)` - they throw on mutation but **reflect later changes to the wrapped collection**; (3) **fixed-size** adapters like `Arrays.asList`. Immutable collections are shallow: the elements themselves may still be mutable.",
            "Shared mutable state is the root of many bugs: a getter that returns the internal list lets any caller corrupt your object (**representation exposure**), and a constructor that stores the caller's list lets the caller change it later. Immutable copies make objects safe to share across threads without locks and easy to reason about. Record-like domain objects (`Order`, `Money`, `Roster`) are typically built from defensive immutable copies.",
            ["Thread-safe by construction and easy to reason about", "`copyOf` is cheap when the source is already immutable (returns it)", "`List.of`/`Set.of`/`Map.of` are compact and null-hostile (fail fast)", "Clear API contract: callers cannot mutate your state"],
            ["Mutation attempts fail at **runtime** with `UnsupportedOperationException`, not at compile time", "`Set.of`/`Map.of` iteration order is unspecified and randomized per JVM run; duplicates in `Set.of(...)`/`Map.of(...)` throw `IllegalArgumentException`", "Shallow immutability: contents may still be mutable objects"],
            "`Collections.unmodifiableList(internal)` returned from a getter looks safe, yet your own later `internal.add(...)` shows up in the caller's \"read-only\" list (and concurrent modification can throw CME in their iteration). Storing the constructor argument directly (`this.names = names`) lets the caller mutate your object. `List.of(\"a\", null)` throws `NullPointerException`; `Set.of(\"a\", \"a\")` throws `IllegalArgumentException`; `List.copyOf(listWithNull)` throws NPE. Assuming `Map.of` keeps insertion order causes flaky tests.",
            """- Defensive copy in: `this.names = List.copyOf(names);` (NPE if `names` or an element is null).
- Defensive copy out: return the already-immutable field directly, or `List.copyOf(internalMutable)`.
- `Map.of(k1, v1, ...)` up to 10 pairs; use `Map.ofEntries(Map.entry(k, v), ...)` beyond that.
- `stream.toList()` (Java 16) returns an unmodifiable list (nulls allowed); `Collectors.toUnmodifiableList()` rejects nulls.
- Test with `assertThatThrownBy(() -> list.add(x)).isInstanceOf(UnsupportedOperationException.class)` - obtain the list *before* the lambda.
- Wither pattern: `public Roster withName(String n)` returns a new instance instead of mutating.""",
            [
                ("Tiny — immutable vs view", """List<String> base = new ArrayList<>(List.of("a"));
List<String> view = Collections.unmodifiableList(base);
List<String> copy = List.copyOf(base);
base.add("b");
System.out.println(view);   // [a, b]  - the view reflects the change
System.out.println(copy);   // [a]     - the copy does not
// view.add("c");           // UnsupportedOperationException"""),
                ("Tiny — fail-fast factories", """try { List.of("a", null); } catch (NullPointerException e) { System.out.println("NPE"); }
try { Set.of("a", "a"); }    catch (IllegalArgumentException e) { System.out.println("IAE"); }
try { Map.of("k", 1, "k", 2); } catch (IllegalArgumentException e) { System.out.println("IAE"); }
// NPE
// IAE
// IAE"""),
                ("Medium — an immutable value object with defensive copies and a wither", """import java.util.*;

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
}"""),
            ],
            [
                ("What is the difference between `Collections.unmodifiableList(x)` and `List.copyOf(x)`?", "The first is a read-only *view* that reflects later changes to `x`; the second is an independent immutable snapshot that rejects nulls."),
                ("Which factory call throws `IllegalArgumentException` and which throws `NullPointerException`: `Set.of(1, 1)` / `List.of(1, null)`?", "`Set.of(1, 1)` -> IAE (duplicate); `List.of(1, null)` -> NPE."),
                ("Is a `List.of(new StringBuilder(\"a\"))` deeply immutable?", "No - the list is immutable but the `StringBuilder` element is mutable (shallow immutability)."),
                ("Why return `List.copyOf(internal)` from a getter instead of `internal`?", "To prevent callers from mutating or holding live references to your internal state (representation exposure)."),
            ],
        ),
    ],
    interview=[
        ("Explain how HashMap works internally.", "Key's `hashCode` is spread and masked to a bucket index; the bucket is a linked list (a red-black tree after 8 collisions at capacity >= 64). `get` finds the bucket then uses `equals`. When size exceeds capacity x 0.75 the table doubles and entries are rehashed. Average O(1), worst O(log n) with treeification."),
        ("HashMap vs LinkedHashMap vs TreeMap vs ConcurrentHashMap?", "Hash: fastest, unordered. LinkedHash: insertion/access order, LRU. Tree: sorted, O(log n), range queries. ConcurrentHashMap: thread-safe, no null keys/values, atomic compute/merge."),
        ("Why must equals and hashCode be overridden together?", "Hash collections locate by hash first; unequal hashes for equal objects make lookups fail and sets hold duplicates."),
        ("When would a PriorityQueue be the right tool?", "Task scheduling by priority, top-K, merging sorted streams, Dijkstra - anywhere you repeatedly need the min/max of a changing set."),
        ("How do you make a class's collection fields safe to expose?", "Defensive copy in the constructor with `List.copyOf`, return immutable fields (or copies), avoid exposing views over mutable internals."),
        ("What happens when two different keys have the same hashCode?", "They share a bucket; `equals` disambiguates; many collisions degrade performance (treeified buckets bound the damage to O(log n))."),
    ],
    mistakes=[
        "Overriding `equals` without `hashCode` (or the reverse) - `HashSet` shows duplicates, `contains` fails.",
        "Mutating an object after using it as a `HashMap` key or `HashSet` element.",
        "Asserting `HashMap`/`HashSet`/`Set.of` iteration order in tests (use `containsExactlyInAnyOrder`).",
        "Treating `PriorityQueue.toString()`/iteration as sorted.",
        "Exposing internal collections from getters or storing constructor arguments without copying.",
        "Using `Stack`/`LinkedList` instead of `ArrayDeque`, or `get(k) == null` checks where `merge`/`computeIfAbsent` is cleaner.",
    ],
    reading=[
        "Javadoc: `java.util.HashMap` (implementation notes), `LinkedHashMap`, `TreeMap`, `PriorityQueue`, `ArrayDeque`, `Collections`",
        "JEP 269 - *Convenience Factory Methods for Collections*",
        "Oracle Java Tutorials - *Collections*: Set, Map, Queue, Deque interfaces",
        "*Effective Java* (Bloch) items 10-11 (equals/hashCode), 50 (defensive copies), 17 (minimize mutability)",
    ],
    glossary=[
        ("Bucket", "A slot in a hash table holding entries whose hash maps to the same index"),
        ("Load factor", "Fill ratio (default 0.75) at which a HashMap resizes"),
        ("Treeification", "Converting a heavily collided bucket into a red-black tree (Java 8+)"),
        ("Heap", "Tree structure keeping the smallest (or largest) element at the root; backs `PriorityQueue`"),
        ("Deque", "Double-ended queue; also used as a stack"),
        ("Unmodifiable view", "Read-only wrapper over a collection that still reflects changes to the underlying one"),
        ("Defensive copy", "Copying mutable input/output to protect internal state"),
        ("Representation exposure", "Leaking a reference to internal mutable state"),
    ],
    tasks=[
        task(
            "unique-normalize", "Unique and Normalize Sets", "Warm-up", "UniqueNormalize",
            "Use `Set` implementations deliberately: normalize raw strings into an insertion-ordered unique set, find duplicates, and implement set algebra (union, intersection, difference) that returns **new** sets and never mutates its arguments.",
            [
                "`normalize(List<String>)` returns a `LinkedHashSet` of trimmed, lower-case, non-blank strings in first-seen order; `null` elements are skipped; a `null` list throws `NullPointerException`",
                "`duplicates(List<T>)` returns a `LinkedHashSet` of elements that occur more than once (in order of their second occurrence)",
                "`union(a, b)`, `intersection(a, b)`, `difference(a, b)` return new sets and leave `a` and `b` unchanged",
                "`sortedCaseInsensitive(Collection<String>)` returns a `TreeSet` using `String.CASE_INSENSITIVE_ORDER` (so \"A\" and \"a\" collapse to the first inserted)",
            ],
            ["null and blank elements", "empty inputs", "disjoint sets", "case-insensitive collapse keeps the first inserted spelling"],
            {"UniqueNormalize.java": r'''package @PKG@;

import java.util.Collection;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Objects;
import java.util.Set;
import java.util.TreeSet;

/** Set-based helpers. */
public final class UniqueNormalize {

    private UniqueNormalize() {
    }

    public static Set<String> normalize(List<String> raw) {
        //@TODO normalize | trim + lower-case each element, skip null and blank, keep first-seen order in a LinkedHashSet; NullPointerException for null list
        Objects.requireNonNull(raw, "raw");
        Set<String> out = new LinkedHashSet<>();
        for (String s : raw) {
            if (s == null) {
                continue;
            }
            String n = s.trim().toLowerCase(Locale.ROOT);
            if (!n.isEmpty()) {
                out.add(n);
            }
        }
        return out;
        //@END
    }

    public static <T> Set<T> duplicates(List<T> items) {
        //@TODO duplicates | return the elements seen more than once, ordered by when the repeat was detected (use the boolean result of Set.add)
        Set<T> seen = new java.util.HashSet<>();
        Set<T> dups = new LinkedHashSet<>();
        for (T item : items) {
            if (!seen.add(item)) {
                dups.add(item);
            }
        }
        return dups;
        //@END
    }

    public static <T> Set<T> union(Set<? extends T> a, Set<? extends T> b) {
        //@TODO union | new set containing every element of a and b; do not mutate a or b
        Set<T> out = new LinkedHashSet<>(a);
        out.addAll(b);
        return out;
        //@END
    }

    public static <T> Set<T> intersection(Set<? extends T> a, Set<? extends T> b) {
        //@TODO intersection | new set of the elements present in both; do not mutate a or b
        Set<T> out = new LinkedHashSet<>(a);
        out.retainAll(b);
        return out;
        //@END
    }

    public static <T> Set<T> difference(Set<? extends T> a, Set<? extends T> b) {
        //@TODO difference | new set of the elements in a that are not in b; do not mutate a or b
        Set<T> out = new LinkedHashSet<>(a);
        out.removeAll(b);
        return out;
        //@END
    }

    public static TreeSet<String> sortedCaseInsensitive(Collection<String> words) {
        //@TODO sortedCaseInsensitive | TreeSet with String.CASE_INSENSITIVE_ORDER containing words; the first inserted spelling wins
        TreeSet<String> out = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);
        for (String w : words) {
            out.add(w);
        }
        return out;
        //@END
    }
}
'''},
            {"UniqueNormalizeTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class UniqueNormalizeTest {

    @Test
    void r1_normalizeTrimsLowercasesAndKeepsOrder() {
        List<String> raw = Arrays.asList("  Apple ", "banana", "APPLE", null, "   ", "Cherry", "BANANA ");
        Set<String> out = UniqueNormalize.normalize(raw);
        assertThat(out).isInstanceOf(LinkedHashSet.class).containsExactly("apple", "banana", "cherry");
    }

    @Test
    void r1_normalizeEdgeCases() {
        assertThat(UniqueNormalize.normalize(List.of())).isEmpty();
        assertThatThrownBy(() -> UniqueNormalize.normalize(null)).isInstanceOf(NullPointerException.class);
    }

    @Test
    void r2_duplicates() {
        assertThat(UniqueNormalize.duplicates(List.of(1, 2, 1, 3, 2, 1, 4))).containsExactly(1, 2);
        assertThat(UniqueNormalize.duplicates(List.of("a", "b"))).isEmpty();
        assertThat(UniqueNormalize.duplicates(List.<String>of())).isEmpty();
    }

    @Test
    void r3_setAlgebra() {
        Set<Integer> a = new LinkedHashSet<>(List.of(1, 2, 3));
        Set<Integer> b = new LinkedHashSet<>(List.of(3, 4));
        assertThat(UniqueNormalize.union(a, b)).containsExactlyInAnyOrder(1, 2, 3, 4);
        assertThat(UniqueNormalize.intersection(a, b)).containsExactly(3);
        assertThat(UniqueNormalize.difference(a, b)).containsExactlyInAnyOrder(1, 2);
        assertThat(UniqueNormalize.difference(b, a)).containsExactly(4);
    }

    @Test
    void r3_argumentsAreNeverMutated() {
        Set<String> a = new LinkedHashSet<>(List.of("x", "y"));
        Set<String> b = new LinkedHashSet<>(List.of("y", "z"));
        UniqueNormalize.union(a, b);
        UniqueNormalize.intersection(a, b);
        UniqueNormalize.difference(a, b);
        assertThat(a).containsExactly("x", "y");
        assertThat(b).containsExactly("y", "z");
    }

    @Test
    void r3_disjointAndEmpty() {
        Set<Integer> empty = Set.of();
        assertThat(UniqueNormalize.intersection(Set.of(1), Set.of(2))).isEmpty();
        assertThat(UniqueNormalize.union(empty, empty)).isEmpty();
        assertThat(UniqueNormalize.difference(Set.of(1, 2), empty)).containsExactlyInAnyOrder(1, 2);
    }

    @Test
    void r4_caseInsensitiveSortedSet() {
        List<String> words = new ArrayList<>(List.of("pear", "Apple", "apple", "Banana", "APPLE"));
        var set = UniqueNormalize.sortedCaseInsensitive(words);
        assertThat(set).containsExactly("Apple", "Banana", "pear");
        assertThat(set.contains("BANANA")).isTrue();
    }
}
'''},
            ["`Set.add` returns false for an element that is already present - use that in `duplicates`.", "Copy first (`new LinkedHashSet<>(a)`), then `addAll`/`retainAll`/`removeAll` the copy."],
            ["Set implementation chosen deliberately for each requirement (Linked/Tree)", "Arguments never mutated", "No `contains` on a `List` for membership"],
        ),
        task(
            "frequency-map", "Frequency Map Toolkit", "Core", "FrequencyMap",
            "Build a word-frequency toolkit with the idiomatic Map API (`merge`, `getOrDefault`, `computeIfAbsent`): count words case-insensitively, rank the top N with deterministic tie-breaking, invert counts into a sorted map of groups, and merge two count maps. Tests never depend on `HashMap` iteration order.",
            [
                "`count(List<String>)` returns word -> occurrences; words are trimmed and lower-cased; blank/null words are ignored",
                "`topN(counts, n)` returns the `n` most frequent words, ordered by count descending then word ascending; `n <= 0` returns an empty list; `n` larger than the number of words returns all",
                "`invert(counts)` returns a `SortedMap<Integer, List<String>>` (counts ascending) where each list of words is sorted alphabetically",
                "`mergeCounts(a, b)` returns a new map summing counts for shared keys without mutating inputs",
            ],
            ["empty input", "ties in `topN`", "blank and null words", "inputs left unmodified by `mergeCounts`"],
            {"FrequencyMap.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.SortedMap;
import java.util.TreeMap;

/** Word-frequency helpers built on the Map API. */
public final class FrequencyMap {

    private FrequencyMap() {
    }

    public static Map<String, Integer> count(List<String> words) {
        //@TODO count | count occurrences of trimmed lower-case words (skip null/blank) using Map.merge
        Map<String, Integer> counts = new HashMap<>();
        for (String w : words) {
            if (w == null || w.isBlank()) {
                continue;
            }
            counts.merge(w.trim().toLowerCase(Locale.ROOT), 1, Integer::sum);
        }
        return counts;
        //@END
    }

    public static List<String> topN(Map<String, Integer> counts, int n) {
        //@TODO topN | return up to n words ordered by count descending, then word ascending; n <= 0 gives an empty list
        if (n <= 0) {
            return new ArrayList<>();
        }
        List<Map.Entry<String, Integer>> entries = new ArrayList<>(counts.entrySet());
        entries.sort(Map.Entry.<String, Integer>comparingByValue().reversed().thenComparing(Map.Entry.comparingByKey()));
        List<String> result = new ArrayList<>();
        for (Map.Entry<String, Integer> e : entries) {
            if (result.size() == n) {
                break;
            }
            result.add(e.getKey());
        }
        return result;
        //@END
    }

    public static SortedMap<Integer, List<String>> invert(Map<String, Integer> counts) {
        //@TODO invert | group words by count into a TreeMap (counts ascending); each word list sorted alphabetically; use computeIfAbsent
        SortedMap<Integer, List<String>> inverted = new TreeMap<>();
        for (Map.Entry<String, Integer> e : counts.entrySet()) {
            inverted.computeIfAbsent(e.getValue(), k -> new ArrayList<>()).add(e.getKey());
        }
        for (List<String> words : inverted.values()) {
            java.util.Collections.sort(words);
        }
        return inverted;
        //@END
    }

    public static Map<String, Integer> mergeCounts(Map<String, Integer> a, Map<String, Integer> b) {
        //@TODO mergeCounts | return a new map with the sum of counts per key; do not mutate a or b
        Map<String, Integer> merged = new HashMap<>(a);
        b.forEach((k, v) -> merged.merge(k, v, Integer::sum));
        return merged;
        //@END
    }
}
'''},
            {"FrequencyMapTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class FrequencyMapTest {

    @Test
    void r1_countIsCaseInsensitiveAndIgnoresBlanks() {
        List<String> words = Arrays.asList("Go", "go", " GO ", "java", null, "  ", "Java", "rust");
        Map<String, Integer> counts = FrequencyMap.count(words);
        assertThat(counts).containsOnlyKeys("go", "java", "rust");
        assertThat(counts).containsEntry("go", 3).containsEntry("java", 2).containsEntry("rust", 1);
    }

    @Test
    void r1_countEmpty() {
        assertThat(FrequencyMap.count(List.of())).isEmpty();
    }

    @Test
    void r2_topNOrdersByCountThenAlphabet() {
        Map<String, Integer> counts = Map.of("pear", 2, "apple", 2, "fig", 5, "kiwi", 1);
        assertThat(FrequencyMap.topN(counts, 3)).containsExactly("fig", "apple", "pear");
        assertThat(FrequencyMap.topN(counts, 1)).containsExactly("fig");
    }

    @Test
    void r2_topNBoundaries() {
        Map<String, Integer> counts = Map.of("a", 1, "b", 1);
        assertThat(FrequencyMap.topN(counts, 0)).isEmpty();
        assertThat(FrequencyMap.topN(counts, -3)).isEmpty();
        assertThat(FrequencyMap.topN(counts, 10)).containsExactly("a", "b");
        assertThat(FrequencyMap.topN(Map.of(), 2)).isEmpty();
    }

    @Test
    void r3_invertGroupsAndSorts() {
        Map<String, Integer> counts = Map.of("pear", 2, "apple", 2, "fig", 5, "kiwi", 1);
        var inverted = FrequencyMap.invert(counts);
        assertThat(inverted.keySet()).containsExactly(1, 2, 5);
        assertThat(inverted.get(2)).containsExactly("apple", "pear");
        assertThat(inverted.get(5)).containsExactly("fig");
    }

    @Test
    void r4_mergeCountsSumsAndDoesNotMutate() {
        Map<String, Integer> a = new java.util.HashMap<>(Map.of("x", 1, "y", 2));
        Map<String, Integer> b = new java.util.HashMap<>(Map.of("y", 3, "z", 4));
        Map<String, Integer> merged = FrequencyMap.mergeCounts(a, b);
        assertThat(merged).containsOnlyKeys("x", "y", "z");
        assertThat(merged).containsEntry("x", 1).containsEntry("y", 5).containsEntry("z", 4);
        assertThat(a).containsOnlyKeys("x", "y").containsEntry("y", 2);
        assertThat(b).containsOnlyKeys("y", "z").containsEntry("y", 3);
    }
}
'''},
            ["Sort `Map.Entry` objects with `Map.Entry.comparingByValue()` then `comparingByKey()`.", "`computeIfAbsent(k, x -> new ArrayList<>()).add(...)` replaces the check-then-put dance."],
            ["Uses `merge`/`computeIfAbsent` rather than `containsKey`/`get`/`put` boilerplate", "Deterministic ordering is produced by explicit comparators, not by `HashMap` luck"],
        ),
        task(
            "priority-queue-lab", "Queues, Deques, and Priority Queues", "Stretch", "PriorityQueueLab",
            "Use a `PriorityQueue` with a custom comparator to schedule jobs, a bounded max-heap to find the K smallest numbers, an `ArrayDeque` as a stack to validate brackets, and a deque to rotate a list.",
            [
                "`processOrder(List<Job>)` returns job ids in execution order: higher `priority` first, ties broken by id ascending (use a `PriorityQueue`)",
                "`kSmallest(List<Integer>, k)` returns the `k` smallest values ascending using a bounded max-heap; `k <= 0` -> empty; `k >= size` -> all values sorted",
                "`isBalanced(String)` checks `()`, `[]`, `{}` nesting using an `ArrayDeque` stack; characters other than brackets are ignored",
                "`rotateLeft(List<T>, k)` rotates left by `k` (mod size, negative allowed) using an `ArrayDeque`, returning a new list",
            ],
            ["empty input", "duplicate priorities", "k of 0 / negative / larger than the list", "unbalanced closers (`\"]\"`), interleaved types (`\"(]\"`), leftover openers", "negative rotation"],
            {"Job.java": r'''package @PKG@;

/** Provided value type. Higher priority runs first. */
public record Job(String id, int priority) {
}
''',
             "PriorityQueueLab.java": r'''package @PKG@;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Deque;
import java.util.List;
import java.util.PriorityQueue;

/** Queue, Deque, and PriorityQueue exercises. */
public final class PriorityQueueLab {

    private PriorityQueueLab() {
    }

    public static List<String> processOrder(List<Job> jobs) {
        //@TODO processOrder | offer all jobs into a PriorityQueue (priority desc, then id asc) and poll them into a list of ids
        PriorityQueue<Job> queue = new PriorityQueue<>(
                Comparator.comparingInt(Job::priority).reversed().thenComparing(Job::id));
        queue.addAll(jobs);
        List<String> order = new ArrayList<>();
        while (!queue.isEmpty()) {
            order.add(queue.poll().id());
        }
        return order;
        //@END
    }

    public static List<Integer> kSmallest(List<Integer> values, int k) {
        //@TODO kSmallest | keep a max-heap of at most k items (evict the largest), then return them in ascending order; k <= 0 gives an empty list
        if (k <= 0) {
            return new ArrayList<>();
        }
        PriorityQueue<Integer> heap = new PriorityQueue<>(Comparator.reverseOrder());
        for (int v : values) {
            heap.offer(v);
            if (heap.size() > k) {
                heap.poll();
            }
        }
        List<Integer> result = new ArrayList<>(heap);
        Collections.sort(result);
        return result;
        //@END
    }

    public static boolean isBalanced(String text) {
        //@TODO isBalanced | use an ArrayDeque as a stack: push openers, pop and match on closers; ignore other characters; true only if the stack ends empty
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : text.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') {
                stack.push(c);
            } else if (c == ')' || c == ']' || c == '}') {
                if (stack.isEmpty()) {
                    return false;
                }
                char open = stack.pop();
                if ("([{".indexOf(open) != ")]}".indexOf(c)) {
                    return false;
                }
            }
        }
        return stack.isEmpty();
        //@END
    }

    public static <T> List<T> rotateLeft(List<T> items, int k) {
        //@TODO rotateLeft | load items into an ArrayDeque, move the head to the tail (k mod size) times, return a new list; empty list gives empty list
        if (items.isEmpty()) {
            return new ArrayList<>();
        }
        Deque<T> deque = new ArrayDeque<>(items);
        int steps = ((k % items.size()) + items.size()) % items.size();
        for (int i = 0; i < steps; i++) {
            deque.addLast(deque.pollFirst());
        }
        return new ArrayList<>(deque);
        //@END
    }
}
'''},
            {"PriorityQueueLabTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.Test;

class PriorityQueueLabTest {

    @Test
    void r1_processOrderByPriorityThenId() {
        List<Job> jobs = List.of(new Job("c", 1), new Job("b", 5), new Job("a", 5), new Job("d", 3));
        assertThat(PriorityQueueLab.processOrder(jobs)).containsExactly("a", "b", "d", "c");
    }

    @Test
    void r1_processOrderEmptyAndSingle() {
        assertThat(PriorityQueueLab.processOrder(List.of())).isEmpty();
        assertThat(PriorityQueueLab.processOrder(List.of(new Job("only", 0)))).containsExactly("only");
    }

    @Test
    void r2_kSmallest() {
        List<Integer> values = List.of(9, 1, 8, 2, 7, 2);
        assertThat(PriorityQueueLab.kSmallest(values, 3)).containsExactly(1, 2, 2);
        assertThat(PriorityQueueLab.kSmallest(values, 1)).containsExactly(1);
    }

    @Test
    void r2_kSmallestBoundaries() {
        List<Integer> values = List.of(3, 1, 2);
        assertThat(PriorityQueueLab.kSmallest(values, 0)).isEmpty();
        assertThat(PriorityQueueLab.kSmallest(values, -1)).isEmpty();
        assertThat(PriorityQueueLab.kSmallest(values, 10)).containsExactly(1, 2, 3);
        assertThat(PriorityQueueLab.kSmallest(List.of(), 2)).isEmpty();
    }

    @Test
    void r3_balancedBrackets() {
        assertThat(PriorityQueueLab.isBalanced("{[()]}")).isTrue();
        assertThat(PriorityQueueLab.isBalanced("a(b)[c]{d}")).isTrue();
        assertThat(PriorityQueueLab.isBalanced("")).isTrue();
    }

    @Test
    void r3_unbalancedBrackets() {
        assertThat(PriorityQueueLab.isBalanced("(]")).isFalse();
        assertThat(PriorityQueueLab.isBalanced("]")).isFalse();
        assertThat(PriorityQueueLab.isBalanced("((")).isFalse();
        assertThat(PriorityQueueLab.isBalanced("([)]")).isFalse();
    }

    @Test
    void r4_rotateLeft() {
        assertThat(PriorityQueueLab.rotateLeft(List.of(1, 2, 3, 4, 5), 2)).containsExactly(3, 4, 5, 1, 2);
        assertThat(PriorityQueueLab.rotateLeft(List.of(1, 2, 3), 3)).containsExactly(1, 2, 3);
        assertThat(PriorityQueueLab.rotateLeft(List.of(1, 2, 3), 4)).containsExactly(2, 3, 1);
        assertThat(PriorityQueueLab.rotateLeft(List.of(1, 2, 3), -1)).containsExactly(3, 1, 2);
        assertThat(PriorityQueueLab.rotateLeft(List.<Integer>of(), 5)).isEmpty();
    }
}
'''},
            ["Remember `Comparator.comparingInt(Job::priority).reversed().thenComparing(Job::id)`.", "For top-K *smallest* you need a **max**-heap so the largest candidate is evicted first."],
            ["Correct data structure for each method (heap, stack, deque)", "`ArrayDeque` used instead of `Stack`/`LinkedList`", "Does not iterate a `PriorityQueue` expecting sorted order"],
            constraints=["Do not use `java.util.Stack`", "Do not sort the whole input list in `kSmallest` (use the bounded heap)", "Do not edit the tests"],
        ),
        task(
            "immutable-copy", "Immutable Roster with Defensive Copies", "Challenge", "Roster",
            "Create an immutable `Roster` value object that defensively copies its inputs, exposes only immutable collections, and offers a wither that returns a new instance. Add helper methods demonstrating the difference between an unmodifiable **view** and an immutable **copy**. **Challenge:** explain in a comment why `Collections.unmodifiableList(internal)` would be a bug here.",
            [
                "`new Roster(names, scores)` stores immutable copies (`List.copyOf`, `Map.copyOf`); null arguments or null elements throw `NullPointerException`",
                "Changes to the caller's original collections after construction do not affect the roster",
                "`names()` and `scores()` return collections that throw `UnsupportedOperationException` on mutation",
                "`withName(String)` returns a **new** roster that has one more name (appended) and the same scores; the original is unchanged",
                "`safeCopy(Collection<? extends T>)` returns an immutable `List<T>` snapshot",
                "`viewReflectsChanges(base)` returns `true` (an unmodifiable view shows later changes to its base) and `copyIgnoresChanges(base)` returns `true` (an immutable copy does not); both must actually perform the experiment on a **copy** of `base` and not mutate `base`",
            ],
            ["null list, null element, null map", "mutating the original after construction", "wither leaves original untouched", "`Map.copyOf` iteration order is unspecified - do not depend on it"],
            {"Roster.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/** Immutable roster: names plus a score per name. */
public final class Roster {

    private final List<String> names;
    private final Map<String, Integer> scores;

    public Roster(List<String> names, Map<String, Integer> scores) {
        //@TODO constructor | store List.copyOf(names) and Map.copyOf(scores) (null arguments or elements -> NullPointerException)
        // The copies are immutable and independent of the caller's collections.
        this.names = List.copyOf(names);
        this.scores = Map.copyOf(scores);
        //@END
    }

    public List<String> names() {
        return names;
    }

    public Map<String, Integer> scores() {
        return scores;
    }

    public Roster withName(String name) {
        //@TODO withName | return a NEW Roster whose names are this.names plus name appended; scores unchanged; this stays unchanged
        List<String> next = new ArrayList<>(names);
        next.add(name);
        return new Roster(next, scores);
        //@END
    }

    public static <T> List<T> safeCopy(Collection<? extends T> source) {
        //@TODO safeCopy | return an immutable snapshot list of source (List.copyOf)
        return List.copyOf(source);
        //@END
    }

    public static boolean viewReflectsChanges(List<String> base) {
        //@TODO viewReflectsChanges | on a mutable COPY of base: wrap it in Collections.unmodifiableList, add an element to the copy, return whether the view's size grew (true); never mutate base
        List<String> work = new ArrayList<>(base);
        List<String> view = Collections.unmodifiableList(work);
        int before = view.size();
        work.add("extra");
        return view.size() > before;
        //@END
    }

    public static boolean copyIgnoresChanges(List<String> base) {
        //@TODO copyIgnoresChanges | on a mutable COPY of base: take List.copyOf, add an element to the copy, return whether the snapshot's size stayed the same (true); never mutate base
        List<String> work = new ArrayList<>(base);
        List<String> snapshot = List.copyOf(work);
        int before = snapshot.size();
        work.add("extra");
        return snapshot.size() == before;
        //@END
    }
}
'''},
            {"RosterTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class RosterTest {

    private static Roster sample() {
        return new Roster(new ArrayList<>(List.of("ann", "bob")), new HashMap<>(Map.of("ann", 10, "bob", 20)));
    }

    @Test
    void r1_constructorCopiesAndRejectsNulls() {
        Roster roster = sample();
        assertThat(roster.names()).containsExactly("ann", "bob");
        assertThat(roster.scores()).containsOnlyKeys("ann", "bob").containsEntry("bob", 20);
        assertThatThrownBy(() -> new Roster(null, Map.of())).isInstanceOf(NullPointerException.class);
        assertThatThrownBy(() -> new Roster(Arrays.asList("a", null), Map.of())).isInstanceOf(NullPointerException.class);
        assertThatThrownBy(() -> new Roster(List.of(), null)).isInstanceOf(NullPointerException.class);
    }

    @Test
    void r2_callerChangesDoNotLeakIn() {
        List<String> names = new ArrayList<>(List.of("ann"));
        Map<String, Integer> scores = new HashMap<>(Map.of("ann", 1));
        Roster roster = new Roster(names, scores);
        names.add("mallory");
        scores.put("mallory", 99);
        assertThat(roster.names()).containsExactly("ann");
        assertThat(roster.scores()).containsOnlyKeys("ann");
    }

    @Test
    void r3_exposedCollectionsAreImmutable() {
        Roster roster = sample();
        List<String> names = roster.names();
        Map<String, Integer> scores = roster.scores();
        assertThatThrownBy(() -> names.add("x")).isInstanceOf(UnsupportedOperationException.class);
        assertThatThrownBy(() -> names.remove(0)).isInstanceOf(UnsupportedOperationException.class);
        assertThatThrownBy(() -> scores.put("x", 1)).isInstanceOf(UnsupportedOperationException.class);
    }

    @Test
    void r4_withNameReturnsNewInstance() {
        Roster original = sample();
        Roster bigger = original.withName("cy");
        assertThat(bigger).isNotSameAs(original);
        assertThat(bigger.names()).containsExactly("ann", "bob", "cy");
        assertThat(bigger.scores()).isEqualTo(original.scores());
        assertThat(original.names()).containsExactly("ann", "bob");
    }

    @Test
    void r5_safeCopyIsAnImmutableSnapshot() {
        List<Integer> source = new ArrayList<>(List.of(1, 2));
        List<Number> copy = Roster.<Number>safeCopy(source);
        source.add(3);
        assertThat(copy).containsExactly(1, 2);
        assertThatThrownBy(() -> copy.add(4)).isInstanceOf(UnsupportedOperationException.class);
    }

    @Test
    void r6_viewVersusCopyExperiments() {
        List<String> base = new ArrayList<>(List.of("a", "b"));
        assertThat(Roster.viewReflectsChanges(base)).isTrue();
        assertThat(Roster.copyIgnoresChanges(base)).isTrue();
        assertThat(base).containsExactly("a", "b");
    }
}
'''},
            ["`List.copyOf` and `Map.copyOf` already throw `NullPointerException` for nulls - no manual checks needed.", "The wither can build a mutable `ArrayList`, append, and pass it to the constructor (which copies again)."],
            ["No field is ever exposed in mutable form", "`unmodifiableList` over internal state is avoided and justified in a comment", "Constructor performs the defensive copy (copy-in), getters return immutables (copy-out not needed)"],
        ),
    ],
)
