from gen_helpers import sec, task

DAY = dict(
    num=14,
    title="Collections I: List, ArrayList, LinkedList, Iterator, Comparable and Comparator",
    theme="Choose and use the right List implementation, iterate and mutate safely, and define ordering for your own types.",
    objectives=[
        "Explain the `Collection` / `List` contract and the cost model of `ArrayList` versus `LinkedList`",
        "Use `Iterator` and `ListIterator` to remove or insert while traversing, and explain fail-fast `ConcurrentModificationException`",
        "Avoid the `List.remove(int)` vs `remove(Object)` overload trap",
        "Implement `Comparable` consistently with `equals` and `hashCode`",
        "Build multi-key sort orders with `Comparator.comparing(...).thenComparing(...)`, `reversed`, and `nullsLast`",
        "Distinguish unmodifiable views, `Arrays.asList`, and `List.of`",
    ],
    prereqs=["Day 13 — generics (collections are generic types)", "Day 08–09 — `equals`/`hashCode` and interfaces"],
    overview="""Almost every backend method returns, filters, sorts, or groups a `List`. Knowing *which* list, *how* it fails, and *how* to order its elements separates code that merely works from code that survives production data.

Today you learn the `Collection`/`List` contracts, why `ArrayList` is the default and when `LinkedList` is a trap, how iterators let you mutate a collection safely during traversal, and how `Comparable` (natural order) and `Comparator` (external, composable order) work. Interviews ask: *ArrayList vs LinkedList*, *why ConcurrentModificationException*, *Comparable vs Comparator*, and *what does it mean for compareTo to be consistent with equals*.""",
    sections=[
        sec(
            "List, ArrayList, and LinkedList",
            "`List<E>` is an **ordered**, index-addressable `Collection` that permits duplicates. `ArrayList` stores elements in a resizable `Object[]`: O(1) random access (`get(i)`), amortized O(1) append, O(n) insert/remove in the middle (shifting). `LinkedList` is a doubly linked list (it is also a `Deque`): O(1) add/remove at the ends and at an *existing iterator position*, but O(n) to *reach* index `i`, and each node costs ~24+ bytes of overhead plus poor cache locality. Mental model: ArrayList = a shelf with numbered slots; LinkedList = a chain of people holding hands.",
            "Choosing the right structure determines latency and memory. In practice **`ArrayList` wins almost always** (even for many middle inserts, because contiguous memory and `System.arraycopy` are fast); `ArrayDeque` beats `LinkedList` as a queue/stack. Knowing the contract (`equals` semantics of `contains`, `indexOf`, `remove(Object)`) prevents subtle bugs.",
            ["`ArrayList`: fast random access, compact memory, cache friendly", "`LinkedList`: constant-time insert/remove at ends and through an iterator", "`List` interface lets you swap implementations without touching callers", "`subList`, `sort`, `replaceAll`, `removeIf` give a rich API"],
            ["`ArrayList` insert/remove in the middle is O(n) shifting; growth copies the array (amortized)", "`LinkedList.get(i)` is O(n); a loop `for (i..) list.get(i)` becomes O(n^2)", "`subList` is a *view* - structural change of the parent invalidates it"],
            "A `for (int i...) linked.get(i)` loop on 100k nodes is 5 billion pointer hops. `List<Integer> l; l.remove(1)` removes **index** 1, not the value 1 (overload resolution picks `remove(int)`); to remove the value use `l.remove(Integer.valueOf(1))`. `Arrays.asList(arr)` returns a fixed-size list that write-through to the array: `add` throws `UnsupportedOperationException`. `List.of(...)` is immutable and rejects `null` elements with `NullPointerException`. Modifying a list while iterating with for-each throws `ConcurrentModificationException`.",
            """- Prefer the interface on the left: `List<String> names = new ArrayList<>();`
- Presize when you know the size: `new ArrayList<>(expected)` to avoid regrowth.
- `remove(int index)` vs `remove(Object o)` - the overload trap with `List<Integer>`.
- Copying: `new ArrayList<>(other)`, `List.copyOf(other)` (immutable copy).
- Removal in bulk: `list.removeIf(x -> x < 0)` is O(n) and safe; repeated `remove` is O(n^2).
- `equals` for lists: same size and pairwise-equal elements in order, regardless of implementation.""",
            [
                ("Tiny — the remove overload trap", """List<Integer> xs = new ArrayList<>(List.of(10, 20, 30, 1, 2));
xs.remove(1);                       // removes INDEX 1 -> value 20
System.out.println(xs);             // [10, 30, 1, 2]
xs.remove(Integer.valueOf(1));      // removes VALUE 1
System.out.println(xs);             // [10, 30, 2]"""),
                ("Tiny — fixed-size and immutable lists", """List<String> a = Arrays.asList("x", "y");
a.set(0, "z");                      // allowed (write-through)
// a.add("w");                      // UnsupportedOperationException
List<String> b = List.of("x", "y");
// b.set(0, "z");                   // UnsupportedOperationException
// List.of("a", null);              // NullPointerException"""),
                ("Medium — safe bulk operations and defensive copy", """import java.util.*;

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
}"""),
            ],
            [
                ("Why is iterating a `LinkedList` with `get(i)` slow?", "Each `get(i)` walks from the nearest end, O(n); the loop becomes O(n^2). Use an iterator or for-each."),
                ("What does `new ArrayList<>(List.of(1,2,3)).remove(1)` remove?", "The element at index 1 (the value 2) because `remove(int)` is chosen over `remove(Object)`."),
                ("Can you add to a list returned by `Arrays.asList`? Can you `set`?", "No for add/remove (`UnsupportedOperationException`); yes for `set`, which writes through to the array."),
                ("Name two reasons `ArrayList` usually beats `LinkedList`.", "Contiguous memory (cache locality) and lower per-element overhead; `get(i)` is O(1)."),
            ],
        ),
        sec(
            "Iterator, ListIterator, and fail-fast behavior",
            "An `Iterator<E>` is a cursor over a collection with `hasNext()`, `next()`, and optional `remove()`. `ListIterator` adds `hasPrevious`, `previous`, `set`, `add`, and index queries. Most JDK collections are **fail-fast**: they keep a `modCount`; if the collection is structurally modified other than through the iterator, the next `next()` throws `ConcurrentModificationException` (best effort, not a guarantee). The enhanced for-loop is syntactic sugar over `iterator()`.",
            "You need iterators to remove or insert *during* traversal without O(n^2) index juggling or CME. They also decouple traversal from storage: any `Iterable` works in a for-each, which is why you implement `Iterable` on your own containers (like the stack from Day 13).",
            ["Safe in-place removal (`it.remove()`) and insertion (`ListIterator.add`)", "Uniform traversal across all collections", "Fail-fast detection reveals concurrency/logic bugs early", "`Iterable` + for-each makes custom containers ergonomic"],
            ["Fail-fast is best effort; it does not make unsynchronized access safe", "`remove()` may be unsupported (immutable/`Arrays.asList`)", "`next()` after the end throws `NoSuchElementException`; calling `remove()` twice throws `IllegalStateException`"],
            "`for (String s : list) if (cond) list.remove(s);` throws `ConcurrentModificationException` - *except* in a notorious case: removing the **second-to-last** element makes `hasNext()` return false, so the loop exits silently and the bug hides until the data changes. Calling `it.remove()` before `it.next()` throws `IllegalStateException`. Sharing a list across threads while one thread iterates and another mutates can throw CME or, worse, silently skip elements.",
            """- Remove safely: `Iterator<T> it = c.iterator(); while (it.hasNext()) { if (bad(it.next())) it.remove(); }`
- Prefer `collection.removeIf(predicate)` (Java 8+) - shorter and usually faster.
- `ListIterator<T> it = list.listIterator();` then `it.add(x)` inserts *before* the next element.
- `remove()` must follow a `next()` (or `previous()`); only one `remove()` per `next()`.
- Concurrent alternatives: `CopyOnWriteArrayList` (snapshot iterators, never CME).""",
            [
                ("Tiny — safe removal", """List<Integer> nums = new ArrayList<>(List.of(5, -1, 7, -3));
for (Iterator<Integer> it = nums.iterator(); it.hasNext(); ) {
    if (it.next() < 0) it.remove();
}
System.out.println(nums);   // [5, 7]"""),
                ("Tiny — the CME and the silent exception", """List<String> a = new ArrayList<>(List.of("a", "b", "c"));
try { for (String s : a) if (s.equals("a")) a.remove(s); }
catch (ConcurrentModificationException e) { System.out.println("CME"); }   // CME

List<String> b = new ArrayList<>(List.of("a", "b", "c"));
for (String s : b) if (s.equals("b")) b.remove(s);   // no exception! hasNext() == false
System.out.println(b);                               // [a, c]"""),
                ("Medium — ListIterator insertion", """// duplicate every even number in place
static void duplicateEvens(List<Integer> list) {
    ListIterator<Integer> it = list.listIterator();
    while (it.hasNext()) {
        int v = it.next();
        if (v % 2 == 0) it.add(v);      // inserted after v; cursor moves past it
    }
}
// [1, 2, 3, 4] -> [1, 2, 2, 3, 4, 4]"""),
            ],
            [
                ("Why does removing the second-to-last element inside a for-each not throw?", "After removal `size` equals the cursor, `hasNext()` returns false and the loop ends before `next()` can check `modCount`."),
                ("What is the difference between `Iterator.remove()` and `List.remove(Object)` during traversal?", "`Iterator.remove()` updates the iterator's expected modCount; `List.remove` does not, so the next `next()` throws CME."),
                ("Which method on `ListIterator` inserts, and where does the element go?", "`add(e)` inserts immediately before the element that `next()` would return, i.e. behind the cursor."),
                ("Is fail-fast a thread-safety mechanism?", "No - it is a best-effort bug detector; use concurrent collections or synchronization."),
            ],
        ),
        sec(
            "Comparable and Comparator",
            "`Comparable<T>` defines a type's **natural order** via `int compareTo(T other)` (negative, zero, positive). `Comparator<T>` is an **external** strategy `int compare(T a, T b)` so you can sort the same type many ways. Since Java 8 comparators compose: `Comparator.comparing(Employee::dept).thenComparing(Employee::salary, Comparator.reverseOrder())`, `reversed()`, `nullsFirst/nullsLast`. A good `compareTo` obeys: sign-symmetry, transitivity, and *should* be consistent with `equals` (`a.compareTo(b)==0` iff `a.equals(b)`), otherwise `TreeSet`/`TreeMap` and `HashSet` disagree on duplicates.",
            "Sorting, binary search, `TreeSet`, `TreeMap`, `PriorityQueue`, `Collections.max`, and streams' `sorted()` all rely on ordering. Real code needs multiple orders (by date for audit, by amount for reports), null-safe orders, and stable multi-key sorts. `List.sort` and `Arrays.sort(Object[])` are **stable** (TimSort): equal elements keep their relative order, which is why chaining sorts works.",
            ["Natural order gives a default for sorted collections", "Comparators are reusable, composable, and testable in isolation", "Stable sorts enable predictable multi-key ordering", "`Comparator.comparing` removes boilerplate and subtraction bugs"],
            ["Inconsistent `compareTo`/`equals` causes surprising `TreeSet` behavior", "A type can have only one natural order", "Comparators with side effects or non-transitive logic break sorting (`Comparison method violates its general contract!`)"],
            "Writing `return a.price - b.price;` overflows for large ints and gives wrong order - use `Integer.compare`. A comparator that returns `1` for both `(a,b)` and `(b,a)` triggers `IllegalArgumentException: Comparison method violates its general contract!` from TimSort on large inputs. Mutable fields used in `compareTo` of an element already inside a `TreeSet` corrupt the tree (lookups fail). A `TreeSet<Product>` whose `compareTo` ignores a field treats distinct products as duplicates and silently drops them. `Comparator.comparing(Person::name)` throws NPE on a null name unless wrapped with `nullsLast`.",
            """- `compareTo` contract: `sgn(x.compareTo(y)) == -sgn(y.compareTo(x))`; transitive; `x.compareTo(y)==0` implies same sign vs any `z`.
- Never subtract to compare; use `Integer.compare`, `Long.compare`, `Double.compare`, `String.compareTo`.
- Multi-key: `Comparator.comparing(A::x).thenComparing(A::y).thenComparing(A::z, Comparator.reverseOrder())`.
- Primitive-specialized: `comparingInt`, `comparingDouble` avoid boxing.
- Null handling: `Comparator.nullsFirst(cmp)` / `nullsLast(cmp)`.
- Case-insensitive strings: `String.CASE_INSENSITIVE_ORDER`.
- Sort: `list.sort(cmp)` (stable), `Collections.sort(list)` uses natural order, `Collections.max(coll, cmp)`.""",
            [
                ("Tiny — natural order record-like class", """final class Version implements Comparable<Version> {
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
}"""),
                ("Tiny — comparator chain", """record Emp(String name, String dept, double salary) {}
List<Emp> emps = new ArrayList<>(List.of(
    new Emp("Zed", "ENG", 100), new Emp("Amy", "ENG", 120), new Emp("Bob", "HR", 90)));
emps.sort(Comparator.comparing(Emp::dept)
        .thenComparing(Emp::salary, Comparator.reverseOrder())
        .thenComparing(Emp::name));
// ENG/Amy(120), ENG/Zed(100), HR/Bob(90)"""),
                ("Medium — null-safe, case-insensitive sort + stability", """import java.util.*;

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
}"""),
            ],
            [
                ("What does \"compareTo consistent with equals\" mean and why does it matter?", "`a.compareTo(b)==0` exactly when `a.equals(b)`. Otherwise sorted sets/maps (compareTo) and hash sets/maps (equals) disagree about duplicates."),
                ("Why is `return a.x - b.x` a bad comparator?", "Integer subtraction can overflow, producing the wrong sign; use `Integer.compare`."),
                ("What does it mean that `List.sort` is stable, and how can you exploit it?", "Elements that compare equal keep their original relative order, so you can sort by a secondary key first, then a primary key."),
                ("How do you sort strings case-insensitively with nulls last?", "`Comparator.nullsLast(String.CASE_INSENSITIVE_ORDER)`."),
            ],
        ),
    ],
    interview=[
        ("ArrayList vs LinkedList - when would you ever choose LinkedList?", "Rarely. ArrayList is faster for nearly everything thanks to locality; LinkedList helps only for heavy insert/remove at an iterator position over large lists, and `ArrayDeque` is better for queue/stack use."),
        ("How does ArrayList grow?", "When full it allocates a new array ~1.5x the old size (`oldCapacity + (oldCapacity >> 1)`) and copies; adds are amortized O(1). Presize to avoid repeated copies."),
        ("What is ConcurrentModificationException and how do you avoid it?", "Thrown by fail-fast iterators when the collection is structurally modified outside the iterator. Use `Iterator.remove`, `removeIf`, collect-then-remove, or a concurrent collection."),
        ("Comparable vs Comparator?", "Comparable is the type's single natural ordering (inside the class); Comparator is a pluggable external ordering, composable and usable on classes you cannot modify."),
        ("Why is `List<Integer>.remove(1)` surprising?", "Overload resolution prefers the exact `remove(int index)` over boxing to `remove(Object)`."),
        ("`Arrays.asList` vs `List.of` vs `new ArrayList<>(...)`?", "`asList`: fixed-size, write-through to the array, nulls allowed. `List.of`: immutable, no nulls. `ArrayList`: independent, fully mutable."),
    ],
    mistakes=[
        "Using index `get(i)` loops on `LinkedList` (accidentally quadratic).",
        "Removing from a list inside a for-each (`ConcurrentModificationException`) - or worse, hitting the silent second-to-last case.",
        "Calling `list.remove(intValue)` on `List<Integer>` and removing by index.",
        "`compareTo` that subtracts ints, ignores a field that `equals` uses, or reads mutable state.",
        "Sorting with a comparator that throws NPE on null fields instead of using `nullsFirst/nullsLast`.",
        "Returning an internal mutable list from a getter instead of a copy/unmodifiable view.",
    ],
    reading=[
        "Javadoc: `java.util.List`, `ArrayList`, `LinkedList`, `Iterator`, `ListIterator`, `Comparable`, `Comparator`",
        "Oracle Java Tutorials - *Collections* trail, *Interfaces: List*, *Object Ordering*",
        "*Effective Java* (Bloch) item 14 (Comparable) and item 28 (prefer lists to arrays)",
        "JDK source: `ArrayList#grow`, `ArrayList$Itr` (to see `modCount` checks)",
    ],
    glossary=[
        ("Fail-fast", "Iterator behavior of detecting concurrent structural modification and throwing CME (best effort)"),
        ("modCount", "Internal modification counter checked by fail-fast iterators"),
        ("Natural order", "The ordering defined by a class's `compareTo`"),
        ("Stable sort", "Sort that preserves the relative order of equal elements"),
        ("Structural modification", "Add/remove (size change); `set` is not structural"),
        ("View", "A live window on another collection (`subList`, `Arrays.asList`)"),
        ("Amortized O(1)", "Average constant cost over many operations despite occasional O(n) resizes"),
    ],
    tasks=[
        task(
            "list-ops", "List Operations Toolkit", "Warm-up", "ListOps",
            "Implement four everyday list utilities: order-preserving de-duplication, rotation, chunking, and removal of the first occurrence of a value (not an index). Each returns a **new** list and never mutates the argument. The tests deliberately use both `ArrayList` and `LinkedList` inputs and include the `remove(int)` vs `remove(Object)` trap.",
            [
                "`dedupe(list)` returns a new list without duplicates, keeping the first occurrence order; `null` input throws `NullPointerException`",
                "`rotate(list, k)` returns a new list rotated right by `k` (negative `k` rotates left, `|k|` larger than size wraps, empty list returns empty)",
                "`chunk(list, size)` splits into consecutive sub-lists of `size` (last may be shorter); chunks are independent copies; `size <= 0` throws `IllegalArgumentException`",
                "`removeFirstOccurrence(list, value)` returns a copy with the first element **equal to** `value` removed (value semantics, not index), or an unchanged copy when absent; the argument is never mutated",
            ],
            ["empty lists", "rotation by multiples of the size", "negative rotation", "chunk size larger than list", "list containing duplicate and `null`-free values"],
            {"ListOps.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Objects;

/** Small List utilities. None of them mutate their argument. */
public final class ListOps {

    private ListOps() {
    }

    public static <T> List<T> dedupe(List<T> input) {
        //@TODO dedupe | return a new list with duplicates removed, first occurrences kept in order; NullPointerException for null input
        Objects.requireNonNull(input, "input");
        return new ArrayList<>(new LinkedHashSet<>(input));
        //@END
    }

    public static <T> List<T> rotate(List<T> input, int k) {
        //@TODO rotate | return a new list rotated right by k; negative k rotates left; |k| may exceed size; empty list gives empty list
        int n = input.size();
        if (n == 0) {
            return new ArrayList<>();
        }
        int shift = ((k % n) + n) % n;
        List<T> result = new ArrayList<>(input);
        for (int i = 0; i < n; i++) {
            result.set((i + shift) % n, input.get(i));
        }
        return result;
        //@END
    }

    public static <T> List<List<T>> chunk(List<T> input, int size) {
        //@TODO chunk | split into consecutive copies of at most size elements; IllegalArgumentException when size <= 0
        if (size <= 0) {
            throw new IllegalArgumentException("size must be > 0");
        }
        List<List<T>> chunks = new ArrayList<>();
        for (int start = 0; start < input.size(); start += size) {
            int end = Math.min(start + size, input.size());
            chunks.add(new ArrayList<>(input.subList(start, end)));
        }
        return chunks;
        //@END
    }

    public static List<Integer> removeFirstOccurrence(List<Integer> input, int value) {
        //@TODO removeFirstOccurrence | return a copy without the first element equal to value (NOT index value); unchanged copy if absent; do not mutate input
        List<Integer> copy = new ArrayList<>(input);
        copy.remove(Integer.valueOf(value));
        return copy;
        //@END
    }
}
'''},
            {"ListOpsTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ListOpsTest {

    @Test
    void r1_dedupeKeepsFirstOccurrenceOrder() {
        assertThat(ListOps.dedupe(List.of("b", "a", "b", "c", "a"))).containsExactly("b", "a", "c");
        assertThat(ListOps.dedupe(new LinkedList<>(List.of(3, 3, 3)))).containsExactly(3);
        assertThat(ListOps.dedupe(List.<String>of())).isEmpty();
    }

    @Test
    void r1_dedupeReturnsNewMutableListAndRejectsNull() {
        List<String> in = new ArrayList<>(List.of("a", "a"));
        List<String> out = ListOps.dedupe(in);
        out.add("z");
        assertThat(in).containsExactly("a", "a");
        assertThatThrownBy(() -> ListOps.dedupe(null)).isInstanceOf(NullPointerException.class);
    }

    @Test
    void r2_rotateRight() {
        assertThat(ListOps.rotate(List.of(1, 2, 3, 4, 5), 2)).containsExactly(4, 5, 1, 2, 3);
        assertThat(ListOps.rotate(List.of(1, 2, 3), 0)).containsExactly(1, 2, 3);
        assertThat(ListOps.rotate(List.of(1, 2, 3), 3)).containsExactly(1, 2, 3);
        assertThat(ListOps.rotate(List.of(1, 2, 3), 4)).containsExactly(3, 1, 2);
    }

    @Test
    void r2_rotateLeftAndEmpty() {
        assertThat(ListOps.rotate(List.of(1, 2, 3, 4), -1)).containsExactly(2, 3, 4, 1);
        assertThat(ListOps.rotate(List.of(1, 2, 3), -7)).containsExactly(2, 3, 1);
        assertThat(ListOps.rotate(List.<Integer>of(), 5)).isEmpty();
    }

    @Test
    void r3_chunk() {
        List<List<Integer>> chunks = ListOps.chunk(List.of(1, 2, 3, 4, 5), 2);
        assertThat(chunks).containsExactly(List.of(1, 2), List.of(3, 4), List.of(5));
        assertThat(ListOps.chunk(List.of(1, 2), 10)).containsExactly(List.of(1, 2));
        assertThat(ListOps.chunk(List.<Integer>of(), 3)).isEmpty();
    }

    @Test
    void r3_chunksAreIndependentCopiesAndSizeIsValidated() {
        List<Integer> source = new ArrayList<>(List.of(1, 2, 3, 4));
        List<List<Integer>> chunks = ListOps.chunk(source, 2);
        source.set(0, 99);
        assertThat(chunks.get(0)).containsExactly(1, 2);
        assertThatThrownBy(() -> ListOps.chunk(source, 0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> ListOps.chunk(source, -2)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    @DisplayName("Trap: remove the VALUE 1, not the element at index 1")
    void r4_removeFirstOccurrenceByValue() {
        List<Integer> in = new ArrayList<>(List.of(10, 20, 30, 1, 2));
        assertThat(ListOps.removeFirstOccurrence(in, 1)).containsExactly(10, 20, 30, 2);
        assertThat(in).containsExactly(10, 20, 30, 1, 2);
    }

    @Test
    void r4_removeOnlyFirstAndMissingValue() {
        assertThat(ListOps.removeFirstOccurrence(List.of(5, 7, 5, 7), 7)).containsExactly(5, 5, 7);
        assertThat(ListOps.removeFirstOccurrence(new LinkedList<>(List.of(1, 2)), 9)).containsExactly(1, 2);
    }
}
'''},
            ["`new ArrayList<>(new LinkedHashSet<>(input))` is a compact dedupe.", "For `rotate`, compute `shift = ((k % n) + n) % n` so negatives behave.", "`list.remove(Integer.valueOf(v))` removes by value."],
            ["Argument lists are never mutated", "The `remove(Object)` vs `remove(int)` trap is handled explicitly", "No O(n^2) work on `LinkedList` inputs beyond what is required"],
        ),
        task(
            "iterator-remove", "Iterator Removal Lab", "Core", "IteratorOps",
            "Practice safe in-place mutation with `Iterator` and `ListIterator`, and prove you understand the fail-fast quirk by writing a method that reports whether a for-each removal throws `ConcurrentModificationException` (including the silent second-to-last case).",
            [
                "`removeNegatives(List<Integer>)` removes negative values **in place** using `Iterator.remove()` and returns how many were removed",
                "`removeMatching(Collection<T>, Predicate<? super T>)` removes matching elements in place and returns the count (use an iterator, not `removeIf`)",
                "`duplicateEvens(List<Integer>)` inserts a copy right after each even number using `ListIterator.add`",
                "`forEachRemovalThrows(input, toRemove)` copies the list, removes `toRemove` inside a for-each loop, and returns `true` if `ConcurrentModificationException` was thrown, else `false`",
            ],
            ["empty collection", "all elements match / none match", "`LinkedList` and `ArrayList` both supported", "removing the second-to-last element does not throw", "value not present"],
            {"IteratorOps.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.Collection;
import java.util.ConcurrentModificationException;
import java.util.Iterator;
import java.util.List;
import java.util.ListIterator;
import java.util.function.Predicate;

/** Iterator-based mutation helpers. */
public final class IteratorOps {

    private IteratorOps() {
    }

    public static int removeNegatives(List<Integer> list) {
        //@TODO removeNegatives | remove every negative value in place via Iterator.remove() and return the number removed
        int removed = 0;
        Iterator<Integer> it = list.iterator();
        while (it.hasNext()) {
            if (it.next() < 0) {
                it.remove();
                removed++;
            }
        }
        return removed;
        //@END
    }

    public static <T> int removeMatching(Collection<T> collection, Predicate<? super T> predicate) {
        //@TODO removeMatching | remove every element matching predicate in place using an explicit Iterator (not removeIf); return the count
        int removed = 0;
        for (Iterator<T> it = collection.iterator(); it.hasNext(); ) {
            if (predicate.test(it.next())) {
                it.remove();
                removed++;
            }
        }
        return removed;
        //@END
    }

    public static void duplicateEvens(List<Integer> list) {
        //@TODO duplicateEvens | using a ListIterator, insert a copy immediately after every even value (e.g. [1,2,3,4] -> [1,2,2,3,4,4])
        ListIterator<Integer> it = list.listIterator();
        while (it.hasNext()) {
            int value = it.next();
            if (value % 2 == 0) {
                it.add(value);
            }
        }
        //@END
    }

    public static boolean forEachRemovalThrows(List<String> input, String toRemove) {
        //@TODO forEachRemovalThrows | copy input into an ArrayList, remove toRemove inside a for-each, return true if ConcurrentModificationException was thrown else false
        List<String> copy = new ArrayList<>(input);
        try {
            for (String s : copy) {
                if (s.equals(toRemove)) {
                    copy.remove(s);
                }
            }
            return false;
        } catch (ConcurrentModificationException e) {
            return true;
        }
        //@END
    }
}
'''},
            {"IteratorOpsTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class IteratorOpsTest {

    @Test
    void r1_removeNegativesInPlace() {
        List<Integer> list = new ArrayList<>(List.of(5, -1, 7, -3, 0));
        int removed = IteratorOps.removeNegatives(list);
        assertThat(removed).isEqualTo(2);
        assertThat(list).containsExactly(5, 7, 0);
    }

    @Test
    void r1_removeNegativesEdgeCases() {
        List<Integer> none = new LinkedList<>(List.of(1, 2));
        assertThat(IteratorOps.removeNegatives(none)).isZero();
        List<Integer> all = new LinkedList<>(List.of(-1, -2, -3));
        assertThat(IteratorOps.removeNegatives(all)).isEqualTo(3);
        assertThat(all).isEmpty();
        assertThat(IteratorOps.removeNegatives(new ArrayList<>())).isZero();
    }

    @Test
    void r2_removeMatchingWorksOnAnyCollection() {
        Set<String> set = new TreeSet<>(List.of("apple", "avocado", "banana"));
        int removed = IteratorOps.removeMatching(set, s -> s.startsWith("a"));
        assertThat(removed).isEqualTo(2);
        assertThat(set).containsExactly("banana");

        List<Integer> nums = new ArrayList<>(List.of(1, 2, 3, 4, 5, 6));
        assertThat(IteratorOps.removeMatching(nums, n -> n % 2 == 0)).isEqualTo(3);
        assertThat(nums).containsExactly(1, 3, 5);
    }

    @Test
    void r3_duplicateEvens() {
        List<Integer> list = new ArrayList<>(List.of(1, 2, 3, 4));
        IteratorOps.duplicateEvens(list);
        assertThat(list).containsExactly(1, 2, 2, 3, 4, 4);
        List<Integer> odds = new LinkedList<>(List.of(1, 3));
        IteratorOps.duplicateEvens(odds);
        assertThat(odds).containsExactly(1, 3);
        List<Integer> zeros = new ArrayList<>(List.of(0));
        IteratorOps.duplicateEvens(zeros);
        assertThat(zeros).containsExactly(0, 0);
    }

    @Test
    @DisplayName("Removing the first element during for-each throws CME")
    void r4_removeFirstThrows() {
        assertThat(IteratorOps.forEachRemovalThrows(List.of("a", "b", "c"), "a")).isTrue();
        assertThat(IteratorOps.forEachRemovalThrows(List.of("a", "b", "c"), "c")).isTrue();
    }

    @Test
    @DisplayName("Removing the second-to-last element silently does NOT throw")
    void r4_secondToLastDoesNotThrow() {
        assertThat(IteratorOps.forEachRemovalThrows(List.of("a", "b", "c"), "b")).isFalse();
        assertThat(IteratorOps.forEachRemovalThrows(List.of("a", "b", "c"), "zzz")).isFalse();
    }

    @Test
    void r4_doesNotMutateTheInput() {
        List<String> input = new ArrayList<>(List.of("a", "b", "c"));
        IteratorOps.forEachRemovalThrows(input, "a");
        assertThat(input).containsExactly("a", "b", "c");
    }
}
'''},
            ["Always call `it.next()` before `it.remove()`.", "`ListIterator.add` inserts before the implicit cursor, so after `next()` it lands right after the element you just read and the cursor skips it automatically."],
            ["Mutation happens through the iterator, never through the collection", "`removeIf` not used where the task demands an explicit iterator", "Explains the silent second-to-last case in a short comment"],
            constraints=["Do not call `Collection.removeIf` or `List.remove(...)` inside loops (except in `forEachRemovalThrows`, which intentionally does)", "Do not edit the tests"],
        ),
        task(
            "comparable-product", "Comparable Product Catalog", "Core", "Product",
            "Create a `Product` value class whose natural order is its SKU, whose `equals`/`hashCode` are consistent with that order, and whose constructor validates its inputs. The tests sort lists, use a `TreeSet`, and check consistency with `equals`.",
            [
                "Constructor `Product(String sku, String name, long priceCents)` rejects a null/blank sku or null/blank name with `IllegalArgumentException` and a negative price with `IllegalArgumentException`",
                "`compareTo` orders by `sku` ascending (use `String.compareTo`), never by subtraction",
                "`equals`/`hashCode` depend on `sku` only, so they are consistent with `compareTo` (same sku -> `compareTo == 0` and `equals == true`)",
                "`sku()`, `name()`, `priceCents()` accessors return the stored values (provided)",
                "`TreeSet<Product>` de-duplicates by SKU, `Collections.sort` orders by SKU, and `Collections.max` returns the highest SKU",
            ],
            ["blank strings (`\"   \"`)", "price 0 allowed, -1 rejected", "same sku with different name/price is equal", "compareTo symmetry"],
            {"Product.java": r'''package @PKG@;

import java.util.Objects;

/** Catalog item. Natural order = SKU; equals/hashCode = SKU (consistent with compareTo). */
public final class Product implements Comparable<Product> {

    private final String sku;
    private final String name;
    private final long priceCents;

    public Product(String sku, String name, long priceCents) {
        //@TODO constructor | validate (blank/null sku or name, negative price -> IllegalArgumentException) then store the fields
        if (sku == null || sku.isBlank()) {
            throw new IllegalArgumentException("sku must not be blank");
        }
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("name must not be blank");
        }
        if (priceCents < 0) {
            throw new IllegalArgumentException("priceCents must be >= 0");
        }
        this.sku = sku;
        this.name = name;
        this.priceCents = priceCents;
        //@END
    }

    public String sku() {
        return sku;
    }

    public String name() {
        return name;
    }

    public long priceCents() {
        return priceCents;
    }

    @Override
    public int compareTo(Product other) {
        //@TODO compareTo | compare by sku using String.compareTo (no subtraction); must be consistent with equals
        return sku.compareTo(other.sku);
        //@END
    }

    @Override
    public boolean equals(Object o) {
        //@TODO equals | equal when the other object is a Product with the same sku
        return o instanceof Product p && sku.equals(p.sku);
        //@END
    }

    @Override
    public int hashCode() {
        //@TODO hashCode | derive from sku only
        return Objects.hash(sku);
        //@END
    }

    @Override
    public String toString() {
        return sku + ":" + name + "@" + priceCents;
    }
}
'''},
            {"ProductTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.TreeSet;
import org.junit.jupiter.api.Test;

class ProductTest {

    @Test
    void r1_constructorStoresValues() {
        Product p = new Product("A-1", "Widget", 250);
        assertThat(p.sku()).isEqualTo("A-1");
        assertThat(p.name()).isEqualTo("Widget");
        assertThat(p.priceCents()).isEqualTo(250);
        assertThat(new Product("Z", "Free", 0).priceCents()).isZero();
    }

    @Test
    void r1_constructorValidation() {
        assertThatThrownBy(() -> new Product(null, "n", 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new Product("   ", "n", 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new Product("s", null, 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new Product("s", " ", 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new Product("s", "n", -1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r2_compareToOrdersBySku() {
        Product a = new Product("A-1", "x", 1);
        Product b = new Product("B-1", "y", 1);
        assertThat(a.compareTo(b)).isNegative();
        assertThat(b.compareTo(a)).isPositive();
        assertThat(a.compareTo(new Product("A-1", "other", 99))).isZero();
    }

    @Test
    void r3_equalsAndHashCodeUseSkuOnly() {
        Product a = new Product("A-1", "x", 1);
        Product same = new Product("A-1", "different", 500);
        assertThat(a).isEqualTo(same).hasSameHashCodeAs(same);
        assertThat(a).isNotEqualTo(new Product("A-2", "x", 1));
        assertThat(a).isNotEqualTo("A-1");
        assertThat(a.equals(null)).isFalse();
    }

    @Test
    void r3_consistentWithEqualsForAllPairs() {
        List<Product> ps = List.of(new Product("a", "1", 1), new Product("b", "2", 2), new Product("a", "3", 3));
        for (Product x : ps) {
            for (Product y : ps) {
                assertThat(x.compareTo(y) == 0).isEqualTo(x.equals(y));
                assertThat(Integer.signum(x.compareTo(y))).isEqualTo(-Integer.signum(y.compareTo(x)));
            }
        }
    }

    @Test
    void r5_sortingAndTreeSet() {
        List<Product> list = new ArrayList<>(List.of(
                new Product("C", "c", 3), new Product("A", "a", 1), new Product("B", "b", 2)));
        Collections.sort(list);
        assertThat(list).extracting(Product::sku).containsExactly("A", "B", "C");
        assertThat(Collections.max(list).sku()).isEqualTo("C");

        TreeSet<Product> set = new TreeSet<>(list);
        set.add(new Product("A", "duplicate sku", 100));
        assertThat(set).hasSize(3);
        assertThat(set.first().name()).isEqualTo("a");
    }
}
'''},
            ["`compareTo` on strings already returns a signed int; do not negate or subtract.", "Remember `Objects.hash(sku)` or `sku.hashCode()` - both fine."],
            ["`compareTo`, `equals`, `hashCode` use the same field(s)", "Immutability: all fields final, no setters", "Validation in one place (constructor)"],
        ),
        task(
            "comparator-chain", "Employee Comparator Chain", "Challenge", "EmployeeSorts",
            "Compose multi-key comparators with `Comparator.comparing(...).thenComparing(...)`, build a null-safe case-insensitive string comparator, fold a list of comparators into one, and produce a sorted **copy** without touching the original list. Challenge: do it without writing any hand-rolled `compare` bodies using subtraction.",
            [
                "`byDeptThenSalaryDescThenName()` orders by department ascending, then salary **descending**, then name ascending",
                "`byNameIgnoreCaseNullsLast()` compares strings case-insensitively, with `null` sorted last",
                "`chain(List<Comparator<T>>)` returns a comparator applying the given comparators in order; an empty list treats all elements as equal",
                "`sortedCopy(list, comparator)` returns a new sorted list (stable) and leaves the input unchanged",
            ],
            ["equal salaries fall through to name", "nulls in the string comparator", "empty comparator list", "stability for elements the comparator considers equal"],
            {"Employee.java": r'''package @PKG@;

/** Provided value type - no changes needed. */
public record Employee(String name, String dept, int age, double salary) {
}
''',
             "EmployeeSorts.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/** Comparator factories. */
public final class EmployeeSorts {

    private EmployeeSorts() {
    }

    public static Comparator<Employee> byDeptThenSalaryDescThenName() {
        //@TODO byDeptThenSalaryDescThenName | dept ascending, then salary descending, then name ascending, built with Comparator.comparing/thenComparing (no subtraction)
        return Comparator.comparing(Employee::dept)
                .thenComparing(Employee::salary, Comparator.reverseOrder())
                .thenComparing(Employee::name);
        //@END
    }

    public static Comparator<String> byNameIgnoreCaseNullsLast() {
        //@TODO byNameIgnoreCaseNullsLast | case-insensitive String comparator that sorts null last
        return Comparator.nullsLast(String.CASE_INSENSITIVE_ORDER);
        //@END
    }

    public static <T> Comparator<T> chain(List<Comparator<T>> comparators) {
        //@TODO chain | combine comparators so that later ones only break ties of earlier ones; empty list -> everything equal
        Comparator<T> result = (a, b) -> 0;
        for (Comparator<T> c : comparators) {
            result = result.thenComparing(c);
        }
        return result;
        //@END
    }

    public static <T> List<T> sortedCopy(List<T> input, Comparator<? super T> comparator) {
        //@TODO sortedCopy | return a new ArrayList sorted with comparator (stable); do not modify input
        List<T> copy = new ArrayList<>(input);
        copy.sort(comparator);
        return copy;
        //@END
    }
}
'''},
            {"EmployeeSortsTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import org.junit.jupiter.api.Test;

class EmployeeSortsTest {

    private static final Employee ZED = new Employee("Zed", "ENG", 30, 100);
    private static final Employee AMY = new Employee("Amy", "ENG", 41, 120);
    private static final Employee BOB = new Employee("Bob", "HR", 25, 90);
    private static final Employee ANN = new Employee("Ann", "ENG", 29, 100);
    private static final Employee CAL = new Employee("Cal", "AUD", 50, 70);

    @Test
    void r1_deptThenSalaryDescThenName() {
        List<Employee> list = new ArrayList<>(List.of(BOB, ZED, AMY, ANN, CAL));
        list.sort(EmployeeSorts.byDeptThenSalaryDescThenName());
        assertThat(list).containsExactly(CAL, AMY, ANN, ZED, BOB);
    }

    @Test
    void r1_comparatorIsSymmetric() {
        Comparator<Employee> c = EmployeeSorts.byDeptThenSalaryDescThenName();
        assertThat(c.compare(AMY, ZED)).isNegative();
        assertThat(c.compare(ZED, AMY)).isPositive();
        assertThat(c.compare(ZED, new Employee("Zed", "ENG", 99, 100))).isZero();
    }

    @Test
    void r2_nameIgnoreCaseNullsLast() {
        List<String> names = new ArrayList<>(Arrays.asList("bob", null, "Alice", "CAROL", "alice"));
        names.sort(EmployeeSorts.byNameIgnoreCaseNullsLast());
        assertThat(names.subList(0, 4)).extracting(String::toLowerCase).containsExactly("alice", "alice", "bob", "carol");
        assertThat(names.get(4)).isNull();
    }

    @Test
    void r3_chainAppliesComparatorsInOrder() {
        Comparator<Employee> byAge = Comparator.comparingInt(Employee::age);
        Comparator<Employee> byDept = Comparator.comparing(Employee::dept);
        Comparator<Employee> chained = EmployeeSorts.chain(List.of(byDept, byAge));
        List<Employee> list = new ArrayList<>(List.of(BOB, AMY, ZED, CAL));
        list.sort(chained);
        assertThat(list).containsExactly(CAL, ZED, AMY, BOB);
    }

    @Test
    void r3_emptyChainTreatsEverythingEqual() {
        Comparator<String> none = EmployeeSorts.chain(List.of());
        assertThat(none.compare("a", "b")).isZero();
        List<String> list = new ArrayList<>(List.of("b", "a", "c"));
        list.sort(none);
        assertThat(list).containsExactly("b", "a", "c");
    }

    @Test
    void r4_sortedCopyLeavesInputUntouched() {
        List<Employee> input = new ArrayList<>(List.of(BOB, AMY, CAL));
        List<Employee> sorted = EmployeeSorts.sortedCopy(input, EmployeeSorts.byDeptThenSalaryDescThenName());
        assertThat(sorted).containsExactly(CAL, AMY, BOB);
        assertThat(input).containsExactly(BOB, AMY, CAL);
        assertThat(sorted).isNotSameAs(input);
    }

    @Test
    void r4_sortIsStable() {
        Employee first = new Employee("Same", "X", 1, 1);
        Employee second = new Employee("Same", "X", 2, 1);
        Employee third = new Employee("Same", "X", 3, 1);
        List<Employee> sorted = EmployeeSorts.sortedCopy(List.of(first, second, third), EmployeeSorts.byDeptThenSalaryDescThenName());
        assertThat(sorted).containsExactly(first, second, third);
    }
}
'''},
            ["`Comparator.comparing(f).thenComparing(g, Comparator.reverseOrder())` handles descending keys.", "`chain` can start from `(a, b) -> 0` and apply `thenComparing` repeatedly."],
            ["No subtraction-based compare logic", "Comparators composed from key extractors", "`sortedCopy` never mutates its argument"],
            constraints=["Do not write comparator lambdas that subtract numbers", "Do not edit the tests"],
        ),
    ],
)
