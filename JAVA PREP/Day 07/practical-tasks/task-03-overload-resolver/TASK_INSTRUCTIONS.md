# Task 3 — Overload Resolver

**Day:** 07 · **Task ID:** Day07-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Provide overloaded format methods for int, double, and String.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../Formatter.java` | Stubs with TODOs |
| `src/test/java/.../FormatterTest.java` | Failing tests |

## Prerequisites

- Day 07 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day07-task03)` in `Formatter`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day07-task03)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 07: complete task-03-overload-resolver`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=FormatterTest test
```

### Manual checks

- [ ] No `TODO(Day07-task03)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `Formatter` / `format` | `TODO(Day07-task03)` | return 'INT:' + value |
| `Formatter` / `format` | `TODO(Day07-task03)` | return 'DBL:' + value |
| `Formatter` / `format` | `TODO(Day07-task03)` | return 'STR:' + value; NPE if null |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `FormatterTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 07: Overload Resolver`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
