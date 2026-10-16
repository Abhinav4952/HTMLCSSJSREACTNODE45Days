# Task 3 — Normalization and Keys

**Day:** 25 · **Task ID:** Day25-task03 · **Type:** SQL script + JDBC test · **Difficulty:** Core

## Summary

Decompose the flat `raw_orders` table into 3NF tables (customers, products, orders, order_lines) with surrogate and composite keys, migrate the data with INSERT ... SELECT, and report per-customer totals.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day25/task03/SqlLab.java` | Stubs / starter code (edit the TODOs) |
| `sql/raw.sql` | Provided helper or test (do not edit) |
| `sql/schema.sql` | Stubs / starter code (edit the TODOs) |
| `sql/seed.sql` | Stubs / starter code (edit the TODOs) |
| `sql/answers.sql` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day25/task03/NormalizationTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 25 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Create the four normalized tables with the exact column names listed in `schema.sql`.
2. Migrate all five raw rows with SELECT-based INSERTs (no hard-coded literals).
3. Write the per-customer revenue query joining the new tables.

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day25-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day25-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 25: complete task-03-normalization-keys`.

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
| `schema.sql` | `Day25-task03` | customers(id identity PK, email UNIQUE NOT NULL, name NOT NULL |
| `schema.sql` | `Day25-task03` | products(id identity PK, sku UNIQUE NOT NULL, name NOT NULL, unit_price_cents INT NOT NULL |
| `schema.sql` | `Day25-task03` | orders(id BIGINT PK  -- reuse the raw order_id, customer_id FK -> customers NOT NULL |
| `schema.sql` | `Day25-task03` | order_lines(order_id FK, product_id FK, qty INT CHECK (qty > 0), PRIMARY KEY (order_id, product_id |
| `seed.sql` | `Day25-task03` | INSERT INTO customers (email, name) SELECT DISTINCT ... FROM raw_orders |
| `seed.sql` | `Day25-task03` | INSERT INTO products (sku, name, unit_price_cents) SELECT DISTINCT ... FROM raw_orders |
| `seed.sql` | `Day25-task03` | INSERT INTO orders (id, customer_id) SELECT DISTINCT r.order_id, c.id ... JOIN customers |
| `seed.sql` | `Day25-task03` | INSERT INTO order_lines (order_id, product_id, qty) SELECT ... JOIN products |
| `answers.sql` | `Day25-task03` | customer email and SUM(qty * unit_price_cents) per customer, ordered by email (2 columns |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `tearDown` |
| 3 | `exec` |
| 4 | `dataWasSplitWithoutDuplicates` |
| 5 | `ordersKeepOriginalIdsAndLinkToCustomers` |
| 6 | `compositeKeyPreventsDuplicateLines` |
| 7 | `quantityMustBePositiveAndKeysEnforced` |
| 8 | `totalsPerCustomer` |

## Edge cases to handle

- Duplicated customers/products must collapse to one row each.
- `order_lines` has a composite primary key `(order_id, product_id)`.
- A line with qty 0 or an unknown order must be rejected.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 25: Normalization and Keys`

## Hints (optional)

<details><summary>Hint 1</summary>
`SELECT DISTINCT customer_email, customer_name FROM raw_orders` gives the customer rows.
</details>

<details><summary>Hint 2</summary>
Join `raw_orders` back to `customers` on email to find `customer_id`.
</details>
