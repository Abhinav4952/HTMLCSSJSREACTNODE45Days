# Task 4 — Access Boundary

**Day:** 07 · **Task ID:** Day07-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Expose only a public API while keeping helper private.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../PasswordMasker.java` | Stubs with TODOs |
| `src/test/java/.../PasswordMaskerTest.java` | Failing tests |

## Prerequisites

- Day 07 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day07-task04)` in `PasswordMasker`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day07-task04)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 07: complete task-04-access-boundary`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=PasswordMaskerTest test
```

### Manual checks

- [ ] No `TODO(Day07-task04)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `PasswordMasker` / `mask` | `TODO(Day07-task04)` | return same length of '*' ; null/blank throws IllegalArgumentException; use a private helper to validate |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `PasswordMaskerTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 07: Access Boundary`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
