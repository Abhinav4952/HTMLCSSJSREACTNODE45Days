# Task 2 — GitHub Actions Workflow Checker

**Day:** 49 · **Task ID:** Day49-task02 · **Type:** Java + CI · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Write a real CI workflow (`ci/ci.yml`) and the small checker that verifies it contains the essential pieces: triggers, checkout, Java 21, Maven cache and a build/test command.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day49/task02/WorkflowChecker.java` | Stubs / starter code (edit the TODOs) |
| `ci/ci.yml` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day49/task02/WorkflowCheckerTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 49 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `missingPieces` with the seven checks in the documented order.
2. Complete `ci/ci.yml` so it passes your own checker.
3. Include a `pull_request` trigger and Maven dependency caching.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day49-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day49-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 49: complete task-02-github-actions-workflow`.

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
| `WorkflowChecker.java` | `Day49-task02` | implement the seven checks above (Pattern with MULTILINE is handy |
| `ci.yml` | `Day49-task02` | write a complete GitHub Actions workflow for a Maven + Java 21 project. |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `completeWorkflowHasNothingMissing` |
| 2 | `emptyWorkflowMissesEverything` |
| 3 | `oldJavaVersionIsDetected` |
| 4 | `missingCacheIsDetected` |
| 5 | `testCommandAlsoCountsAsBuild` |
| 6 | `yourWorkflowFileIsAcceptable` |

## Edge cases to handle

- Indentation variations.
- Quotes around the Java version.
- `mvn test` vs `mvn verify`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 49: GitHub Actions Workflow Checker`

## Hints (optional)

<details><summary>Hint 1</summary>
`Pattern.compile("^\\s*push:", Pattern.MULTILINE)`.
</details>

<details><summary>Hint 2</summary>
The workflow file is plain text; you do not need a YAML library.
</details>
