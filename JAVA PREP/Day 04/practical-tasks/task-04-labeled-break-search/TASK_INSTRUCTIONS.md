# Task 4 — Labeled Break Search

**Day:** 04 · **Task ID:** Day04-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Find first pair (i,j) with i<j and a[i]+a[j]==target using labeled break.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../PairSearch.java` | Stubs with TODOs |
| `src/test/java/.../PairSearchTest.java` | Failing tests |

## Prerequisites

- Day 04 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day04-task04)` in `PairSearch`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day04-task04)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 04: complete task-04-labeled-break-search`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=PairSearchTest test
```

### Manual checks

- [ ] No `TODO(Day04-task04)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `PairSearch` / `findPair` | `TODO(Day04-task04)` | return int[]{i,j} of first pair or empty array if none; null input throws NPE |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `PairSearchTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 04: Labeled Break Search`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
