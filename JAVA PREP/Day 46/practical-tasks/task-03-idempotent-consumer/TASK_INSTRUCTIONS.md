# Task 3 — Idempotent Consumer with a Processed-Events Table

**Day:** 46 · **Task ID:** Day46-task03 · **Type:** Java + JDBC (H2) · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Guarantee a side effect runs once even when the same event is delivered twice, using a primary-key insert in the same transaction.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day46/task03/Schema.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day46/task03/IdempotentConsumer.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day46/task03/IdempotentConsumerTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 46 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Insert the event id inside a transaction before running the side effect.
2. Detect duplicates via `SQLIntegrityConstraintViolationException` and return false.
3. Roll back and rethrow when the side effect fails so the event can be retried.
4. Always restore auto-commit.

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day46-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day46-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 46: complete task-03-idempotent-consumer`.

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
| `IdempotentConsumer.java` | `Day46-task03` | setAutoCommit(false), insert, detect SQLIntegrityConstraintViolationException, run, commit / rollback |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `tearDown` |
| 3 | `firstDeliveryRunsTheSideEffect` |
| 4 | `duplicateDeliveryIsSkipped` |
| 5 | `differentEventsAreBothProcessed` |
| 6 | `failedSideEffectRollsBackSoRetryWorks` |
| 7 | `autoCommitIsRestored` |

## Edge cases to handle

- Failure of the side effect after the insert.
- Duplicate id.
- Connection state after errors.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 46: Idempotent Consumer with a Processed-Events Table`

## Hints (optional)

<details><summary>Hint 1</summary>
Use try/finally to restore auto-commit.
</details>

<details><summary>Hint 2</summary>
On duplicate, roll back before returning.
</details>
