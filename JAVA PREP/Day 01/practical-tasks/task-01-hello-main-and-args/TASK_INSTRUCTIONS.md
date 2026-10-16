# Task 1 — Hello Main and Args

**Day:** 01 · **Task ID:** Day01-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Return a greeting that includes the first command-line argument, or a default if none.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../HelloGreeter.java` | Stubs with TODOs |
| `src/test/java/.../HelloGreeterTest.java` | Failing tests |

## Prerequisites

- Day 01 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day01-task01)` in `HelloGreeter`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day01-task01)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 01: complete task-01-hello-main-and-args`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=HelloGreeterTest test
```

### Manual checks

- [ ] No `TODO(Day01-task01)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `HelloGreeter` / `greet` | `TODO(Day01-task01)` | return 'Hello, <name>!' using args[0] when present and non-blank; otherwise 'Hello, World!' |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `HelloGreeterTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 01: Hello Main and Args`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
