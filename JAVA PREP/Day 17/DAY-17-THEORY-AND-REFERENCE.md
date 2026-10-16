# Day 17 — Streams I: Pipelines, filter/map/reduce, and Collectors

**Phase:** Core Java  
**Primary theme:** Process data declaratively with the Stream API: sources, lazy intermediate operations, terminal operations, reduction, and collectors.  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-stream-filter-map`, `task-02-reduce-sum`, `task-03-collectors-tolist`, `task-04-challenge-word-count`  
**Instruction alignment:** Maps to the Day 17 entry of the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21 (no Spring today)

## Overview

A **stream** is a lazily evaluated *pipeline* over a data source (a collection, array, file lines, generator). You describe **what** to compute - filter these, transform those, group the rest - and the library decides how to iterate. Streams do not store data and never modify their source.

Streams are everywhere in modern Java backends: mapping entities to DTOs, filtering orders, summarizing reports, aggregating metrics. Interviews ask: *intermediate vs terminal operations*, *why are streams lazy*, *map vs flatMap*, *reduce signature*, *Collectors.toMap pitfalls*, *can you reuse a stream* (no: `IllegalStateException: stream has already been operated upon or closed`). Today covers the core pipeline and collectors; Day 18 adds grouping, partitioning, flatMap, primitive specializations and parallel streams.

## Day roadmap

1. The stream pipeline: sources, intermediate and terminal operations, laziness
2. Mapping, filtering, and reduction (including primitive streams)
3. Collectors: toList, toSet, toMap, joining, counting
4. Interview angles
5. Common mistakes & debugging
6. Further reading, glossary, answers

### The stream pipeline: sources, intermediate and terminal operations, laziness

#### What it is

A pipeline has three parts: a **source** (`list.stream()`, `Stream.of(...)`, `Arrays.stream(arr)`, `IntStream.range`, `Files.lines`, `Stream.iterate/generate`), zero or more **intermediate operations** that return a new stream (`filter`, `map`, `distinct`, `sorted`, `limit`, `skip`, `peek`), and exactly one **terminal operation** (`collect`, `forEach`, `reduce`, `count`, `findFirst`, `anyMatch`, `toList`, `min`/`max`). Intermediate operations are **lazy** - nothing runs until the terminal operation starts. Elements flow through the whole pipeline **one at a time** (vertical processing), not stage by stage, which enables **short-circuiting** (`limit`, `findFirst`, `anyMatch`).

#### Why it exists / why it matters

Laziness lets the library fuse stages into one pass, avoid intermediate collections, and stop early on infinite or huge sources (`Stream.iterate(1, x -> x * 2).limit(10)`). The declarative style reduces loop/index bookkeeping and makes transformations composable and testable. It also sets the rules you must respect: lambdas should be **non-interfering** and (preferably) **stateless**.

#### Pros and cons

**Pros**

- Readable, composable data transformations
- Single pass with short-circuiting and no intermediate collections
- Works uniformly for collections, arrays, files, generators
- Easy to switch to a parallel pipeline later (with care - Day 18)

**Cons / tradeoffs**

- A stream can be consumed only once
- Debugging is harder (stack traces through the library, lazy evaluation)
- Not always clearer or faster than a simple loop; checked exceptions do not fit lambdas

#### What happens without it / when misused

Forgetting the terminal operation means **nothing happens** (`list.stream().peek(System.out::println);` prints nothing). Reusing a stream throws `IllegalStateException`. Modifying the source collection while the pipeline runs gives `ConcurrentModificationException` or undefined behavior (interference). Side effects in `map`/`filter` (incrementing a shared counter, adding to an outside list) work sequentially but break or race in parallel and make code hard to reason about. `Stream.iterate(...)` without `limit` loops forever / runs out of memory.

#### Syntax and rules

- Create: `collection.stream()`, `Stream.of(a, b)`, `Arrays.stream(arr)`, `IntStream.rangeClosed(1, n)`, `Stream.iterate(seed, hasNext, next)`, `Stream.generate(supplier)`.
- Intermediate (lazy): `filter(Predicate)`, `map(Function)`, `mapToInt`, `distinct()`, `sorted()`, `sorted(Comparator)`, `limit(n)`, `skip(n)`, `peek(Consumer)` (debugging only).
- Terminal (eager): `forEach`, `collect`, `toList()` (Java 16, unmodifiable), `reduce`, `count`, `min/max(Comparator)`, `findFirst/findAny`, `anyMatch/allMatch/noneMatch`, `toArray`.
- `sorted()` and `distinct()` are **stateful** (buffer elements); `limit` short-circuits.
- A stream **cannot be reused**; store the `Supplier<Stream<T>>` if you need to create it repeatedly.
- Order: for ordered sources (`List`), encounter order is preserved unless you call `unordered()`.

#### Examples

**Example 1.1 — Tiny — a first pipeline**

```java
List<String> names = List.of("ann", "bob", "cy", "dave");
List<String> result = names.stream()
        .filter(n -> n.length() > 2)
        .map(String::toUpperCase)
        .sorted(Comparator.reverseOrder())
        .toList();
