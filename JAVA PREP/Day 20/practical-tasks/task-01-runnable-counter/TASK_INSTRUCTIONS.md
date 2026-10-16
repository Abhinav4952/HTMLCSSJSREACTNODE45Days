# Task 1 — Runnable Counter

**Day:** 20 · **Task ID:** Day20-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Start threads that increment a shared counter and prove the final count is exact by making the counter's methods `synchronized`. Also demonstrate the difference between calling `run()` and `start()` by reporting which thread executed the task.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day20/task01/Counter.java` | Stubs with TODOs |
| `src/main/java/com/javaprep/day20/task01/RunnableCounter.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day20/task01/RunnableCounterTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 20 theory file read

## What you will implement

1. `Counter.increment()` and `Counter.get()` are thread-safe (`synchronized`)
2. `incrementTask(counter, times)` returns a `Runnable` that calls `increment()` `times` times
3. `runConcurrently(counter, threads, perThread)` starts `threads` named threads (`counter-0`, `counter-1`, ...), joins them all, and returns the counter value (`threads <= 0` or `perThread < 0` -> `IllegalArgumentException`)
4. `startNamed(name, runnable)` returns a **started** thread having that name
5. `executedByWithRun()` runs a task via `Thread.run()` and returns the name of the thread that executed it (the **calling** thread)
6. `executedByWithStart(name)` runs a task via `start()`, joins, and returns the executing thread's name (the new thread's name)

## Constraints

- Do not use `AtomicInteger` or `java.util.concurrent.locks` in `Counter` (the point is `synchronized`)
- Do not use `Thread.sleep` to wait for threads
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=RunnableCounterTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **8 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day20-task01)`).

### Run one test class

```bash
mvn -Dtest=RunnableCounterTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `Counter.java` — `increment` | `TODO(Day20-task01)` | make this method thread-safe: mark it synchronized (or lock a private final monitor) and increment value |
| `Counter.java` — `get` | `TODO(Day20-task01)` | return value using the SAME lock as increment so that the latest value is visible |
| `RunnableCounter.java` — `incrementTask` | `TODO(Day20-task01)` | return a Runnable that calls counter.increment() exactly times times |
| `RunnableCounter.java` — `runConcurrently` | `TODO(Day20-task01)` | validate (threads > 0, perThread >= 0), start threads named counter-0.. each running incrementTask, join ALL of them, then return counter.get() |
| `RunnableCounter.java` — `startNamed` | `TODO(Day20-task01)` | create a Thread with the given name for the task, start it, and return it |
| `RunnableCounter.java` — `executedByWithRun` | `TODO(Day20-task01)` | create a thread named "worker" whose task records Thread.currentThread().getName(), call run() directly (NOT start) and return the recorded name |
| `RunnableCounter.java` — `executedByWithStart` | `TODO(Day20-task01)` | same task but on a Thread called name started with start(); join it and return the recorded name |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_counterCountsSequentially` |
| 2 | `r2_incrementTaskRunsExactlyTimes` |
| 3 | `r3_concurrentIncrementsAreExact`, `r3_validation`, `r3_zeroIncrementsGivesZero` |
| 4 | `r4_startNamedStartsAThreadWithThatName` |
| 5 | `r5_runDirectlyExecutesOnTheCallingThread` |
| 6 | `r6_startExecutesOnTheNewThread` |

## Edge cases to handle

- zero increments
- invalid thread counts
- join all threads before reading the result
- never swallow `InterruptedException` (declare it)

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 20: Runnable Counter`

## Hints (optional)

<details><summary>Hint 1</summary>

Both `increment()` and `get()` need the **same** lock: visibility requires the reader to synchronize too.

</details>

<details><summary>Hint 2</summary>

Start all threads first, then join them all; joining inside the starting loop serializes the work.

</details>
