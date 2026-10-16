# Task 2 — A JWT Authentication Filter

**Day:** 38 · **Task ID:** Day38-task02 · **Type:** Spring Boot (Security + JWT) · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Write a OncePerRequestFilter that turns a Bearer token into a SecurityContext authentication — and never blocks the request itself.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day38/task02/JwtUtil.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day38/task02/JwtAuthFilter.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day38/task02/JwtAuthFilterTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 38 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `doFilterInternal`.
2. Prefix roles with `ROLE_` when creating authorities.
3. Always continue the chain; authorization happens later.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day38-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day38-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 38: complete task-02-jwt-filter`.

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
| `JwtAuthFilter.java` | `Day38-task02` | parse the header, validate the token, populate SecurityContextHolder, always call chain.doFilter |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `clear` |
| 2 | `validTokenAuthenticates` |
| 3 | `missingHeaderLeavesContextEmpty` |
| 4 | `invalidTokenDoesNotAuthenticateButContinues` |
| 5 | `otherSchemesAreIgnored` |

## Edge cases to handle

- Invalid tokens must not authenticate and must not crash the request.
- Non-Bearer schemes are ignored.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 38: A JWT Authentication Filter`

## Hints (optional)

<details><summary>Hint 1</summary>
`JwtUtil` is provided: do not edit it.
</details>

<details><summary>Hint 2</summary>
Do not register the filter as a `@Component` unless you also disable servlet auto-registration (it would run twice).
</details>
