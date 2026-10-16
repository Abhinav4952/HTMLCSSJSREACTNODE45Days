from gen_helpers import sec, task

DAY = dict(
    num=17,
    title="Streams I: Pipelines, filter/map/reduce, and Collectors",
    theme="Process data declaratively with the Stream API: sources, lazy intermediate operations, terminal operations, reduction, and collectors.",
    objectives=[
        "Describe a stream pipeline as source -> intermediate operations -> terminal operation and explain laziness and short-circuiting",
        "Use `filter`, `map`, `distinct`, `sorted`, `limit`, `skip`, `peek`, `findFirst`, `anyMatch` correctly",
        "Reduce streams with `reduce`, primitive streams (`IntStream`) and summary statistics",
        "Collect results with `Collectors.toList/toSet/toMap/joining/counting/collectingAndThen`",
        "Avoid stream anti-patterns: reuse, side effects in lambdas, `toMap` duplicate keys, `get()` on empty results",
        "Decide when a plain loop is clearer than a stream",
    ],
    prereqs=["Day 16 — lambdas, functional interfaces, method references, Optional", "Day 14–15 — collections, comparators, maps"],
    overview="""A **stream** is a lazily evaluated *pipeline* over a data source (a collection, array, file lines, generator). You describe **what** to compute - filter these, transform those, group the rest - and the library decides how to iterate. Streams do not store data and never modify their source.

Streams are everywhere in modern Java backends: mapping entities to DTOs, filtering orders, summarizing reports, aggregating metrics. Interviews ask: *intermediate vs terminal operations*, *why are streams lazy*, *map vs flatMap*, *reduce signature*, *Collectors.toMap pitfalls*, *can you reuse a stream* (no: `IllegalStateException: stream has already been operated upon or closed`). Today covers the core pipeline and collectors; Day 18 adds grouping, partitioning, flatMap, primitive specializations and parallel streams.""",
    sections=[
        sec(
            "The stream pipeline: sources, intermediate and terminal operations, laziness",
            "A pipeline has three parts: a **source** (`list.stream()`, `Stream.of(...)`, `Arrays.stream(arr)`, `IntStream.range`, `Files.lines`, `Stream.iterate/generate`), zero or more **intermediate operations** that return a new stream (`filter`, `map`, `distinct`, `sorted`, `limit`, `skip`, `peek`), and exactly one **terminal operation** (`collect`, `forEach`, `reduce`, `count`, `findFirst`, `anyMatch`, `toList`, `min`/`max`). Intermediate operations are **lazy** - nothing runs until the terminal operation starts. Elements flow through the whole pipeline **one at a time** (vertical processing), not stage by stage, which enables **short-circuiting** (`limit`, `findFirst`, `anyMatch`).",
            "Laziness lets the library fuse stages into one pass, avoid intermediate collections, and stop early on infinite or huge sources (`Stream.iterate(1, x -> x * 2).limit(10)`). The declarative style reduces loop/index bookkeeping and makes transformations composable and testable. It also sets the rules you must respect: lambdas should be **non-interfering** and (preferably) **stateless**.",
            ["Readable, composable data transformations", "Single pass with short-circuiting and no intermediate collections", "Works uniformly for collections, arrays, files, generators", "Easy to switch to a parallel pipeline later (with care - Day 18)"],
            ["A stream can be consumed only once", "Debugging is harder (stack traces through the library, lazy evaluation)", "Not always clearer or faster than a simple loop; checked exceptions do not fit lambdas"],
            "Forgetting the terminal operation means **nothing happens** (`list.stream().peek(System.out::println);` prints nothing). Reusing a stream throws `IllegalStateException`. Modifying the source collection while the pipeline runs gives `ConcurrentModificationException` or undefined behavior (interference). Side effects in `map`/`filter` (incrementing a shared counter, adding to an outside list) work sequentially but break or race in parallel and make code hard to reason about. `Stream.iterate(...)` without `limit` loops forever / runs out of memory.",
            """- Create: `collection.stream()`, `Stream.of(a, b)`, `Arrays.stream(arr)`, `IntStream.rangeClosed(1, n)`, `Stream.iterate(seed, hasNext, next)`, `Stream.generate(supplier)`.
- Intermediate (lazy): `filter(Predicate)`, `map(Function)`, `mapToInt`, `distinct()`, `sorted()`, `sorted(Comparator)`, `limit(n)`, `skip(n)`, `peek(Consumer)` (debugging only).
- Terminal (eager): `forEach`, `collect`, `toList()` (Java 16, unmodifiable), `reduce`, `count`, `min/max(Comparator)`, `findFirst/findAny`, `anyMatch/allMatch/noneMatch`, `toArray`.
- `sorted()` and `distinct()` are **stateful** (buffer elements); `limit` short-circuits.
- A stream **cannot be reused**; store the `Supplier<Stream<T>>` if you need to create it repeatedly.
- Order: for ordered sources (`List`), encounter order is preserved unless you call `unordered()`.""",
            [
                ("Tiny — a first pipeline", """List<String> names = List.of("ann", "bob", "cy", "dave");
List<String> result = names.stream()
        .filter(n -> n.length() > 2)
        .map(String::toUpperCase)
        .sorted(Comparator.reverseOrder())
        .toList();
System.out.println(result);   // [DAVE, BOB, ANN]"""),
                ("Tiny — laziness and vertical processing", """List<String> log = new ArrayList<>();
Optional<String> first = Stream.of("a", "bb", "cc")
        .filter(s -> { log.add("filter:" + s); return s.length() > 1; })
        .map(s -> { log.add("map:" + s); return s.toUpperCase(); })
        .findFirst();
System.out.println(first.get());  // BB
System.out.println(log);          // [filter:a, filter:bb, map:bb]   <- "cc" was never touched"""),
                ("Medium — pagination and the one-shot stream rule", """import java.util.*;
import java.util.stream.*;

public class PageDemo {
    static <T> List<T> page(List<T> items, int pageIndex, int size) {
        if (pageIndex < 0 || size <= 0) throw new IllegalArgumentException("bad page");
        return items.stream().skip((long) pageIndex * size).limit(size).toList();
    }

    public static void main(String[] args) {
        List<Integer> nums = IntStream.rangeClosed(1, 10).boxed().toList();
        System.out.println(page(nums, 1, 4));    // [5, 6, 7, 8]
        System.out.println(page(nums, 5, 4));    // []

        Stream<Integer> s = nums.stream();
        s.count();
        try { s.count(); }
        catch (IllegalStateException e) { System.out.println("stream reused!"); }  // stream reused!
    }
}"""),
            ],
            [
                ("What prints: `Stream.of(1,2,3).peek(System.out::println);`?", "Nothing - there is no terminal operation, so the pipeline never executes."),
                ("Why does `findFirst` after `filter` not examine every element?", "Streams are lazy and process element-by-element; `findFirst` short-circuits as soon as one element passes."),
                ("Name two stateful intermediate operations.", "`sorted` and `distinct` (they must buffer elements)."),
                ("How do you obtain a stream you can \"reuse\"?", "You cannot reuse one; create a new stream from the source each time, e.g. via a `Supplier<Stream<T>>`."),
            ],
        ),
        sec(
            "Mapping, filtering, and reduction (including primitive streams)",
            "`map(Function)` transforms each element one-to-one; `filter(Predicate)` keeps the matching ones. **Reduction** folds a stream into a single result: `reduce(identity, accumulator)`, `reduce(accumulator)` returning `Optional`, and the three-argument form for different result types. The accumulator must be **associative** and the identity a true identity (`0` for +, `1` for *) so that results are correct under parallel evaluation. For numbers prefer **primitive streams** (`IntStream`, `LongStream`, `DoubleStream`) via `mapToInt` etc.: they avoid boxing and offer `sum()`, `average()`, `max()`, `summaryStatistics()`.",
            "Most reports are reductions: totals, counts, min/max, averages. Using `mapToInt(...).sum()` is both clearer and faster than boxing into `Stream<Integer>` and reducing. Understanding identity/associativity is the key to correct `reduce` use and to later parallelism.",
            ["`mapToInt().sum()/average()/summaryStatistics()` are concise and unboxed", "`reduce` expresses any fold generically", "`Optional` results force handling of empty input", "Same code works sequentially or in parallel if the reduction is associative"],
            ["`reduce` with a non-associative or non-identity function gives wrong results in parallel", "Boxing overhead for `Stream<Integer>`", "`reduce` to build collections is wrong (mutable reduction needs `collect`)"],
            "`stream.reduce(0, (a, b) -> a - b)` is not associative, so parallel results differ from sequential ones. `reduce(1, Integer::sum)` (wrong identity) adds an extra 1 once per parallel segment. Calling `max(...)` or `reduce(op)` on an empty stream returns an empty `Optional` - calling `.get()` throws `NoSuchElementException`. `average()` of an empty `IntStream` is `OptionalDouble.empty()`, not 0. `IntStream.sum()` overflows silently on `int` (use `mapToLong`). Using `reduce(new ArrayList<>(), ...)` to build lists mutates a shared identity: use `collect`.",
            """- `T reduce(T identity, BinaryOperator<T> acc)`; `Optional<T> reduce(BinaryOperator<T> acc)`; `<U> U reduce(U identity, BiFunction<U,? super T,U> acc, BinaryOperator<U> combiner)`.
- Convenience: `count()`, `min(Comparator)`, `max(Comparator)`, `IntStream.sum/min/max/average`.
- `mapToInt(Integer::intValue)`, `mapToObj`, `boxed()`, `asLongStream()` convert between stream kinds.
- `IntSummaryStatistics s = ints.summaryStatistics();` gives count, sum, min, max, average in one pass.
- Identity laws: `identity op x == x`; associativity: `(a op b) op c == a op (b op c)`.""",
            [
                ("Tiny — three reductions", """List<Integer> xs = List.of(3, 1, 4, 1, 5);
int sum = xs.stream().reduce(0, Integer::sum);                 // 14
Optional<Integer> max = xs.stream().reduce(Integer::max);       // Optional[5]
long product = xs.stream().mapToLong(Integer::longValue).reduce(1L, (a, b) -> a * b); // 60
System.out.println(sum + " " + max.get() + " " + product);"""),
                ("Tiny — primitive streams and statistics", """IntSummaryStatistics st = List.of(3, 1, 4, 1, 5).stream().mapToInt(Integer::intValue).summaryStatistics();
System.out.println(st.getMin() + " " + st.getMax() + " " + st.getAverage() + " " + st.getCount());
// 1 5 2.8 5
System.out.println(IntStream.empty().average());   // OptionalDouble.empty"""),
                ("Medium — longest word keeps the first on ties, and a wrong reduce", """List<String> words = List.of("kiwi", "pear", "banana", "melon", "cherry");
Optional<String> longest = words.stream().reduce((a, b) -> b.length() > a.length() ? b : a);
System.out.println(longest.orElse("-"));           // banana (first of the two 6-letter words)

// BUG: subtraction is not associative; parallel() would give a different answer
int bad = Stream.of(10, 3, 2).parallel().reduce(0, (a, b) -> a - b);
// sequential: ((0-10)-3)-2 = -15, parallel may produce a different value"""),
            ],
            [
                ("Why must the `reduce` identity be a true identity?", "Parallel evaluation may apply the identity once per segment; a wrong identity (e.g. 1 for sum) is counted several times."),
                ("What does `IntStream.empty().average()` return?", "`OptionalDouble.empty()` - not `0`."),
                ("Why prefer `mapToInt(...).sum()` over `map(...).reduce(0, Integer::sum)`?", "It avoids boxing and expresses intent; it also cannot be mis-specified with a wrong identity."),
                ("Is `reduce(\"\", String::concat)` a good way to join strings?", "It works but is O(n^2) in copying; prefer `Collectors.joining`."),
            ],
        ),
        sec(
            "Collectors: toList, toSet, toMap, joining, counting",
            "`stream.collect(Collector)` is a **mutable reduction**: it accumulates elements into a container (a list, map, string builder). `java.util.stream.Collectors` provides ready-made collectors: `toList()`, `toSet()`, `toCollection(TreeSet::new)`, `toMap(keyFn, valueFn[, mergeFn[, mapSupplier]])`, `joining(delimiter, prefix, suffix)`, `counting()`, `summingInt`, `averagingDouble`, `mapping`, `collectingAndThen(downstream, finisher)`, and the unmodifiable variants `toUnmodifiableList/Set/Map` (Java 10). `Stream.toList()` (Java 16) is a shortcut returning an unmodifiable list that **permits nulls**.",
            "Collectors turn pipelines into the shapes services need: DTO lists, lookup maps, CSV strings, counts per key (Day 18 adds `groupingBy`). Choosing the correct collector (and map supplier) controls ordering, duplicate handling, and mutability of results.",
            ["Concise, well-tested building blocks", "Control over result type (`TreeMap::new`, `LinkedHashMap::new`)", "Composable via downstream collectors and `collectingAndThen`", "`joining` builds strings efficiently with a `StringBuilder`"],
            ["`toMap` throws on duplicate keys unless a merge function is supplied", "`toMap` rejects null values (`NullPointerException`)", "`Collectors.toList()` makes **no guarantee** about the returned list's mutability or type"],
            "`Stream.of(\"a\",\"b\",\"a\").collect(Collectors.toMap(s -> s, String::length))` throws `IllegalStateException: Duplicate key a (attempted merging values 1 and 1)`. A null value in `toMap` throws `NullPointerException` from `HashMap.merge`. Relying on `Collectors.toList()` returning a mutable `ArrayList` is an unwritten assumption; use `toCollection(ArrayList::new)` if you need that. `Stream.toList()` returns an unmodifiable list: `add` throws `UnsupportedOperationException`. `joining` on a `Stream<Integer>` does not compile - map to `String` first.",
            """- `collect(Collectors.toList())`, `toSet()`, `toCollection(LinkedHashSet::new)`.
- `toMap(k, v)`; with duplicates `toMap(k, v, (a, b) -> a)`; choose map type `toMap(k, v, merge, LinkedHashMap::new)`.
- `joining()`, `joining(\", \")`, `joining(\", \", \"[\", \"]\")` (elements must be `CharSequence`).
- `counting()` returns `Long`; `summingInt(ToIntFunction)`; `averagingInt`; `mapping(f, downstream)`.
- `collectingAndThen(Collectors.toList(), Collections::unmodifiableList)` post-processes the result.
- `Stream.toList()` unmodifiable, nulls allowed; `Collectors.toUnmodifiableList()` rejects nulls.""",
            [
                ("Tiny — joining and toSet", """List<String> words = List.of("b", "a", "b");
System.out.println(words.stream().collect(Collectors.joining(", ", "[", "]")));   // [b, a, b]
System.out.println(words.stream().collect(Collectors.toCollection(TreeSet::new))); // [a, b]"""),
                ("Tiny — toMap with merge function and map supplier", """Map<String, Integer> m = Stream.of("kiwi", "fig", "kiwi")
        .collect(Collectors.toMap(w -> w, String::length, (first, second) -> first, LinkedHashMap::new));
System.out.println(m);   // {kiwi=4, fig=3}"""),
                ("Medium — word count with collectors", """import java.util.*;
import java.util.function.Function;
import java.util.stream.*;

public class WordCountDemo {
    static Map<String, Long> count(String text) {
        return Arrays.stream(text.toLowerCase().split("[^\\p{L}]+"))
                .filter(w -> !w.isEmpty())
                .collect(Collectors.groupingBy(Function.identity(), TreeMap::new, Collectors.counting()));
    }

    public static void main(String[] args) {
        System.out.println(count("The cat and the hat. The END!"));
        // {and=1, cat=1, end=1, hat=1, the=3}
    }
}"""),
            ],
            [
                ("What happens when `Collectors.toMap` sees a duplicate key and no merge function?", "`IllegalStateException: Duplicate key ...`."),
                ("Difference between `Stream.toList()` and `Collectors.toList()`?", "`Stream.toList()` returns an unmodifiable list and allows nulls; `Collectors.toList()` returns an unspecified (in practice mutable `ArrayList`) list."),
                ("How do you get a `LinkedHashMap` out of `toMap`?", "Use the four-argument overload and pass `LinkedHashMap::new` as the map supplier."),
                ("Why does `Stream<Integer>.collect(Collectors.joining(\",\"))` not compile?", "`joining` requires `CharSequence` elements; map them with `String::valueOf` first."),
            ],
        ),
    ],
    interview=[
        ("Intermediate vs terminal operations?", "Intermediate operations return a stream and are lazy; a terminal operation triggers execution and produces a result or side effect. A stream is consumed by exactly one terminal operation."),
        ("map vs flatMap?", "`map` is one-to-one; `flatMap` maps each element to a stream and flattens (one-to-many). See Day 18."),
        ("What is short-circuiting?", "Operations such as `limit`, `findFirst`, `anyMatch` can finish before consuming the whole source, which also makes infinite streams usable."),
        ("Is it safe to modify a list inside `forEach` over its own stream?", "No - interference; it can throw `ConcurrentModificationException` or yield undefined results."),
        ("When would you not use a stream?", "Complex control flow with early exits and checked exceptions, tight inner loops with primitive math where clarity or performance suffers, or when debugging needs step-through of mutable state."),
        ("What are the pitfalls of `Collectors.toMap`?", "Duplicate keys throw `IllegalStateException`; null values throw `NullPointerException`; the map implementation is unspecified unless you pass a supplier."),
    ],
    mistakes=[
        "No terminal operation - the pipeline silently does nothing.",
        "Reusing a stream (`IllegalStateException: stream has already been operated upon or closed`).",
        "Using `forEach` with an external mutable list/counter instead of `collect`/`reduce`.",
        "Calling `Optional.get()` on `findFirst()`/`max()` of possibly empty streams.",
        "`toMap` without a merge function on data that may contain duplicates.",
        "Wrong `reduce` identity or non-associative accumulator.",
    ],
    reading=[
        "Javadoc: `java.util.stream` package summary (see *Non-interference*, *Stateless behaviors*, *Reduction*, *Associativity*)",
        "Oracle Java Tutorials - *Aggregate Operations* (Lesson)",
        "Javadoc: `java.util.stream.Collectors`, `Stream`, `IntStream`",
        "*Effective Java* (Bloch) items 42-48 (lambdas and streams)",
    ],
    glossary=[
        ("Pipeline", "Source + intermediate operations + terminal operation"),
        ("Lazy", "Intermediate operations do no work until a terminal operation runs"),
        ("Short-circuit", "Terminal/intermediate operation that may stop before consuming all input"),
        ("Stateful operation", "Needs to see multiple elements (`sorted`, `distinct`)"),
        ("Mutable reduction", "Accumulating into a container via `collect`"),
        ("Associative", "`(a op b) op c == a op (b op c)`; required for correct reductions"),
        ("Interference", "Modifying the stream source during execution"),
        ("Collector", "Strategy describing supplier, accumulator, combiner, finisher"),
    ],
    tasks=[
        task(
            "stream-filter-map", "Filter, Map, Sort, and Page", "Warm-up", "StreamFilterMap",
            "Practice the core intermediate operations: filter, map, distinct, sorted, skip/limit, and findFirst - plus one *predict the output* method that reveals how streams process elements lazily, one at a time.",
            [
                "`upperLongNames(names, minLen)` trims names, drops `null`s and names shorter than `minLen`, and returns them upper-cased in input order",
                "`squaresOfOdds(numbers)` returns the squares of the odd numbers (including negative odd numbers)",
                "`distinctSortedLower(words)` returns trimmed, lower-cased, non-blank, de-duplicated words sorted alphabetically; `null` entries are ignored",
                "`page(items, pageIndex, size)` returns the zero-based page using `skip`/`limit`; `pageIndex < 0` or `size <= 0` throws `IllegalArgumentException`; pages past the end are empty",
                "`firstStartingWith(names, prefix)` returns the first name starting with the prefix as an `Optional`",
                "`traceLaziness()` runs `filter(len > 1)` then `map(upper)` then `findFirst` over `\"a\", \"bb\", \"cc\"`, recording `filter:<x>` and `map:<x>` events, and returns the trace",
            ],
            ["empty list", "null elements", "page index past the end", "size 0", "negative odd numbers (`-3 % 2 == -1`)"],
            {"StreamFilterMap.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Stream;

/** Core intermediate operations. */
public final class StreamFilterMap {

    private StreamFilterMap() {
    }

    public static List<String> upperLongNames(List<String> names, int minLen) {
        //@TODO upperLongNames | stream: drop nulls, trim, keep length >= minLen, upper-case, toList (input order)
        return names.stream()
                .filter(Objects::nonNull)
                .map(String::trim)
                .filter(s -> s.length() >= minLen)
                .map(String::toUpperCase)
                .toList();
        //@END
    }

    public static List<Integer> squaresOfOdds(List<Integer> numbers) {
        //@TODO squaresOfOdds | keep odd numbers (negative ones too) and map each to its square
        return numbers.stream()
                .filter(n -> n % 2 != 0)
                .map(n -> n * n)
                .toList();
        //@END
    }

    public static List<String> distinctSortedLower(List<String> words) {
        //@TODO distinctSortedLower | drop nulls, trim, lower-case, drop blank, distinct, sorted alphabetically
        return words.stream()
                .filter(Objects::nonNull)
                .map(w -> w.trim().toLowerCase())
                .filter(w -> !w.isEmpty())
                .distinct()
                .sorted()
                .toList();
        //@END
    }

    public static <T> List<T> page(List<T> items, int pageIndex, int size) {
        //@TODO page | validate (pageIndex >= 0, size > 0 else IllegalArgumentException), then skip(pageIndex * size) and limit(size); use long arithmetic
        if (pageIndex < 0 || size <= 0) {
            throw new IllegalArgumentException("pageIndex must be >= 0 and size > 0");
        }
        return items.stream()
                .skip((long) pageIndex * size)
                .limit(size)
                .toList();
        //@END
    }

    public static Optional<String> firstStartingWith(List<String> names, String prefix) {
        //@TODO firstStartingWith | findFirst among non-null names that start with prefix
        return names.stream()
                .filter(n -> n != null && n.startsWith(prefix))
                .findFirst();
        //@END
    }

    public static List<String> traceLaziness() {
        //@TODO traceLaziness | pipeline over "a","bb","cc": filter(length>1) logging "filter:<s>", map(upper) logging "map:<s>", then findFirst(); return the log (it shows per-element, short-circuited processing)
        List<String> log = new ArrayList<>();
        Stream.of("a", "bb", "cc")
                .filter(s -> {
                    log.add("filter:" + s);
                    return s.length() > 1;
                })
                .map(s -> {
                    log.add("map:" + s);
                    return s.toUpperCase();
                })
                .findFirst();
        return log;
        //@END
    }
}
'''},
            {"StreamFilterMapTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.Arrays;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class StreamFilterMapTest {

    @Test
    void r1_upperLongNames() {
        List<String> in = Arrays.asList(" ann ", null, "bo", "carl", "  ");
        assertThat(StreamFilterMap.upperLongNames(in, 3)).containsExactly("ANN", "CARL");
        assertThat(StreamFilterMap.upperLongNames(List.of(), 1)).isEmpty();
        assertThat(StreamFilterMap.upperLongNames(List.of("x"), 0)).containsExactly("X");
    }

    @Test
    void r2_squaresOfOdds() {
        assertThat(StreamFilterMap.squaresOfOdds(List.of(1, 2, 3, 4, 5))).containsExactly(1, 9, 25);
        assertThat(StreamFilterMap.squaresOfOdds(List.of(-3, -2, 0))).containsExactly(9);
        assertThat(StreamFilterMap.squaresOfOdds(List.of(2, 4))).isEmpty();
    }

    @Test
    void r3_distinctSortedLower() {
        List<String> in = Arrays.asList("Pear", " apple", "PEAR ", null, "  ", "Apple", "fig");
        assertThat(StreamFilterMap.distinctSortedLower(in)).containsExactly("apple", "fig", "pear");
        assertThat(StreamFilterMap.distinctSortedLower(List.of())).isEmpty();
    }

    @Test
    void r4_page() {
        List<Integer> nums = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        assertThat(StreamFilterMap.page(nums, 0, 4)).containsExactly(1, 2, 3, 4);
        assertThat(StreamFilterMap.page(nums, 1, 4)).containsExactly(5, 6, 7, 8);
        assertThat(StreamFilterMap.page(nums, 2, 4)).containsExactly(9, 10);
        assertThat(StreamFilterMap.page(nums, 3, 4)).isEmpty();
    }

    @Test
    void r4_pageValidatesArguments() {
        assertThatThrownBy(() -> StreamFilterMap.page(List.of(1), -1, 2)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> StreamFilterMap.page(List.of(1), 0, 0)).isInstanceOf(IllegalArgumentException.class);
        assertThat(StreamFilterMap.page(List.of(1, 2), Integer.MAX_VALUE, Integer.MAX_VALUE)).isEmpty();
    }

    @Test
    void r5_firstStartingWith() {
        List<String> names = Arrays.asList(null, "Bob", "Barbara", "Alice");
        assertThat(StreamFilterMap.firstStartingWith(names, "Ba")).contains("Barbara");
        assertThat(StreamFilterMap.firstStartingWith(names, "B")).contains("Bob");
        assertThat(StreamFilterMap.firstStartingWith(names, "Z")).isEmpty();
    }

    @Test
    @DisplayName("Laziness: each element flows through the whole pipeline; findFirst short-circuits")
    void r6_traceLaziness() {
        assertThat(StreamFilterMap.traceLaziness()).containsExactly("filter:a", "filter:bb", "map:bb");
    }
}
'''},
            ["`Stream.skip` takes a `long`: cast before multiplying to avoid `int` overflow.", "In `traceLaziness`, remember the log is mutated from inside lambdas (acceptable for a demo; never in production pipelines)."],
            ["Single pipeline per method, no temporary collections", "No explicit `for`/`while` loops", "`Optional` returned, never `get()`"],
            constraints=["Use the Stream API - no explicit `for`/`while` loops (except none are needed)", "Do not edit the tests"],
        ),
        task(
            "reduce-sum", "Reduce, Sum, and Statistics", "Core", "ReduceSum",
            "Implement reductions over number and string lists with `reduce` and primitive streams: sum, product, max, average, longest string (first wins ties), and summary statistics.",
            [
                "`sum(numbers)` adds all values with `reduce(0, Integer::sum)`; empty list -> 0",
                "`product(numbers)` returns the product as a `long` (empty list -> 1)",
                "`max(numbers)` returns an `Optional<Integer>`; empty -> empty",
                "`average(numbers)` returns an `OptionalDouble` using a primitive stream; empty -> empty",
                "`longest(words)` returns the longest word as `Optional`; when several have the same maximum length the **first** wins; `null` words are ignored",
                "`stats(numbers)` returns an `IntSummaryStatistics` (count, sum, min, max)",
                "`sumLong(numbers)` sums as `long` so large inputs do not overflow `int`",
            ],
            ["empty list", "negative numbers", "ties for longest", "overflow (`Integer.MAX_VALUE` twice)"],
            {"ReduceSum.java": r'''package @PKG@;

import java.util.IntSummaryStatistics;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.OptionalDouble;

/** Reductions. */
public final class ReduceSum {

    private ReduceSum() {
    }

    public static int sum(List<Integer> numbers) {
        //@TODO sum | reduce with identity 0 and Integer::sum
        return numbers.stream().reduce(0, Integer::sum);
        //@END
    }

    public static long product(List<Integer> numbers) {
        //@TODO product | multiply as long; identity 1 so an empty list gives 1
        return numbers.stream().mapToLong(Integer::longValue).reduce(1L, (a, b) -> a * b);
        //@END
    }

    public static Optional<Integer> max(List<Integer> numbers) {
        //@TODO max | reduce(Integer::max) without identity so empty input gives Optional.empty()
        return numbers.stream().reduce(Integer::max);
        //@END
    }

    public static OptionalDouble average(List<Integer> numbers) {
        //@TODO average | mapToInt then average(); empty gives OptionalDouble.empty()
        return numbers.stream().mapToInt(Integer::intValue).average();
        //@END
    }

    public static Optional<String> longest(List<String> words) {
        //@TODO longest | ignore nulls; reduce keeping the first word on length ties
        return words.stream()
                .filter(Objects::nonNull)
                .reduce((a, b) -> b.length() > a.length() ? b : a);
        //@END
    }

    public static IntSummaryStatistics stats(List<Integer> numbers) {
        //@TODO stats | mapToInt(Integer::intValue).summaryStatistics()
        return numbers.stream().mapToInt(Integer::intValue).summaryStatistics();
        //@END
    }

    public static long sumLong(List<Integer> numbers) {
        //@TODO sumLong | mapToLong then sum() so that large inputs do not overflow int
        return numbers.stream().mapToLong(Integer::longValue).sum();
        //@END
    }
}
'''},
            {"ReduceSumTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Arrays;
import java.util.IntSummaryStatistics;
import java.util.List;
import org.junit.jupiter.api.Test;

class ReduceSumTest {

    @Test
    void r1_sum() {
        assertThat(ReduceSum.sum(List.of(3, 1, 4, 1, 5))).isEqualTo(14);
        assertThat(ReduceSum.sum(List.of(-5, 5))).isZero();
        assertThat(ReduceSum.sum(List.of())).isZero();
    }

    @Test
    void r2_product() {
        assertThat(ReduceSum.product(List.of(3, 1, 4, 1, 5))).isEqualTo(60L);
        assertThat(ReduceSum.product(List.of())).isEqualTo(1L);
        assertThat(ReduceSum.product(List.of(100_000, 100_000))).isEqualTo(10_000_000_000L);
        assertThat(ReduceSum.product(List.of(7, 0, 9))).isZero();
    }

    @Test
    void r3_max() {
        assertThat(ReduceSum.max(List.of(3, 9, -1))).contains(9);
        assertThat(ReduceSum.max(List.of(-8, -3))).contains(-3);
        assertThat(ReduceSum.max(List.of())).isEmpty();
    }

    @Test
    void r4_average() {
        assertThat(ReduceSum.average(List.of(1, 2, 3, 4)).getAsDouble()).isEqualTo(2.5);
        assertThat(ReduceSum.average(List.of())).isEmpty();
    }

    @Test
    void r5_longestKeepsFirstOnTies() {
        assertThat(ReduceSum.longest(List.of("kiwi", "pear", "banana", "melon", "cherry"))).contains("banana");
        assertThat(ReduceSum.longest(Arrays.asList(null, "a", null, "b"))).contains("a");
        assertThat(ReduceSum.longest(List.of())).isEmpty();
        assertThat(ReduceSum.longest(Arrays.asList((String) null))).isEmpty();
    }

    @Test
    void r6_stats() {
        IntSummaryStatistics s = ReduceSum.stats(List.of(3, 1, 4, 1, 5));
        assertThat(s.getCount()).isEqualTo(5);
        assertThat(s.getSum()).isEqualTo(14);
        assertThat(s.getMin()).isEqualTo(1);
        assertThat(s.getMax()).isEqualTo(5);
        assertThat(ReduceSum.stats(List.of()).getCount()).isZero();
    }

    @Test
    void r7_sumLongDoesNotOverflow() {
        assertThat(ReduceSum.sumLong(List.of(Integer.MAX_VALUE, Integer.MAX_VALUE))).isEqualTo(4_294_967_294L);
        assertThat(ReduceSum.sumLong(List.of())).isZero();
    }
}
'''},
            ["`IntStream.average()` returns `OptionalDouble`, not `double`.", "Use `reduce` without an identity when the empty case must be distinguishable."],
            ["Correct identities and associative accumulators", "Primitive streams used where boxing is pointless", "No mutable external accumulators"],
            constraints=["Do not use loops; no mutable accumulator variables outside the stream", "Do not edit the tests"],
        ),
        task(
            "collectors-tolist", "Collectors Workout", "Stretch", "CollectorsWorkout",
            "Collect streams into lists, sets, maps and strings with the right collector: handle duplicate keys in `toMap`, preserve insertion order, build bracketed CSV strings, and return an unmodifiable sorted list with `collectingAndThen`.",
            [
                "`upperNames(names)` collects the upper-cased names into a `List` in input order",
                "`uniqueLengths(words)` collects the distinct word lengths into a `Set<Integer>`",
                "`lengthByWord(words)` returns a `Map<String,Integer>` word -> length that keeps the **first** value on duplicate words and preserves first-seen order (`LinkedHashMap`)",
                "`csv(items)` joins with `\", \"` and wraps in `[` `]`; an empty list gives `[]`",
                "`immutableSorted(items)` returns a naturally sorted list that rejects modification with `UnsupportedOperationException` (use `collectingAndThen`)",
                "`toIdsByType(entries)` groups `type:id` strings like `\"a:1\"` into a `TreeMap<String, List<String>>` of ids per type (sorted by type, ids in input order) using `Collectors.groupingBy` with a `mapping` downstream",
            ],
            ["duplicate words in `toMap`", "empty input", "ids appear in encounter order within each type"],
            {"CollectorsWorkout.java": r'''package @PKG@;

import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.stream.Collectors;

/** Collector practice. */
public final class CollectorsWorkout {

    private CollectorsWorkout() {
    }

    public static List<String> upperNames(List<String> names) {
        //@TODO upperNames | map to upper case and collect with Collectors.toList()
        return names.stream().map(String::toUpperCase).collect(Collectors.toList());
        //@END
    }

    public static Set<Integer> uniqueLengths(List<String> words) {
        //@TODO uniqueLengths | map to length and collect with Collectors.toSet()
        return words.stream().map(String::length).collect(Collectors.toSet());
        //@END
    }

    public static Map<String, Integer> lengthByWord(List<String> words) {
        //@TODO lengthByWord | Collectors.toMap with a merge function keeping the first value and LinkedHashMap::new as the map supplier
        return words.stream().collect(Collectors.toMap(w -> w, String::length, (first, second) -> first, LinkedHashMap::new));
        //@END
    }

    public static String csv(List<String> items) {
        //@TODO csv | Collectors.joining(", ", "[", "]") - an empty list yields "[]"
        return items.stream().collect(Collectors.joining(", ", "[", "]"));
        //@END
    }

    public static List<String> immutableSorted(Collection<String> items) {
        //@TODO immutableSorted | sorted() then collectingAndThen(toList(), Collections::unmodifiableList)
        return items.stream()
                .sorted()
                .collect(Collectors.collectingAndThen(Collectors.toList(), Collections::unmodifiableList));
        //@END
    }

    public static Map<String, List<String>> toIdsByType(List<String> entries) {
        //@TODO toIdsByType | entries look like "type:id"; groupingBy(type, TreeMap::new, mapping(id, toList()))
        return entries.stream().collect(Collectors.groupingBy(
                e -> e.substring(0, e.indexOf(':')),
                TreeMap::new,
                Collectors.mapping(e -> e.substring(e.indexOf(':') + 1), Collectors.toList())));
        //@END
    }
}
'''},
            {"CollectorsWorkoutTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class CollectorsWorkoutTest {

    @Test
    void r1_upperNames() {
        assertThat(CollectorsWorkout.upperNames(List.of("ann", "Bob"))).containsExactly("ANN", "BOB");
        assertThat(CollectorsWorkout.upperNames(List.of())).isEmpty();
    }

    @Test
    void r2_uniqueLengths() {
        assertThat(CollectorsWorkout.uniqueLengths(List.of("a", "bb", "cc", "d"))).containsExactlyInAnyOrder(1, 2);
    }

    @Test
    void r3_lengthByWordKeepsFirstAndOrder() {
        Map<String, Integer> m = CollectorsWorkout.lengthByWord(List.of("kiwi", "fig", "kiwi", "apple"));
        assertThat(m).containsOnlyKeys("kiwi", "fig", "apple");
        assertThat(new ArrayList<>(m.keySet())).containsExactly("kiwi", "fig", "apple");
        assertThat(m).containsEntry("kiwi", 4).containsEntry("fig", 3).containsEntry("apple", 5);
    }

    @Test
    void r4_csv() {
        assertThat(CollectorsWorkout.csv(List.of("a", "b", "c"))).isEqualTo("[a, b, c]");
        assertThat(CollectorsWorkout.csv(List.of("solo"))).isEqualTo("[solo]");
        assertThat(CollectorsWorkout.csv(List.of())).isEqualTo("[]");
    }

    @Test
    void r5_immutableSorted() {
        List<String> sorted = CollectorsWorkout.immutableSorted(new ArrayList<>(List.of("pear", "apple", "fig")));
        assertThat(sorted).containsExactly("apple", "fig", "pear");
        assertThatThrownBy(() -> sorted.add("zzz")).isInstanceOf(UnsupportedOperationException.class);
        assertThatThrownBy(() -> sorted.set(0, "x")).isInstanceOf(UnsupportedOperationException.class);
    }

    @Test
    void r6_toIdsByType() {
        Map<String, List<String>> grouped = CollectorsWorkout.toIdsByType(List.of("b:2", "a:1", "b:9", "a:7", "c:5"));
        assertThat(new ArrayList<>(grouped.keySet())).containsExactly("a", "b", "c");
        assertThat(grouped.get("a")).containsExactly("1", "7");
        assertThat(grouped.get("b")).containsExactly("2", "9");
        assertThat(CollectorsWorkout.toIdsByType(List.of())).isEmpty();
    }
}
'''},
            ["`toMap`'s 4-argument overload is `(keyFn, valueFn, mergeFn, mapSupplier)`.", "`groupingBy(classifier, mapFactory, downstream)` is covered in depth on Day 18; use it here as shown in the TODO."],
            ["Chooses the collector overload that fits (merge function, map supplier)", "No intermediate mutable collections built by hand", "Result mutability matches the requirements"],
            constraints=["Do not build results with loops or `forEach` into outer collections", "Do not edit the tests"],
        ),
        task(
            "challenge-word-count", "Challenge: Word Count Analyzer", "Challenge", "WordCount",
            "Build a small text analytics service entirely with streams and collectors: word frequencies (with stop words), the top-N words, a length histogram, and words that occur exactly once. Words are maximal runs of letters or digits, compared case-insensitively. **Challenge:** deliver deterministic ordering from `groupingBy`'s unordered maps.",
            [
                "`countWords(text, stopWords)` returns word -> count; words are lower-cased runs of letters/digits; stop words are excluded; `null`/blank text gives an empty map",
                "`topN(text, n, stopWords)` returns `\"word=count\"` strings, most frequent first, ties broken alphabetically; `n <= 0` gives an empty list",
                "`lengthHistogram(text)` returns a `SortedMap<Integer, Long>` word length -> number of word occurrences",
                "`hapax(text)` returns a `SortedSet<String>` of words that appear exactly once",
            ],
            ["punctuation, apostrophes and newlines split words", "mixed case", "digits are word characters", "stop words are matched case-insensitively (provided lower-case)", "null/blank text"],
            {"WordCount.java": r'''package @PKG@;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.SortedMap;
import java.util.SortedSet;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** Text analytics with streams. */
public final class WordCount {

    private WordCount() {
    }

    /** Lower-cased runs of letters/digits; blank or null text yields an empty stream. */
    private static Stream<String> words(String text) {
        if (text == null || text.isBlank()) {
            return Stream.empty();
        }
        return Arrays.stream(text.toLowerCase(Locale.ROOT).split("[^\\p{L}\\p{N}]+"))
                .filter(w -> !w.isEmpty());
    }

    public static Map<String, Long> countWords(String text, Set<String> stopWords) {
        //@TODO countWords | words(text) minus stop words, grouped by identity with Collectors.counting()
        return words(text)
                .filter(w -> !stopWords.contains(w))
                .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
        //@END
    }

    public static List<String> topN(String text, int n, Set<String> stopWords) {
        //@TODO topN | sort the entries by count desc then word asc, limit n (n <= 0 -> empty), map to "word=count"
        if (n <= 0) {
            return List.of();
        }
        return countWords(text, stopWords).entrySet().stream()
                .sorted(Map.Entry.<String, Long>comparingByValue(Comparator.reverseOrder())
                        .thenComparing(Map.Entry.comparingByKey()))
                .limit(n)
                .map(e -> e.getKey() + "=" + e.getValue())
                .toList();
        //@END
    }

    public static SortedMap<Integer, Long> lengthHistogram(String text) {
        //@TODO lengthHistogram | group word occurrences by length into a TreeMap with counting()
        return words(text).collect(Collectors.groupingBy(String::length, TreeMap::new, Collectors.counting()));
        //@END
    }

    public static SortedSet<String> hapax(String text) {
        //@TODO hapax | words with count exactly 1, collected into a TreeSet
        return countWords(text, Set.of()).entrySet().stream()
                .filter(e -> e.getValue() == 1L)
                .map(Map.Entry::getKey)
                .collect(Collectors.toCollection(TreeSet::new));
        //@END
    }
}
'''},
            {"WordCountTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class WordCountTest {

    private static final String TEXT = "The cat and the hat.\nThe END! Cat's hat? the-end 42 42";

    @Test
    void r1_countWordsSplitsOnNonLettersAndLowercases() {
        var counts = WordCount.countWords(TEXT, Set.of());
        assertThat(counts).containsEntry("the", 4L)
                .containsEntry("cat", 2L)
                .containsEntry("hat", 2L)
                .containsEntry("end", 2L)
                .containsEntry("and", 1L)
                .containsEntry("s", 1L)
                .containsEntry("42", 2L);
    }

    @Test
    void r1_stopWordsAndEmptyText() {
        var counts = WordCount.countWords(TEXT, Set.of("the", "and"));
        assertThat(counts).doesNotContainKeys("the", "and").containsKey("cat");
        assertThat(WordCount.countWords(null, Set.of())).isEmpty();
        assertThat(WordCount.countWords("  \n ", Set.of())).isEmpty();
        assertThat(WordCount.countWords("...", Set.of())).isEmpty();
    }

    @Test
    void r2_topNOrdersByCountThenWord() {
        assertThat(WordCount.topN(TEXT, 3, Set.of())).containsExactly("the=4", "42=2", "cat=2");
        assertThat(WordCount.topN(TEXT, 2, Set.of("the"))).containsExactly("42=2", "cat=2");
    }

    @Test
    void r2_topNBoundaries() {
        assertThat(WordCount.topN(TEXT, 0, Set.of())).isEmpty();
        assertThat(WordCount.topN(TEXT, -4, Set.of())).isEmpty();
        assertThat(WordCount.topN("a b", 10, Set.of())).containsExactly("a=1", "b=1");
        assertThat(WordCount.topN(null, 3, Set.of())).isEmpty();
    }

    @Test
    void r3_lengthHistogramIsSortedAndCountsOccurrences() {
        var hist = WordCount.lengthHistogram("a bb cc ddd a");
        assertThat(List.copyOf(hist.keySet())).containsExactly(1, 2, 3);
        assertThat(hist.get(1)).isEqualTo(2L);
        assertThat(hist.get(2)).isEqualTo(2L);
        assertThat(hist.get(3)).isEqualTo(1L);
        assertThat(WordCount.lengthHistogram("")).isEmpty();
    }

    @Test
    void r4_hapax() {
        var once = WordCount.hapax("Red green red BLUE green yellow");
        assertThat(List.copyOf(once)).containsExactly("blue", "yellow");
        assertThat(WordCount.hapax("same same")).isEmpty();
        assertThat(WordCount.hapax(null)).isEmpty();
    }
}
'''},
            ["Ties in `topN` are why a `HashMap` alone is not enough: sort the entries by two keys.", "A `TreeMap::new` map factory in `groupingBy` gives sorted keys for free."],
            ["Entire pipelines are expressed with streams and collectors", "Deterministic ordering is produced explicitly", "Private helper `words(...)` reused instead of duplicated splitting logic"],
            constraints=["No explicit loops in the public methods", "Do not edit the tests"],
        ),
    ],
)
