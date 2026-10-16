# Task 4 — Virtual Threads in Spring Boot

**Day:** 42 · **Task ID:** Day42-task04 · **Type:** Spring Boot (Async / Scheduling / Cache) · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Turn on virtual threads with one property, prove it through an @Async probe, and use Java 21 virtual-thread executors and factories directly.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day42/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day42/task04/ThreadProbe.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day42/task04/VirtualThreadRunner.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day42/task04/VirtualThreadsTest.java` | Provided helper or test (do not edit) |
| `src/main/resources/application.properties` | Stubs / starter code (edit the TODOs) |

## Prerequisites

- Day 42 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Set the Spring Boot property in `src/main/resources/application.properties`.
2. Implement `runAll`, `namedFactory` and `onVirtualThread` with Java 21 APIs.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day42-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day42-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 42: complete task-04-virtual-threads-in-boot`.

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
| `VirtualThreadRunner.java` | `Day42-task04` | use try-with-resources on the executor, invokeAll, then collect future.get() in order |
| `VirtualThreadRunner.java` | `Day42-task04` | Thread.ofVirtual().name(prefix, 0).factory( |
| `VirtualThreadRunner.java` | `Day42-task04` | ask the current thread |
| `application.properties` | `Day42-task04` | make Spring Boot run its task executors (and Tomcat request threads) on virtual threads (Java 21+). |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `propertyEnablesVirtualThreads` |
| 2 | `asyncWorkRunsOnVirtualThreads` |
| 3 | `runAllKeepsInputOrderAndUsesVirtualThreads` |
| 4 | `thousandsOfBlockingTasksAreCheap` |
| 5 | `namedFactoryCreatesNamedVirtualThreads` |
| 6 | `testThreadIsPlatformThread` |

## Edge cases to handle

- Virtual threads help with blocking I/O, not CPU-bound work.
- Do not pool virtual threads; create one per task.
- `synchronized` blocks around blocking calls can pin carrier threads in Java 21 (prefer `ReentrantLock`).

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 42: Virtual Threads in Spring Boot`

## Hints (optional)

<details><summary>Hint 1</summary>
`Executors.newVirtualThreadPerTaskExecutor()` is an `AutoCloseable` ExecutorService.
</details>

<details><summary>Hint 2</summary>
`Thread.ofVirtual().name(prefix, start).factory()`.
</details>
