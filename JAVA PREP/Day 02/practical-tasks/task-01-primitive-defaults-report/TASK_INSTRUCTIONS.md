# Task 1 — Primitive Defaults Report

**Day:** 02 · **Task ID:** Day02-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Report default values for uninitialized instance fields of each primitive family.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../DefaultValues.java` | Stubs with TODOs |
| `src/test/java/.../DefaultValuesTest.java` | Failing tests |

## Prerequisites

- Day 02 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day02-task01)` in `DefaultValues`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day02-task01)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 02: complete task-01-primitive-defaults-report`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=DefaultValuesTest test
```

### Manual checks

- [ ] No `TODO(Day02-task01)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `DefaultValues` / `getIntDefault` | `TODO(Day02-task01)` | return the default int field value (0) |
| `DefaultValues` / `getBooleanDefault` | `TODO(Day02-task01)` | return the default boolean field value (false) |
| `DefaultValues` / `getReferenceDefault` | `TODO(Day02-task01)` | return the default reference field value (null) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `DefaultValuesTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 02: Primitive Defaults Report`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
