# Task 3 — JDBC Transaction Transfer

**Day:** 27 · **Task ID:** Day27-task03 · **Type:** Plain Java + JDBC (H2) · **Difficulty:** Core

## Summary

Implement an atomic money transfer with manual commit/rollback and restore autocommit afterwards.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day27/task03/TransferService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day27/task03/TransferServiceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 27 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `balanceOf`.
2. Implement `transfer` in one transaction: validate, check funds, debit, credit, commit.
3. Roll back on any failure and rethrow the original unchecked exception.
4. Always restore `autoCommit(true)` in a finally block.

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day27-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day27-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 27: complete task-03-transaction-transfer`.

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
| `TransferService.java` | `Day27-task03` | SELECT balance_cents; unknown account -> IllegalArgumentException |
| `TransferService.java` | `Day27-task03` | implement the transactional transfer described above |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `exec` |
| 3 | `transferMovesMoney` |
| 4 | `insufficientFundsChangesNothing` |
| 5 | `unknownDestinationRollsBackTheDebit` |
| 6 | `invalidArguments` |
| 7 | `totalMoneyIsConservedAfterManyTransfers` |

## Edge cases to handle

- Unknown destination: the debit must be undone.
- `amount <= 0` or same account: reject before opening a transaction.
- Total money is invariant.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 27: JDBC Transaction Transfer`

## Hints (optional)

<details><summary>Hint 1</summary>
Do the unknown-account check by inspecting `executeUpdate()` row counts.
</details>

<details><summary>Hint 2</summary>
Use one Connection for the whole transfer — transactions are per connection.
</details>
