# Task 4 — Aspect Ordering with @Order

**Day:** 40 · **Task ID:** Day40-task04 · **Type:** Spring AOP · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Combine two around aspects on a shared named pointcut and control their nesting with @Order.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day40/task04/AopConfig.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task04/CallRecorder.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task04/Pointcuts.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task04/PaymentService.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task04/SecurityAspect.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day40/task04/TxAspect.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day40/task04/AspectOrderingTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 40 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Make both classes aspect beans with explicit precedence (`@Order(1)` outer, `@Order(2)` inner).
2. Reference the shared pointcut `Pointcuts.payment()` from both advices.
3. Implement both around bodies so the recorded sequence is onion-shaped.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day40-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day40-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 40: complete task-04-aspect-ordering-challenge`.

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
| `SecurityAspect.java` | `Day40-task04` | aspect bean with the HIGHEST precedence of the two (@Order(1 |
| `SecurityAspect.java` | `Day40-task04` | @Around using the named pointcut Pointcuts.payment( |
| `SecurityAspect.java` | `Day40-task04` | record in, proceed, record out in finally |
| `TxAspect.java` | `Day40-task04` | aspect bean with LOWER precedence than SecurityAspect (@Order(2 |
| `TxAspect.java` | `Day40-task04` | @Around using the named pointcut Pointcuts.payment( |
| `TxAspect.java` | `Day40-task04` | begin, proceed, commit or rollback |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `start` |
| 2 | `stop` |
| 3 | `classBasedProxyBecausePaymentServiceHasNoInterface` |
| 4 | `successOrderIsOnionShaped` |
| 5 | `failureRollsBackInsideSecurity` |

## Edge cases to handle

- Lower `@Order` value = higher precedence = outermost.
- An exception must travel through `tx:rollback` first, then `security:out`.
- Without `@Order` the order is undefined.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 40: Aspect Ordering with @Order`

## Hints (optional)

<details><summary>Hint 1</summary>
Think of the aspects as nested try/finally blocks.
</details>

<details><summary>Hint 2</summary>
Named pointcuts from another class are referenced as `fully.qualified.Class.method()`.
</details>
