# Day 45 — Kafka I: Producers, Consumers, and EmbeddedKafka

## Learning objectives

- Explain topics, partitions, offsets and keys
- Publish keyed events with `KafkaTemplate` and handle acknowledgements
- Consume with `@KafkaListener` and consumer groups
- Prove per-key ordering
- Test with `@EmbeddedKafka` without Docker

## Prerequisites

- Day 43-44 microservices
- Optional: `setup/KAFKA_SETUP.md` for manual labs (tests do not need it)

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-45-THEORY-AND-REFERENCE.md`](DAY-45-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-producer-kafka-template` | Spring Boot + Kafka | `mvn test` |
| 2 | `task-02-listener-kafka-listener` | Spring Boot + Kafka | `mvn test` |
| 3 | `task-03-keyed-partition-ordering` | Spring Boot + Kafka | `mvn test` |
| 4 | `task-04-consumer-groups-challenge` | Spring Boot + Kafka | `mvn test` |

**Estimated time:** 2-3 h theory + 4-6 h tasks  
**Phase:** Microservices (Kafka)
