# Task 1 — Virtual Thread Runner

**Day:** 22 · **Task ID:** Day22-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Build a tiny toolkit on top of Java 21 virtual threads: start a named virtual thread, detect virtual threads, run a batch of `Callable`s on a virtual-thread-per-task executor with results in input order, create a named virtual `ThreadFactory`, and run many tasks while limiting concurrency with a `Semaphore`.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day22/task01/VirtualThreads.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day22/task01/VirtualThreadsTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 22 theory file read

## What you will implement

1. `start(name, runnable)` starts and returns a **virtual** thread with exactly that name
2. `isVirtual(thread)` reports whether the thread is virtual
3. `runAll(tasks)` runs every callable on a virtual-thread-per-task executor and returns the results **in input order**; a failing task surfaces as `ExecutionException`; the executor is always closed
4. `factory(prefix)` returns a `ThreadFactory` whose threads are unstarted virtual threads named `prefix0`, `prefix1`, ...
5. `runLimited(tasks, permits, sleepMillis)` runs `tasks` virtual threads that each hold a semaphore permit while sleeping `sleepMillis`, and returns a `Stats(completed, peakConcurrency)` where the peak never exceeds `permits`

## Constraints

- Use `Thread.ofVirtual()` / `newVirtualThreadPerTaskExecutor()` - no platform thread pools
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=VirtualThreadsTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **9 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day22-task01)`).

### Run one test class

```bash
mvn -Dtest=VirtualThreadsTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `VirtualThreads.java` — `start` | `TODO(Day22-task01)` | Thread.ofVirtual().name(name).start(body) and return the started thread |
| `VirtualThreads.java` — `isVirtual` | `TODO(Day22-task01)` | return thread.isVirtual() |
| `VirtualThreads.java` — `runAll` | `TODO(Day22-task01)` | try-with-resources on Executors.newVirtualThreadPerTaskExecutor(); submit every task, then collect future.get() in input order |
| `VirtualThreads.java` — `factory` | `TODO(Day22-task01)` | Thread.ofVirtual().name(prefix, 0).factory() so names are prefix0, prefix1, ... |
| `VirtualThreads.java` — `runLimited` | `TODO(Day22-task01)` | IllegalArgumentException if permits <= 0 or tasks < 0; Semaphore(permits); one virtual thread per task: acquire, bump running/peak (AtomicInteger), sleep, decrement, completed++, release in finally; close the executor to wait |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_startCreatesNamedVirtualThreadThatRunsTheBody` |
| 2 | `r2_isVirtualDistinguishesThreadKinds` |
| 3 | `r3_runAllKeepsInputOrderAndRunsOnVirtualThreads`, `r3_runAllScalesToManyBlockingTasks`, `r3_failureSurfacesAsExecutionException` |
| 4 | `r4_factoryBuildsUnstartedNamedVirtualThreads` |
| 5 | `r5_runLimitedNeverExceedsPermitsButUsesThem`, `r5_morePermitsThanTasksAndZeroTasks`, `r5_invalidArgumentsAreRejected` |

## Edge cases to handle

- empty task list
- a failing callable in `runAll`
- permits larger than tasks
- invalid arguments (`permits <= 0`) rejected

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 22: Virtual Thread Runner`

## Hints (optional)

<details><summary>Hint 1</summary>

`Thread.ofVirtual().name(prefix, 0)` appends an incrementing counter to the prefix.

</details>

<details><summary>Hint 2</summary>

`ExecutorService` is `AutoCloseable` in Java 19+: leaving the try block waits for all submitted tasks.

</details>

<details><summary>Hint 3</summary>

The semaphore must be released in `finally`, otherwise one failure starves the rest.

</details>
