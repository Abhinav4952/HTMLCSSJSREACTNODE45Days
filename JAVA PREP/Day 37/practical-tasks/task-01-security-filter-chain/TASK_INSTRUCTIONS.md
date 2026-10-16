# Task 1 — SecurityFilterChain: Rules, Basic Auth and Stateless Mode

**Day:** 37 · **Task ID:** Day37-task01 · **Type:** Spring Boot · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Replace Boot's default security with your own SecurityFilterChain: path rules, role checks, HTTP Basic, CSRF off and stateless sessions.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day37/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day37/task01/DemoController.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day37/task01/SecurityConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day37/task01/FilterChainTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 37 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `SecurityConfig.filterChain` with the documented rules.
2. Make anonymous requests answer 401 with a Basic challenge.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day37-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day37-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 37: complete task-01-security-filter-chain`.

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
| `SecurityConfig.java` | `Day37-task01` | configure csrf, sessionManagement (STATELESS), authorizeHttpRequests and httpBasic, then return http.build( |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `publicPathsAreOpen` |
| 2 | `anonymousGets401WithBasicChallenge` |
| 3 | `unknownPathsAreProtectedToo` |
| 4 | `authenticatedUserSeesOwnName` |
| 5 | `plainUserCannotEnterAdminArea` |
| 6 | `adminCanEnterAdminArea` |
| 7 | `postWorksWithoutCsrfTokenForStatelessApi` |

## Edge cases to handle

- Rule order matters: the first matching rule wins.
- Without `httpBasic` anonymous requests get 403 (no entry point).
- Disabling CSRF is only acceptable for stateless token/basic APIs, never for browser session apps.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 37: SecurityFilterChain: Rules, Basic Auth and Stateless Mode`

## Hints (optional)

<details><summary>Hint 1</summary>
`requestMatchers("/admin/**").hasRole("ADMIN")` checks authority `ROLE_ADMIN`.
</details>

<details><summary>Hint 2</summary>
`anyRequest().authenticated()` must come last.
</details>
