# Task 3 — Scope and Shadowing

**Day:** 02 · **Task ID:** Day02-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Compute a value using intentional shadowing rules as specified in tests.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../ScopeDemo.java` | Stubs with TODOs |
| `src/test/java/.../ScopeDemoTest.java` | Failing tests |

## Prerequisites

- Day 02 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day02-task03)` in `ScopeDemo`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day02-task03)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 02: complete task-03-scope-and-shadowing`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=ScopeDemoTest test
```

### Manual checks

- [ ] No `TODO(Day02-task03)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `ScopeDemo` / `compute` | `TODO(Day02-task03)` | return x + 10 using a local shadowed name as described in TODO; document the result path |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `ScopeDemoTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 02: Scope and Shadowing`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