System.out.println(result);   // [DAVE, BOB, ANN]
```

**Example 1.2 — Tiny — laziness and vertical processing**

```java
List<String> log = new ArrayList<>();
Optional<String> first = Stream.of("a", "bb", "cc")
        .filter(s -> { log.add("filter:" + s); return s.length() > 1; })
        .map(s -> { log.add("map:" + s); return s.toUpperCase(); })
        .findFirst();
System.out.println(first.get());  // BB
System.out.println(log);          // [filter:a, filter:bb, map:bb]   <- "cc" was never touched
```

**Example 1.3 — Medium — pagination and the one-shot stream rule**

```java
import java.util.*;
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
}
```

#### Quick checks

1. What prints: `Stream.of(1,2,3).peek(System.out::println);`?
2. Why does `findFirst` after `filter` not examine every element?
3. Name two stateful intermediate operations.
4. How do you obtain a stream you can "reuse"?

### Mapping, filtering, and reduction (including primitive streams)

#### What it is

`map(Function)` transforms each element one-to-one; `filter(Predicate)` keeps the matching ones. **Reduction** folds a stream into a single result: `reduce(identity, accumulator)`, `reduce(accumulator)` returning `Optional`, and the three-argument form for different result types. The accumulator must be **associative** and the identity a true identity (`0` for +, `1` for *) so that results are correct under parallel evaluation. For numbers prefer **primitive streams** (`IntStream`, `LongStream`, `DoubleStream`) via `mapToInt` etc.: they avoid boxing and offer `sum()`, `average()`, `max()`, `summaryStatistics()`.

#### Why it exists / why it matters

Most reports are reductions: totals, counts, min/max, averages. Using `mapToInt(...).sum()` is both clearer and faster than boxing into `Stream<Integer>` and reducing. Understanding identity/associativity is the key to correct `reduce` use and to later parallelism.

#### Pros and cons

**Pros**

- `mapToInt().sum()/average()/summaryStatistics()` are concise and unboxed
- `reduce` expresses any fold generically
- `Optional` results force handling of empty input
- Same code works sequentially or in parallel if the reduction is associative

**Cons / tradeoffs**

- `reduce` with a non-associative or non-identity function gives wrong results in parallel
- Boxing overhead for `Stream<Integer>`
- `reduce` to build collections is wrong (mutable reduction needs `collect`)

#### What happens without it / when misused

`stream.reduce(0, (a, b) -> a - b)` is not associative, so parallel results differ from sequential ones. `reduce(1, Integer::sum)` (wrong identity) adds an extra 1 once per parallel segment. Calling `max(...)` or `reduce(op)` on an empty stream returns an empty `Optional` - calling `.get()` throws `NoSuchElementException`. `average()` of an empty `IntStream` is `OptionalDouble.empty()`, not 0. `IntStream.sum()` overflows silently on `int` (use `mapToLong`). Using `reduce(new ArrayList<>(), ...)` to build lists mutates a shared identity: use `collect`.

#### Syntax and rules

- `T reduce(T identity, BinaryOperator<T> acc)`; `Optional<T> reduce(BinaryOperator<T> acc)`; `<U> U reduce(U identity, BiFunction<U,? super T,U> acc, BinaryOperator<U> combiner)`.
- Convenience: `count()`, `min(Comparator)`, `max(Comparator)`, `IntStream.sum/min/max/average`.
- `mapToInt(Integer::intValue)`, `mapToObj`, `boxed()`, `asLongStream()` convert between stream kinds.
- `IntSummaryStatistics s = ints.summaryStatistics();` gives count, sum, min, max, average in one pass.
- Identity laws: `identity op x == x`; associativity: `(a op b) op c == a op (b op c)`.

#### Examples

**Example 2.1 — Tiny — three reductions**

```java
List<Integer> xs = List.of(3, 1, 4, 1, 5);
int sum = xs.stream().reduce(0, Integer::sum);                 // 14
Optional<Integer> max = xs.stream().reduce(Integer::max);       // Optional[5]
long product = xs.stream().mapToLong(Integer::longValue).reduce(1L, (a, b) -> a * b); // 60
System.out.println(sum + " " + max.get() + " " + product);
```

**Example 2.2 — Tiny — primitive streams and statistics**

```java
IntSummaryStatistics st = List.of(3, 1, 4, 1, 5).stream().mapToInt(Integer::intValue).summaryStatistics();
System.out.println(st.getMin() + " " + st.getMax() + " " + st.getAverage() + " " + st.getCount());
// 1 5 2.8 5
System.out.println(IntStream.empty().average());   // OptionalDouble.empty
```

**Example 2.3 — Medium — longest word keeps the first on ties, and a wrong reduce**

```java
List<String> words = List.of("kiwi", "pear", "banana", "melon", "cherry");
Optional<String> longest = words.stream().reduce((a, b) -> b.length() > a.length() ? b : a);
System.out.println(longest.orElse("-"));           // banana (first of the two 6-letter words)

