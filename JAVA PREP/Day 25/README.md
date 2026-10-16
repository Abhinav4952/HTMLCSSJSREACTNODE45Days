# Day 25 — PostgreSQL and RDBMS Fundamentals

## Learning objectives

- Design tables with PK, FK, UNIQUE, CHECK, NOT NULL and DEFAULT constraints
- Write INSERT/UPDATE/DELETE statements and reason about affected rows
- Normalize a flat dataset to 3NF with surrogate and composite keys
- Explain ACID and demonstrate COMMIT/ROLLBACK atomicity
- Run SQL scripts from Java via JDBC against H2 (MODE=PostgreSQL)

## Prerequisites

- Day 16–24 core Java background (collections, exceptions)
- Optional: `setup/POSTGRESQL_SETUP.md` to try the same scripts in psql

## How to use this folder

1. Read [`DAY-25-THEORY-AND-REFERENCE.md`](DAY-25-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-create-tables-constraints` | SQL script + JDBC test | `mvn test` |
| 2 | `task-02-insert-update-delete` | SQL script + JDBC test | `mvn test` |
| 3 | `task-03-normalization-keys` | SQL script + JDBC test | `mvn test` |
| 4 | `task-04-acid-transaction-demo` | SQL script + JDBC test | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** SQL/JDBC
