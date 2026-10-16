# Task 2 — Poison Message and Dead-Letter Topic

**Day:** 46 · **Task ID:** Day46-task02 · **Type:** Spring Boot + Kafka · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Configure a `DefaultErrorHandler` with bounded retries and a `DeadLetterPublishingRecoverer` so one bad record cannot block a partition.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day46/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/resources/application.yml` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day46/task02/ReceivedEvents.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day46/task02/ReceivedConfig.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day46/task02/PaymentListener.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day46/task02/ErrorHandlingConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day46/task02/KafkaReader.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day46/task02/DeadLetterTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 46 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Create a `DeadLetterPublishingRecoverer` from the template (default destination `<topic>.DLT`, same partition).
2. Use `FixedBackOff(10L, 2L)`: two retries after the first failure.
3. Return a `DefaultErrorHandler(recoverer, backOff)`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day46-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day46-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 46: complete task-02-poison-message-dlt`.

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
| `ErrorHandlingConfig.java` | `Day46-task02` | DeadLetterPublishingRecoverer(template) + FixedBackOff(10L, 2L) -> new DefaultErrorHandler(recoverer, backOff |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `poisonMessageGoesToDltAndHealthyMessagesStillFlow` |

## Edge cases to handle

- The DLT must have at least as many partitions as the source topic.
- Healthy records after the poison one must still be processed.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 46: Poison Message and Dead-Letter Topic`

## Hints (optional)

<details><summary>Hint 1</summary>
`org.springframework.util.backoff.FixedBackOff`.
</details>

<details><summary>Hint 2</summary>
Spring Boot applies a `CommonErrorHandler` bean to the auto-configured listener container factory.
</details>
