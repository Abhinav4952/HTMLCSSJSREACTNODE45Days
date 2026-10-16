# Task 1 — Create User: DTOs and Bean Validation

**Day:** 31 · **Task ID:** Day31-task01 · **Type:** Spring Boot · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Protect a POST endpoint with Bean Validation constraints on a request DTO and return a password-free response DTO.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day31/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task01/CreateUserRequest.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day31/task01/UserResponse.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task01/UserController.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day31/task01/UserControllerTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 31 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Add constraints to `CreateUserRequest`.
2. Enable validation with `@Valid` in `UserController`.
3. Map the request to `UserResponse` (trim name, lowercase email, no password).

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day31-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day31-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 31: complete task-01-create-user-validation`.

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
| `CreateUserRequest.java` | `Day31-task01` | add @NotBlank |
| `CreateUserRequest.java` | `Day31-task01` | add @Email and @NotBlank |
| `CreateUserRequest.java` | `Day31-task01` | add @Min(18) and @Max(120 |
| `CreateUserRequest.java` | `Day31-task01` | add @Size(min = 8 |
| `UserController.java` | `Day31-task01` | trigger validation of the body with @Valid |
| `UserController.java` | `Day31-task01` | build a UserResponse from the request (no password) using ids.incrementAndGet( |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `validRequestCreatesUserWithoutPassword` |
| 2 | `blankNameRejected` |
| 3 | `badEmailRejected` |
| 4 | `ageBoundsRejected` |
| 5 | `shortPasswordRejected` |

## Edge cases to handle

- Missing validation -> the handler would run with bad data (NPE or silent success).
- Boundary ages 18 and 120 are valid.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 31: Create User: DTOs and Bean Validation`

## Hints (optional)

<details><summary>Hint 1</summary>
Constraints live on record components.
</details>

<details><summary>Hint 2</summary>
`@Valid` on the parameter triggers `MethodArgumentNotValidException` -> 400.
</details>
