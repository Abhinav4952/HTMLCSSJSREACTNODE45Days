# Task 3 — StringBuilder Join

**Day:** 05 · **Task ID:** Day05-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Join strings with a delimiter using StringBuilder (no String.join).

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../Joiner.java` | Stubs with TODOs |
| `src/test/java/.../JoinerTest.java` | Failing tests |

## Prerequisites

- Day 05 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day05-task03)` in `Joiner`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day05-task03)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 05: complete task-03-stringbuilder-join`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=JoinerTest test
```

### Manual checks

- [ ] No `TODO(Day05-task03)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `Joiner` / `join` | `TODO(Day05-task03)` | join parts with delimiter; null delimiter or parts throws NPE; null part treated as empty string |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `JoinerTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 05: StringBuilder Join`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
