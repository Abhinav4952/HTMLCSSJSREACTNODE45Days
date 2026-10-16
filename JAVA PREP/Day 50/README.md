# Day 50 — Interview Review: Core Java, Spring, and Timed Rounds

## Learning objectives

- Answer core Java, Spring, JPA, SQL and security questions precisely
- Solve collection/stream problems under time pressure
- Debug seeded defects in a Spring + JPA service
- Fix concurrency problems with atomics, locks and executors
- Reason about SQL queries and indexes; structure a system-design answer

## Prerequisites

- Days 1-49 (use the question bank as a self-test)

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-50-THEORY-AND-REFERENCE.md`](DAY-50-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-timed-collections-streams-45min` | Core Java | `mvn test` |
| 2 | `task-02-timed-spring-jpa-bug-hunt-60min` | Spring Boot (JPA) | `mvn test` |
| 3 | `task-03-timed-concurrency-fix-90min` | Core Java | `mvn test` |
| 4 | `task-04-timed-sql-reasoning-60min` | SQL + JDBC (H2) | `mvn test` |

**Estimated time:** 3-4 h review + 4 timed rounds (45/60/90/60 min)  
**Phase:** Capstone
