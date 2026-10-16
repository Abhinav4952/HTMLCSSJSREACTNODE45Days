# Task 2 — Retry with Resilience4j

**Day:** 43 · **Task ID:** Day43-task02 · **Type:** Java + Resilience4j · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Wrap a flaky in-process downstream with Resilience4j `Retry`: bounded attempts, wait between attempts, selective exception types.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day43/task02/ResilientCaller.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day43/task02/FlakyDownstream.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day43/task02/DownstreamException.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day43/task02/ResilientCallerTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 43 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Build a `RetryConfig` with `maxAttempts`, `waitDuration` and `retryExceptions(retryOn)`.
2. Decorate the supplier with `Retry.decorateSupplier` and execute it.
3. Rethrow the last exception when attempts are exhausted.
4. Do not retry exceptions outside `retryOn`.
5. Reject `maxAttempts < 1` with `IllegalArgumentException`.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day43-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day43-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 43: complete task-02-retry-with-backoff`.

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
| `ResilientCaller.java` | `Day43-task02` | build a RetryConfig (maxAttempts, waitDuration, retryExceptions) and decorate the supplier |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `succeedsAfterTransientFailures` |
| 2 | `givesUpAfterMaxAttemptsAndRethrowsLastFailure` |
| 3 | `nonRetryableExceptionsAreNotRetried` |
| 4 | `firstSuccessIsNotRepeated` |
| 5 | `waitsBetweenAttempts` |
| 6 | `rejectsInvalidAttemptCount` |

## Edge cases to handle

- `maxAttempts` counts the first call too.
- Resilience4j requires a wait of at least a few milliseconds.
- Retrying non-idempotent calls is dangerous (discuss in theory).

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 43: Retry with Resilience4j`

## Hints (optional)

<details><summary>Hint 1</summary>
`Retry.of("name", config)` creates the retry instance.
</details>

<details><summary>Hint 2</summary>
The decorated supplier throws the original exception after the last attempt.
</details>
