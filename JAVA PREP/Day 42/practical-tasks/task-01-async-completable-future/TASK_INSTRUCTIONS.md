# Task 1 — @Async with CompletableFuture

**Day:** 42 · **Task ID:** Day42-task01 · **Type:** Spring Boot (Async / Scheduling / Cache) · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Run work on Spring's task executor with @Async, return CompletableFuture, handle failures and combine results.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day42/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day42/task01/AsyncConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day42/task01/SlowService.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day42/task01/Aggregator.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day42/task01/AsyncTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 42 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Enable async support and annotate the four service methods with `@Async`.
2. Implement the four async methods and `Aggregator.sumOfSquares`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day42-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day42-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 42: complete task-01-async-completable-future`.

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
| `AsyncConfig.java` | `Day42-task01` | switch on @Async processing for the application (@EnableAsync |
| `SlowService.java` | `Day42-task01` | run asynchronously (@Async |
| `SlowService.java` | `Day42-task01` | return a completed future with Thread.currentThread().getName( |
| `SlowService.java` | `Day42-task01` | sleep ~50 ms (restore the interrupt flag when interrupted) and complete with n*n |
| `SlowService.java` | `Day42-task01` | failedFuture |
| `SlowService.java` | `Day42-task01` | record the thread name and count down |
| `Aggregator.java` | `Day42-task01` | start every future before joining any; allOf(...).join(); sum |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `serviceIsProxiedForAsync` |
| 2 | `runsOnExecutorThread` |
| 3 | `futureCompletesWithValue` |
| 4 | `failureTravelsInsideTheFuture` |
| 5 | `fireAndForgetRunsInBackground` |
| 6 | `aggregatorCombinesFutures` |

## Edge cases to handle

- Calling an `@Async` method from the same class bypasses the proxy: that is why `Aggregator` is a separate bean.
- Return failures inside the future; `void` async methods lose exceptions (use an AsyncUncaughtExceptionHandler).
- Always restore the interrupt flag after catching `InterruptedException`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 42: @Async with CompletableFuture`

## Hints (optional)

<details><summary>Hint 1</summary>
`@Async` methods must be public and called from another bean.
</details>

<details><summary>Hint 2</summary>
`CompletableFuture.allOf(...)` does not return values: join the individual futures.
</details>
