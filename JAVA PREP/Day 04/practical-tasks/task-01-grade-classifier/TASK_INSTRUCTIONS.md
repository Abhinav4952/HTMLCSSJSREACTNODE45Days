# Task 1 — Grade Classifier

**Day:** 04 · **Task ID:** Day04-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Map a numeric score to a letter grade with if/else.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../GradeClassifier.java` | Stubs with TODOs |
| `src/test/java/.../GradeClassifierTest.java` | Failing tests |

## Prerequisites

- Day 04 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day04-task01)` in `GradeClassifier`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day04-task01)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 04: complete task-01-grade-classifier`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=GradeClassifierTest test
```

### Manual checks

- [ ] No `TODO(Day04-task01)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `GradeClassifier` / `grade` | `TODO(Day04-task01)` | A>=90 B>=80 C>=70 D>=60 else F; throw IllegalArgumentException if score not in 0..100 |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `GradeClassifierTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 04: Grade Classifier`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
