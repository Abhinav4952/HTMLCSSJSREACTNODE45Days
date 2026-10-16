# Day 41 — Observability: SLF4J/Logback, MDC, Actuator Health and Micrometer Metrics

## Learning objectives

- Log correctly with SLF4J levels and parameterized messages
- Correlate requests with MDC
- Write custom health indicators and understand status aggregation
- Instrument code with Micrometer meters
- Test logging and metrics without external systems

## Prerequisites

- Day 29 Actuator basics
- Day 36 RestClient/CORS

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-41-THEORY-AND-REFERENCE.md`](DAY-41-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-slf4j-logging-contract` | Spring Boot (Observability) | `mvn test` |
| 2 | `task-02-mdc-request-id-filter` | Spring Boot (Observability) | `mvn test` |
| 3 | `task-03-custom-health-indicator` | Spring Boot (Observability) | `mvn test` |
| 4 | `task-04-micrometer-order-metrics` | Spring Boot (Observability) | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
