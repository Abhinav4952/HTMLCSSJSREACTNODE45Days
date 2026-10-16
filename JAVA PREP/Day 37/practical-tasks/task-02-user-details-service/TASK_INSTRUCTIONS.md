# Task 2 — Custom UserDetailsService

**Day:** 37 · **Task ID:** Day37-task02 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Bridge your own user storage to Spring Security by implementing UserDetailsService, then see DaoAuthenticationProvider use it.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day37/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day37/task02/UserRecord.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day37/task02/UserStore.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day37/task02/StoreUserDetailsService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day37/task02/UserDetailsServiceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 37 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `loadUserByUsername` using `User.withUsername(...)`.
2. Throw `UsernameNotFoundException` for unknown users and honor the `enabled` flag.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day37-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day37-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 37: complete task-02-user-details-service`.

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
| `StoreUserDetailsService.java` | `Day37-task02` | look up the record and map it to UserDetails |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `mapsRolesToPrefixedAuthorities` |
| 3 | `lookupIsCaseInsensitive` |
| 4 | `unknownUserThrows` |
| 5 | `disabledAccountIsReportedDisabled` |
| 6 | `authenticationSucceedsWithRightPassword` |
| 7 | `wrongPasswordAndUnknownUserLookTheSame` |
| 8 | `disabledUserCannotLogIn` |

## Edge cases to handle

- `roles("ADMIN")` adds the `ROLE_` prefix itself; `authorities("ADMIN")` does not.
- Never reveal whether the username or the password was wrong (`BadCredentialsException`).

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 37: Custom UserDetailsService`

## Hints (optional)

<details><summary>Hint 1</summary>
`User.withUsername(name).password(hash).roles(...).disabled(bool).build()`.
</details>

<details><summary>Hint 2</summary>
The hash must already be encoded: the provider compares with the `PasswordEncoder`.
</details>
