# Task 1 — Before, AfterReturning, AfterThrowing and After

**Day:** 40 · **Task ID:** Day40-task01 · **Type:** Spring AOP · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Write an @Aspect with the four classic advice types and observe their order for success and failure.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day40/task01/AopConfig.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task01/CallRecorder.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task01/OrderService.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task01/AuditAspect.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day40/task01/AdviceTypesTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 40 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Mark `AuditAspect` as an aspect and bean.
2. Annotate the four advice methods and implement the recorded messages.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day40-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day40-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 40: complete task-01-advice-types-order-service`.

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
| `AuditAspect.java` | `Day40-task01` | declare this class as an aspect and a Spring bean (@Aspect + @Component |
| `AuditAspect.java` | `Day40-task01` | run before orderOps( |
| `AuditAspect.java` | `Day40-task01` | record before:<method> |
| `AuditAspect.java` | `Day40-task01` | run after normal return, binding the result to the parameter named result |
| `AuditAspect.java` | `Day40-task01` | record returned:<method>=<result> |
| `AuditAspect.java` | `Day40-task01` | run after an exception, binding it to the parameter named ex |
| `AuditAspect.java` | `Day40-task01` | record threw:<method>:<exception simple class name> |
| `AuditAspect.java` | `Day40-task01` | run after the method no matter how it ended |
| `AuditAspect.java` | `Day40-task01` | record finally:<method> |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `start` |
| 2 | `stop` |
| 3 | `serviceIsProxied` |
| 4 | `normalCallRunsBeforeReturnedAndFinally` |
| 5 | `failingCallRunsBeforeThrewAndFinally` |
| 6 | `adviceDoesNotRunForOtherBeans` |

## Edge cases to handle

- `@AfterReturning` must not run when an exception escapes; `@AfterThrowing` must not run on success.
- `@After` always runs (like `finally`).
- Aspects only apply to Spring beans called through the proxy.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 40: Before, AfterReturning, AfterThrowing and After`

## Hints (optional)

<details><summary>Hint 1</summary>
`returning`/`throwing` names must match the advice method parameter names.
</details>

<details><summary>Hint 2</summary>
`JoinPoint#getSignature().getName()` gives the method name.
</details>
