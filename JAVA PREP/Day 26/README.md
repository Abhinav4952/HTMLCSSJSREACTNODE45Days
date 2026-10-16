# Day 26 — Joins, Aggregates, Indexes, Views, and Transactions

## Learning objectives

- Choose between inner, outer, anti and self joins
- Aggregate with GROUP BY/HAVING and rank results
- Recommend composite and unique indexes; recognize non-sargable predicates
- Create and query views; use SQL functions
- Reason about view visibility inside transactions

## Prerequisites

- Day 25 (DDL, DML, keys, ACID)

## How to use this folder

1. Read [`DAY-26-THEORY-AND-REFERENCE.md`](DAY-26-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-inner-outer-joins` | SQL script + JDBC test | `mvn test` |
| 2 | `task-02-group-by-having` | SQL script + JDBC test | `mvn test` |
| 3 | `task-03-index-explain-notes` | Plain Java | `mvn test` |
| 4 | `task-04-view-and-txn` | SQL script + JDBC test | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** SQL/JDBC
