# Task 2 — CRUD with JpaRepository

**Day:** 32 · **Task ID:** Day32-task02 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Use the repository CRUD methods inside a transactional service: save, findById, existsById, deleteById, findAll, count and dirty checking.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day32/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day32/task02/Customer.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day32/task02/CustomerRepository.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day32/task02/CustomerService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day32/task02/CustomerServiceTest.java` | Provided helper or test (do not edit) |
| `src/test/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 32 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `create`, `get`, `rename`, `delete`, `all`, `count`.
2. `rename` must rely on dirty checking (no `save` call).
3. Unknown ids raise `NoSuchElementException` with the documented message.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day32-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day32-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 32: complete task-02-customer-crud-service`.

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
| `CustomerService.java` | `Day32-task02` | save a new Customer |
| `CustomerService.java` | `Day32-task02` | findById or throw NoSuchElementException |
| `CustomerService.java` | `Day32-task02` | load the managed entity and mutate it (dirty checking flushes the UPDATE |
| `CustomerService.java` | `Day32-task02` | check existence, then deleteById |
| `CustomerService.java` | `Day32-task02` | return every customer |
| `CustomerService.java` | `Day32-task02` | number of rows |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `createAssignsId` |
| 2 | `getUnknownThrows` |
| 3 | `renameUsesDirtyChecking` |
| 4 | `renameUnknownThrows` |
| 5 | `deleteRemovesRow` |
| 6 | `allAndCount` |

## Edge cases to handle

- `deleteById` on a missing id is silently ignored in Spring Data 3 — check with `existsById` first.
- Read methods use `readOnly = true`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 32: CRUD with JpaRepository`

## Hints (optional)

<details><summary>Hint 1</summary>
`findById` returns `Optional`.
</details>

<details><summary>Hint 2</summary>
Inside a transaction, a managed entity's changes are flushed automatically.
</details>
