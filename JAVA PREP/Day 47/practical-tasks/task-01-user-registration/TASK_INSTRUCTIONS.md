# Task 1 — User Registration Service

**Day:** 47 · **Task ID:** Day47-task01 · **Type:** Spring Boot (JPA + Security) · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

First slice of the capstone API: register users with validation, normalized emails, duplicate detection and BCrypt-hashed passwords.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day47/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task01/User.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task01/UserRepository.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task01/RegisterRequest.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task01/UserResponse.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task01/DuplicateEmailException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task01/BeansConfig.java` | Provided helper or test (do not edit) |
| `src/main/resources/application.yml` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task01/RegistrationService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day47/task01/RegistrationServiceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 47 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Validate email, password length (>= 8) and display name.
2. Normalize the email (trim + lower-case).
3. Reject duplicates with `DuplicateEmailException`.
4. Hash the password with the injected `PasswordEncoder`; never return it.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day47-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day47-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 47: complete task-01-user-registration`.

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
| `RegistrationService.java` | `Day47-task01` | validate, normalise, check duplicates, encode the password, save, map to UserResponse |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `clean` |
| 2 | `registersAndNormalisesEmail` |
| 3 | `passwordIsStoredAsBcryptHash` |
| 4 | `duplicateEmailIsRejectedCaseInsensitively` |
| 5 | `invalidInputIsRejected` |

## Edge cases to handle

- Case-variants of the same email.
- Whitespace-only display name.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 47: User Registration Service`

## Hints (optional)

<details><summary>Hint 1</summary>
`users.existsByEmail(normalized)`.
</details>

<details><summary>Hint 2</summary>
`new User(email, encoder.encode(password), displayName)`.
</details>
