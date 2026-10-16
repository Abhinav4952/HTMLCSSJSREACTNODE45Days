# Day 44 — API Gateway, Filters, and Configuration Across Services

## Learning objectives

- Explain the gateway pattern and what belongs at the edge
- Model routes, predicates and filter chains
- Implement StripPrefix/AddHeader/Rewrite style filters
- Build API-key authentication and rate limiting as ordered filters
- Describe config sharing (profiles, Config Server concept)

## Prerequisites

- Day 43 Microservices and Resilience4j

## How to use this folder

1. Read [`DAY-44-THEORY-AND-REFERENCE.md`](DAY-44-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-route-matching` | Java | `mvn test` |
| 2 | `task-02-filter-chain` | Java | `mvn test` |
| 3 | `task-03-header-and-rewrite-filters` | Java | `mvn test` |
| 4 | `task-04-gateway-auth-rate-limit-challenge` | Java | `mvn test` |

**Estimated time:** 2-3 h theory + 4-6 h tasks  
**Phase:** Microservices
