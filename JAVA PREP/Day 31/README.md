# Day 31 — REST II: DTOs, Bean Validation, Error Handling and Layered Design

## Learning objectives

- Model requests/responses with DTO records
- Validate input with Bean Validation and write custom constraints
- Translate exceptions to ProblemDetail with @RestControllerAdvice
- Organize code in controller/service/repository/mapper layers

## Prerequisites

- Day 30 REST I

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-31-THEORY-AND-REFERENCE.md`](DAY-31-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-create-user-validation` | Spring Boot | `mvn test` |
| 2 | `task-02-problem-detail-advice` | Spring Boot | `mvn test` |
| 3 | `task-03-layered-todo-service` | Spring Boot | `mvn test` |
| 4 | `task-04-custom-constraints` | Spring Boot | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
