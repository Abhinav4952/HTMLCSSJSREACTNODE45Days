# Day 27 — JDBC, PreparedStatement, DAO, HikariCP, and SQL Injection

## Learning objectives

- Write a DAO with try-with-resources over DataSource/Connection/PreparedStatement/ResultSet
- Demonstrate and prevent SQL injection with parameters and whitelists
- Implement atomic JDBC transactions with commit/rollback
- Read and validate HikariCP pool settings and build a HikariConfig
- Explain pool exhaustion and sizing

## Prerequisites

- Day 25–26 SQL fundamentals
- Exceptions and try-with-resources from earlier core Java days

## How to use this folder

1. Read [`DAY-27-THEORY-AND-REFERENCE.md`](DAY-27-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-jdbc-select-dao` | Plain Java + JDBC (H2) | `mvn test` |
| 2 | `task-02-prepared-statement-safe` | Plain Java + JDBC (H2) | `mvn test` |
| 3 | `task-03-transaction-transfer` | Plain Java + JDBC (H2) | `mvn test` |
| 4 | `task-04-hikari-config-reader` | Plain Java + JDBC (H2) | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** SQL/JDBC
