# Day 26 — Joins, Aggregates, Indexes, Views, and Transactions

**Phase:** SQL/JDBC  
**Primary theme:** Query-writing skills for real backends: joins, aggregation, indexing strategy, views, and transaction behavior (H2 in PostgreSQL mode)  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-inner-outer-joins`, `task-02-group-by-having`, `task-03-index-explain-notes`, `task-04-view-and-txn`  
**Instruction alignment:** Maps to Day 26 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, H2 2.3.232 (PostgreSQL mode)

## Overview

Query-writing skills for real backends: joins, aggregation, indexing strategy, views, and transaction behavior (H2 in PostgreSQL mode). This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. Joins
2. Aggregation: GROUP BY, HAVING and window-free reporting
3. Indexes and EXPLAIN
4. Views, functions, and transactions in practice
5. Interview corner, common mistakes, glossary

## Subtopics

### Joins

#### What it is

A **join** combines rows from two tables on a condition. `INNER JOIN` keeps matches only; `LEFT/RIGHT OUTER JOIN` keep all rows of one side and fill NULLs for missing matches; `FULL OUTER JOIN` keeps both; `CROSS JOIN` is the Cartesian product; a **self join** joins a table with itself (e.g. employee -> manager).

#### Why it exists / why it matters

Normalized data (Day 25) is spread across tables; joins reassemble it. Choosing the wrong join type silently drops or duplicates rows — a top source of wrong reports.

#### Pros and cons

**Pros**

- Express relationships declaratively; the optimizer picks nested-loop, hash or merge join
- Outer joins answer 'what is missing?' (anti-join)
- Self joins model hierarchies without extra tables
- Set-based and fast with proper indexes

**Cons / trade-offs**

- Joining on non-indexed columns is slow on big tables
- One-to-many joins multiply rows, breaking aggregates
- Many-join queries get hard to read and plan

#### What happens without it / when misused

Using INNER JOIN where you needed LEFT JOIN silently hides employees without a department. Joining a one-to-many table before `SUM` double-counts. A missing ON clause produces a Cartesian product (millions of rows).

#### Syntax and rules

```sql
SELECT e.name, d.name FROM employees e JOIN departments d ON d.id = e.dept_id;           -- inner
SELECT e.name FROM employees e LEFT JOIN departments d ON d.id = e.dept_id WHERE d.id IS NULL; -- anti-join
SELECT e.name, m.name FROM employees e JOIN employees m ON m.id = e.manager_id;           -- self
```
Filter on the right table of a LEFT JOIN in `ON`, not `WHERE`, or you turn it into an inner join.

#### Examples

**Example 1 — Inner vs left**

```sql
-- employees without department are dropped:
SELECT e.name, d.name FROM employees e JOIN departments d ON d.id = e.dept_id;
-- employees kept, d.name NULL when absent:
SELECT e.name, d.name FROM employees e LEFT JOIN departments d ON d.id = e.dept_id;
```

**Example 2 — Anti-join**

```sql
SELECT d.name FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
WHERE e.id IS NULL;
```

**Example 3 — Full outer via UNION**

```sql
SELECT e.id, d.id FROM employees e LEFT JOIN departments d ON d.id = e.dept_id
UNION
SELECT e.id, d.id FROM employees e RIGHT JOIN departments d ON d.id = e.dept_id;
```

#### Quick checks

1. Which join finds departments with no employees?
2. Why can a WHERE on the right table break a LEFT JOIN?
3. What does a missing ON condition produce?

### Aggregation: GROUP BY, HAVING and window-free reporting

#### What it is

Aggregate functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) collapse many rows into one value. `GROUP BY` forms groups; `HAVING` filters groups; `ORDER BY ... LIMIT` ranks them. Logical order: FROM/JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT.

#### Why it exists / why it matters

Reports, dashboards and invariants (e.g. money supply) are aggregations. Understanding evaluation order explains why aliases are not usable in WHERE and why HAVING exists.

#### Pros and cons

**Pros**

- Database does the heavy lifting close to the data
- Declarative and portable across engines
- Combine with joins for rich reporting
- `COUNT(DISTINCT x)` answers cardinality questions

**Cons / trade-offs**

- Aggregating huge tables is I/O heavy without summaries/indexes
- NULL handling surprises (`COUNT(col)` ignores NULLs, `COUNT(*)` does not)
- Integer division and AVG rounding differ between engines

#### What happens without it / when misused

Selecting a non-grouped column raises `column must appear in the GROUP BY clause`. Using WHERE for an aggregate condition raises `aggregate functions are not allowed in WHERE`. Averaging ints and expecting decimals gives truncated numbers.

#### Syntax and rules

```sql
SELECT region, SUM(amount_cents) AS total FROM sales GROUP BY region HAVING SUM(amount_cents) > 10000 ORDER BY region;
SELECT rep, SUM(amount_cents) t FROM sales GROUP BY rep ORDER BY t DESC LIMIT 1;
```

#### Examples

**Example 1 — Totals per group**

```sql
SELECT region, COUNT(*) n, SUM(amount_cents) total FROM sales GROUP BY region ORDER BY region;
```

**Example 2 — HAVING**

```sql
SELECT region FROM sales GROUP BY region HAVING SUM(amount_cents) > 10000;
```

**Example 3 — Top-1 per ranking**

```sql
SELECT rep, SUM(amount_cents) t FROM sales GROUP BY rep ORDER BY t DESC LIMIT 1;
```

#### Quick checks

1. WHERE vs HAVING?
2. COUNT(*) vs COUNT(col)?
3. Why does `SELECT region, rep, SUM(x) ... GROUP BY region` fail?

### Indexes and EXPLAIN

#### What it is

An **index** is a sorted structure (usually a B-tree) that lets the database find rows without scanning the table. `EXPLAIN` shows the plan: sequential scan vs index scan, join algorithm, estimated rows. Composite indexes follow the **leftmost prefix** rule; a predicate is **sargable** if an index can serve it.

#### Why it exists / why it matters

Most production slowness is a missing or unusable index. Backend engineers must read plans and reason about write cost vs read speed.

#### Pros and cons

**Pros**

- Turns O(n) scans into O(log n) lookups
- UNIQUE indexes enforce constraints
- Covering indexes avoid table lookups
- Partial/expression indexes (PostgreSQL) target hot queries

**Cons / trade-offs**

- Each index slows INSERT/UPDATE/DELETE and uses disk/RAM
- Wrong column order makes a composite index useless
- Planner may ignore an index for small tables or low selectivity — that is correct

#### What happens without it / when misused

`WHERE lower(email) = ?` and `LIKE '%x'` cannot use a plain index on `email`; implicit casts also disable indexes. Over-indexing slows writes and bloats storage.

#### Syntax and rules

```sql
CREATE INDEX idx_orders_customer_status_created ON orders (customer_id, status, created_at);
EXPLAIN SELECT * FROM orders WHERE customer_id = 1 AND status = 'NEW' AND created_at > '2024-01-01';
-- PostgreSQL: EXPLAIN (ANALYZE, BUFFERS) shows real timing
```
Rule: equality columns first, then range, then ORDER BY columns.

#### Examples

**Example 1 — Composite index design**

```sql
-- query: WHERE customer_id = ? AND status = ? ORDER BY created_at DESC
CREATE INDEX idx_orders_cust_status_created ON orders (customer_id, status, created_at);
```

**Example 2 — Not sargable vs sargable**

```sql
WHERE lower(email) = 'a@x.io'   -- full scan
WHERE email = 'a@x.io'          -- index lookup
CREATE INDEX idx_users_lower_email ON users (lower(email)); -- PostgreSQL expression index
```

**Example 3 — Reading a plan (H2)**

```text
SELECT ... FROM PUBLIC.ORDERS /* PUBLIC.IDX_ORDERS_STATUS: STATUS = 'NEW' */   -> index scan
SELECT ... FROM PUBLIC.ORDERS /* PUBLIC.ORDERS.tableScan */                     -> full scan
```

#### Quick checks

1. Why order composite index columns equality-first?
2. Why can LIKE '%abc' not use a B-tree index?
3. What is the cost of an extra index?

### Views, functions, and transactions in practice

#### What it is

A **view** is a stored query presented as a virtual table (PostgreSQL also has materialized views that store results). **Functions** include built-ins (`SUBSTR`, `COALESCE`, `NOW()`) and user-defined PL/pgSQL functions. **Transactions** wrap multiple statements; a view inside a transaction sees that transaction's own uncommitted changes.

#### Why it exists / why it matters

Views encapsulate complex joins and hide columns for security; functions avoid repeating logic; transactions guarantee consistency across multi-step operations.

#### Pros and cons

**Pros**

- Views simplify queries and enforce column-level access
- Built-in functions push formatting/parsing to the database
- Transactions + views give consistent snapshots
- Materialized views accelerate heavy reports

**Cons / trade-offs**

- Views hide complexity — a slow view is a slow query everywhere
- Materialized views go stale until refreshed
- PL/pgSQL logic in the database is harder to test and version

#### What happens without it / when misused

Nesting views several levels deep produces unreadable plans. Forgetting `COMMIT` leaves a connection holding locks (idle in transaction). Relying on H2-only functions breaks on PostgreSQL.

#### Syntax and rules

```sql
CREATE VIEW order_totals AS
  SELECT order_id, SUM(qty * unit_price_cents) AS total_cents FROM order_items GROUP BY order_id;
