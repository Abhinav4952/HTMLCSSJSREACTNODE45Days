# Day 18 — Streams II: groupingBy, partitioningBy, flatMap, Primitive Streams, and Parallel Cautions

**Phase:** Core Java  
**Primary theme:** Aggregate and reshape data with advanced collectors, flatten nested structures, and decide when parallel streams are (not) appropriate.  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-group-by-dept`, `task-02-partition-even`, `task-03-flatmap-orders`, `task-04-parallel-safe-note`  
**Instruction alignment:** Maps to the Day 18 entry of the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21 (no Spring today)

## Overview

Day 17 taught the pipeline; today you learn the collectors that power reporting code and the operations that reshape data. `groupingBy` is the SQL `GROUP BY` of Java, `partitioningBy` is a two-bucket split, `flatMap` turns *a stream of collections* into *a stream of elements*, and primitive streams make numeric code fast and boxing-free.

Then comes the part interviewers love: **parallel streams**. `parallelStream()` looks like a free speed-up but runs on the shared `ForkJoinPool.commonPool()`, requires associative and stateless operations, and often makes small or I/O-bound workloads slower. Knowing *when not to* is the senior-level answer.

## Day roadmap

1. groupingBy and partitioningBy with downstream collectors
2. flatMap and primitive streams
3. Parallel streams: cautions and when not to use them
4. Interview angles
5. Common mistakes & debugging
6. Further reading, glossary, answers

### groupingBy and partitioningBy with downstream collectors

#### What it is

`Collectors.groupingBy(classifier)` builds a `Map<K, List<T>>` where each element is placed under the key its classifier returns. The overloads add a **map factory** (`TreeMap::new`) and a **downstream collector** that reduces each group: `counting()`, `summingInt/Double`, `averagingX`, `mapping(f, downstream)`, `maxBy/minBy(comparator)`, `toSet()`, `collectingAndThen(downstream, finisher)`, `reducing`, `teeing` (Java 12). `partitioningBy(predicate[, downstream])` is a special grouping with exactly two keys, `true` and `false`.

#### Why it exists / why it matters

Reports and dashboards are almost all grouping: orders per customer, revenue per month, employees per department. Doing it with one collector replaces nested loops with `computeIfAbsent`. `partitioningBy` is the right tool for pass/fail, valid/invalid, even/odd splits because it **always contains both keys**, even if one bucket is empty.

#### Pros and cons

**Pros**

- One declarative expression for GROUP BY style aggregations
- Downstream collectors compose to any depth (group by dept then by city)
- Choosable map implementation for deterministic ordering
- `partitioningBy` guarantees both `true` and `false` entries

**Cons / tradeoffs**

- The default `groupingBy` map is a `HashMap` (unordered, not specified) - wrong for stable output
- `maxBy`/`minBy` yield `Optional` values that you must unwrap or finish with `collectingAndThen`
- Deeply nested collectors become hard to read - extract helper methods

#### What happens without it / when misused

Asserting on `groupingBy` output ordering without `TreeMap::new` yields flaky tests. `groupingBy(f)` with a classifier returning `null` throws `NullPointerException: element cannot be mapped to a null key`. Using `toMap` where several rows share a key throws `IllegalStateException` (grouping would have been correct). Forgetting that `groupingBy` omits keys with no elements while `partitioningBy` always has two keys causes `NullPointerException` when you unbox `map.get(false)` for an empty partition under `groupingBy`. `averagingInt` on an empty group never occurs, but `maxBy` per group is `Optional` - calling `get()` blindly is a smell.

#### Syntax and rules

- `groupingBy(f)` -> `Map<K, List<T>>`; `groupingBy(f, downstream)`; `groupingBy(f, TreeMap::new, downstream)`.
- Downstream: `counting()` -> `Long`; `summingInt(ToIntFunction)` -> `Integer`; `averagingDouble(ToDoubleFunction)` -> `Double`; `mapping(Function, downstream)`; `maxBy(Comparator)` -> `Optional<T>`.
- Unwrap: `collectingAndThen(maxBy(cmp), o -> o.orElseThrow().name())`.
- `partitioningBy(p)` -> `Map<Boolean, List<T>>`; `partitioningBy(p, downstream)`.
- Multi-level: `groupingBy(Emp::dept, groupingBy(Emp::city, counting()))`.
- `Collectors.teeing(c1, c2, merger)` computes two results in one pass.

#### Examples

**Example 1.1 — Tiny — group and count**

```java
record Emp(String name, String dept, double salary) {}
List<Emp> emps = List.of(new Emp("a", "ENG", 100), new Emp("b", "HR", 80), new Emp("c", "ENG", 120));
Map<String, Long> headcount = emps.stream()
        .collect(Collectors.groupingBy(Emp::dept, TreeMap::new, Collectors.counting()));
