# Task 4 — Security Rules Matrix

**Day:** 47 · **Task ID:** Day47-task04 · **Type:** Spring Boot (Security) · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Write the `SecurityFilterChain` that protects the capstone API: public auth endpoints, admin-only area, authenticated everything else, stateless and CSRF-free, answering 401 vs 403 correctly.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day47/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task04/ProbeController.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task04/SecurityConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day47/task04/SecurityRulesTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 47 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Permit `/public/**` and `/api/auth/**`.
2. Require role `ADMIN` for `/api/admin/**`.
3. Require authentication for every other request.
4. Disable CSRF and use `SessionCreationPolicy.STATELESS`.
5. Enable HTTP Basic so anonymous requests receive 401.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day47-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day47-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 47: complete task-04-security-rules-matrix`.

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
| `SecurityConfig.java` | `Day47-task04` | http.csrf(...).sessionManagement(...).authorizeHttpRequests(...).httpBasic(...); return http.build( |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `publicEndpointsAreOpen` |
| 2 | `anonymousGets401OnProtectedEndpoints` |
| 3 | `userCanUseProtectedButNotAdminEndpoints` |
| 4 | `adminCanUseAdminEndpoints` |
| 5 | `postWorksWithoutCsrfToken` |

## Edge cases to handle

- 401 (not authenticated) vs 403 (authenticated but not allowed).
- Rule order: specific matchers before `anyRequest()`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 47: Security Rules Matrix`

## Hints (optional)

<details><summary>Hint 1</summary>
`Customizer.withDefaults()` for `httpBasic`.
</details>

<details><summary>Hint 2</summary>
`hasRole("ADMIN")` expects the authority `ROLE_ADMIN`.
</details>
