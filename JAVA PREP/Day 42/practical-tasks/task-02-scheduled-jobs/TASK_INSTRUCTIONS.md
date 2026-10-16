# Task 2 — @Scheduled: Fixed Delay, Cron and Property-Driven Rates

**Day:** 42 · **Task ID:** Day42-task02 · **Type:** Spring Boot (Async / Scheduling / Cache) · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Declare scheduled jobs with fixedDelay, cron with a time zone and a fixedRate resolved from a property placeholder, and verify them through the scheduler registry.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day42/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day42/task02/SchedulingConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day42/task02/Jobs.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day42/task02/SchedulingTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 42 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Enable scheduling.
2. Add the three `@Scheduled` annotations exactly as documented and implement the three job bodies.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day42-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day42-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 42: complete task-02-scheduled-jobs`.

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
| `SchedulingConfig.java` | `Day42-task02` | switch on scheduled task processing (@EnableScheduling |
| `Jobs.java` | `Day42-task02` | @Scheduled(fixedDelay = 5000, initialDelay = 60000 |
| `Jobs.java` | `Day42-task02` | count a beat |
| `Jobs.java` | `Day42-task02` | @Scheduled with the cron expression and zone UTC |
| `Jobs.java` | `Day42-task02` | count a cleanup |
| `Jobs.java` | `Day42-task02` | @Scheduled(fixedRateString = "${jobs.refresh-rate:60000}", initialDelay = 60000 |
| `Jobs.java` | `Day42-task02` | count a refresh |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `threeTasksAreRegistered` |
| 2 | `fixedDelayTask` |
| 3 | `cronTaskAtTwoAmUtc` |
| 4 | `fixedRateComesFromThePropertyPlaceholder` |
| 5 | `jobBodiesDoRealWork` |
| 6 | `methodsCarryScheduledAnnotations` |

## Edge cases to handle

- `fixedDelay` waits after completion; `fixedRate` starts at fixed intervals even if runs overlap.
- Cron has six fields in Spring: second minute hour day month weekday.
- Scheduled methods must be void and take no arguments.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 42: @Scheduled: Fixed Delay, Cron and Property-Driven Rates`

## Hints (optional)

<details><summary>Hint 1</summary>
`fixedRateString` accepts placeholders.
</details>

<details><summary>Hint 2</summary>
A long `initialDelay` keeps jobs from firing during the test.
</details>
