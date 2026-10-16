# Task 3 — Global Error Contract (ProblemDetail)

**Day:** 48 · **Task ID:** Day48-task03 · **Type:** Spring Boot (Web) · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Replace ad-hoc error responses with one RFC 9457 `ProblemDetail` contract: consistent fields, field-level validation errors and no information leaks.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day48/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task03/NotFoundException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task03/ForbiddenException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task03/ThingController.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task03/GlobalExceptionHandler.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day48/task03/ErrorContractTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 48 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. 404 and 403 handlers with status/title/detail.
2. Validation handler with an `errors` object (field -> message).
3. Malformed JSON handler with a generic detail.
4. Catch-all 500 handler that logs and returns a generic message.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day48-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day48-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 48: complete task-03-error-contract`.

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
| `GlobalExceptionHandler.java` | `Day48-task03` | ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ...) + title |
| `GlobalExceptionHandler.java` | `Day48-task03` | 403 problem detail |
| `GlobalExceptionHandler.java` | `Day48-task03` | collect ex.getBindingResult().getFieldErrors() into a LinkedHashMap and setProperty("errors", map |
| `GlobalExceptionHandler.java` | `Day48-task03` | 400 problem detail |
| `GlobalExceptionHandler.java` | `Day48-task03` | log the exception, return a generic 500 problem detail |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `okPathStillWorks` |
| 2 | `notFoundIsAProblemDetail` |
| 3 | `forbiddenIsAProblemDetail` |
| 4 | `unexpectedErrorsDoNotLeakDetails` |
| 5 | `validationErrorsListFields` |
| 6 | `malformedJsonIs400WithoutParserDetails` |

## Edge cases to handle

- Secret text inside exception messages.
- Several violations on one field (keep the first).
- Specific handlers must win over the catch-all.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 48: Global Error Contract (ProblemDetail)`

## Hints (optional)

<details><summary>Hint 1</summary>
`ProblemDetail.forStatusAndDetail(HttpStatus.X, detail)` then `setTitle(...)`.
</details>

<details><summary>Hint 2</summary>
`HttpStatus.NOT_FOUND.getReasonPhrase()`.
</details>
