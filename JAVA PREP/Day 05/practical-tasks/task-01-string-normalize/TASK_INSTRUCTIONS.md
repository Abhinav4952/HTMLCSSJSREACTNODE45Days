# Task 1 — String Normalize

**Day:** 05 · **Task ID:** Day05-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Normalize whitespace and case for comparisons.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../StringNormalize.java` | Stubs with TODOs |
| `src/test/java/.../StringNormalizeTest.java` | Failing tests |

## Prerequisites

- Day 05 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day05-task01)` in `StringNormalize`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day05-task01)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 05: complete task-01-string-normalize`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=StringNormalizeTest test
```

### Manual checks

- [ ] No `TODO(Day05-task01)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `StringNormalize` / `normalize` | `TODO(Day05-task01)` | strip, collapse internal whitespace to single spaces, lower-case; null throws NPE |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `StringNormalizeTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 05: String Normalize`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
