# Task 4 — Users, Encoder and Role Rules Together

**Day:** 37 · **Task ID:** Day37-task04 · **Type:** Spring Boot · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Wire a PasswordEncoder, an in-memory user store and method-specific URL rules into a working Basic-auth API.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day37/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day37/task04/ReportController.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day37/task04/SecurityConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day37/task04/RoleRulesTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 37 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Define the `PasswordEncoder`, the `UserDetailsService` with two users and the `SecurityFilterChain`.
2. 403 for authenticated-but-forbidden, 401 for unauthenticated.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day37-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day37-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 37: complete task-04-role-rules-challenge`.

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
| `SecurityConfig.java` | `Day37-task04` | return a BCryptPasswordEncoder(4 |
| `SecurityConfig.java` | `Day37-task04` | InMemoryUserDetailsManager with the two users |
| `SecurityConfig.java` | `Day37-task04` | authorizeHttpRequests with HttpMethod-specific matchers; stateless; basic |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `publicIsOpen` |
| 2 | `anonymousIsRejected` |
| 3 | `wrongPasswordIsRejected` |
| 4 | `userCanReadReports` |
| 5 | `userCannotDelete` |
| 6 | `adminCanDelete` |
| 7 | `whoamiShowsAuthorities` |

## Edge cases to handle

- Store encoded passwords only.
- Matchers with an HTTP method are more specific than path-only ones: order them before `anyRequest()`.
- A defined `UserDetailsService` bean disables Boot's generated default user.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 37: Users, Encoder and Role Rules Together`

## Hints (optional)

<details><summary>Hint 1</summary>
`hasAnyRole("USER", "ADMIN")` accepts either.
</details>

<details><summary>Hint 2</summary>
`InMemoryUserDetailsManager` takes varargs of `UserDetails`.
</details>
