# Task 4 — Independent Consumer Groups (Challenge)

**Day:** 45 · **Task ID:** Day45-task04 · **Type:** Spring Boot + Kafka · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Two services (billing and shipping) must each see every order event: give them different consumer groups, then reason about what would change if they shared a group.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day45/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/resources/application.yml` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day45/task04/ReceivedEvents.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day45/task04/BillingListener.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day45/task04/ShippingListener.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day45/task04/ConsumerGroupsTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 45 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Make `BillingListener.onMessage` a listener in group `billing` that records the record value.
2. Make `ShippingListener.onMessage` a listener in group `shipping` doing the same.
3. Explain in your commit message (or a short comment) what would happen if both used the same group id.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day45-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day45-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 45: complete task-04-consumer-groups-challenge`.

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
| `BillingListener.java` | `Day45-task04` | @KafkaListener(topics = TOPIC, groupId = "billing |
| `BillingListener.java` | `Day45-task04` | record the value |
| `ShippingListener.java` | `Day45-task04` | @KafkaListener(topics = TOPIC, groupId = "shipping |
| `ShippingListener.java` | `Day45-task04` | record the value |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `everyGroupReceivesEveryMessage` |

## Edge cases to handle

- Same group = messages are split between members (competing consumers); different groups = each group gets all messages.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 45: Independent Consumer Groups (Challenge)`

## Hints (optional)

<details><summary>Hint 1</summary>
The listener classes already own their collectors.
</details>

<details><summary>Hint 2</summary>
Both listeners subscribe to the same topic.
</details>
