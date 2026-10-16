# Task 2 — Partitioning Data

**Day:** 18 · **Task ID:** Day18-task02 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Use `partitioningBy` for two-way splits and its downstream collectors. The tests highlight the key property: both `true` and `false` entries exist even when a bucket is empty.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day18/task02/PartitionEven.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day18/task02/PartitionEvenTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 18 theory file read

## What you will implement

1. `partitionEven(numbers)` returns `Map<Boolean, List<Integer>>` with evens under `true` and odds under `false` (input order kept)
2. `partition(items, predicate)` is the generic version for any element type and predicate
3. `countPassFail(scores, passMark)` returns the number of scores `>= passMark` under `true` and `< passMark` under `false` as `Long`
4. `sumEvenOdd(numbers)` returns the sum of evens under `true` and odds under `false`
5. For empty input, **both keys must still be present** with empty/zero results

## Constraints

- Use `Collectors.partitioningBy` for every method
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=PartitionEvenTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **6 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day18-task02)`).

### Run one test class

```bash
mvn -Dtest=PartitionEvenTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `PartitionEven.java` — `partitionEven` | `TODO(Day18-task02)` | partitioningBy(n -> n % 2 == 0): evens under true, odds under false |
| `PartitionEven.java` — `partition` | `TODO(Day18-task02)` | generic partitioningBy(predicate) |
| `PartitionEven.java` — `countPassFail` | `TODO(Day18-task02)` | partitioningBy(score >= passMark, counting()) |
| `PartitionEven.java` — `sumEvenOdd` | `TODO(Day18-task02)` | partitioningBy(even, summingInt(Integer::intValue)) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_partitionEven` |
| 2 | `r2_genericPartition` |
| 3 | `r3_countPassFail`, `r3_countPassFailEmptyHasZeroes` |
| 4 | `r4_sumEvenOdd` |
| 5 | `r5_bothKeysAlwaysPresent` |

## Edge cases to handle

- empty input
- all even / all odd
- negative odd numbers
- pass mark boundary (equal passes)

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 18: Partitioning Data`

## Hints (optional)

<details><summary>Hint 1</summary>

`partitioningBy(p, downstream)` applies the downstream collector to each side - even an empty one (which is why `counting()` yields `0`).

</details>

<details><summary>Hint 2</summary>

Boxed `Long`/`Integer` values: use `isEqualTo(3L)` for `Long`.

</details>
