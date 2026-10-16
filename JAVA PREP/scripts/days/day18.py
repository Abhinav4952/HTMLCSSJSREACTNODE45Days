from gen_helpers import sec, task

DAY = dict(
    num=18,
    title="Streams II: groupingBy, partitioningBy, flatMap, Primitive Streams, and Parallel Cautions",
    theme="Aggregate and reshape data with advanced collectors, flatten nested structures, and decide when parallel streams are (not) appropriate.",
    objectives=[
        "Group and aggregate with `Collectors.groupingBy` and downstream collectors (`counting`, `summingX`, `averagingX`, `mapping`, `maxBy`, `collectingAndThen`)",
        "Split data in two with `partitioningBy` and explain how it differs from `groupingBy`",
        "Flatten nested collections with `flatMap`, `flatMapToInt`, and `mapMulti` awareness",
        "Use `IntStream`, `LongStream`, `DoubleStream`, ranges, and boxing conversions",
        "State the rules for safe parallel streams (stateless, non-interfering, associative) and list their performance cautions",
        "Choose deterministic result types (`TreeMap`, `LinkedHashMap`) for tests and APIs",
    ],
    prereqs=["Day 17 — stream pipelines, reduce, collectors", "Day 15 — maps and ordering", "Day 16 — Optional and functional interfaces"],
    overview="""Day 17 taught the pipeline; today you learn the collectors that power reporting code and the operations that reshape data. `groupingBy` is the SQL `GROUP BY` of Java, `partitioningBy` is a two-bucket split, `flatMap` turns *a stream of collections* into *a stream of elements*, and primitive streams make numeric code fast and boxing-free.

Then comes the part interviewers love: **parallel streams**. `parallelStream()` looks like a free speed-up but runs on the shared `ForkJoinPool.commonPool()`, requires associative and stateless operations, and often makes small or I/O-bound workloads slower. Knowing *when not to* is the senior-level answer.""",
    sections=[
        sec(
            "groupingBy and partitioningBy with downstream collectors",
            "`Collectors.groupingBy(classifier)` builds a `Map<K, List<T>>` where each element is placed under the key its classifier returns. The overloads add a **map factory** (`TreeMap::new`) and a **downstream collector** that reduces each group: `counting()`, `summingInt/Double`, `averagingX`, `mapping(f, downstream)`, `maxBy/minBy(comparator)`, `toSet()`, `collectingAndThen(downstream, finisher)`, `reducing`, `teeing` (Java 12). `partitioningBy(predicate[, downstream])` is a special grouping with exactly two keys, `true` and `false`.",
            "Reports and dashboards are almost all grouping: orders per customer, revenue per month, employees per department. Doing it with one collector replaces nested loops with `computeIfAbsent`. `partitioningBy` is the right tool for pass/fail, valid/invalid, even/odd splits because it **always contains both keys**, even if one bucket is empty.",
            ["One declarative expression for GROUP BY style aggregations", "Downstream collectors compose to any depth (group by dept then by city)", "Choosable map implementation for deterministic ordering", "`partitioningBy` guarantees both `true` and `false` entries"],
            ["The default `groupingBy` map is a `HashMap` (unordered, not specified) - wrong for stable output", "`maxBy`/`minBy` yield `Optional` values that you must unwrap or finish with `collectingAndThen`", "Deeply nested collectors become hard to read - extract helper methods"],
            "Asserting on `groupingBy` output ordering without `TreeMap::new` yields flaky tests. `groupingBy(f)` with a classifier returning `null` throws `NullPointerException: element cannot be mapped to a null key`. Using `toMap` where several rows share a key throws `IllegalStateException` (grouping would have been correct). Forgetting that `groupingBy` omits keys with no elements while `partitioningBy` always has two keys causes `NullPointerException` when you unbox `map.get(false)` for an empty partition under `groupingBy`. `averagingInt` on an empty group never occurs, but `maxBy` per group is `Optional` - calling `get()` blindly is a smell.",
            """- `groupingBy(f)` -> `Map<K, List<T>>`; `groupingBy(f, downstream)`; `groupingBy(f, TreeMap::new, downstream)`.
- Downstream: `counting()` -> `Long`; `summingInt(ToIntFunction)` -> `Integer`; `averagingDouble(ToDoubleFunction)` -> `Double`; `mapping(Function, downstream)`; `maxBy(Comparator)` -> `Optional<T>`.
- Unwrap: `collectingAndThen(maxBy(cmp), o -> o.orElseThrow().name())`.
- `partitioningBy(p)` -> `Map<Boolean, List<T>>`; `partitioningBy(p, downstream)`.
- Multi-level: `groupingBy(Emp::dept, groupingBy(Emp::city, counting()))`.
- `Collectors.teeing(c1, c2, merger)` computes two results in one pass.""",
            [
                ("Tiny — group and count", """record Emp(String name, String dept, double salary) {}
List<Emp> emps = List.of(new Emp("a", "ENG", 100), new Emp("b", "HR", 80), new Emp("c", "ENG", 120));
Map<String, Long> headcount = emps.stream()
        .collect(Collectors.groupingBy(Emp::dept, TreeMap::new, Collectors.counting()));
System.out.println(headcount);   // {ENG=2, HR=1}"""),
                ("Tiny — partitioningBy always has both keys", """Map<Boolean, List<Integer>> parts = Stream.of(1, 3, 5).collect(Collectors.partitioningBy(n -> n % 2 == 0));
System.out.println(parts);               // {false=[1, 3, 5], true=[]}
Map<Integer, List<Integer>> groups = Stream.of(1, 3, 5).collect(Collectors.groupingBy(n -> n % 2));
System.out.println(groups);              // {1=[1, 3, 5]}  <- no key 0 at all"""),
                ("Medium — a small report with downstream collectors", """import java.util.*;
import java.util.stream.*;

public class DeptReport {
    record Emp(String name, String dept, double salary) {}

    public static void main(String[] args) {
        List<Emp> emps = List.of(new Emp("Ann", "ENG", 120), new Emp("Bob", "ENG", 100),
                new Emp("Cy", "HR", 90), new Emp("Di", "HR", 95));

        Map<String, Double> avg = emps.stream().collect(
                Collectors.groupingBy(Emp::dept, TreeMap::new, Collectors.averagingDouble(Emp::salary)));
        Map<String, String> top = emps.stream().collect(
                Collectors.groupingBy(Emp::dept, TreeMap::new,
                        Collectors.collectingAndThen(
                                Collectors.maxBy(Comparator.comparingDouble(Emp::salary)),
                                o -> o.orElseThrow().name())));
        System.out.println(avg);   // {ENG=110.0, HR=92.5}
        System.out.println(top);   // {ENG=Ann, HR=Di}
    }
}"""),
            ],
            [
                ("What is the type of `groupingBy(f, counting())` values and why does it matter?", "`Long` - assigning to `Map<K,Integer>` does not compile; convert with `.intValue()` if needed."),
                ("How do you make `groupingBy` return sorted keys?", "Use the three-argument overload with `TreeMap::new`."),
                ("Difference between `groupingBy(p)` and `partitioningBy(p)`?", "`partitioningBy` takes a boolean predicate and always has exactly the keys `true` and `false`; `groupingBy` keys come from the data and empty groups are absent."),
                ("How do you get a plain value instead of `Optional` from `maxBy` per group?", "Wrap it with `collectingAndThen(maxBy(cmp), o -> o.orElseThrow()...)` (the group is never empty)."),
            ],
        ),
        sec(
            "flatMap and primitive streams",
            "`flatMap(Function<T, Stream<R>>)` replaces each element with a *stream* of results and concatenates them: `Stream<List<Item>>` becomes `Stream<Item>`; `Stream<String>` of sentences becomes a `Stream<String>` of words. Variants: `flatMapToInt`, `flatMapToDouble`, `mapMulti` (Java 16). **Primitive streams** (`IntStream`, `LongStream`, `DoubleStream`) hold unboxed values with `sum`, `average`, `range(a, b)` (exclusive), `rangeClosed`, `boxed()`, `mapToObj`, `asLongStream`, and `summaryStatistics`.",
            "Real data is nested: orders have line items, users have roles, documents have paragraphs. `flatMap` is the stream equivalent of nested loops and the way to \"explode\" a collection into rows. Primitive streams avoid millions of `Integer` allocations in numeric code and provide the right aggregate operations.",
            ["Flatten nested structures declaratively", "Handle missing inner collections gracefully with `Stream.ofNullable` / empty streams", "Unboxed numeric pipelines are faster and more memory efficient", "`IntStream.range` replaces most index loops"],
            ["Easy to confuse `map` (one-to-one) and `flatMap` (one-to-many); `map(List::stream)` gives `Stream<Stream<T>>`", "A `null` returned from the flatMap function throws `NullPointerException` (return `Stream.empty()`)", "Conversions between boxed and primitive streams add noise"],
            "Using `map(Order::items)` then trying to sum item quantities fails because you are still iterating lists, not items. Returning `null` from the flatMap mapper when an order has no items throws NPE; return `Stream.empty()`. `IntStream.range(0, n)` is end-exclusive: using it where you meant `rangeClosed` is an off-by-one bug. `int` overflow in `IntStream.sum()` is silent (use `mapToLong`). `Arrays.stream(int[])` gives an `IntStream` but `Arrays.asList(int[])` gives a `List<int[]>` with one element - a famous trap.",
            """- `Stream<R> flatMap(Function<? super T, ? extends Stream<? extends R>> mapper)`.
- Guard nulls: `o.items() == null ? Stream.empty() : o.items().stream()` or `Stream.ofNullable(...)` (single element).
- `IntStream.range(0, 5)` -> 0..4; `rangeClosed(1, 5)` -> 1..5.
- `boxed()` -> `Stream<Integer>`; `mapToObj(i -> ...)`; `mapToInt(Integer::intValue)`; `asDoubleStream()`.
- `mapMulti((x, sink) -> { sink.accept(a); sink.accept(b); })` - imperative alternative when emitting few items.
- `IntStream.iterate(1, i -> i * 2).limit(10)` / `takeWhile` / `dropWhile` for ordered streams.""",
            [
                ("Tiny — words from sentences", """List<String> sentences = List.of("to be", "or not");
List<String> words = sentences.stream()
        .flatMap(s -> Arrays.stream(s.split(" ")))
        .toList();
System.out.println(words);   // [to, be, or, not]"""),
                ("Tiny — primitive ranges", """System.out.println(IntStream.range(0, 5).sum());          // 10
System.out.println(IntStream.rangeClosed(1, 5).sum());    // 15
System.out.println(IntStream.rangeClosed(1, 5).mapToObj(Integer::toString).collect(Collectors.joining("-"))); // 1-2-3-4-5
int[] arr = {3, 1, 2};
System.out.println(Arrays.stream(arr).max().getAsInt());  // 3"""),
                ("Medium — order lines: total units, revenue, units per SKU", """import java.util.*;
import java.util.stream.*;

public class Orders {
    record Line(String sku, int qty, double price) {}
    record Order(String id, List<Line> lines) {}

    static Stream<Line> lines(List<Order> orders) {
        return orders.stream().flatMap(o -> o.lines() == null ? Stream.empty() : o.lines().stream());
    }

    public static void main(String[] args) {
        List<Order> orders = List.of(
                new Order("o1", List.of(new Line("A", 2, 2.5), new Line("B", 1, 10.0))),
                new Order("o2", null),
                new Order("o3", List.of(new Line("A", 3, 2.5))));
        System.out.println(lines(orders).mapToInt(Line::qty).sum());                          // 6
        System.out.println(lines(orders).mapToDouble(l -> l.qty() * l.price()).sum());        // 22.5
        System.out.println(lines(orders).collect(Collectors.groupingBy(Line::sku, TreeMap::new,
                Collectors.summingInt(Line::qty))));                                          // {A=5, B=1}
    }
}"""),
            ],
            [
                ("What is the type of `orders.stream().map(Order::items)` and how do you get the items themselves?", "`Stream<List<Line>>`; use `flatMap(o -> o.items().stream())` to get `Stream<Line>`."),
                ("What does `IntStream.range(0, 3)` produce?", "0, 1, 2 (end exclusive)."),
                ("Why does `Arrays.asList(new int[]{1,2,3})` have size 1?", "`int[]` is a single object, so you get `List<int[]>`; use `Arrays.stream` or `IntStream`."),
                ("What should the flatMap mapper return for \"no children\"?", "`Stream.empty()` (never `null`)."),
            ],
        ),
        sec(
            "Parallel streams: cautions and when not to use them",
            "`collection.parallelStream()` or `stream.parallel()` splits the source into chunks (via a `Spliterator`), processes them on the **common ForkJoinPool** (default parallelism = cores - 1, shared by the whole JVM), and merges partial results. It is a *performance* feature, not a correctness feature: for sequential pipelines results are deterministic; for parallel pipelines you must ensure the operations are **stateless**, **non-interfering**, and that reductions are **associative** with a true identity. `forEachOrdered` preserves encounter order at a cost; `forEach` does not.",
            "CPU-bound, large (tens of thousands of elements or heavy per-element work), easily splittable sources (arrays, `ArrayList`, ranges) can scale. But overhead (splitting, merging, thread handoff), contention on shared mutable state, ordered/stateful operations, boxing, and blocking I/O inside the common pool often make parallel streams slower - or break the whole application because every parallel stream shares the same pool.",
            ["Can speed up large CPU-bound data-parallel work with one method call", "Same pipeline code as sequential (`stream()` vs `parallelStream()`)", "Fork/join framework handles splitting and merging", "`ArrayList`/arrays/ranges split efficiently"],
            ["Overhead usually dominates for small or cheap workloads", "Shared mutable state, non-associative reductions, and side effects produce wrong or nondeterministic results", "The shared common pool means one blocking task can starve unrelated parallel streams (and `CompletableFuture` async tasks)", "Poor splitting for `LinkedList`, `Stream.iterate`, `BufferedReader.lines`; ordered operations (`limit`, `findFirst`, `sorted`) reduce parallelism"],
            "Adding to an `ArrayList` from `parallelStream().forEach(list::add)` corrupts the list (`ArrayIndexOutOfBoundsException`, lost elements, nulls) because `ArrayList` is not thread-safe. A `reduce` with `(a, b) -> a - b` or a wrong identity yields different answers per run. Doing blocking I/O (HTTP, JDBC) in a parallel stream ties up the common pool and degrades unrelated requests. A parallel stream over 20 elements is typically 10-100x slower than sequential. `parallel()` on `Stream.iterate` can *hang or run out of memory* without `limit`. Benchmarks without JMH usually mislead (JIT warm-up, GC).",
            """- **Checklist before `parallel()`:** large source? splittable source? CPU-bound work? stateless and non-interfering lambdas? associative reduction with real identity? no blocking I/O? measured (JMH) benefit?
- Safe collection: `collect(Collectors.toList())` (thread-confined partial containers merged by the combiner) - never `forEach(list::add)`.
- `reduce(identity, accumulator, combiner)`: accumulator and combiner must agree.
- `unordered()` can improve `distinct`/`limit` performance when order does not matter.
- Custom pool trick (`pool.submit(() -> stream.parallel()...)`) is an implementation detail, not a supported API contract - prefer an explicit `ExecutorService` (Day 21).
- Default recommendation: **start sequential**; only parallelize with evidence.""",
            [
                ("Tiny — the broken parallel forEach", """List<Integer> out = new ArrayList<>();
IntStream.range(0, 10_000).parallel().forEach(out::add);     // BUG: ArrayList is not thread-safe
System.out.println(out.size());    // usually < 10000, or throws ArrayIndexOutOfBoundsException

List<Integer> ok = IntStream.range(0, 10_000).parallel().boxed().collect(Collectors.toList());
System.out.println(ok.size());     // 10000 - collect is designed for parallelism"""),
                ("Tiny — safe vs unsafe reduction", """int sum = IntStream.rangeClosed(1, 1_000).parallel().sum();           // 500500 every time (associative)
int bad = Stream.of(10, 3, 2).parallel().reduce(0, (a, b) -> a - b);     // not associative: result may vary
System.out.println(sum);"""),
                ("Medium — a documented, deliberately sequential implementation", """import java.util.*;
import java.util.stream.*;

public final class ReportService {
    /**
     * Sequential on purpose: the per-element work is trivial (a multiplication),
     * the list is small, and the code runs inside a web request thread. Parallelizing would add
     * fork/join overhead, compete on the common pool, and gain nothing.
     */
    public static long sumOfSquares(List<Integer> values) {
        return values.stream().mapToLong(v -> (long) v * v).sum();
    }

    public static void main(String[] args) {
        System.out.println(sumOfSquares(List.of(1, 2, 3)));   // 14
    }
}"""),
            ],
            [
                ("Name three conditions a reduction must satisfy to be safe in parallel.", "Associative accumulator, a true identity, and stateless/non-interfering lambdas."),
                ("Why can one blocking task in a parallel stream hurt unrelated code?", "All parallel streams share the common ForkJoinPool; blocked workers cannot serve other tasks."),
                ("Why is `parallelStream().forEach(list::add)` wrong?", "`ArrayList` is not thread-safe and `forEach` gives no ordering/merging guarantees; use `collect`."),
                ("Give two situations where parallel streams are almost always a bad idea.", "Small collections / cheap work (overhead dominates) and blocking I/O or `LinkedList`/`iterate` sources."),
            ],
        ),
    ],
    interview=[
        ("groupingBy vs partitioningBy vs toMap?", "`groupingBy` buckets by an arbitrary key and may reduce each bucket downstream; `partitioningBy` is a two-bucket boolean split with both keys always present; `toMap` maps one element to one entry and fails on duplicate keys unless you provide a merge function."),
        ("map vs flatMap?", "`map` transforms one element into one element; `flatMap` transforms one element into a stream and flattens the streams into one."),
        ("Are parallel streams always faster? When would you use them?", "No. Use them for large, CPU-bound, splittable, stateless workloads after measuring; avoid for small data, I/O, or shared mutable state."),
        ("What pool do parallel streams use and what is the risk?", "`ForkJoinPool.commonPool()`; sharing it means one slow/blocking pipeline can starve others."),
        ("How do you compute two aggregates in a single pass?", "`Collectors.teeing(c1, c2, merger)` (Java 12) or a custom collector."),
        ("Why use primitive streams?", "To avoid boxing allocations, and to get `sum`, `average`, `summaryStatistics` directly."),
    ],
    mistakes=[
        "Unordered `HashMap` results from `groupingBy` asserted in tests (use `TreeMap::new` or order-insensitive assertions).",
        "Expecting `groupingBy` to include empty groups (use `partitioningBy` for two-way splits).",
        "Returning `null` instead of `Stream.empty()` from a `flatMap` mapper.",
        "Mutating shared state from parallel stream lambdas.",
        "Using `parallelStream()` by reflex for small lists or blocking calls.",
        "Off-by-one with `range` vs `rangeClosed`.",
    ],
    reading=[
        "Javadoc: `java.util.stream.Collectors` (groupingBy, partitioningBy, teeing), `java.util.stream` package docs (*Parallelism*, *Side-effects*, *Ordering*)",
        "Brian Goetz, \"Parallel Streams: When to use them\" guidance and the JDK `Stream` Javadoc NOTEs",
        "Oracle Java Tutorials - *Parallelism* lesson",
        "*Effective Java* (Bloch) item 48 (be careful when making streams parallel)",
    ],
    glossary=[
        ("Downstream collector", "A collector applied to each group produced by `groupingBy`/`partitioningBy`"),
        ("Partition", "A two-way split by a predicate (keys `true` and `false`)"),
        ("Flattening", "Merging many inner streams into one (flatMap)"),
        ("Spliterator", "Splittable iterator that parallel streams use to divide work"),
        ("Common pool", "`ForkJoinPool.commonPool()` shared by all parallel streams in the JVM"),
        ("Associative", "Grouping of operands does not change the result"),
        ("Encounter order", "The order in which a stream's source defines its elements"),
    ],
    tasks=[
        task(
            "group-by-dept", "Group Employees by Department", "Warm-up", "GroupByDept",
            "Produce department reports with `groupingBy` and downstream collectors: names per department, total and average salary, headcount, and the top earner per department. All results are sorted maps so output is deterministic.",
            [
                "`namesByDept(emps)` returns a `SortedMap<String, List<String>>` of employee names per department in input order",
                "`totalSalaryByDept(emps)` returns the sum of salaries per department (sorted by department)",
                "`averageSalaryByDept(emps)` returns the average salary per department",
                "`headcountByDept(emps)` returns the number of employees per department as `Long`",
                "`topEarnerByDept(emps)` returns the name of the highest-paid employee per department; on a salary tie the **first listed** employee wins",
            ],
            ["empty input -> empty map", "single-employee departments", "salary ties", "departments sorted alphabetically"],
            {"Emp.java": r'''package @PKG@;

/** Provided value type. */
public record Emp(String name, String dept, double salary) {
}
''',
             "GroupByDept.java": r'''package @PKG@;

import java.util.Comparator;
import java.util.List;
import java.util.SortedMap;
import java.util.TreeMap;
import java.util.stream.Collectors;

/** Department reports built with groupingBy. */
public final class GroupByDept {

    private GroupByDept() {
    }

    public static SortedMap<String, List<String>> namesByDept(List<Emp> emps) {
        //@TODO namesByDept | groupingBy(dept, TreeMap::new, mapping(name, toList()))
        return emps.stream().collect(Collectors.groupingBy(
                Emp::dept, TreeMap::new, Collectors.mapping(Emp::name, Collectors.toList())));
        //@END
    }

    public static SortedMap<String, Double> totalSalaryByDept(List<Emp> emps) {
        //@TODO totalSalaryByDept | groupingBy(dept, TreeMap::new, summingDouble(salary))
        return emps.stream().collect(Collectors.groupingBy(
                Emp::dept, TreeMap::new, Collectors.summingDouble(Emp::salary)));
        //@END
    }

    public static SortedMap<String, Double> averageSalaryByDept(List<Emp> emps) {
        //@TODO averageSalaryByDept | groupingBy(dept, TreeMap::new, averagingDouble(salary))
        return emps.stream().collect(Collectors.groupingBy(
                Emp::dept, TreeMap::new, Collectors.averagingDouble(Emp::salary)));
        //@END
    }

    public static SortedMap<String, Long> headcountByDept(List<Emp> emps) {
        //@TODO headcountByDept | groupingBy(dept, TreeMap::new, counting())
        return emps.stream().collect(Collectors.groupingBy(
                Emp::dept, TreeMap::new, Collectors.counting()));
        //@END
    }

    public static SortedMap<String, String> topEarnerByDept(List<Emp> emps) {
        //@TODO topEarnerByDept | groupingBy(dept, TreeMap::new, collectingAndThen(maxBy(by salary), optional -> optional.orElseThrow().name())); first listed wins ties
        return emps.stream().collect(Collectors.groupingBy(
                Emp::dept,
                TreeMap::new,
                Collectors.collectingAndThen(
                        Collectors.maxBy(Comparator.comparingDouble(Emp::salary)),
                        best -> best.orElseThrow().name())));
        //@END
    }
}
'''},
            {"GroupByDeptTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class GroupByDeptTest {

    private static final List<Emp> EMPS = List.of(
            new Emp("Ann", "ENG", 120),
            new Emp("Bob", "HR", 80),
            new Emp("Cy", "ENG", 100),
            new Emp("Di", "OPS", 70),
            new Emp("Eve", "HR", 80),
            new Emp("Flo", "ENG", 120));

    @Test
    void r1_namesByDeptSortedAndInInputOrder() {
        var names = GroupByDept.namesByDept(EMPS);
        assertThat(new ArrayList<>(names.keySet())).containsExactly("ENG", "HR", "OPS");
        assertThat(names.get("ENG")).containsExactly("Ann", "Cy", "Flo");
        assertThat(names.get("HR")).containsExactly("Bob", "Eve");
        assertThat(names.get("OPS")).containsExactly("Di");
    }

    @Test
    void r2_totalSalary() {
        var totals = GroupByDept.totalSalaryByDept(EMPS);
        assertThat(totals.get("ENG")).isEqualTo(340.0);
        assertThat(totals.get("HR")).isEqualTo(160.0);
        assertThat(totals.get("OPS")).isEqualTo(70.0);
    }

    @Test
    void r3_averageSalary() {
        var avg = GroupByDept.averageSalaryByDept(EMPS);
        assertThat(avg.get("ENG")).isCloseTo(113.3333, org.assertj.core.data.Offset.offset(0.001));
        assertThat(avg.get("HR")).isEqualTo(80.0);
    }

    @Test
    void r4_headcount() {
        var counts = GroupByDept.headcountByDept(EMPS);
        assertThat(counts.get("ENG")).isEqualTo(3L);
        assertThat(counts.get("HR")).isEqualTo(2L);
        assertThat(counts.get("OPS")).isEqualTo(1L);
        assertThat(counts).hasSize(3);
    }

    @Test
    void r5_topEarnerFirstWinsTies() {
        var top = GroupByDept.topEarnerByDept(EMPS);
        assertThat(top.get("ENG")).isEqualTo("Ann");
        assertThat(top.get("HR")).isEqualTo("Bob");
        assertThat(top.get("OPS")).isEqualTo("Di");
    }

    @Test
    void emptyInputGivesEmptyMaps() {
        assertThat(GroupByDept.namesByDept(List.of())).isEmpty();
        assertThat(GroupByDept.totalSalaryByDept(List.of())).isEmpty();
        assertThat(GroupByDept.averageSalaryByDept(List.of())).isEmpty();
        assertThat(GroupByDept.headcountByDept(List.of())).isEmpty();
        assertThat(GroupByDept.topEarnerByDept(List.of())).isEmpty();
    }
}
'''},
            ["`Collectors.maxBy` returns the *first* of equal elements, which matches the tie rule.", "Use the three-argument `groupingBy` so the map is a `TreeMap`."],
            ["One collector expression per method", "Sorted map factory used for deterministic ordering", "Optional unwrapped through `collectingAndThen`, not `get()`"],
            constraints=["Use `Collectors.groupingBy` - no hand-written loops or `computeIfAbsent`", "Do not edit the tests"],
        ),
        task(
            "partition-even", "Partitioning Data", "Core", "PartitionEven",
            "Use `partitioningBy` for two-way splits and its downstream collectors. The tests highlight the key property: both `true` and `false` entries exist even when a bucket is empty.",
            [
                "`partitionEven(numbers)` returns `Map<Boolean, List<Integer>>` with evens under `true` and odds under `false` (input order kept)",
                "`partition(items, predicate)` is the generic version for any element type and predicate",
                "`countPassFail(scores, passMark)` returns the number of scores `>= passMark` under `true` and `< passMark` under `false` as `Long`",
                "`sumEvenOdd(numbers)` returns the sum of evens under `true` and odds under `false`",
                "For empty input, **both keys must still be present** with empty/zero results",
            ],
            ["empty input", "all even / all odd", "negative odd numbers", "pass mark boundary (equal passes)"],
            {"PartitionEven.java": r'''package @PKG@;

import java.util.List;
import java.util.Map;
import java.util.function.Predicate;
import java.util.stream.Collectors;

/** partitioningBy practice. */
public final class PartitionEven {

    private PartitionEven() {
    }

    public static Map<Boolean, List<Integer>> partitionEven(List<Integer> numbers) {
        //@TODO partitionEven | partitioningBy(n -> n % 2 == 0): evens under true, odds under false
        return numbers.stream().collect(Collectors.partitioningBy(n -> n % 2 == 0));
        //@END
    }

    public static <T> Map<Boolean, List<T>> partition(List<T> items, Predicate<? super T> predicate) {
        //@TODO partition | generic partitioningBy(predicate)
        return items.stream().collect(Collectors.partitioningBy(predicate));
        //@END
    }

    public static Map<Boolean, Long> countPassFail(List<Integer> scores, int passMark) {
        //@TODO countPassFail | partitioningBy(score >= passMark, counting())
        return scores.stream().collect(Collectors.partitioningBy(s -> s >= passMark, Collectors.counting()));
        //@END
    }

    public static Map<Boolean, Integer> sumEvenOdd(List<Integer> numbers) {
        //@TODO sumEvenOdd | partitioningBy(even, summingInt(Integer::intValue))
        return numbers.stream().collect(
                Collectors.partitioningBy(n -> n % 2 == 0, Collectors.summingInt(Integer::intValue)));
        //@END
    }
}
'''},
            {"PartitionEvenTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class PartitionEvenTest {

    @Test
    void r1_partitionEven() {
        var parts = PartitionEven.partitionEven(List.of(1, 2, 3, 4, 5, -3, -4));
        assertThat(parts.get(true)).containsExactly(2, 4, -4);
        assertThat(parts.get(false)).containsExactly(1, 3, 5, -3);
    }

    @Test
    @DisplayName("Both keys exist even when one bucket (or the input) is empty")
    void r5_bothKeysAlwaysPresent() {
        var allOdd = PartitionEven.partitionEven(List.of(1, 3));
        assertThat(allOdd).containsOnlyKeys(true, false);
        assertThat(allOdd.get(true)).isEmpty();
        var none = PartitionEven.partitionEven(List.of());
        assertThat(none).containsOnlyKeys(true, false);
        assertThat(none.get(false)).isEmpty();
    }

    @Test
    void r2_genericPartition() {
        var parts = PartitionEven.partition(List.of("a", "bb", "ccc", "dd"), s -> s.length() >= 2);
        assertThat(parts.get(true)).containsExactly("bb", "ccc", "dd");
        assertThat(parts.get(false)).containsExactly("a");
        Object marker = new Object();
        java.util.function.Predicate<Object> anything = o -> o == marker;
        assertThat(PartitionEven.partition(List.of("x"), anything).get(false)).containsExactly("x");
    }

    @Test
    void r3_countPassFail() {
        var result = PartitionEven.countPassFail(List.of(40, 50, 75, 49, 100), 50);
        assertThat(result.get(true)).isEqualTo(3L);
        assertThat(result.get(false)).isEqualTo(2L);
    }

    @Test
    void r3_countPassFailEmptyHasZeroes() {
        var result = PartitionEven.countPassFail(List.of(), 50);
        assertThat(result).containsOnlyKeys(true, false);
        assertThat(result.get(true)).isZero();
        assertThat(result.get(false)).isZero();
    }

    @Test
    void r4_sumEvenOdd() {
        var sums = PartitionEven.sumEvenOdd(List.of(1, 2, 3, 4, 5));
        assertThat(sums.get(true)).isEqualTo(6);
        assertThat(sums.get(false)).isEqualTo(9);
        var empty = PartitionEven.sumEvenOdd(List.of());
        assertThat(empty.get(true)).isZero();
        assertThat(empty.get(false)).isZero();
    }
}
'''},
            ["`partitioningBy(p, downstream)` applies the downstream collector to each side - even an empty one (which is why `counting()` yields `0`).", "Boxed `Long`/`Integer` values: use `isEqualTo(3L)` for `Long`."],
            ["Uses `partitioningBy`, not `groupingBy` with a boolean classifier", "No manual null checks for missing keys"],
            constraints=["Use `Collectors.partitioningBy` for every method", "Do not edit the tests"],
        ),
        task(
            "flatmap-orders", "FlatMap Orders", "Stretch", "OrderAnalytics",
            "Flatten orders into line items with `flatMap` and compute analytics: distinct SKUs, units, revenue, units per SKU, the best-selling SKU, and words from sentences. Orders may have a `null` item list and must be treated as empty.",
            [
                "`allSkus(orders)` returns the distinct SKUs sorted alphabetically",
                "`totalUnits(orders)` sums all line quantities (use a primitive stream)",
                "`totalRevenue(orders)` sums `qty * price` over all lines",
                "`unitsBySku(orders)` returns a `SortedMap<String,Integer>` of total units per SKU",
                "`bestSellerSku(orders)` returns the SKU with most units as an `Optional` (ties: alphabetically first SKU); empty when there are no lines",
                "`flattenWords(sentences)` splits sentences on whitespace into one list of words (blank sentences contribute nothing)",
                "Orders whose `items` list is `null` are treated as having no items",
            ],
            ["null item list", "empty orders list", "ties for best seller", "blank sentences and multiple spaces"],
            {"LineItem.java": r'''package @PKG@;

/** Provided value type. */
public record LineItem(String sku, int qty, double price) {
}
''',
             "Order.java": r'''package @PKG@;

import java.util.List;

/** Provided value type; items may be null. */
public record Order(String id, List<LineItem> items) {
}
''',
             "OrderAnalytics.java": r'''package @PKG@;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.SortedMap;
import java.util.TreeMap;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** flatMap-based analytics. */
public final class OrderAnalytics {

    private OrderAnalytics() {
    }

    private static Stream<LineItem> lines(List<Order> orders) {
        return orders.stream().flatMap(o -> o.items() == null ? Stream.<LineItem>empty() : o.items().stream());
    }

    public static List<String> allSkus(List<Order> orders) {
        //@TODO allSkus | flatten to line items, map to sku, distinct, sorted
        return lines(orders).map(LineItem::sku).distinct().sorted().toList();
        //@END
    }

    public static int totalUnits(List<Order> orders) {
        //@TODO totalUnits | flatten and sum qty with mapToInt
        return lines(orders).mapToInt(LineItem::qty).sum();
        //@END
    }

    public static double totalRevenue(List<Order> orders) {
        //@TODO totalRevenue | flatten and sum qty * price with mapToDouble
        return lines(orders).mapToDouble(l -> l.qty() * l.price()).sum();
        //@END
    }

    public static SortedMap<String, Integer> unitsBySku(List<Order> orders) {
        //@TODO unitsBySku | groupingBy(sku, TreeMap::new, summingInt(qty)) over the flattened lines
        return lines(orders).collect(Collectors.groupingBy(
                LineItem::sku, TreeMap::new, Collectors.summingInt(LineItem::qty)));
        //@END
    }

    public static Optional<String> bestSellerSku(List<Order> orders) {
        //@TODO bestSellerSku | the SKU with most units; ties -> alphabetically first; Optional.empty() when there are no lines
        return unitsBySku(orders).entrySet().stream()
                .max(Map.Entry.<String, Integer>comparingByValue()
                        .thenComparing(Map.Entry.comparingByKey(Comparator.reverseOrder())))
                .map(Map.Entry::getKey);
        //@END
    }

    public static List<String> flattenWords(List<String> sentences) {
        //@TODO flattenWords | flatMap each sentence to its whitespace-separated words, dropping empty tokens
        return sentences.stream()
                .flatMap(s -> Arrays.stream(s.trim().split("\\s+")))
                .filter(w -> !w.isEmpty())
                .toList();
        //@END
    }
}
'''},
            {"OrderAnalyticsTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.within;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class OrderAnalyticsTest {

    private static final List<Order> ORDERS = List.of(
            new Order("o1", List.of(new LineItem("B", 1, 10.0), new LineItem("A", 2, 2.5))),
            new Order("o2", null),
            new Order("o3", List.of(new LineItem("A", 3, 2.5), new LineItem("C", 5, 1.0))),
            new Order("o4", List.of()));

    @Test
    void r1_allSkusDistinctSorted() {
        assertThat(OrderAnalytics.allSkus(ORDERS)).containsExactly("A", "B", "C");
        assertThat(OrderAnalytics.allSkus(List.of())).isEmpty();
    }

    @Test
    void r2_totalUnits() {
        assertThat(OrderAnalytics.totalUnits(ORDERS)).isEqualTo(11);
        assertThat(OrderAnalytics.totalUnits(List.of())).isZero();
    }

    @Test
    void r3_totalRevenue() {
        assertThat(OrderAnalytics.totalRevenue(ORDERS)).isCloseTo(10.0 + 5.0 + 7.5 + 5.0, within(1e-9));
        assertThat(OrderAnalytics.totalRevenue(List.of(new Order("x", null)))).isZero();
    }

    @Test
    void r4_unitsBySku() {
        var units = OrderAnalytics.unitsBySku(ORDERS);
        assertThat(new ArrayList<>(units.keySet())).containsExactly("A", "B", "C");
        assertThat(units.get("A")).isEqualTo(5);
        assertThat(units.get("B")).isEqualTo(1);
        assertThat(units.get("C")).isEqualTo(5);
    }

    @Test
    void r5_bestSellerTieBreaksAlphabetically() {
        assertThat(OrderAnalytics.bestSellerSku(ORDERS)).contains("A");
        List<Order> single = List.of(new Order("o", List.of(new LineItem("Z", 9, 1.0), new LineItem("Y", 1, 1.0))));
        assertThat(OrderAnalytics.bestSellerSku(single)).contains("Z");
        assertThat(OrderAnalytics.bestSellerSku(List.of(new Order("e", null)))).isEmpty();
        assertThat(OrderAnalytics.bestSellerSku(List.of())).isEmpty();
    }

    @Test
    void r6_flattenWords() {
        assertThat(OrderAnalytics.flattenWords(List.of("to be", "  or   not ", "", "  "))).containsExactly("to", "be", "or", "not");
        assertThat(OrderAnalytics.flattenWords(List.of())).isEmpty();
    }

    @Test
    void r7_nullItemListsAreEmpty() {
        List<Order> onlyNull = List.of(new Order("a", null), new Order("b", null));
        assertThat(OrderAnalytics.allSkus(onlyNull)).isEmpty();
        assertThat(OrderAnalytics.totalUnits(onlyNull)).isZero();
        assertThat(OrderAnalytics.unitsBySku(onlyNull)).isEmpty();
    }
}
'''},
            ["Write one private helper that returns `Stream<LineItem>` and reuse it everywhere.", "In the best-seller tie-break the *reversed* key comparator makes `max` pick the alphabetically first key."],
            ["A single reusable flatMap helper", "Null item lists handled once, in the helper", "Primitive streams for numeric sums"],
            constraints=["No explicit loops; `flatMap` must be used to flatten", "Do not edit the tests"],
        ),
        task(
            "parallel-safe-note", "Parallel Safety Note (Documentation + Sequential Implementation)", "Challenge", "ParallelSafety",
            "Parallel streams are a judgment call. Implement sequential versions of simple numeric pipelines, a decision helper that encodes the safety checklist, and **write the cautions as documentation**: the `parallelCautions()` method must return a list of guidance sentences, and the tests assert that the key ideas (associative, stateless, side effects, common pool, blocking, measure) appear. **Challenge (requires research):** be precise - each sentence must say *why*.",
            [
                "`sumOfSquares(values)` computes the sum of squares as a `long` **sequentially** (no `parallel()`), without `int` overflow",
                "`squaresInOrder(values)` returns the squares in encounter order (sequential `map`, `toList`)",
                "`isSafeToParallelize(stateless, associative, splittable, elementCount, blocking)` returns `true` only when the work is stateless AND associative AND the source is splittable AND it is not blocking AND `elementCount >= 10_000`",
                "`parallelCautions()` returns at least 5 non-trivial sentences (each longer than 40 characters) that together mention: `associative`, `stateless`, `side effect`, `common pool`, `blocking`, and `measure` (case-insensitive)",
            ],
            ["empty input to the numeric methods", "boundary at exactly 10_000 elements", "`int` overflow (`46341 * 46341`)", "documentation sentences must be meaningful, not keyword stuffing"],
            {"ParallelSafety.java": r'''package @PKG@;

import java.util.List;

/**
 * Sequential implementations plus documented guidance about parallel streams.
 * Everything here is sequential on purpose: the per-element work is trivial and the lists are small.
 */
public final class ParallelSafety {

    private ParallelSafety() {
    }

    public static long sumOfSquares(List<Integer> values) {
        //@TODO sumOfSquares | sequential stream: mapToLong(v -> (long) v * v).sum(); do NOT call parallel()
        return values.stream().mapToLong(v -> (long) v * v).sum();
        //@END
    }

    public static List<Integer> squaresInOrder(List<Integer> values) {
        //@TODO squaresInOrder | sequential map to v * v preserving encounter order, then toList()
        return values.stream().map(v -> v * v).toList();
        //@END
    }

    public static boolean isSafeToParallelize(boolean stateless, boolean associative, boolean splittable,
                                              long elementCount, boolean blocking) {
        //@TODO isSafeToParallelize | true only if stateless && associative && splittable && !blocking && elementCount >= 10_000
        return stateless && associative && splittable && !blocking && elementCount >= 10_000;
        //@END
    }

    public static List<String> parallelCautions() {
        //@TODO parallelCautions | return >= 5 sentences (each > 40 chars) explaining WHY: associative reductions, stateless lambdas, side effects on shared state, the common pool, blocking work, and measuring first
        return List.of(
                "Reductions must be associative with a true identity, otherwise partial results combine differently on every run.",
                "Lambdas must be stateless and non-interfering because chunks run concurrently on different threads.",
                "Avoid any side effect on shared mutable state (such as adding to an ArrayList) since it is not thread-safe and causes lost updates.",
                "All parallel streams share the JVM-wide common pool, so one slow task can starve unrelated parallel work.",
                "Never put blocking I/O or locks inside a parallel stream; it ties up common pool threads and can deadlock or stall.",
                "Always measure with a proper benchmark first; splitting and merging overhead often makes small or cheap workloads slower.");
        //@END
    }
}
'''},
            {"ParallelSafetyTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Locale;
import org.junit.jupiter.api.Test;

class ParallelSafetyTest {

    @Test
    void r1_sumOfSquaresDoesNotOverflow() {
        assertThat(ParallelSafety.sumOfSquares(List.of(1, 2, 3))).isEqualTo(14L);
        assertThat(ParallelSafety.sumOfSquares(List.of(46_341))).isEqualTo(2_147_488_281L);
        assertThat(ParallelSafety.sumOfSquares(List.of())).isZero();
        assertThat(ParallelSafety.sumOfSquares(List.of(-3, 3))).isEqualTo(18L);
    }

    @Test
    void r2_squaresInOrder() {
        assertThat(ParallelSafety.squaresInOrder(List.of(3, -1, 2))).containsExactly(9, 1, 4);
        assertThat(ParallelSafety.squaresInOrder(List.of())).isEmpty();
    }

    @Test
    void r3_decisionHelper() {
        assertThat(ParallelSafety.isSafeToParallelize(true, true, true, 10_000, false)).isTrue();
        assertThat(ParallelSafety.isSafeToParallelize(true, true, true, 9_999, false)).isFalse();
        assertThat(ParallelSafety.isSafeToParallelize(false, true, true, 1_000_000, false)).isFalse();
        assertThat(ParallelSafety.isSafeToParallelize(true, false, true, 1_000_000, false)).isFalse();
        assertThat(ParallelSafety.isSafeToParallelize(true, true, false, 1_000_000, false)).isFalse();
        assertThat(ParallelSafety.isSafeToParallelize(true, true, true, 1_000_000, true)).isFalse();
    }

    @Test
    void r4_cautionsAreSubstantive() {
        List<String> cautions = ParallelSafety.parallelCautions();
        assertThat(cautions).hasSizeGreaterThanOrEqualTo(5);
        assertThat(cautions).allSatisfy(c -> assertThat(c.length()).isGreaterThan(40));
        assertThat(cautions).doesNotHaveDuplicates();
    }

    @Test
    void r4_cautionsCoverTheKeyIdeas() {
        String all = String.join(" ", ParallelSafety.parallelCautions()).toLowerCase(Locale.ROOT);
        assertThat(all).contains("associative", "stateless", "side effect", "common pool", "blocking", "measure");
    }
}
'''},
            ["Cast to `long` **before** multiplying: `(long) v * v`.", "The goal of the documentation task is not keyword stuffing: a reviewer will read each sentence and ask \"is the reason correct?\"."],
            ["No `parallel()`/`parallelStream()` in the implementations", "Each caution states a reason, not just a rule", "Decision helper expresses the checklist exactly"],
            constraints=["Sequential implementations only - do not call `parallel()` or `parallelStream()`", "Do not edit the tests"],
        ),
    ],
)
