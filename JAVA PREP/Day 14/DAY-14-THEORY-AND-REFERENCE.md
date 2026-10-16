# Day 14 — Collections I: List, ArrayList, LinkedList, Iterator, Comparable and Comparator

**Phase:** Core Java  
**Primary theme:** Choose and use the right List implementation, iterate and mutate safely, and define ordering for your own types.  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-list-ops`, `task-02-iterator-remove`, `task-03-comparable-product`, `task-04-comparator-chain`  
**Instruction alignment:** Maps to the Day 14 entry of the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21 (no Spring today)

## Overview

Almost every backend method returns, filters, sorts, or groups a `List`. Knowing *which* list, *how* it fails, and *how* to order its elements separates code that merely works from code that survives production data.

Today you learn the `Collection`/`List` contracts, why `ArrayList` is the default and when `LinkedList` is a trap, how iterators let you mutate a collection safely during traversal, and how `Comparable` (natural order) and `Comparator` (external, composable order) work. Interviews ask: *ArrayList vs LinkedList*, *why ConcurrentModificationException*, *Comparable vs Comparator*, and *what does it mean for compareTo to be consistent with equals*.

## Day roadmap

1. List, ArrayList, and LinkedList
2. Iterator, ListIterator, and fail-fast behavior
3. Comparable and Comparator
4. Interview angles
5. Common mistakes & debugging
6. Further reading, glossary, answers

### List, ArrayList, and LinkedList

#### What it is

`List<E>` is an **ordered**, index-addressable `Collection` that permits duplicates. `ArrayList` stores elements in a resizable `Object[]`: O(1) random access (`get(i)`), amortized O(1) append, O(n) insert/remove in the middle (shifting). `LinkedList` is a doubly linked list (it is also a `Deque`): O(1) add/remove at the ends and at an *existing iterator position*, but O(n) to *reach* index `i`, and each node costs ~24+ bytes of overhead plus poor cache locality. Mental model: ArrayList = a shelf with numbered slots; LinkedList = a chain of people holding hands.

#### Why it exists / why it matters

Choosing the right structure determines latency and memory. In practice **`ArrayList` wins almost always** (even for many middle inserts, because contiguous memory and `System.arraycopy` are fast); `ArrayDeque` beats `LinkedList` as a queue/stack. Knowing the contract (`equals` semantics of `contains`, `indexOf`, `remove(Object)`) prevents subtle bugs.

#### Pros and cons

**Pros**

- `ArrayList`: fast random access, compact memory, cache friendly
- `LinkedList`: constant-time insert/remove at ends and through an iterator
- `List` interface lets you swap implementations without touching callers
- `subList`, `sort`, `replaceAll`, `removeIf` give a rich API

**Cons / tradeoffs**

- `ArrayList` insert/remove in the middle is O(n) shifting; growth copies the array (amortized)
- `LinkedList.get(i)` is O(n); a loop `for (i..) list.get(i)` becomes O(n^2)
- `subList` is a *view* - structural change of the parent invalidates it

#### What happens without it / when misused

A `for (int i...) linked.get(i)` loop on 100k nodes is 5 billion pointer hops. `List<Integer> l; l.remove(1)` removes **index** 1, not the value 1 (overload resolution picks `remove(int)`); to remove the value use `l.remove(Integer.valueOf(1))`. `Arrays.asList(arr)` returns a fixed-size list that write-through to the array: `add` throws `UnsupportedOperationException`. `List.of(...)` is immutable and rejects `null` elements with `NullPointerException`. Modifying a list while iterating with for-each throws `ConcurrentModificationException`.

#### Syntax and rules

- Prefer the interface on the left: `List<String> names = new ArrayList<>();`
- Presize when you know the size: `new ArrayList<>(expected)` to avoid regrowth.
- `remove(int index)` vs `remove(Object o)` - the overload trap with `List<Integer>`.
- Copying: `new ArrayList<>(other)`, `List.copyOf(other)` (immutable copy).
- Removal in bulk: `list.removeIf(x -> x < 0)` is O(n) and safe; repeated `remove` is O(n^2).
- `equals` for lists: same size and pairwise-equal elements in order, regardless of implementation.

#### Examples

**Example 1.1 — Tiny — the remove overload trap**

```java
List<Integer> xs = new ArrayList<>(List.of(10, 20, 30, 1, 2));
xs.remove(1);                       // removes INDEX 1 -> value 20
System.out.println(xs);             // [10, 30, 1, 2]
xs.remove(Integer.valueOf(1));      // removes VALUE 1
System.out.println(xs);             // [10, 30, 2]
```

**Example 1.2 — Tiny — fixed-size and immutable lists**

```java
List<String> a = Arrays.asList("x", "y");
a.set(0, "z");                      // allowed (write-through)
// a.add("w");                      // UnsupportedOperationException
List<String> b = List.of("x", "y");
// b.set(0, "z");                   // UnsupportedOperationException
// List.of("a", null);              // NullPointerException
```

**Example 1.3 — Medium — safe bulk operations and defensive copy**

```java
import java.util.*;

