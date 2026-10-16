# Day 35 — Spring Data JPA IV: N+1, Transactions, Versioning, Auditing and Flyway

## Learning objectives

- Detect and fix N+1 problems
- Apply @Transactional with correct rollback rules
- Use @Version for optimistic locking
- Add JPA auditing
- Manage schema evolution with Flyway

## Prerequisites

- Day 34 relationships

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-35-THEORY-AND-REFERENCE.md`](DAY-35-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-n-plus-one-join-fetch` | Spring Boot | `mvn test` |
| 2 | `task-02-transactional-transfer` | Spring Boot | `mvn test` |
| 3 | `task-03-version-and-auditing` | Spring Boot | `mvn test` |
| 4 | `task-04-flyway-migrations` | Spring Boot | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
