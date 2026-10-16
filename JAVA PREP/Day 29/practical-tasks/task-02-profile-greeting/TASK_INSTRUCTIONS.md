# Task 2 — Profiles and Per-Environment Beans

**Day:** 29 · **Task ID:** Day29-task02 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Activate different beans per Spring profile and understand how application-{profile}.yml overlays shared defaults.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day29/task02/GreetingProvider.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day29/task02/DevGreeting.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day29/task02/ProdGreeting.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day29/task02/ProfileConfig.java` | Provided helper or test (do not edit) |
| `src/main/resources/application.yml` | Provided helper or test (do not edit) |
| `src/main/resources/application-dev.yml` | Provided helper or test (do not edit) |
| `src/main/resources/application-prod.yml` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day29/task02/ProfileGreetingTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 29 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Restrict `DevGreeting` and `ProdGreeting` with `@Profile`.
2. Implement both `greeting()` methods.
3. Read the three YAML files and explain which value wins when `dev` is active.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day29-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day29-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 29: complete task-02-profile-greeting`.

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
| `DevGreeting.java` | `Day29-task02` | this bean must exist ONLY when the "dev" profile is active (@Profile |
| `DevGreeting.java` | `Day29-task02` | return "Hello from DEV |
| `ProdGreeting.java` | `Day29-task02` | this bean must exist ONLY when the "prod" profile is active (@Profile |
| `ProdGreeting.java` | `Day29-task02` | return "Hello from PROD |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `devProfileUsesDevGreeting` |
| 2 | `prodProfileUsesProdGreeting` |
| 3 | `noProfileMeansNoGreetingBean` |

## Edge cases to handle

- No active profile -> neither bean exists.
- Profile names are case-sensitive.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 29: Profiles and Per-Environment Beans`

## Hints (optional)

<details><summary>Hint 1</summary>
`@Profile("!prod")` negates a profile.
</details>

<details><summary>Hint 2</summary>
In Boot apps use `spring.profiles.active=dev` or `SPRING_PROFILES_ACTIVE=dev`.
</details>
