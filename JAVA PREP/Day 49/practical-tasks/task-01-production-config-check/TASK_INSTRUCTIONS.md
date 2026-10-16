# Task 1 — Production Configuration Validator

**Day:** 49 · **Task ID:** Day49-task01 · **Type:** Java · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Write the fail-fast configuration check that a deployment runs before starting: required environment variables, weak secrets and the active profile.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day49/task01/ProductionConfigCheck.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day49/task01/ProductionConfigCheckTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 49 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Report missing/blank required keys in a fixed order.
2. Validate the JDBC URL prefix, weak database passwords and short JWT secrets.
3. Require the `prod` profile.
4. Do not double-report a missing key as weak.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day49-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day49-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 49: complete task-01-production-config-check`.

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
| `ProductionConfigCheck.java` | `Day49-task01` | apply the rules in the stated order |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `validEnvironmentHasNoProblems` |
| 2 | `missingAndBlankKeysAreReportedInOrder` |
| 3 | `badUrlAndWeakSecretsAreReported` |
| 4 | `wrongOrMissingProfileIsReported` |
| 5 | `missingPasswordIsOnlyReportedAsMissing` |

## Edge cases to handle

- Blank values.
- Mixed-case weak passwords.
- Absent profile.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 49: Production Configuration Validator`

## Hints (optional)

<details><summary>Hint 1</summary>
Use a `List<String>` and add problems in the documented order.
</details>

<details><summary>Hint 2</summary>
`String.isBlank()` handles whitespace-only values.
</details>
