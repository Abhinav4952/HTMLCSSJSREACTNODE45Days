# Day 30 — REST I: Controllers, Mappings, Request Binding, ResponseEntity and Jackson

## Learning objectives

- Write @RestController classes with the right mapping annotations
- Bind path variables, query parameters, headers and JSON bodies
- Control status codes and headers with ResponseEntity
- Shape JSON output with Jackson annotations
- Test controllers with MockMvc

## Prerequisites

- Day 29 Spring Boot starters and configuration

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-30-THEORY-AND-REFERENCE.md`](DAY-30-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-greeting-endpoints` | Spring Boot | `mvn test` |
| 2 | `task-02-books-response-entity` | Spring Boot | `mvn test` |
| 3 | `task-03-jackson-event-contract` | Spring Boot | `mvn test` |
| 4 | `task-04-notes-search-and-update` | Spring Boot | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