SELECT * FROM order_totals WHERE total_cents >= 10000;
```
PostgreSQL extras: `CREATE MATERIALIZED VIEW ...; REFRESH MATERIALIZED VIEW ...;` and `CREATE FUNCTION ... LANGUAGE plpgsql`.

#### Examples

**Example 1 — View over aggregation**

```sql
CREATE VIEW order_totals AS SELECT order_id, SUM(qty*unit_price_cents) total_cents FROM order_items GROUP BY order_id;
```

**Example 2 — String functions**

```sql
SELECT SUBSTR(email, POSITION('@' IN email) + 1) AS domain, COUNT(*) FROM customers GROUP BY 1;
```

**Example 3 — Rollback and views**

```java
c.setAutoCommit(false);
insert(...);               // visible through the view in this transaction
c.rollback();             // gone again
```

#### Quick checks

1. Does a plain view store data?
2. How is a materialized view different?
3. What does an uncommitted insert look like to another connection?

## Interview corner

**Q1. INNER vs LEFT JOIN?**

INNER keeps only matches; LEFT keeps every left row with NULLs where no match.

**Q2. Explain the leftmost-prefix rule.**

A composite index (a,b,c) can serve predicates on a, a+b, a+b+c but not b alone.

**Q3. How do you find a slow query's problem?**

EXPLAIN (ANALYZE), look for seq scans on large tables, bad row estimates, missing indexes, sort spills.

**Q4. WHERE vs HAVING?**

Row filter before grouping vs group filter after aggregation.

**Q5. When is a materialized view appropriate?**

Expensive, read-heavy reports tolerating stale data between refreshes.

## Common mistakes & debugging

- Putting a right-table filter in WHERE of a LEFT JOIN.
- Summing after joining a one-to-many table (double counting).
- Assuming the optimizer uses every index — always check EXPLAIN.
- Creating indexes on low-selectivity columns (boolean) without reason.

## Further reading

- PostgreSQL docs: Queries, Indexes, Performance Tips
- Markus Winand — Use The Index, Luke
- H2 grammar reference

## Glossary

| Term | Meaning |
|------|---------|
| Sargable | Search-ARGument-able: predicate usable by an index |
| Anti-join | Rows with no match in another table |
| Seq scan | Reading every row of a table |
| Covering index | Index containing all columns the query needs |
| Materialized view | View whose result is stored and refreshed |

## Answers

### Joins

1. LEFT JOIN from departments to employees with `WHERE e.id IS NULL` (anti-join).
2. Rows with NULL on the right fail the predicate and are removed, making it behave like an inner join.
3. A Cartesian product of both tables.

### Aggregation: GROUP BY, HAVING and window-free reporting

1. WHERE filters rows before grouping; HAVING filters groups after aggregation.
2. COUNT(*) counts rows; COUNT(col) counts non-NULL values of col.
3. `rep` is neither grouped nor aggregated.

### Indexes and EXPLAIN

1. The B-tree can only narrow by a leftmost prefix; a range column ends the usable prefix.
2. B-trees sort by the beginning of the string; a leading wildcard has no starting point.
3. Slower writes and more storage/memory.

### Views, functions, and transactions in practice

1. No — it stores the query and runs it on each access.
2. It stores the result set and must be refreshed.
3. Invisible under READ COMMITTED.
