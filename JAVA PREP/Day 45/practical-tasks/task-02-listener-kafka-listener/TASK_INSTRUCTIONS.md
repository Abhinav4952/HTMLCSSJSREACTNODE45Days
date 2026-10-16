# Task 2 — Consumer with @KafkaListener

**Day:** 45 · **Task ID:** Day45-task02 · **Type:** Spring Boot + Kafka · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Turn a plain method into a Kafka consumer with `@KafkaListener`, using a consumer group, and assert the records arrive in order.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day45/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/resources/application.yml` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day45/task02/ReceivedEvents.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day45/task02/ReceivedConfig.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day45/task02/OrderListener.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day45/task02/OrderListenerTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 45 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Annotate `onMessage` with `@KafkaListener(topics = TOPIC, groupId = "audit")`.
2. Store `key=value` for every record.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day45-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day45-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 45: complete task-02-listener-kafka-listener`.

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
| `OrderListener.java` | `Day45-task02` | make this method a Kafka listener: @KafkaListener(topics = TOPIC, groupId = "audit |
| `OrderListener.java` | `Day45-task02` | received.add(record.key() + "=" + record.value( |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `listenerReceivesRecordsInOrder` |

## Edge cases to handle

- Listener starts after the first message was sent: `auto-offset-reset: earliest` (provided) handles this.
- Order is preserved inside one partition.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 45: Consumer with @KafkaListener`

## Hints (optional)

<details><summary>Hint 1</summary>
Import `org.springframework.kafka.annotation.KafkaListener`.
</details>

<details><summary>Hint 2</summary>
Boot enables listener annotations automatically when spring-kafka is on the classpath.
</details>