public class Inventory {
    private final List<String> skus = new ArrayList<>();

    public void add(String sku) { skus.add(Objects.requireNonNull(sku)); }

    /** Callers get a snapshot; they cannot corrupt internal state. */
    public List<String> snapshot() { return List.copyOf(skus); }

    public int purge(String prefix) {
        int before = skus.size();
        skus.removeIf(s -> s.startsWith(prefix));   // one pass, no CME
        return before - skus.size();
    }

    public static void main(String[] args) {
        Inventory inv = new Inventory();
        inv.add("A-1"); inv.add("B-1"); inv.add("A-2");
        System.out.println(inv.purge("A-"));        // 2
        System.out.println(inv.snapshot());         // [B-1]
    }
}
```

#### Quick checks

1. Why is iterating a `LinkedList` with `get(i)` slow?
2. What does `new ArrayList<>(List.of(1,2,3)).remove(1)` remove?
3. Can you add to a list returned by `Arrays.asList`? Can you `set`?
4. Name two reasons `ArrayList` usually beats `LinkedList`.

### Iterator, ListIterator, and fail-fast behavior

#### What it is

An `Iterator<E>` is a cursor over a collection with `hasNext()`, `next()`, and optional `remove()`. `ListIterator` adds `hasPrevious`, `previous`, `set`, `add`, and index queries. Most JDK collections are **fail-fast**: they keep a `modCount`; if the collection is structurally modified other than through the iterator, the next `next()` throws `ConcurrentModificationException` (best effort, not a guarantee). The enhanced for-loop is syntactic sugar over `iterator()`.

#### Why it exists / why it matters

You need iterators to remove or insert *during* traversal without O(n^2) index juggling or CME. They also decouple traversal from storage: any `Iterable` works in a for-each, which is why you implement `Iterable` on your own containers (like the stack from Day 13).

#### Pros and cons

**Pros**

- Safe in-place removal (`it.remove()`) and insertion (`ListIterator.add`)
- Uniform traversal across all collections
- Fail-fast detection reveals concurrency/logic bugs early
- `Iterable` + for-each makes custom containers ergonomic

**Cons / tradeoffs**

- Fail-fast is best effort; it does not make unsynchronized access safe
- `remove()` may be unsupported (immutable/`Arrays.asList`)
- `next()` after the end throws `NoSuchElementException`; calling `remove()` twice throws `IllegalStateException`

#### What happens without it / when misused

`for (String s : list) if (cond) list.remove(s);` throws `ConcurrentModificationException` - *except* in a notorious case: removing the **second-to-last** element makes `hasNext()` return false, so the loop exits silently and the bug hides until the data changes. Calling `it.remove()` before `it.next()` throws `IllegalStateException`. Sharing a list across threads while one thread iterates and another mutates can throw CME or, worse, silently skip elements.

#### Syntax and rules

- Remove safely: `Iterator<T> it = c.iterator(); while (it.hasNext()) { if (bad(it.next())) it.remove(); }`
- Prefer `collection.removeIf(predicate)` (Java 8+) - shorter and usually faster.
- `ListIterator<T> it = list.listIterator();` then `it.add(x)` inserts *before* the next element.
- `remove()` must follow a `next()` (or `previous()`); only one `remove()` per `next()`.
- Concurrent alternatives: `CopyOnWriteArrayList` (snapshot iterators, never CME).

#### Examples

**Example 2.1 — Tiny — safe removal**

```java
List<Integer> nums = new ArrayList<>(List.of(5, -1, 7, -3));
for (Iterator<Integer> it = nums.iterator(); it.hasNext(); ) {
    if (it.next() < 0) it.remove();
}
System.out.println(nums);   // [5, 7]
```

**Example 2.2 — Tiny — the CME and the silent exception**

```java
List<String> a = new ArrayList<>(List.of("a", "b", "c"));
try { for (String s : a) if (s.equals("a")) a.remove(s); }
catch (ConcurrentModificationException e) { System.out.println("CME"); }   // CME

