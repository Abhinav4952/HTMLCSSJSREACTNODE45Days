# Task 3 — Pointcut Expression Lab

**Day:** 40 · **Task ID:** Day40-task03 · **Type:** Spring AOP · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Practice AspectJ pointcut designators (execution, within, @annotation, boolean combinations) and verify them against real methods.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day40/task03/PointcutExpressions.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day40/task03/sample/Audited.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task03/sample/UserService.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task03/sample/OrderService.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day40/task03/sample/web/UserController.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day40/task03/PointcutExpressionsTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 40 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Write six pointcut expressions in `PointcutExpressions` according to their Javadoc.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day40-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day40-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 40: complete task-03-pointcut-expressions-lab`.

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
| `PointcutExpressions.java` | `Day40-task03` | execution(...) with a *Service type pattern |
| `PointcutExpressions.java` | `Day40-task03` | execution with any declaring type |
| `PointcutExpressions.java` | `Day40-task03` | execution with (*, |
| `PointcutExpressions.java` | `Day40-task03` | within(...) with a .. pattern |
| `PointcutExpressions.java` | `Day40-task03` | @annotation(... |
| `PointcutExpressions.java` | `Day40-task03` | boolean combination |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `allInServices` |
| 2 | `saveWithString` |
| 3 | `twoArguments` |
| 4 | `webLayer` |
| 5 | `audited` |
| 6 | `serviceLayerOnly` |

## Edge cases to handle

- `execution` matches method signatures; `within` matches the declaring type's package/class.
- `..` in a package pattern includes sub-packages; `.` alone does not.
- Spring AOP supports only method-execution join points on beans.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 40: Pointcut Expression Lab`

## Hints (optional)

<details><summary>Hint 1</summary>
Format: `execution(modifiers? return-type declaring-type?.name(params))`.
</details>

<details><summary>Hint 2</summary>
Combine with `&&`, `||`, `!`.
</details>
