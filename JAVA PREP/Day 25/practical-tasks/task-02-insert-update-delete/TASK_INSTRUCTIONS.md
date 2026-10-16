# Task 2 — Insert, Update, Delete

**Day:** 25 · **Task ID:** Day25-task02 · **Type:** SQL script + JDBC test · **Difficulty:** Core

## Summary

Given a finished `accounts` table, write the seed INSERTs and the UPDATE / DELETE statements that return the exact affected-row counts the tests expect.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day25/task02/SqlLab.java` | Stubs / starter code (edit the TODOs) |
| `sql/schema.sql` | Provided helper or test (do not edit) |
| `sql/seed.sql` | Stubs / starter code (edit the TODOs) |
| `sql/answers.sql` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day25/task02/DmlTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 25 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Write `seed.sql` with exactly the four specified rows.
2. Write the four DML blocks and one SELECT block in `answers.sql`.
3. Use WHERE clauses precisely — the tests check the affected-row counts returned by `executeUpdate`.

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day25-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day25-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 25: complete task-02-insert-update-delete`.

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
| `seed.sql` | `Day25-task02` | INSERT exactly these four rows (id, owner, balance_cents, status): |
| `answers.sql` | `Day25-task02` | UPDATE: add 500 to balance_cents of every ACTIVE account |
| `answers.sql` | `Day25-task02` | UPDATE: set status = 'CLOSED' where balance_cents = 0 |
| `answers.sql` | `Day25-task02` | DELETE every CLOSED account (the test runs close_zero first |
| `answers.sql` | `Day25-task02` | INSERT account id 5, owner 'eve', balance 100 — omit status so the DEFAULT applies |
| `answers.sql` | `Day25-task02` | SELECT the sum of all balance_cents |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `tearDown` |
| 3 | `seedHasExactlyTheFourAccounts` |
| 4 | `raiseActiveBalancesByFiveHundred` |
| 5 | `closeZeroBalanceThenPurge` |
| 6 | `insertEveUsesDefaultStatus` |
| 7 | `totalBalance` |

## Edge cases to handle

- An UPDATE/DELETE without WHERE would affect all rows — tests catch this.
- Rely on the column DEFAULT in `insert_eve` rather than repeating the literal.
- `close_zero` must run before `purge_closed` in the test, never in your script.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 25: Insert, Update, Delete`

## Hints (optional)

<details><summary>Hint 1</summary>
`executeUpdate` returns the number of rows changed; think what each WHERE should match.
</details>

<details><summary>Hint 2</summary>
`SELECT SUM(balance_cents) FROM accounts` yields a single value.
</details>