List<String> b = new ArrayList<>(List.of("a", "b", "c"));
for (String s : b) if (s.equals("b")) b.remove(s);   // no exception! hasNext() == false
System.out.println(b);                               // [a, c]
```

**Example 2.3 — Medium — ListIterator insertion**

```java
// duplicate every even number in place
static void duplicateEvens(List<Integer> list) {
    ListIterator<Integer> it = list.listIterator();
    while (it.hasNext()) {
        int v = it.next();
        if (v % 2 == 0) it.add(v);      // inserted after v; cursor moves past it
    }
}
// [1, 2, 3, 4] -> [1, 2, 2, 3, 4, 4]
```

#### Quick checks

1. Why does removing the second-to-last element inside a for-each not throw?
2. What is the difference between `Iterator.remove()` and `List.remove(Object)` during traversal?
3. Which method on `ListIterator` inserts, and where does the element go?
4. Is fail-fast a thread-safety mechanism?

### Comparable and Comparator

#### What it is

`Comparable<T>` defines a type's **natural order** via `int compareTo(T other)` (negative, zero, positive). `Comparator<T>` is an **external** strategy `int compare(T a, T b)` so you can sort the same type many ways. Since Java 8 comparators compose: `Comparator.comparing(Employee::dept).thenComparing(Employee::salary, Comparator.reverseOrder())`, `reversed()`, `nullsFirst/nullsLast`. A good `compareTo` obeys: sign-symmetry, transitivity, and *should* be consistent with `equals` (`a.compareTo(b)==0` iff `a.equals(b)`), otherwise `TreeSet`/`TreeMap` and `HashSet` disagree on duplicates.

#### Why it exists / why it matters

Sorting, binary search, `TreeSet`, `TreeMap`, `PriorityQueue`, `Collections.max`, and streams' `sorted()` all rely on ordering. Real code needs multiple orders (by date for audit, by amount for reports), null-safe orders, and stable multi-key sorts. `List.sort` and `Arrays.sort(Object[])` are **stable** (TimSort): equal elements keep their relative order, which is why chaining sorts works.

#### Pros and cons

**Pros**

- Natural order gives a default for sorted collections
- Comparators are reusable, composable, and testable in isolation
- Stable sorts enable predictable multi-key ordering
- `Comparator.comparing` removes boilerplate and subtraction bugs

**Cons / tradeoffs**

- Inconsistent `compareTo`/`equals` causes surprising `TreeSet` behavior
- A type can have only one natural order
- Comparators with side effects or non-transitive logic break sorting (`Comparison method violates its general contract!`)

#### What happens without it / when misused

Writing `return a.price - b.price;` overflows for large ints and gives wrong order - use `Integer.compare`. A comparator that returns `1` for both `(a,b)` and `(b,a)` triggers `IllegalArgumentException: Comparison method violates its general contract!` from TimSort on large inputs. Mutable fields used in `compareTo` of an element already inside a `TreeSet` corrupt the tree (lookups fail). A `TreeSet<Product>` whose `compareTo` ignores a field treats distinct products as duplicates and silently drops them. `Comparator.comparing(Person::name)` throws NPE on a null name unless wrapped with `nullsLast`.

#### Syntax and rules

- `compareTo` contract: `sgn(x.compareTo(y)) == -sgn(y.compareTo(x))`; transitive; `x.compareTo(y)==0` implies same sign vs any `z`.
- Never subtract to compare; use `Integer.compare`, `Long.compare`, `Double.compare`, `String.compareTo`.
- Multi-key: `Comparator.comparing(A::x).thenComparing(A::y).thenComparing(A::z, Comparator.reverseOrder())`.
- Primitive-specialized: `comparingInt`, `comparingDouble` avoid boxing.
- Null handling: `Comparator.nullsFirst(cmp)` / `nullsLast(cmp)`.
- Case-insensitive strings: `String.CASE_INSENSITIVE_ORDER`.
- Sort: `list.sort(cmp)` (stable), `Collections.sort(list)` uses natural order, `Collections.max(coll, cmp)`.

#### Examples

**Example 3.1 — Tiny — natural order record-like class**

```java
final class Version implements Comparable<Version> {
    final int major, minor;
    Version(int major, int minor) { this.major = major; this.minor = minor; }
    @Override public int compareTo(Version o) {
        int c = Integer.compare(major, o.major);
        return c != 0 ? c : Integer.compare(minor, o.minor);
    }
    @Override public boolean equals(Object o) {
        return o instanceof Version v && v.major == major && v.minor == minor;
    }
    @Override public int hashCode() { return 31 * major + minor; }
}
```

**Example 3.2 — Tiny — comparator chain**

```java
record Emp(String name, String dept, double salary) {}
List<Emp> emps = new ArrayList<>(List.of(
    new Emp("Zed", "ENG", 100), new Emp("Amy", "ENG", 120), new Emp("Bob", "HR", 90)));
