# Task 3 — Sort and Search

**Day:** 06 · **Task ID:** Day06-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Sort a copy and binary-search without mutating the original.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../SortSearch.java` | Stubs with TODOs |
| `src/test/java/.../SortSearchTest.java` | Failing tests |

## Prerequisites

- Day 06 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day06-task03)` in `SortSearch`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day06-task03)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 06: complete task-03-sort-and-search`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=SortSearchTest test
```

### Manual checks

- [ ] No `TODO(Day06-task03)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `SortSearch` / `indexOfSortedCopy` | `TODO(Day06-task03)` | sort a copy, binarySearch, return index or -1 if not found; null original throws NPE |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `SortSearchTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 06: Sort and Search`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
