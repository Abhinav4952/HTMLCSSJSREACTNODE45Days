# Day 46 — Kafka II: JSON Events, Dead Letters, Idempotency, and Outbox

## Learning objectives

- Design versioned JSON events with a tolerant reader
- Configure retries and a dead-letter topic
- Make consumers idempotent with a processed-events table
- Explain and simulate the transactional outbox
- Reason about delivery guarantees

## Prerequisites

- Day 45 Kafka I
- Day 25-27 JDBC and transactions

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-46-THEORY-AND-REFERENCE.md`](DAY-46-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-json-event-contract` | Spring Boot (Jackson) | `mvn test` |
| 2 | `task-02-poison-message-dlt` | Spring Boot + Kafka | `mvn test` |
| 3 | `task-03-idempotent-consumer` | Java + JDBC (H2) | `mvn test` |
| 4 | `task-04-transactional-outbox-challenge` | Java + JDBC (H2) | `mvn test` |

**Estimated time:** 2-3 h theory + 4-6 h tasks  
**Phase:** Microservices (Kafka)