// BUG: subtraction is not associative; parallel() would give a different answer
int bad = Stream.of(10, 3, 2).parallel().reduce(0, (a, b) -> a - b);
// sequential: ((0-10)-3)-2 = -15, parallel may produce a different value
```

#### Quick checks

1. Why must the `reduce` identity be a true identity?
2. What does `IntStream.empty().average()` return?
3. Why prefer `mapToInt(...).sum()` over `map(...).reduce(0, Integer::sum)`?
4. Is `reduce("", String::concat)` a good way to join strings?

### Collectors: toList, toSet, toMap, joining, counting

#### What it is

`stream.collect(Collector)` is a **mutable reduction**: it accumulates elements into a container (a list, map, string builder). `java.util.stream.Collectors` provides ready-made collectors: `toList()`, `toSet()`, `toCollection(TreeSet::new)`, `toMap(keyFn, valueFn[, mergeFn[, mapSupplier]])`, `joining(delimiter, prefix, suffix)`, `counting()`, `summingInt`, `averagingDouble`, `mapping`, `collectingAndThen(downstream, finisher)`, and the unmodifiable variants `toUnmodifiableList/Set/Map` (Java 10). `Stream.toList()` (Java 16) is a shortcut returning an unmodifiable list that **permits nulls**.

#### Why it exists / why it matters

Collectors turn pipelines into the shapes services need: DTO lists, lookup maps, CSV strings, counts per key (Day 18 adds `groupingBy`). Choosing the correct collector (and map supplier) controls ordering, duplicate handling, and mutability of results.

#### Pros and cons

**Pros**

- Concise, well-tested building blocks
- Control over result type (`TreeMap::new`, `LinkedHashMap::new`)
- Composable via downstream collectors and `collectingAndThen`
- `joining` builds strings efficiently with a `StringBuilder`

**Cons / tradeoffs**

- `toMap` throws on duplicate keys unless a merge function is supplied
- `toMap` rejects null values (`NullPointerException`)
- `Collectors.toList()` makes **no guarantee** about the returned list's mutability or type

#### What happens without it / when misused

`Stream.of("a","b","a").collect(Collectors.toMap(s -> s, String::length))` throws `IllegalStateException: Duplicate key a (attempted merging values 1 and 1)`. A null value in `toMap` throws `NullPointerException` from `HashMap.merge`. Relying on `Collectors.toList()` returning a mutable `ArrayList` is an unwritten assumption; use `toCollection(ArrayList::new)` if you need that. `Stream.toList()` returns an unmodifiable list: `add` throws `UnsupportedOperationException`. `joining` on a `Stream<Integer>` does not compile - map to `String` first.

#### Syntax and rules

- `collect(Collectors.toList())`, `toSet()`, `toCollection(LinkedHashSet::new)`.
- `toMap(k, v)`; with duplicates `toMap(k, v, (a, b) -> a)`; choose map type `toMap(k, v, merge, LinkedHashMap::new)`.
- `joining()`, `joining(", ")`, `joining(", ", "[", "]")` (elements must be `CharSequence`).
- `counting()` returns `Long`; `summingInt(ToIntFunction)`; `averagingInt`; `mapping(f, downstream)`.
- `collectingAndThen(Collectors.toList(), Collections::unmodifiableList)` post-processes the result.
- `Stream.toList()` unmodifiable, nulls allowed; `Collectors.toUnmodifiableList()` rejects nulls.

#### Examples

**Example 3.1 — Tiny — joining and toSet**

```java
List<String> words = List.of("b", "a", "b");
System.out.println(words.stream().collect(Collectors.joining(", ", "[", "]")));   // [b, a, b]
System.out.println(words.stream().collect(Collectors.toCollection(TreeSet::new))); // [a, b]
```

**Example 3.2 — Tiny — toMap with merge function and map supplier**

```java
Map<String, Integer> m = Stream.of("kiwi", "fig", "kiwi")
        .collect(Collectors.toMap(w -> w, String::length, (first, second) -> first, LinkedHashMap::new));
