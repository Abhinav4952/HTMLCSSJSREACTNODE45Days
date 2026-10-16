# Task 2 — @Around: Timing and Argument Rewriting

**Day:** 40 · **Task ID:** Day40-task02 · **Type:** Spring AOP · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Use around advice for cross-cutting timing (with try/finally) and to rewrite method arguments before proceeding.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day40/task02/AopConfig.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task02/Timed.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task02/MetricsRegistry.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task02/ReportService.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task02/TextService.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task02/TimingAspect.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day40/task02/TrimAspect.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day40/task02/AroundAdviceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 40 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `TimingAspect` (annotation-driven pointcut, always record).
2. Implement `TrimAspect` and pass modified arguments to `proceed`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day40-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day40-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 40: complete task-02-around-timing-and-args`.

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
| `TimingAspect.java` | `Day40-task02` | make this an aspect bean |
| `TimingAspect.java` | `Day40-task02` | @Around on methods annotated with Timed (pointcut: @annotation(com.javaprep.day40.task02.Timed |
| `TimingAspect.java` | `Day40-task02` | time pjp.proceed() in try/finally and record under pjp.getSignature().getName( |
| `TrimAspect.java` | `Day40-task02` | make this an aspect bean |
| `TrimAspect.java` | `Day40-task02` | @Around with execution(* com.javaprep.day40.task02.TextService.*(String |
| `TrimAspect.java` | `Day40-task02` | copy args, trim strings, proceed with the new arguments |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `start` |
| 2 | `stop` |
| 3 | `timedMethodIsMeasuredAndResultPassesThrough` |
| 4 | `exceptionsAreRecordedAndRethrownUnchanged` |
| 5 | `untimedMethodsAreNotRecorded` |
| 6 | `stringArgumentsAreTrimmedByAroundAdvice` |
| 7 | `otherSignaturesAreUntouched` |

## Edge cases to handle

- Always call `proceed()` exactly once unless you intentionally short-circuit.
- Rethrow exceptions; never swallow them in an around advice.
- `pjp.getArgs()` returns a copy-safe array but modify a clone for clarity.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 40: @Around: Timing and Argument Rewriting`

## Hints (optional)

<details><summary>Hint 1</summary>
`try/finally` guarantees the metric is recorded on failure.
</details>

<details><summary>Hint 2</summary>
`pjp.proceed(Object[])` replaces the arguments.
</details>