emps.sort(Comparator.comparing(Emp::dept)
        .thenComparing(Emp::salary, Comparator.reverseOrder())
        .thenComparing(Emp::name));
// ENG/Amy(120), ENG/Zed(100), HR/Bob(90)
```

**Example 3.3 — Medium — null-safe, case-insensitive sort + stability**

```java
import java.util.*;

public class SortDemo {
    record Person(String name, int age) {}

    public static void main(String[] args) {
        List<Person> people = new ArrayList<>(List.of(
                new Person("bob", 30), new Person(null, 25),
                new Person("Alice", 30), new Person("carol", 25)));

        Comparator<Person> byName = Comparator.comparing(Person::name,
                Comparator.nullsLast(String.CASE_INSENSITIVE_ORDER));
        people.sort(Comparator.comparingInt(Person::age).thenComparing(byName));

        people.forEach(System.out::println);
        // Person[name=carol, age=25]
        // Person[name=null, age=25]
        // Person[name=Alice, age=30]
        // Person[name=bob, age=30]
    }
}
```

#### Quick checks

1. What does "compareTo consistent with equals" mean and why does it matter?
2. Why is `return a.x - b.x` a bad comparator?
3. What does it mean that `List.sort` is stable, and how can you exploit it?
4. How do you sort strings case-insensitively with nulls last?

## Interview angles

**Q: ArrayList vs LinkedList - when would you ever choose LinkedList?**

Rarely. ArrayList is faster for nearly everything thanks to locality; LinkedList helps only for heavy insert/remove at an iterator position over large lists, and `ArrayDeque` is better for queue/stack use.

**Q: How does ArrayList grow?**

When full it allocates a new array ~1.5x the old size (`oldCapacity + (oldCapacity >> 1)`) and copies; adds are amortized O(1). Presize to avoid repeated copies.

**Q: What is ConcurrentModificationException and how do you avoid it?**

Thrown by fail-fast iterators when the collection is structurally modified outside the iterator. Use `Iterator.remove`, `removeIf`, collect-then-remove, or a concurrent collection.

**Q: Comparable vs Comparator?**

Comparable is the type's single natural ordering (inside the class); Comparator is a pluggable external ordering, composable and usable on classes you cannot modify.

**Q: Why is `List<Integer>.remove(1)` surprising?**

Overload resolution prefers the exact `remove(int index)` over boxing to `remove(Object)`.

**Q: `Arrays.asList` vs `List.of` vs `new ArrayList<>(...)`?**

`asList`: fixed-size, write-through to the array, nulls allowed. `List.of`: immutable, no nulls. `ArrayList`: independent, fully mutable.

## Common mistakes & debugging

- Using index `get(i)` loops on `LinkedList` (accidentally quadratic).
- Removing from a list inside a for-each (`ConcurrentModificationException`) - or worse, hitting the silent second-to-last case.
- Calling `list.remove(intValue)` on `List<Integer>` and removing by index.
- `compareTo` that subtracts ints, ignores a field that `equals` uses, or reads mutable state.
- Sorting with a comparator that throws NPE on null fields instead of using `nullsFirst/nullsLast`.
- Returning an internal mutable list from a getter instead of a copy/unmodifiable view.

## Further reading

- Javadoc: `java.util.List`, `ArrayList`, `LinkedList`, `Iterator`, `ListIterator`, `Comparable`, `Comparator`
- Oracle Java Tutorials - *Collections* trail, *Interfaces: List*, *Object Ordering*
- *Effective Java* (Bloch) item 14 (Comparable) and item 28 (prefer lists to arrays)
- JDK source: `ArrayList#grow`, `ArrayList$Itr` (to see `modCount` checks)

