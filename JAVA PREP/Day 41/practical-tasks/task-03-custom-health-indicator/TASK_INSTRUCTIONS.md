# Task 3 — Custom Actuator HealthIndicator

**Day:** 41 · **Task ID:** Day41-task03 · **Type:** Spring Boot (Observability) · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Contribute your own component to /actuator/health with status mapping, details and HTTP 503 semantics.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day41/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day41/task03/QueueStats.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day41/task03/QueueHealthIndicator.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day41/task03/QueueHealthTest.java` | Provided helper or test (do not edit) |
| `src/main/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 41 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Register `QueueHealthIndicator` as a bean named `queueHealthIndicator` (shown as component `queue`).
2. Map queue depth to UP / OUT_OF_SERVICE / DOWN and add details.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day41-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day41-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 41: complete task-03-custom-health-indicator`.

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
| `QueueHealthIndicator.java` | `Day41-task03` | register as a Spring bean so Actuator picks it up as the component named "queue |
| `QueueHealthIndicator.java` | `Day41-task03` | choose status by depth and add the two details |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `reset` |
| 2 | `unitLevelStatusMapping` |
| 3 | `detailsAreAlwaysPresent` |
| 4 | `healthyQueueGivesHttp200AndComponentUp` |
| 5 | `drainingQueueGivesHttp503` |
| 6 | `fullQueueMakesTheApplicationDown` |

## Edge cases to handle

- The component name is the bean name without the `HealthIndicator` suffix.
- Health checks must be fast and must not throw; exceptions turn into DOWN.
- Aggregate status: the worst component wins.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 41: Custom Actuator HealthIndicator`

## Hints (optional)

<details><summary>Hint 1</summary>
`Health.up()`, `Health.outOfService()`, `Health.down()` return builders.
</details>

<details><summary>Hint 2</summary>
OUT_OF_SERVICE and DOWN map to HTTP 503 by default.
</details>
