# Task 3 — Style Linter (Checkstyle in Miniature)

**Day:** 49 · **Task ID:** Day49-task03 · **Type:** Java · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Build a small linter for the style rules in the team Checkstyle configuration (tabs, trailing whitespace, line length, star imports, console prints, final newline).

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day49/task03/StyleLinter.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day49/task03/StyleLinterTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 49 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Return `line:RULE` entries ordered by line and rule order.
2. Detect the five line-level rules.
3. Report a missing final newline as `EOF:NO_FINAL_NEWLINE`.
4. Empty input has no violations.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day49-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day49-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 49: complete task-03-style-linter`.

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
| `StyleLinter.java` | `Day49-task03` | split on '\n' (keep trailing empties out of the line count) and apply the rules |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `cleanSourceHasNoViolations` |
| 2 | `emptySourceHasNoViolations` |
| 3 | `tabsAndTrailingWhitespaceAreFound` |
| 4 | `longLinesAreFound` |
| 5 | `starImportsAndConsolePrintsAreFound` |
| 6 | `m` |
| 7 | `oneLineCanHaveSeveralRulesInOrder` |
| 8 | `missingFinalNewlineIsReportedLast` |

## Edge cases to handle

- File without trailing newline.
- A line that violates several rules.
- Exactly 100 characters is allowed.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 49: Style Linter (Checkstyle in Miniature)`

## Hints (optional)

<details><summary>Hint 1</summary>
`source.split("\n", -1)` keeps trailing empty strings; drop the last one if the source ends with a newline.
</details>

<details><summary>Hint 2</summary>
Compare lengths with `>`, not `>=`.
</details>