## Glossary

| Term | Meaning |
|------|---------|
| Fail-fast | Iterator behavior of detecting concurrent structural modification and throwing CME (best effort) |
| modCount | Internal modification counter checked by fail-fast iterators |
| Natural order | The ordering defined by a class's `compareTo` |
| Stable sort | Sort that preserves the relative order of equal elements |
| Structural modification | Add/remove (size change); `set` is not structural |
| View | A live window on another collection (`subList`, `Arrays.asList`) |
| Amortized O(1) | Average constant cost over many operations despite occasional O(n) resizes |

## Answers

Answers to every **Quick check** above (numbered `section.question`).

- **1.1** — Why is iterating a `LinkedList` with `get(i)` slow?  
  Each `get(i)` walks from the nearest end, O(n); the loop becomes O(n^2). Use an iterator or for-each.

- **1.2** — What does `new ArrayList<>(List.of(1,2,3)).remove(1)` remove?  
  The element at index 1 (the value 2) because `remove(int)` is chosen over `remove(Object)`.

- **1.3** — Can you add to a list returned by `Arrays.asList`? Can you `set`?  
  No for add/remove (`UnsupportedOperationException`); yes for `set`, which writes through to the array.

- **1.4** — Name two reasons `ArrayList` usually beats `LinkedList`.  
  Contiguous memory (cache locality) and lower per-element overhead; `get(i)` is O(1).

- **2.1** — Why does removing the second-to-last element inside a for-each not throw?  
  After removal `size` equals the cursor, `hasNext()` returns false and the loop ends before `next()` can check `modCount`.

- **2.2** — What is the difference between `Iterator.remove()` and `List.remove(Object)` during traversal?  
  `Iterator.remove()` updates the iterator's expected modCount; `List.remove` does not, so the next `next()` throws CME.

- **2.3** — Which method on `ListIterator` inserts, and where does the element go?  
  `add(e)` inserts immediately before the element that `next()` would return, i.e. behind the cursor.

- **2.4** — Is fail-fast a thread-safety mechanism?  
  No - it is a best-effort bug detector; use concurrent collections or synchronization.

- **3.1** — What does "compareTo consistent with equals" mean and why does it matter?  
  `a.compareTo(b)==0` exactly when `a.equals(b)`. Otherwise sorted sets/maps (compareTo) and hash sets/maps (equals) disagree about duplicates.

- **3.2** — Why is `return a.x - b.x` a bad comparator?  
  Integer subtraction can overflow, producing the wrong sign; use `Integer.compare`.

- **3.3** — What does it mean that `List.sort` is stable, and how can you exploit it?  
  Elements that compare equal keep their original relative order, so you can sort by a secondary key first, then a primary key.

- **3.4** — How do you sort strings case-insensitively with nulls last?  
  `Comparator.nullsLast(String.CASE_INSENSITIVE_ORDER)`.
