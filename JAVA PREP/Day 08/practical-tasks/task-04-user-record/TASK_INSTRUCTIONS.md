# Task 4 — User Record

**Day:** 08 · **Task ID:** Day08-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Define a record with compact canonical constructor validation.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../UserId.java` | Stubs with TODOs |
| `src/test/java/.../UserIdTest.java` | Failing tests |

## Prerequisites

- Day 08 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day08-task04)` in `UserId`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day08-task04)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 08: complete task-04-user-record`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=UserIdTest test
```

### Manual checks

- [ ] No `TODO(Day08-task04)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `UserId` / `UserId` | `TODO(Day08-task04)` | record component; reject null/blank; store stripped value |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `UserIdTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 08: User Record`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
