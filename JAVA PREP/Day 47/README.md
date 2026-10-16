# Day 47 — Capstone API Slice I: Authentication, Entities, and Relationships

## Learning objectives

- Implement registration with validation and BCrypt
- Explain and implement JWT issue/verify (and its attack surface)
- Map User-Project-Task relationships with correct ownership and cascade
- Express and test a URL security rules matrix
- Prepare the structure that Project 01/02 will reuse

## Prerequisites

- Days 31-40 REST, JPA, Security
- Day 45-46 optional (events)

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-47-THEORY-AND-REFERENCE.md`](DAY-47-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-user-registration` | Spring Boot (JPA + Security) | `mvn test` |
| 2 | `task-02-jwt-token-service` | Spring Boot (security concepts) | `mvn test` |
| 3 | `task-03-project-task-relationships` | Spring Boot (JPA) | `mvn test` |
| 4 | `task-04-security-rules-matrix` | Spring Boot (Security) | `mvn test` |

**Estimated time:** 2-3 h theory + 5-7 h tasks  
**Phase:** Capstone
