# Task 4 — Git Conventions and Release Versions

**Day:** 49 · **Task ID:** Day49-task04 · **Type:** Java + Git · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Turn the team's branching, commit-message and release-version rules into code, the same checks a PR bot or commit hook would run.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day49/task04/GitConventions.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day49/task04/GitConventionsTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 49 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Validate branch names (main/develop, ticketed work branches, release branches).
2. Validate Conventional Commit first lines.
3. Bump semantic versions and reject invalid input.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day49-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day49-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 49: complete task-04-git-conventions-release-checklist`.

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
| `GitConventions.java` | `Day49-task04` | implement with one or more regular expressions |
| `GitConventions.java` | `Day49-task04` | validate the first line |
| `GitConventions.java` | `Day49-task04` | parse MAJOR.MINOR.PATCH and apply the bump |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `validBranchNames` |
| 2 | `invalidBranchNames` |
| 3 | `validCommitMessages` |
| 4 | `invalidCommitMessages` |
| 5 | `versionBumps` |
| 6 | `invalidVersionInputs` |

## Edge cases to handle

- Null inputs.
- Subject length boundary (72).
- Double dashes in slugs.
- Versions with missing parts.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 49: Git Conventions and Release Versions`

## Hints (optional)

<details><summary>Hint 1</summary>
Anchor patterns with `^...$` and use `Pattern.matches`/`matcher().matches()`.
</details>

<details><summary>Hint 2</summary>
Slug: `[a-z0-9]+(-[a-z0-9]+)*`.
</details>
