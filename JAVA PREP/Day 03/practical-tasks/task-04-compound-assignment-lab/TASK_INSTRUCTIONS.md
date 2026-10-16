# Task 4 — Compound Assignment Lab

**Day:** 03 · **Task ID:** Day03-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Apply compound assignment on a byte and return the new value (with implicit cast).

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../CompoundAssign.java` | Stubs with TODOs |
| `src/test/java/.../CompoundAssignTest.java` | Failing tests |

## Prerequisites

- Day 03 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day03-task04)` in `CompoundAssign`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day03-task04)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 03: complete task-04-compound-assignment-lab`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=CompoundAssignTest test
```

### Manual checks

- [ ] No `TODO(Day03-task04)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `CompoundAssign` / `addToByte` | `TODO(Day03-task04)` | return (byte)(current + delta) as compound += would |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `CompoundAssignTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 03: Compound Assignment Lab`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
