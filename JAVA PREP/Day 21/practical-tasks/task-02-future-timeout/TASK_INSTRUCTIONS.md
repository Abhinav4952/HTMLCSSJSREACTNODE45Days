# Task 2 — Future Timeouts, Cancellation, and invokeAny

**Day:** 21 · **Task ID:** Day21-task02 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Wrap `Future` usage in safe helpers: get a result within a deadline (cancelling on timeout), fall back to a default on any failure, take the first successful result of several redundant tasks (`invokeAny`), and cancel a running task while verifying it was interrupted.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day21/task02/FutureTimeout.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day21/task02/FutureTimeoutTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 21 theory file read

## What you will implement

1. `getWithTimeout(future, timeoutMillis)` returns `Optional.of(value)`; on timeout it **cancels** the future (interrupting) and returns empty; a task failure becomes `IllegalStateException` with the original exception as cause
2. `getOrDefault(future, timeoutMillis, fallback)` returns the value, or `fallback` on timeout or task failure (and cancels on timeout)
3. `firstSuccessful(pool, tasks)` returns the result of the first task that completes successfully (`invokeAny`); if all fail an `ExecutionException` propagates
4. `cancelRunning(future)` returns `true` only if the future was actually cancelled (interrupting a running task); completed futures return `false`

## Constraints

- Do not create threads or executors in the helpers (use the given future/pool)
- Do not use `Thread.sleep`
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=FutureTimeoutTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **8 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day21-task02)`).

### Run one test class

```bash
mvn -Dtest=FutureTimeoutTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `FutureTimeout.java` — `getWithTimeout` | `TODO(Day21-task02)` | future.get(timeout, MILLISECONDS) -> Optional.ofNullable; on TimeoutException cancel(true) and return empty; on ExecutionException throw IllegalStateException with the cause |
| `FutureTimeout.java` — `getOrDefault` | `TODO(Day21-task02)` | value within the timeout, otherwise fallback on timeout (cancel the future) or task failure; if the calling thread is interrupted restore its flag and return fallback |
| `FutureTimeout.java` — `firstSuccessful` | `TODO(Day21-task02)` | return pool.invokeAny(tasks): the first successful result; ExecutionException when every task fails |
| `FutureTimeout.java` — `cancelRunning` | `TODO(Day21-task02)` | cancel(true) and report whether the future is now cancelled (false for futures that already completed) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_returnsValueWhenFastEnough`, `r1_timeoutCancelsAndReturnsEmpty`, `r1_failureBecomesIllegalStateWithCause` |
| 2 | `r2_getOrDefault` |
| 3 | `r3_firstSuccessfulIgnoresFailures`, `r3_allFailingPropagatesExecutionException` |
| 4 | `r4_cancelRunningInterruptsTheTask`, `r4_cancellingACompletedFutureReturnsFalse` |

## Edge cases to handle

- timeout shorter than the task
- failing task
- all tasks failing in invokeAny
- cancelling an already-finished future

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 21: Future Timeouts, Cancellation, and invokeAny`

## Hints (optional)

<details><summary>Hint 1</summary>

`Future.cancel(true)` returns `false` for tasks that already completed - make sure your helper reports exactly that.

</details>

<details><summary>Hint 2</summary>

Wrap `ExecutionException#getCause()` to preserve the original failure for callers.

</details>
