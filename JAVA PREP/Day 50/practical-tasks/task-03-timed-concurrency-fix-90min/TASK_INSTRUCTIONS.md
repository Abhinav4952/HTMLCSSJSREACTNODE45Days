# Task 3 — Timed Round 3 (90 min): Concurrency Fixes

**Day:** 50 · **Task ID:** Day50-task03 · **Type:** Core Java · **Difficulty:** Timed

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Make three small components thread-safe: a counter, a lazy holder and an executor-based parallel sum. Start a 90-minute timer.

## Learning goals

- Recognize and fix race conditions and visibility problems
- Choose between atomics, locks and executors
- Manage thread-pool lifecycle correctly

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day50/task03/SafeCounter.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day50/task03/LazyHolder.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day50/task03/ParallelSum.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day50/task03/ConcurrencyTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 50 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. `SafeCounter`: no lost updates under contention.
2. `LazyHolder`: exactly-once initialisation, same instance for everyone.
3. `ParallelSum`: chunking, futures, correct shutdown and error handling.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day50-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day50-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 50: complete task-03-timed-concurrency-fix-90min`.

## How to run and verify

```bash
java -version   # 21.x
mvn -v          # 3.9+
mvn test        # expected RED at the start
mvn -Dtest=<TestClass> test
```

## TODO map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `SafeCounter.java` | `Day50-task03` | make this thread-safe (AtomicLong, LongAdder, synchronized or a lock |
| `SafeCounter.java` | `Day50-task03` | return the current value consistently with increment( |
| `LazyHolder.java` | `Day50-task03` | thread-safe lazy initialisation (double-checked locking with volatile, holder, or synchronized |
| `ParallelSum.java` | `Day50-task03` | ExecutorService + Callable<Long> per chunk, collect Futures, shut down in finally |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `counterDoesNotLoseUpdates` |
| 2 | `lazyHolderRunsSupplierOnce` |
| 3 | `parallelSumMatchesSequentialSum` |
| 4 | `parallelSumEdgeCases` |
| 5 | `parallelSumDoesNotLeakThreads` |

## Edge cases to handle

- `threads` greater than array length.
- Interrupted threads.
- Visibility (volatile / happens-before).
- Leaking executors.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 50: Timed Round 3 (90 min): Concurrency Fixes`

## Hints (optional)

<details><summary>Hint 1</summary>
`AtomicLong` is the simplest correct counter; `synchronized` also works.
</details>

<details><summary>Hint 2</summary>
`Executors.newFixedThreadPool(n)` and always `shutdown()` in `finally`.
</details>

<details><summary>Hint 3</summary>
Empty chunks are fine: their sum is 0.
</details>
