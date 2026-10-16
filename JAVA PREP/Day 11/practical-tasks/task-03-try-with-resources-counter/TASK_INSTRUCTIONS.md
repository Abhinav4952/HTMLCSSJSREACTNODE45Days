# Task 3 — Try-With-Resources Counter

**Day:** 11 · **Task ID:** Day11-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Implement AutoCloseable that counts closes.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../CountingResource.java` | Stubs with TODOs |
| `src/test/java/.../CountingResourceTest.java` | Failing tests |

## Prerequisites

- Day 11 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day11-task03)` in `CountingResource`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day11-task03)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 11: complete task-03-try-with-resources-counter`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=CountingResourceTest test
```

### Manual checks

- [ ] No `TODO(Day11-task03)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `CountingResource` / `close` | `TODO(Day11-task03)` | increment closeCount; implement AutoCloseable |
| `CountingResource` / `getCloseCount` | `TODO(Day11-task03)` | return closes |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `CountingResourceTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 11: Try-With-Resources Counter`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
