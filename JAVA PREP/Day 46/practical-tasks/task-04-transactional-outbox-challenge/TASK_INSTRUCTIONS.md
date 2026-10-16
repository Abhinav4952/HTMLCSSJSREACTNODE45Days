# Task 4 — Transactional Outbox Simulation (Challenge)

**Day:** 46 · **Task ID:** Day46-task04 · **Type:** Java + JDBC (H2) · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Solve the dual-write problem: write the order and its event in one transaction, then relay events to the broker with a poller that preserves order and tolerates failures.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day46/task04/OutboxSchema.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day46/task04/OutboxPublisher.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day46/task04/OrderService.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day46/task04/OutboxPoller.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day46/task04/OutboxTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 46 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. `placeOrder` inserts order + outbox row atomically.
2. Any failure rolls back both rows; restore auto-commit.
3. `pollOnce` publishes unpublished rows in id order and marks each after success.
4. Stop at the first publisher failure and return the count so far.

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day46-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day46-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 46: complete task-04-transactional-outbox-challenge`.

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
| `OrderService.java` | `Day46-task04` | setAutoCommit(false); insert into orders; insert into outbox; commit; rollback on any exception |
| `OutboxPoller.java` | `Day46-task04` | select unpublished rows order by id; publish; update published = true; stop on first failure |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `tearDown` |
| 3 | `placeOrderWritesOrderAndOutboxRow` |
| 4 | `failureRollsBackTheOrderToo` |
| 5 | `pollerPublishesInOrderAndMarksRows` |
| 6 | `failedPublishStopsAndRetriesLater` |

## Edge cases to handle

- Null payload (outbox constraint).
- Publisher fails mid-batch.
- Second poll republishes only what remains.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 46: Transactional Outbox Simulation (Challenge)`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the result set fully into a list before updating rows.
</details>

<details><summary>Hint 2</summary>
Use `PreparedStatement` with parameters.
</details>