System.out.println(headcount);   // {ENG=2, HR=1}
```

**Example 1.2 — Tiny — partitioningBy always has both keys**

```java
Map<Boolean, List<Integer>> parts = Stream.of(1, 3, 5).collect(Collectors.partitioningBy(n -> n % 2 == 0));
System.out.println(parts);               // {false=[1, 3, 5], true=[]}
Map<Integer, List<Integer>> groups = Stream.of(1, 3, 5).collect(Collectors.groupingBy(n -> n % 2));
System.out.println(groups);              // {1=[1, 3, 5]}  <- no key 0 at all
```

**Example 1.3 — Medium — a small report with downstream collectors**

```java
import java.util.*;
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
}
```

#### Quick checks

1. What is the type of `groupingBy(f, counting())` values and why does it matter?
2. How do you make `groupingBy` return sorted keys?
3. Difference between `groupingBy(p)` and `partitioningBy(p)`?
4. How do you get a plain value instead of `Optional` from `maxBy` per group?

### flatMap and primitive streams

#### What it is

`flatMap(Function<T, Stream<R>>)` replaces each element with a *stream* of results and concatenates them: `Stream<List<Item>>` becomes `Stream<Item>`; `Stream<String>` of sentences becomes a `Stream<String>` of words. Variants: `flatMapToInt`, `flatMapToDouble`, `mapMulti` (Java 16). **Primitive streams** (`IntStream`, `LongStream`, `DoubleStream`) hold unboxed values with `sum`, `average`, `range(a, b)` (exclusive), `rangeClosed`, `boxed()`, `mapToObj`, `asLongStream`, and `summaryStatistics`.

#### Why it exists / why it matters

Real data is nested: orders have line items, users have roles, documents have paragraphs. `flatMap` is the stream equivalent of nested loops and the way to "explode" a collection into rows. Primitive streams avoid millions of `Integer` allocations in numeric code and provide the right aggregate operations.

#### Pros and cons

**Pros**

- Flatten nested structures declaratively
- Handle missing inner collections gracefully with `Stream.ofNullable` / empty streams
- Unboxed numeric pipelines are faster and more memory efficient
- `IntStream.range` replaces most index loops

**Cons / tradeoffs**

- Easy to confuse `map` (one-to-one) and `flatMap` (one-to-many); `map(List::stream)` gives `Stream<Stream<T>>`
- A `null` returned from the flatMap function throws `NullPointerException` (return `Stream.empty()`)
- Conversions between boxed and primitive streams add noise

#### What happens without it / when misused

Using `map(Order::items)` then trying to sum item quantities fails because you are still iterating lists, not items. Returning `null` from the flatMap mapper when an order has no items throws NPE; return `Stream.empty()`. `IntStream.range(0, n)` is end-exclusive: using it where you meant `rangeClosed` is an off-by-one bug. `int` overflow in `IntStream.sum()` is silent (use `mapToLong`). `Arrays.stream(int[])` gives an `IntStream` but `Arrays.asList(int[])` gives a `List<int[]>` with one element - a famous trap.

#### Syntax and rules

- `Stream<R> flatMap(Function<? super T, ? extends Stream<? extends R>> mapper)`.
- Guard nulls: `o.items() == null ? Stream.empty() : o.items().stream()` or `Stream.ofNullable(...)` (single element).
- `IntStream.range(0, 5)` -> 0..4; `rangeClosed(1, 5)` -> 1..5.
- `boxed()` -> `Stream<Integer>`; `mapToObj(i -> ...)`; `mapToInt(Integer::intValue)`; `asDoubleStream()`.
- `mapMulti((x, sink) -> { sink.accept(a); sink.accept(b); })` - imperative alternative when emitting few items.
- `IntStream.iterate(1, i -> i * 2).limit(10)` / `takeWhile` / `dropWhile` for ordered streams.

#### Examples

**Example 2.1 — Tiny — words from sentences**

```java
List<String> sentences = List.of("to be", "or not");
List<String> words = sentences.stream()
        .flatMap(s -> Arrays.stream(s.split(" ")))
        .toList();
