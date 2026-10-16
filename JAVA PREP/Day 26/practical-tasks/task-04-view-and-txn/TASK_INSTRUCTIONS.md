# Task 4 — Views, Functions and Transactions

**Day:** 26 · **Task ID:** Day26-task04 · **Type:** SQL script + JDBC test · **Difficulty:** Challenge

## Summary

Create a view that summarizes order totals, query it, use SQL string functions, and show that a view sees uncommitted data in its own transaction and respects ROLLBACK.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day26/task04/SqlLab.java` | Stubs / starter code (edit the TODOs) |
| `sql/schema.sql` | Provided helper or test (do not edit) |
| `sql/seed.sql` | Provided helper or test (do not edit) |
| `sql/answers.sql` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day26/task04/ViewTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 26 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Define the `order_totals` view with columns `order_id` and `total_cents`.
2. Query the view for big orders and compute customer counts per email domain with SQL functions.

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day26-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day26-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 26: complete task-04-view-and-txn`.

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
| `answers.sql` | `Day26-task04` | CREATE VIEW order_totals AS SELECT order_id, SUM(qty * unit_price_cents) AS total_cents FROM order_items GROUP BY order_id |
| `answers.sql` | `Day26-task04` | SELECT order_id, total_cents FROM the VIEW where total_cents >= 10000 ORDER BY order_id |
| `answers.sql` | `Day26-task04` | email domain (text after '@') and number of customers per domain, ORDER BY domain. |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `tearDown` |
| 3 | `viewExposesOneRowPerOrder` |
| 4 | `bigOrdersQueryUsesTheView` |
| 5 | `domainCountsUseStringFunctions` |
| 6 | `viewReflectsNewDataAndRollbackWorks` |

## Edge cases to handle

- The view must update automatically when new items are inserted.
- Rolled-back inserts must not appear in the view.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 26: Views, Functions and Transactions`

## Hints (optional)

<details><summary>Hint 1</summary>
A view stores a query, not data.
</details>

<details><summary>Hint 2</summary>
`GROUP BY` the expression you SELECT for the domain.
</details>
