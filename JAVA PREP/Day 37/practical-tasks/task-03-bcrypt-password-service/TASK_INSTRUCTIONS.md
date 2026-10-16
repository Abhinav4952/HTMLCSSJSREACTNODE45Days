# Task 3 — BCrypt Password Hashing

**Day:** 37 · **Task ID:** Day37-task03 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Hash and verify passwords with BCrypt: salting, cost factor, upgrade detection and the DelegatingPasswordEncoder id prefix.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day37/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day37/task03/PasswordService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day37/task03/PasswordServiceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 37 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Create the encoder with the configurable strength.
2. Implement `hash`, `matches` and `needsUpgrade` with the documented null/length rules.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day37-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day37-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 37: complete task-03-bcrypt-password-service`.

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
| `PasswordService.java` | `Day37-task03` | create a BCryptPasswordEncoder with the given strength |
| `PasswordService.java` | `Day37-task03` | validate then encode |
| `PasswordService.java` | `Day37-task03` | null-safe matches |
| `PasswordService.java` | `Day37-task03` | ask the encoder |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `hashLooksLikeBcryptAndIsNotThePassword` |
| 2 | `sameInputGivesDifferentHashesBecauseOfSalt` |
| 3 | `matchesAcceptsOnlyTheRightPassword` |
| 4 | `shortOrMissingPasswordsAreRejected` |
| 5 | `weakerHashesNeedAnUpgrade` |
| 6 | `delegatingEncoderUnderstandsIdPrefixes` |

## Edge cases to handle

- Never log or store raw passwords.
- BCrypt only uses the first 72 bytes of input.
- Hash verification must be timing-safe: always use `matches`, never `equals`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 37: BCrypt Password Hashing`

## Hints (optional)

<details><summary>Hint 1</summary>
`PasswordEncoder.upgradeEncoding(hash)` compares the cost embedded in the hash with the configured cost.
</details>

<details><summary>Hint 2</summary>
`{bcrypt}` is the id the delegating encoder uses to pick the algorithm.
</details>
