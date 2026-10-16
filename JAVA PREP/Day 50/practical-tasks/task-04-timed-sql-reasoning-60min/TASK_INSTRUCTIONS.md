# Task 4 — Timed Round 4 (60 min): SQL Reporting and Index Reasoning

**Day:** 50 · **Task ID:** Day50-task04 · **Type:** SQL + JDBC (H2) · **Difficulty:** Timed

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Write two reporting queries (aggregate with join, anti-join) and the index that supports them, then explain your choices in a short note in your commit message. Start a 60-minute timer.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day50/task04/ReportQueries.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day50/task04/ReportQueriesTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 50 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. `topCustomersSql`: PAID totals per customer, top 2, name + total.
2. `customersWithoutPaidOrdersSql`: anti-join with `NOT EXISTS`, ordered by name.
3. `supportingIndexDdl`: composite index `(customer_id, status)` named `idx_orders_customer_status`.
4. Be ready to explain: why `NOT EXISTS` over `NOT IN` (NULL semantics), and why the column order of the index matters.

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day50-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day50-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 50: complete task-04-timed-sql-reasoning-60min`.

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
| `ReportQueries.java` | `Day50-task04` | join + where status = 'PAID' + group by + order by total desc + limit 2 |
| `ReportQueries.java` | `Day50-task04` | select name from customers c where not exists (...) order by name |
| `ReportQueries.java` | `Day50-task04` | create index idx_orders_customer_status on orders (customer_id, status |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `tearDown` |
| 3 | `topCustomersByPaidTotal` |
| 4 | `customersWithoutPaidOrders` |
| 5 | `antiJoinUsesNotExists` |
| 6 | `supportingIndexIsCreatedWithTheExpectedName` |

## Edge cases to handle

- Customers with no orders.
- Cancelled orders must not count.
- NULL handling in `NOT IN`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 50: Timed Round 4 (60 min): SQL Reporting and Index Reasoning`

## Hints (optional)

<details><summary>Hint 1</summary>
`join` is inner: customers without paid orders vanish automatically in query 1.
</details>

<details><summary>Hint 2</summary>
`select ... from customers c where not exists (select 1 from orders o where o.customer_id = c.id and o.status = 'PAID')`.
</details>
