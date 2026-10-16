# Task 2 — Global Errors with @RestControllerAdvice and ProblemDetail

**Day:** 31 · **Task ID:** Day31-task02 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Centralize error translation into RFC 9457 problem responses: 404, 409 and a 400 that lists field errors.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day31/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task02/ResourceNotFoundException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task02/DemoController.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task02/ApiExceptionHandler.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day31/task02/ApiExceptionHandlerTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 31 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Annotate `ApiExceptionHandler` as a controller advice and register the three handlers.
2. Build `ProblemDetail` bodies with the specified titles and details.
3. Expose per-field messages in an `errors` property.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day31-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day31-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 31: complete task-02-problem-detail-advice`.

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
| `ApiExceptionHandler.java` | `Day31-task02` | make this a global REST exception translator |
| `ApiExceptionHandler.java` | `Day31-task02` | register for ResourceNotFoundException |
| `ApiExceptionHandler.java` | `Day31-task02` | ProblemDetail.forStatusAndDetail(NOT_FOUND, message) with title "Not Found |
| `ApiExceptionHandler.java` | `Day31-task02` | register for IllegalStateException |
| `ApiExceptionHandler.java` | `Day31-task02` | build a 409 ProblemDetail |
| `ApiExceptionHandler.java` | `Day31-task02` | register for MethodArgumentNotValidException |
| `ApiExceptionHandler.java` | `Day31-task02` | collect field errors into a map and set it as property errors |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `notFoundBecomesProblemDetail` |
| 2 | `illegalStateBecomesConflict` |
| 3 | `validationFailureListsFieldErrors` |
| 4 | `happyPathUntouched` |

## Edge cases to handle

- Content type must be `application/problem+json`.
- Successful requests are unaffected.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 31: Global Errors with @RestControllerAdvice and ProblemDetail`

## Hints (optional)

<details><summary>Hint 1</summary>
`ProblemDetail.forStatusAndDetail(status, detail)`.
</details>

<details><summary>Hint 2</summary>
`ex.getBindingResult().getFieldErrors()` gives field + message.
</details>
