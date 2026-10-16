# Day 48 — Capstone API Slice II: Ownership, Pagination, Errors, and Tests

## Learning objectives

- Enforce owner-only access with an explicit 403/404 policy
- Implement paged, sorted, owner-scoped search with whitelisting
- Return a single ProblemDetail-based error contract without leaks
- Integrate ownership checks with JPA services (rename/delete) and validation order
- Apply the test pyramid (unit, slice, integration)

## Prerequisites

- Day 47 Capstone slice I
- Day 38 Spring Security basics

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-48-THEORY-AND-REFERENCE.md`](DAY-48-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-ownership-guard` | Java | `mvn test` |
| 2 | `task-02-paged-note-search` | Spring Boot (JPA) | `mvn test` |
| 3 | `task-03-error-contract` | Spring Boot (Web) | `mvn test` |
| 4 | `task-04-note-service-ownership-challenge` | Spring Boot (JPA) | `mvn test` |

**Estimated time:** 2-3 h theory + 5-7 h tasks  
**Phase:** Capstone