System.out.println(words);   // [to, be, or, not]
```

**Example 2.2 — Tiny — primitive ranges**

```java
System.out.println(IntStream.range(0, 5).sum());          // 10
System.out.println(IntStream.rangeClosed(1, 5).sum());    // 15
System.out.println(IntStream.rangeClosed(1, 5).mapToObj(Integer::toString).collect(Collectors.joining("-"))); // 1-2-3-4-5
int[] arr = {3, 1, 2};
System.out.println(Arrays.stream(arr).max().getAsInt());  // 3
```

**Example 2.3 — Medium — order lines: total units, revenue, units per SKU**

```java
import java.util.*;
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
}
```

#### Quick checks

1. What is the type of `orders.stream().map(Order::items)` and how do you get the items themselves?
2. What does `IntStream.range(0, 3)` produce?
3. Why does `Arrays.asList(new int[]{1,2,3})` have size 1?
4. What should the flatMap mapper return for "no children"?

### Parallel streams: cautions and when not to use them

#### What it is

`collection.parallelStream()` or `stream.parallel()` splits the source into chunks (via a `Spliterator`), processes them on the **common ForkJoinPool** (default parallelism = cores - 1, shared by the whole JVM), and merges partial results. It is a *performance* feature, not a correctness feature: for sequential pipelines results are deterministic; for parallel pipelines you must ensure the operations are **stateless**, **non-interfering**, and that reductions are **associative** with a true identity. `forEachOrdered` preserves encounter order at a cost; `forEach` does not.

#### Why it exists / why it matters

CPU-bound, large (tens of thousands of elements or heavy per-element work), easily splittable sources (arrays, `ArrayList`, ranges) can scale. But overhead (splitting, merging, thread handoff), contention on shared mutable state, ordered/stateful operations, boxing, and blocking I/O inside the common pool often make parallel streams slower - or break the whole application because every parallel stream shares the same pool.

#### Pros and cons

**Pros**

- Can speed up large CPU-bound data-parallel work with one method call
- Same pipeline code as sequential (`stream()` vs `parallelStream()`)
- Fork/join framework handles splitting and merging
- `ArrayList`/arrays/ranges split efficiently

**Cons / tradeoffs**

- Overhead usually dominates for small or cheap workloads
- Shared mutable state, non-associative reductions, and side effects produce wrong or nondeterministic results
- The shared common pool means one blocking task can starve unrelated parallel streams (and `CompletableFuture` async tasks)
- Poor splitting for `LinkedList`, `Stream.iterate`, `BufferedReader.lines`; ordered operations (`limit`, `findFirst`, `sorted`) reduce parallelism

#### What happens without it / when misused

Adding to an `ArrayList` from `parallelStream().forEach(list::add)` corrupts the list (`ArrayIndexOutOfBoundsException`, lost elements, nulls) because `ArrayList` is not thread-safe. A `reduce` with `(a, b) -> a - b` or a wrong identity yields different answers per run. Doing blocking I/O (HTTP, JDBC) in a parallel stream ties up the common pool and degrades unrelated requests. A parallel stream over 20 elements is typically 10-100x slower than sequential. `parallel()` on `Stream.iterate` can *hang or run out of memory* without `limit`. Benchmarks without JMH usually mislead (JIT warm-up, GC).

#### Syntax and rules

- **Checklist before `parallel()`:** large source? splittable source? CPU-bound work? stateless and non-interfering lambdas? associative reduction with real identity? no blocking I/O? measured (JMH) benefit?
- Safe collection: `collect(Collectors.toList())` (thread-confined partial containers merged by the combiner) - never `forEach(list::add)`.
- `reduce(identity, accumulator, combiner)`: accumulator and combiner must agree.
- `unordered()` can improve `distinct`/`limit` performance when order does not matter.
- Custom pool trick (`pool.submit(() -> stream.parallel()...)`) is an implementation detail, not a supported API contract - prefer an explicit `ExecutorService` (Day 21).
- Default recommendation: **start sequential**; only parallelize with evidence.

#### Examples

**Example 3.1 — Tiny — the broken parallel forEach**

```java
List<Integer> out = new ArrayList<>();
IntStream.range(0, 10_000).parallel().forEach(out::add);     // BUG: ArrayList is not thread-safe
System.out.println(out.size());    // usually < 10000, or throws ArrayIndexOutOfBoundsException

