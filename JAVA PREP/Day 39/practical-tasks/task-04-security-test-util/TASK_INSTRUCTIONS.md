# Task 4 — Reusable Security Test Helpers

**Day:** 39 · **Task ID:** Day39-task04 · **Type:** Spring Boot (Testing) · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Write a small test-support class around spring-security-test post-processors, then use it to test a secured controller with CSRF enabled.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day39/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day39/task04/NoteController.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day39/task04/AppSecurityConfig.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day39/task04/SecurityTestSupport.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day39/task04/SecurityTestSupportTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 39 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement the four helper methods in `SecurityTestSupport`.
2. Notice the stub lives in `src/test/java`: helpers are test code, not production code.
3. Add a helper of your own, e.g. `asRole(String...)`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day39-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day39-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 39: complete task-04-security-test-util`.

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
| (see sources) | `TODO(Day39-task04)` | implement |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `anonymousIs401` |
| 2 | `userHelperSetsPrincipal` |
| 3 | `userIsNotAdmin` |
| 4 | `adminHelperOpensAdmin` |
| 5 | `postWithoutCsrfIsForbidden` |
| 6 | `postWithCsrfHelperWorks` |
| 7 | `basicHelperAuthenticatesRealUser` |

## Edge cases to handle

- POSTs fail with 403 unless a CSRF token accompanies the request.
- Wrong Basic credentials give 401 (authentication), a missing role gives 403.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 39: Reusable Security Test Helpers`

## Hints (optional)

<details><summary>Hint 1</summary>
`user(name).roles(..)` fabricates an authentication without a UserDetailsService lookup.
</details>

<details><summary>Hint 2</summary>
`csrf()` adds a valid token for the request.
</details>
