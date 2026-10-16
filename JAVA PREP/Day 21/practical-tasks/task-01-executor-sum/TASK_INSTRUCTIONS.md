# Task 1 — Executor Chunked Sum

**Day:** 21 · **Task ID:** Day21-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Use an `ExecutorService` to sum a list in parallel chunks with `Callable`/`Future`, run a batch with `invokeAll` preserving order, and implement a correct graceful shutdown (shutdown, await, then `shutdownNow`).

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day21/task01/ExecutorSum.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day21/task01/ExecutorSumTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 21 theory file read

## What you will implement

1. `parallelSum(numbers, chunks, pool)` splits the list into at most `chunks` consecutive slices, sums each in the pool, and returns the total as a `long`; `chunks <= 0` -> `IllegalArgumentException`; empty list -> 0
2. `runAll(pool, tasks)` runs all callables with `invokeAll` and returns their results **in input order**; if a task failed, the `ExecutionException` (with its cause) propagates
3. `shutdownGracefully(pool, timeoutMillis)` calls `shutdown`, waits up to the timeout, then `shutdownNow`; returns `true` if the pool terminated on its own, `false` if it had to be forced

## Constraints

- Use only the provided `ExecutorService` - do not create threads or pools inside `parallelSum`/`runAll`
- No `parallelStream`
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=ExecutorSumTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day21-task01)`).

### Run one test class

```bash
mvn -Dtest=ExecutorSumTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `ExecutorSum.java` — `parallelSum` | `TODO(Day21-task01)` | IllegalArgumentException if chunks <= 0; empty list -> 0; split into <= chunks consecutive slices, submit one Callable<Long> per slice, then add up future.get() results |
| `ExecutorSum.java` — `runAll` | `TODO(Day21-task01)` | pool.invokeAll(tasks) then collect future.get() values in input order; a failed task propagates ExecutionException |
| `ExecutorSum.java` — `shutdownGracefully` | `TODO(Day21-task01)` | shutdown(); awaitTermination(timeoutMillis); if not terminated call shutdownNow() (and wait briefly) and return false; restore the interrupt flag if interrupted; return true when it terminated by itself |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_parallelSumMatchesSequentialSum`, `r1_edgeCases`, `r1_usesThePoolThreads` |
| 2 | `r2_runAllKeepsInputOrder`, `r2_failureKeepsItsCause` |
| 3 | `r3_gracefulShutdownWhenIdle`, `r3_forcedShutdownWhenATaskNeverFinishes` |

## Edge cases to handle

- more chunks than elements
- empty list
- a failing task in `runAll`
- pool with a task that never finishes (forced shutdown)

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 21: Executor Chunked Sum`

## Hints (optional)

<details><summary>Hint 1</summary>

Compute the slice size with ceiling division, then loop with `start += step`; the last slice may be shorter.

</details>

<details><summary>Hint 2</summary>

`shutdownNow()` interrupts running tasks - your graceful method must return `false` when it had to use it.

</details>
