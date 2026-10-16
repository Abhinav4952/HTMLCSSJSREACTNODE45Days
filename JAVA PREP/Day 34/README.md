# Day 34 — Spring Data JPA III: Relationships, Cascade and Fetching

## Learning objectives

- Map 1:1, 1:N/N:1 and N:M relationships
- Explain owning vs inverse side and mappedBy
- Choose cascade, orphanRemoval and fetch strategies
- Verify mappings with @DataJpaTest, JdbcTemplate and PersistenceUnitUtil

## Prerequisites

- Day 33 queries and projections

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-34-THEORY-AND-REFERENCE.md`](DAY-34-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-one-to-one-profile` | Spring Boot | `mvn test` |
| 2 | `task-02-one-to-many-orders` | Spring Boot | `mvn test` |
| 3 | `task-03-many-to-many-enrollment` | Spring Boot | `mvn test` |
| 4 | `task-04-library-model-challenge` | Spring Boot | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
