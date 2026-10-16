# Task 1 — SLF4J Logging Contract

**Day:** 41 · **Task ID:** Day41-task01 · **Type:** Spring Boot (Observability) · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Log with SLF4J levels and parameterized messages, attach exceptions correctly, and verify output with a Logback ListAppender.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day41/task01/OrderProcessor.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day41/task01/LoggingContractTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 41 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `OrderProcessor.process` following the numbered logging contract.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day41-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day41-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 41: complete task-01-slf4j-logging-contract`.

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
| `OrderProcessor.java` | `Day41-task01` | implement the logging contract |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `attach` |
| 2 | `detach` |
| 3 | `normalOrderLogsOneInfoLineWithParameters` |
| 4 | `largeOrdersWarn` |
| 5 | `invalidAmountLogsErrorWithStackTraceAndReturnsFalse` |
| 6 | `debugLineOnlyWhenDebugIsEnabled` |
| 7 | `messagesAreTemplatesNotConcatenated` |

## Edge cases to handle

- The exception must be the LAST argument so SLF4J prints the stack trace.
- Debug messages must be skipped when the level is INFO.
- Never log secrets or full payloads.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 41: SLF4J Logging Contract`

## Hints (optional)

<details><summary>Hint 1</summary>
`log.error("msg {}", arg, exception)` treats the final Throwable as the exception.
</details>

<details><summary>Hint 2</summary>
Parameterized messages avoid building strings when the level is disabled.
</details>
