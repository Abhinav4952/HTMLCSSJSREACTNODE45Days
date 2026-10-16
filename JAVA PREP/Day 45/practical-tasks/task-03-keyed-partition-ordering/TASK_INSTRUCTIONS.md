# Task 3 — Keyed Partition Ordering

**Day:** 45 · **Task ID:** Day45-task03 · **Type:** Spring Boot + Kafka · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Prove Kafka's ordering guarantee: records with the same key go to the same partition and are read back in order, even on a 3-partition topic.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day45/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/resources/application.yml` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day45/task03/OrderedPublisher.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day45/task03/KafkaReader.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day45/task03/OrderedPublisherTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 45 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Send each value with the given key, in order.
2. Block on every send and collect `RecordMetadata.partition()`.
3. Return an empty list for empty input.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day45-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day45-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 45: complete task-03-keyed-partition-ordering`.

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
| `OrderedPublisher.java` | `Day45-task03` | loop over values, send with the key, block on each future, collect metadata.partition( |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `sameKeyAlwaysLandsOnOnePartition` |
| 2 | `perKeyOrderIsPreserved` |
| 3 | `emptyInputSendsNothing` |

## Edge cases to handle

- Without waiting you cannot know the partition.
- Ordering is only guaranteed per partition, not across partitions.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 45: Keyed Partition Ordering`

## Hints (optional)

<details><summary>Hint 1</summary>
`Integer` list via `new ArrayList<>()`.
</details>

<details><summary>Hint 2</summary>
Default partitioner hashes the key (murmur2) modulo partition count.
</details>
