# Task 4 — ACID Transaction Demo

**Day:** 25 · **Task ID:** Day25-task04 · **Type:** SQL script + JDBC test · **Difficulty:** Challenge

## Summary

Write the debit/credit/overdraft statements for a money transfer, prove atomicity with COMMIT and ROLLBACK, and implement two small ACID helper methods.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day25/task04/SqlLab.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day25/task04/AcidNotes.java` | Stubs / starter code (edit the TODOs) |
| `sql/schema.sql` | Provided helper or test (do not edit) |
| `sql/seed.sql` | Provided helper or test (do not edit) |
| `sql/answers.sql` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day25/task04/AcidTransactionTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 25 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Complete the four named blocks in `sql/answers.sql`.
2. Implement `AcidNotes.propertyFor` and `AcidNotes.isolationFor`.
3. Be able to explain why the total of 15000 is invariant after commit and after rollback (atomicity + consistency).

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day25-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day25-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 25: complete task-04-acid-transaction-demo`.

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
| `AcidNotes.java` | `Day25-task04` | map the ACID letter to its property name; throw IllegalArgumentException for any other letter |
| `AcidNotes.java` | `Day25-task04` | implement (case-insensitive, trimmed); unknown anomaly -> IllegalArgumentException |
| `answers.sql` | `Day25-task04` | UPDATE: subtract 3000 from ana's balance |
| `answers.sql` | `Day25-task04` | UPDATE: add 3000 to bob's balance |
| `answers.sql` | `Day25-task04` | UPDATE: subtract 999999 from ana's balance (must be rejected by the CHECK constraint |
| `answers.sql` | `Day25-task04` | SELECT the sum of all balances (the money supply invariant |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `tearDown` |
| 3 | `commitedTransferMovesMoneyAndKeepsTotal` |
| 4 | `rollbackUndoesTheDebit` |
| 5 | `overdraftViolatesCheckConstraintAndRollsBack` |
| 6 | `acidLetters` |
| 7 | `isolationLevels` |

## Edge cases to handle

- Unknown ACID letters or anomalies -> `IllegalArgumentException`.
- Anomaly names are case-insensitive and trimmed.
- The overdraft block must fail with a constraint error, not succeed with a negative balance.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 25: ACID Transaction Demo`

## Hints (optional)

<details><summary>Hint 1</summary>
Atomicity: all statements in the transaction apply or none do.
</details>

<details><summary>Hint 2</summary>
`SELECT SUM(balance_cents) FROM accounts` is the invariant to check.
</details>
