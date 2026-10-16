# Task 3 — 401 vs 403 with JSON Handlers

**Day:** 38 · **Task ID:** Day38-task03 · **Type:** Spring Boot (Security + JWT) · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Wire the JWT filter into a stateless security chain and make unauthenticated (401) and unauthorized (403) failures distinguishable JSON responses.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day38/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day38/task03/JwtUtil.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day38/task03/JwtAuthFilter.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day38/task03/JwtConfig.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day38/task03/ApiController.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day38/task03/SecurityConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day38/task03/Status401Vs403Test.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 38 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement the entry point and the access-denied handler.
2. Assemble the filter chain: rules, stateless sessions, JWT filter placement, handlers.
3. State precisely when each status code is correct.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day38-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day38-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 38: complete task-03-status-401-vs-403`.

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
| `SecurityConfig.java` | `Day38-task03` | return an entry point that writes status 401 and the JSON body |
| `SecurityConfig.java` | `Day38-task03` | return a handler that writes status 403 and the JSON body |
| `SecurityConfig.java` | `Day38-task03` | wire csrf, sessions, exception handling, authorization rules and the JWT filter |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `publicIsOpen` |
| 2 | `noTokenIs401Json` |
| 3 | `garbageTokenIs401` |
| 4 | `userCanReadApiButNotAdmin` |
| 5 | `adminCanReadAdmin` |

## Edge cases to handle

- A syntactically broken token is an authentication failure -> 401.
- Role mismatch for an authenticated user is 403.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 38: 401 vs 403 with JSON Handlers`

## Hints (optional)

<details><summary>Hint 1</summary>
`exceptionHandling` registers both handlers.
</details>

<details><summary>Hint 2</summary>
`addFilterBefore` positions the JWT filter ahead of the username/password filter.
</details>
