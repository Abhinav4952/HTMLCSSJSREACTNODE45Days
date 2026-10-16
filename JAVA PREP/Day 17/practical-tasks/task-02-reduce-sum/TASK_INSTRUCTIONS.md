# Task 2 — Reduce, Sum, and Statistics

**Day:** 17 · **Task ID:** Day17-task02 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Implement reductions over number and string lists with `reduce` and primitive streams: sum, product, max, average, longest string (first wins ties), and summary statistics.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day17/task02/ReduceSum.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day17/task02/ReduceSumTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 17 theory file read

## What you will implement

1. `sum(numbers)` adds all values with `reduce(0, Integer::sum)`; empty list -> 0
2. `product(numbers)` returns the product as a `long` (empty list -> 1)
3. `max(numbers)` returns an `Optional<Integer>`; empty -> empty
4. `average(numbers)` returns an `OptionalDouble` using a primitive stream; empty -> empty
5. `longest(words)` returns the longest word as `Optional`; when several have the same maximum length the **first** wins; `null` words are ignored
6. `stats(numbers)` returns an `IntSummaryStatistics` (count, sum, min, max)
7. `sumLong(numbers)` sums as `long` so large inputs do not overflow `int`

## Constraints

- Do not use loops; no mutable accumulator variables outside the stream
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=ReduceSumTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day17-task02)`).

### Run one test class

```bash
mvn -Dtest=ReduceSumTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `ReduceSum.java` — `sum` | `TODO(Day17-task02)` | reduce with identity 0 and Integer::sum |
| `ReduceSum.java` — `product` | `TODO(Day17-task02)` | multiply as long; identity 1 so an empty list gives 1 |
| `ReduceSum.java` — `max` | `TODO(Day17-task02)` | reduce(Integer::max) without identity so empty input gives Optional.empty() |
| `ReduceSum.java` — `average` | `TODO(Day17-task02)` | mapToInt then average(); empty gives OptionalDouble.empty() |
| `ReduceSum.java` — `longest` | `TODO(Day17-task02)` | ignore nulls; reduce keeping the first word on length ties |
| `ReduceSum.java` — `stats` | `TODO(Day17-task02)` | mapToInt(Integer::intValue).summaryStatistics() |
| `ReduceSum.java` — `sumLong` | `TODO(Day17-task02)` | mapToLong then sum() so that large inputs do not overflow int |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_sum` |
| 2 | `r2_product` |
| 3 | `r3_max` |
| 4 | `r4_average` |
| 5 | `r5_longestKeepsFirstOnTies` |
| 6 | `r6_stats` |
| 7 | `r7_sumLongDoesNotOverflow` |

## Edge cases to handle

- empty list
- negative numbers
- ties for longest
- overflow (`Integer.MAX_VALUE` twice)

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 17: Reduce, Sum, and Statistics`

## Hints (optional)

<details><summary>Hint 1</summary>

`IntStream.average()` returns `OptionalDouble`, not `double`.

</details>

<details><summary>Hint 2</summary>

Use `reduce` without an identity when the empty case must be distinguishable.

</details>
