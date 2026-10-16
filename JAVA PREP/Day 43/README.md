# Day 43 — Microservices, RestClient, and Resilience4j

## Learning objectives

- Explain when to split a system into services and how to size boundaries
- Call another service with `RestClient` and map failures
- Apply retry with backoff safely (idempotency)
- Configure and test a circuit breaker life cycle
- Design graceful degradation instead of cascading failures

## Prerequisites

- Day 31-33 REST + validation
- Day 40 Spring Boot testing basics

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-43-THEORY-AND-REFERENCE.md`](DAY-43-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-restclient-inventory-client` | Spring Boot | `mvn test` |
| 2 | `task-02-retry-with-backoff` | Java + Resilience4j | `mvn test` |
| 3 | `task-03-circuit-breaker-facade` | Java + Resilience4j | `mvn test` |
| 4 | `task-04-order-service-degradation-challenge` | Java | `mvn test` |

**Estimated time:** 2-3 h theory + 4-6 h tasks  
**Phase:** Microservices