System.out.println(m);   // {kiwi=4, fig=3}
```

**Example 3.3 — Medium — word count with collectors**

```java
import java.util.*;
import java.util.function.Function;
import java.util.stream.*;

public class WordCountDemo {
    static Map<String, Long> count(String text) {
        return Arrays.stream(text.toLowerCase().split("[^\p{L}]+"))
                .filter(w -> !w.isEmpty())
                .collect(Collectors.groupingBy(Function.identity(), TreeMap::new, Collectors.counting()));
    }

    public static void main(String[] args) {
        System.out.println(count("The cat and the hat. The END!"));
        // {and=1, cat=1, end=1, hat=1, the=3}
    }
}
```

#### Quick checks

1. What happens when `Collectors.toMap` sees a duplicate key and no merge function?
2. Difference between `Stream.toList()` and `Collectors.toList()`?
3. How do you get a `LinkedHashMap` out of `toMap`?
4. Why does `Stream<Integer>.collect(Collectors.joining(","))` not compile?

## Interview angles

**Q: Intermediate vs terminal operations?**

Intermediate operations return a stream and are lazy; a terminal operation triggers execution and produces a result or side effect. A stream is consumed by exactly one terminal operation.

**Q: map vs flatMap?**

`map` is one-to-one; `flatMap` maps each element to a stream and flattens (one-to-many). See Day 18.

**Q: What is short-circuiting?**

Operations such as `limit`, `findFirst`, `anyMatch` can finish before consuming the whole source, which also makes infinite streams usable.

**Q: Is it safe to modify a list inside `forEach` over its own stream?**

No - interference; it can throw `ConcurrentModificationException` or yield undefined results.

**Q: When would you not use a stream?**

Complex control flow with early exits and checked exceptions, tight inner loops with primitive math where clarity or performance suffers, or when debugging needs step-through of mutable state.

**Q: What are the pitfalls of `Collectors.toMap`?**

Duplicate keys throw `IllegalStateException`; null values throw `NullPointerException`; the map implementation is unspecified unless you pass a supplier.

## Common mistakes & debugging

- No terminal operation - the pipeline silently does nothing.
- Reusing a stream (`IllegalStateException: stream has already been operated upon or closed`).
- Using `forEach` with an external mutable list/counter instead of `collect`/`reduce`.
- Calling `Optional.get()` on `findFirst()`/`max()` of possibly empty streams.
- `toMap` without a merge function on data that may contain duplicates.
- Wrong `reduce` identity or non-associative accumulator.

## Further reading

- Javadoc: `java.util.stream` package summary (see *Non-interference*, *Stateless behaviors*, *Reduction*, *Associativity*)
- Oracle Java Tutorials - *Aggregate Operations* (Lesson)
- Javadoc: `java.util.stream.Collectors`, `Stream`, `IntStream`
- *Effective Java* (Bloch) items 42-48 (lambdas and streams)

## Glossary

| Term | Meaning |
|------|---------|
| Pipeline | Source + intermediate operations + terminal operation |
| Lazy | Intermediate operations do no work until a terminal operation runs |
| Short-circuit | Terminal/intermediate operation that may stop before consuming all input |
| Stateful operation | Needs to see multiple elements (`sorted`, `distinct`) |
| Mutable reduction | Accumulating into a container via `collect` |
| Associative | `(a op b) op c == a op (b op c)`; required for correct reductions |
| Interference | Modifying the stream source during execution |
| Collector | Strategy describing supplier, accumulator, combiner, finisher |

## Answers

Answers to every **Quick check** above (numbered `section.question`).

- **1.1** — What prints: `Stream.of(1,2,3).peek(System.out::println);`?  
  Nothing - there is no terminal operation, so the pipeline never executes.

- **1.2** — Why does `findFirst` after `filter` not examine every element?  
  Streams are lazy and process element-by-element; `findFirst` short-circuits as soon as one element passes.

- **1.3** — Name two stateful intermediate operations.  
  `sorted` and `distinct` (they must buffer elements).

- **1.4** — How do you obtain a stream you can "reuse"?  
  You cannot reuse one; create a new stream from the source each time, e.g. via a `Supplier<Stream<T>>`.

- **2.1** — Why must the `reduce` identity be a true identity?  
  Parallel evaluation may apply the identity once per segment; a wrong identity (e.g. 1 for sum) is counted several times.

- **2.2** — What does `IntStream.empty().average()` return?  
  `OptionalDouble.empty()` - not `0`.

- **2.3** — Why prefer `mapToInt(...).sum()` over `map(...).reduce(0, Integer::sum)`?  
  It avoids boxing and expresses intent; it also cannot be mis-specified with a wrong identity.

- **2.4** — Is `reduce("", String::concat)` a good way to join strings?  
  It works but is O(n^2) in copying; prefer `Collectors.joining`.

- **3.1** — What happens when `Collectors.toMap` sees a duplicate key and no merge function?  
  `IllegalStateException: Duplicate key ...`.

- **3.2** — Difference between `Stream.toList()` and `Collectors.toList()`?  
  `Stream.toList()` returns an unmodifiable list and allows nulls; `Collectors.toList()` returns an unspecified (in practice mutable `ArrayList`) list.

- **3.3** — How do you get a `LinkedHashMap` out of `toMap`?  
  Use the four-argument overload and pass `LinkedHashMap::new` as the map supplier.

- **3.4** — Why does `Stream<Integer>.collect(Collectors.joining(","))` not compile?  
  `joining` requires `CharSequence` elements; map them with `String::valueOf` first.
