# Task 2 — Books API with ResponseEntity

**Day:** 30 · **Task ID:** Day30-task02 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Implement list/get/create/delete endpoints using ResponseEntity to control status codes and the Location header.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day30/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day30/task02/Book.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day30/task02/BookService.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day30/task02/CreateBookRequest.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day30/task02/BookController.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day30/task02/BookControllerTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 30 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `list`, `get`, `create`, `delete` in `BookController`.
2. `create` must return 201 with `Location: /api/books/{id}` and the created book.
3. Unknown ids must produce 404 for `get` and `delete`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day30-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day30-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 30: complete task-02-books-response-entity`.

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
| `BookController.java` | `Day30-task02` | return all books |
| `BookController.java` | `Day30-task02` | 200 with the book or 404 (ResponseEntity.notFound |
| `BookController.java` | `Day30-task02` | create the book and answer 201 Created with a Location header and the book as body |
| `BookController.java` | `Day30-task02` | 204 No Content when removed, otherwise 404 |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `create` |
| 2 | `emptyListInitially` |
| 3 | `createReturns201WithLocation` |
| 4 | `getExistingAndMissing` |
| 5 | `listContainsCreatedBooks` |
| 6 | `deleteIs204ThenMissingIs404` |
| 7 | `malformedJsonIs400` |

## Edge cases to handle

- Malformed JSON body -> 400 (handled by Spring).
- `delete` twice: 204 then 404.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 30: Books API with ResponseEntity`

## Hints (optional)

<details><summary>Hint 1</summary>
`ResponseEntity.created(URI).body(x)`.
</details>

<details><summary>Hint 2</summary>
`ResponseEntity.notFound().build()` has no body.
</details>
