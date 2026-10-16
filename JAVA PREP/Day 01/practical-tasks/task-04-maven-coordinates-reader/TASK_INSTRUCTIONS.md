# Task 4 — Maven Coordinates Reader

**Day:** 01 · **Task ID:** Day01-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Parse groupId:artifactId:version from a GAV string and validate each segment is non-blank.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../GavParser.java` | Stubs with TODOs |
| `src/test/java/.../GavParserTest.java` | Failing tests |

## Prerequisites

- Day 01 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day01-task04)` in `GavParser`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day01-task04)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 01: complete task-04-maven-coordinates-reader`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=GavParserTest test
```

### Manual checks

- [ ] No `TODO(Day01-task04)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `GavParser` / `parse` | `TODO(Day01-task04)` | split on ':' into exactly 3 non-blank parts; throw IllegalArgumentException otherwise |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `GavParserTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 01: Maven Coordinates Reader`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
