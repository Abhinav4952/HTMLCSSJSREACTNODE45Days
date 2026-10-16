# Task 3 — Bean Lifecycle and Scope

**Day:** 28 · **Task ID:** Day28-task03 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Hook into construction, initialization and destruction with @PostConstruct/@PreDestroy and demonstrate singleton vs prototype scope.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day28/task03/LifecycleRecorder.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day28/task03/LifecycleBean.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day28/task03/ReportBuilder.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day28/task03/LifecycleConfig.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day28/task03/LifecycleTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 28 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `init` and `close` and register them as lifecycle callbacks.
2. Make `ReportBuilder` a prototype-scoped bean.
3. Explain the order constructor -> `@PostConstruct` -> use -> `@PreDestroy`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day28-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day28-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 28: complete task-03-bean-lifecycle`.

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
| `LifecycleBean.java` | `Day28-task03` | run this after dependency injection (@PostConstruct) and record "init |
| `LifecycleBean.java` | `Day28-task03` | run this on context shutdown (@PreDestroy) and record "destroy |
| `ReportBuilder.java` | `Day28-task03` | every injection/lookup must get a NEW instance (prototype scope |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `initAndDestroyRecordEvents` |
| 2 | `containerCallsCallbacksInOrder` |
| 3 | `singletonIsSharedPrototypeIsNot` |

## Edge cases to handle

- Callbacks must not run before the context has injected dependencies.
- `ctx.close()` triggers destroy callbacks for singletons only.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 28: Bean Lifecycle and Scope`

## Hints (optional)

<details><summary>Hint 1</summary>
Annotations live in `jakarta.annotation` (Spring Boot 3+).
</details>

<details><summary>Hint 2</summary>
Prototype beans are not destroyed by the container.
</details>
