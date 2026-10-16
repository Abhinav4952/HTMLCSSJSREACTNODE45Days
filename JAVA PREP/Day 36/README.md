# Day 36 — OpenAPI, RestClient and CORS

## Learning objectives

- Generate OpenAPI documents with springdoc and enrich them
- Call remote services with RestClient and handle failures
- Test HTTP clients with MockRestServiceServer
- Configure and verify CORS policies

## Prerequisites

- Day 30-31 REST
- Day 35 transactions (for context)

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-36-THEORY-AND-REFERENCE.md`](DAY-36-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-springdoc-openapi-docs` | Spring Boot | `mvn test` |
| 2 | `task-02-rest-client-basics` | Spring Boot | `mvn test` |
| 3 | `task-03-cors-policy` | Spring Boot | `mvn test` |
| 4 | `task-04-quote-gateway-challenge` | Spring Boot | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
