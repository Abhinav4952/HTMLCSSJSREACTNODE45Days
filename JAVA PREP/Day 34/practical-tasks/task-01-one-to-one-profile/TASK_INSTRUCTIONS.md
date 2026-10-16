# Task 1 — One-to-One: Account and Profile

**Day:** 34 · **Task ID:** Day34-task01 · **Type:** Spring Boot · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Map a unidirectional one-to-one with a foreign key, lazy fetching, cascade and orphan removal.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day34/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day34/task01/Account.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day34/task01/Profile.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day34/task01/OneToOneTest.java` | Provided helper or test (do not edit) |
| `src/test/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 34 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Annotate `Account.profile` as the owning side of a one-to-one (LAZY, cascade ALL, orphanRemoval, join column `profile_id`).

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day34-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day34-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 34: complete task-01-one-to-one-profile`.

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
| `Account.java` | `Day34-task01` | owning side of a one-to-one: LAZY, cascade ALL, orphanRemoval, join column profile_id |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `savingAccountCascadesToProfile` |
| 2 | `foreignKeyLivesOnAccounts` |
| 3 | `profileIsLazy` |
| 4 | `replacingProfileDeletesTheOrphan` |
| 5 | `removingAccountRemovesProfile` |

## Edge cases to handle

- Replacing the profile must delete the previous one (orphanRemoval).
- Lazy to-one needs a proxy: the entity cannot be final.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 34: One-to-One: Account and Profile`

## Hints (optional)

<details><summary>Hint 1</summary>
`@OneToOne` defaults to EAGER; override with `fetch = LAZY`.
</details>

<details><summary>Hint 2</summary>
`@JoinColumn` on the owning side names the FK column.
</details>
