# Task 4 — Custom Bean Validation Constraints

**Day:** 31 · **Task ID:** Day31-task04 · **Type:** Spring Boot · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Implement a field-level (@StrongPassword) and a class-level (@ValidDateRange) ConstraintValidator and verify them with the Jakarta Validator API.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day31/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task04/StrongPassword.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task04/StrongPasswordValidator.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day31/task04/ValidDateRange.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task04/DateRangeValidator.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day31/task04/Booking.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day31/task04/Registration.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day31/task04/CustomConstraintsTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 31 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `StrongPasswordValidator.isValid`.
2. Implement `DateRangeValidator.isValid`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day31-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day31-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 31: complete task-04-custom-constraints`.

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
| `StrongPasswordValidator.java` | `Day31-task04` | null valid; otherwise length >= 8 with upper, lower and digit |
| `DateRangeValidator.java` | `Day31-task04` | null-tolerant strict end-after-start check |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `strongPasswordRules` |
| 2 | `nullPasswordReportedByNotNullOnly` |
| 3 | `validRange` |
| 4 | `sameDayAndReversedRangesRejected` |
| 5 | `missingDatesReportedOnlyByNotNull` |

## Edge cases to handle

- Null values are valid for custom constraints; `@NotNull` reports them once.
- Same-day range is invalid.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 31: Custom Bean Validation Constraints`

## Hints (optional)

<details><summary>Hint 1</summary>
Single responsibility: each constraint checks one thing and ignores null.
</details>

<details><summary>Hint 2</summary>
`LocalDate.isAfter` is strict.
</details>
