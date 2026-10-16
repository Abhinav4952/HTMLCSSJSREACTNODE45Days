# Task 4 — Method Security with @PreAuthorize

**Day:** 38 · **Task ID:** Day38-task04 · **Type:** Spring Boot (Security + JWT) · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Protect service methods instead of URLs: enable method security, write SpEL expressions with roles and argument checks.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day38/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day38/task04/MethodSecurityConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day38/task04/ReportService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day38/task04/MethodSecurityTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 38 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Enable method security on the configuration class.
2. Add the three documented `@PreAuthorize` expressions.
3. Explain why method security is safer than URL rules alone.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day38-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day38-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 38: complete task-04-preauthorize-method`.

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
| `MethodSecurityConfig.java` | `Day38-task04` | switch on method security with @EnableMethodSecurity |
| `ReportService.java` | `Day38-task04` | restrict to ADMIN with @PreAuthorize("hasRole('ADMIN' |
| `ReportService.java` | `Day38-task04` | restrict with @PreAuthorize("hasAnyRole('USER','ADMIN' |
| `ReportService.java` | `Day38-task04` | restrict with @PreAuthorize("#owner == authentication.name or hasRole('ADMIN' |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `userCannotDeleteAll` |
| 2 | `adminCanDeleteAll` |
| 3 | `userCanView` |
| 4 | `guestCannotView` |
| 5 | `ownerReadsOwnReportOnly` |
| 6 | `adminReadsAnyReport` |
| 7 | `anonymousCallsAreRejected` |

## Edge cases to handle

- `#owner` refers to the method parameter by name (compile with `-parameters`, which Boot's parent pom enables).
- Anonymous callers must be rejected, not given a default pass.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 38: Method Security with @PreAuthorize`

## Hints (optional)

<details><summary>Hint 1</summary>
Calls within the same class bypass the proxy and therefore the check.
</details>

<details><summary>Hint 2</summary>
`authentication.name` is the principal's username.
</details>
