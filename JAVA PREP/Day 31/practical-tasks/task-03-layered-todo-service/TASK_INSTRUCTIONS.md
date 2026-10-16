# Task 3 — Layered Architecture: Controller, Service, Repository, Mapper

**Day:** 31 · **Task ID:** Day31-task03 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Implement the business and mapping layers of a todo API so HTTP concerns, rules and storage stay separate.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day31/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task03/Todo.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task03/TodoDto.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task03/TodoRepository.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task03/DuplicateTodoException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task03/TodoNotFoundException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task03/TodoMapper.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day31/task03/TodoService.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day31/task03/TodoController.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day31/task03/TodoServiceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 31 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `TodoMapper.toDto`.
2. Implement `TodoService.create`, `complete`, `list` with the documented rules and exceptions.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day31-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day31-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 31: complete task-03-layered-todo-service`.

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
| `TodoMapper.java` | `Day31-task03` | map to TodoDto with status DONE or OPEN |
| `TodoService.java` | `Day31-task03` | validate, reject duplicates (ignore case), save and map |
| `TodoService.java` | `Day31-task03` | load, check state, save the done copy and map |
| `TodoService.java` | `Day31-task03` | map all (or only open) todos |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `createTrimsAndStartsOpen` |
| 3 | `blankTitleRejected` |
| 4 | `duplicateIgnoringCaseRejected` |
| 5 | `completeFlow` |
| 6 | `listCanFilterOpen` |
| 7 | `controllerDependsOnServiceOnly` |

## Edge cases to handle

- Duplicate detection ignores case and surrounding whitespace.
- A second `complete` fails with `IllegalStateException`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 31: Layered Architecture: Controller, Service, Repository, Mapper`

## Hints (optional)

<details><summary>Hint 1</summary>
Keep rules in the service, not the controller.
</details>

<details><summary>Hint 2</summary>
Records are immutable: save a new `Todo` copy with `done=true`.
</details>
