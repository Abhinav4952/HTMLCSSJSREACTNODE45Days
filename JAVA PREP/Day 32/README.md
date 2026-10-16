# Day 32 — Spring Data JPA I: Entities, Repositories, CRUD and Datasource

## Learning objectives

- Map entities with JPA annotations
- Use JpaRepository CRUD inside transactional services
- Explain persistence context and dirty checking
- Configure datasource and choose ddl-auto vs SQL scripts
- Test persistence with @DataJpaTest on H2 (PostgreSQL mode)

## Prerequisites

- Day 31 REST II
- Days 22-24 SQL and JDBC basics

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-32-THEORY-AND-REFERENCE.md`](DAY-32-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-book-entity-mapping` | Spring Boot | `mvn test` |
| 2 | `task-02-customer-crud-service` | Spring Boot | `mvn test` |
| 3 | `task-03-schema-sql-validate` | Spring Boot | `mvn test` |
| 4 | `task-04-datasource-properties-lab` | Spring Boot | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