List<Integer> ok = IntStream.range(0, 10_000).parallel().boxed().collect(Collectors.toList());
System.out.println(ok.size());     // 10000 - collect is designed for parallelism
```

**Example 3.2 — Tiny — safe vs unsafe reduction**

```java
int sum = IntStream.rangeClosed(1, 1_000).parallel().sum();           // 500500 every time (associative)
int bad = Stream.of(10, 3, 2).parallel().reduce(0, (a, b) -> a - b);     // not associative: result may vary
System.out.println(sum);
```

**Example 3.3 — Medium — a documented, deliberately sequential implementation**

```java
import java.util.*;
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
}
```

#### Quick checks

1. Name three conditions a reduction must satisfy to be safe in parallel.
2. Why can one blocking task in a parallel stream hurt unrelated code?
3. Why is `parallelStream().forEach(list::add)` wrong?
4. Give two situations where parallel streams are almost always a bad idea.

## Interview angles

**Q: groupingBy vs partitioningBy vs toMap?**

`groupingBy` buckets by an arbitrary key and may reduce each bucket downstream; `partitioningBy` is a two-bucket boolean split with both keys always present; `toMap` maps one element to one entry and fails on duplicate keys unless you provide a merge function.

**Q: map vs flatMap?**

`map` transforms one element into one element; `flatMap` transforms one element into a stream and flattens the streams into one.

**Q: Are parallel streams always faster? When would you use them?**

No. Use them for large, CPU-bound, splittable, stateless workloads after measuring; avoid for small data, I/O, or shared mutable state.

**Q: What pool do parallel streams use and what is the risk?**

`ForkJoinPool.commonPool()`; sharing it means one slow/blocking pipeline can starve others.

**Q: How do you compute two aggregates in a single pass?**

`Collectors.teeing(c1, c2, merger)` (Java 12) or a custom collector.

**Q: Why use primitive streams?**

To avoid boxing allocations, and to get `sum`, `average`, `summaryStatistics` directly.

## Common mistakes & debugging

- Unordered `HashMap` results from `groupingBy` asserted in tests (use `TreeMap::new` or order-insensitive assertions).
- Expecting `groupingBy` to include empty groups (use `partitioningBy` for two-way splits).
- Returning `null` instead of `Stream.empty()` from a `flatMap` mapper.
- Mutating shared state from parallel stream lambdas.
- Using `parallelStream()` by reflex for small lists or blocking calls.
- Off-by-one with `range` vs `rangeClosed`.

## Further reading

- Javadoc: `java.util.stream.Collectors` (groupingBy, partitioningBy, teeing), `java.util.stream` package docs (*Parallelism*, *Side-effects*, *Ordering*)
- Brian Goetz, "Parallel Streams: When to use them" guidance and the JDK `Stream` Javadoc NOTEs
- Oracle Java Tutorials - *Parallelism* lesson
- *Effective Java* (Bloch) item 48 (be careful when making streams parallel)

## Glossary

| Term | Meaning |
|------|---------|
| Downstream collector | A collector applied to each group produced by `groupingBy`/`partitioningBy` |
| Partition | A two-way split by a predicate (keys `true` and `false`) |
| Flattening | Merging many inner streams into one (flatMap) |
| Spliterator | Splittable iterator that parallel streams use to divide work |
| Common pool | `ForkJoinPool.commonPool()` shared by all parallel streams in the JVM |
| Associative | Grouping of operands does not change the result |
| Encounter order | The order in which a stream's source defines its elements |

## Answers

Answers to every **Quick check** above (numbered `section.question`).

- **1.1** — What is the type of `groupingBy(f, counting())` values and why does it matter?  
  `Long` - assigning to `Map<K,Integer>` does not compile; convert with `.intValue()` if needed.

- **1.2** — How do you make `groupingBy` return sorted keys?  
  Use the three-argument overload with `TreeMap::new`.

- **1.3** — Difference between `groupingBy(p)` and `partitioningBy(p)`?  
  `partitioningBy` takes a boolean predicate and always has exactly the keys `true` and `false`; `groupingBy` keys come from the data and empty groups are absent.

- **1.4** — How do you get a plain value instead of `Optional` from `maxBy` per group?  
  Wrap it with `collectingAndThen(maxBy(cmp), o -> o.orElseThrow()...)` (the group is never empty).

- **2.1** — What is the type of `orders.stream().map(Order::items)` and how do you get the items themselves?  
  `Stream<List<Line>>`; use `flatMap(o -> o.items().stream())` to get `Stream<Line>`.

- **2.2** — What does `IntStream.range(0, 3)` produce?  
  0, 1, 2 (end exclusive).

- **2.3** — Why does `Arrays.asList(new int[]{1,2,3})` have size 1?  
  `int[]` is a single object, so you get `List<int[]>`; use `Arrays.stream` or `IntStream`.

- **2.4** — What should the flatMap mapper return for "no children"?  
  `Stream.empty()` (never `null`).

- **3.1** — Name three conditions a reduction must satisfy to be safe in parallel.  
  Associative accumulator, a true identity, and stateless/non-interfering lambdas.

- **3.2** — Why can one blocking task in a parallel stream hurt unrelated code?  
  All parallel streams share the common ForkJoinPool; blocked workers cannot serve other tasks.

- **3.3** — Why is `parallelStream().forEach(list::add)` wrong?  
  `ArrayList` is not thread-safe and `forEach` gives no ordering/merging guarantees; use `collect`.

- **3.4** — Give two situations where parallel streams are almost always a bad idea.  
  Small collections / cheap work (overhead dominates) and blocking I/O or `LinkedList`/`iterate` sources.
