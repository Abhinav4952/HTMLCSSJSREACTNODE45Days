# Task 1 — Producer with KafkaTemplate

**Day:** 45 · **Task ID:** Day45-task01 · **Type:** Spring Boot + Kafka · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Publish keyed String events with `KafkaTemplate`, wait for the broker acknowledgement and verify with an `EmbeddedKafka` broker (no Docker, no local Kafka).

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day45/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/resources/application.yml` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day45/task01/EventPublisher.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day45/task01/KafkaReader.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day45/task01/EventPublisherTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 45 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Reject `null` values with `IllegalArgumentException`.
2. Send to `TOPIC` with the given key.
3. Block on the returned future (<= 10 s) and return the `RecordMetadata`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day45-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day45-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 45: complete task-01-producer-kafka-template`.

## How to run and verify

```bash
java -version   # 21.x
mvn -v          # 3.9+
mvn test        # expected RED at the start
mvn -Dtest=<TestClass> test
```

## TODO map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `EventPublisher.java` | `Day45-task01` | validate, kafkaTemplate.send(TOPIC, key, value), block on the future with a timeout |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `publishReturnsMetadataForTheTopic` |
| 2 | `recordArrivesWithKeyAndValue` |
| 3 | `nullValueIsRejected` |

## Edge cases to handle

- Broker slow to answer -> timeout exception.
- Null key is allowed (round-robin partitioning).

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 45: Producer with KafkaTemplate`

## Hints (optional)

<details><summary>Hint 1</summary>
`kafkaTemplate.send(...)` returns a `CompletableFuture<SendResult>` in Spring Kafka 3.x.
</details>

<details><summary>Hint 2</summary>
`future.get(10, TimeUnit.SECONDS).getRecordMetadata()`.
</details>
