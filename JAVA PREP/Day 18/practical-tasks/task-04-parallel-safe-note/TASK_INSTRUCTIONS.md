# Task 4 — Parallel Safety Note (Documentation + Sequential Implementation)

**Day:** 18 · **Task ID:** Day18-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Parallel streams are a judgment call. Implement sequential versions of simple numeric pipelines, a decision helper that encodes the safety checklist, and **write the cautions as documentation**: the `parallelCautions()` method must return a list of guidance sentences, and the tests assert that the key ideas (associative, stateless, side effects, common pool, blocking, measure) appear. **Challenge (requires research):** be precise - each sentence must say *why*.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day18/task04/ParallelSafety.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day18/task04/ParallelSafetyTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 18 theory file read

## What you will implement

1. `sumOfSquares(values)` computes the sum of squares as a `long` **sequentially** (no `parallel()`), without `int` overflow
2. `squaresInOrder(values)` returns the squares in encounter order (sequential `map`, `toList`)
3. `isSafeToParallelize(stateless, associative, splittable, elementCount, blocking)` returns `true` only when the work is stateless AND associative AND the source is splittable AND it is not blocking AND `elementCount >= 10_000`
4. `parallelCautions()` returns at least 5 non-trivial sentences (each longer than 40 characters) that together mention: `associative`, `stateless`, `side effect`, `common pool`, `blocking`, and `measure` (case-insensitive)

## Constraints

- Sequential implementations only - do not call `parallel()` or `parallelStream()`
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=ParallelSafetyTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **5 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day18-task04)`).

### Run one test class

```bash
mvn -Dtest=ParallelSafetyTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `ParallelSafety.java` — `sumOfSquares` | `TODO(Day18-task04)` | sequential stream: mapToLong(v -> (long) v * v).sum(); do NOT call parallel() |
| `ParallelSafety.java` — `squaresInOrder` | `TODO(Day18-task04)` | sequential map to v * v preserving encounter order, then toList() |
| `ParallelSafety.java` — `isSafeToParallelize` | `TODO(Day18-task04)` | true only if stateless && associative && splittable && !blocking && elementCount >= 10_000 |
| `ParallelSafety.java` — `parallelCautions` | `TODO(Day18-task04)` | return >= 5 sentences (each > 40 chars) explaining WHY: associative reductions, stateless lambdas, side effects on shared state, the common pool, blocking work, and measuring first |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_sumOfSquaresDoesNotOverflow` |
| 2 | `r2_squaresInOrder` |
| 3 | `r3_decisionHelper` |
| 4 | `r4_cautionsAreSubstantive`, `r4_cautionsCoverTheKeyIdeas` |

## Edge cases to handle

- empty input to the numeric methods
- boundary at exactly 10_000 elements
- `int` overflow (`46341 * 46341`)
- documentation sentences must be meaningful, not keyword stuffing

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 18: Parallel Safety Note (Documentation + Sequential Implementation)`

## Hints (optional)

<details><summary>Hint 1</summary>

Cast to `long` **before** multiplying: `(long) v * v`.

</details>

<details><summary>Hint 2</summary>

The goal of the documentation task is not keyword stuffing: a reviewer will read each sentence and ask "is the reason correct?".

</details>
