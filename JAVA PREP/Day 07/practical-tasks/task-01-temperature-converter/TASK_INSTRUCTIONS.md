# Task 1 — Temperature Converter

**Day:** 07 · **Task ID:** Day07-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Static methods converting C↔F.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../TemperatureConverter.java` | Stubs with TODOs |
| `src/test/java/.../TemperatureConverterTest.java` | Failing tests |

## Prerequisites

- Day 07 theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day07-task01)` in `TemperatureConverter`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day07-task01)`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day 07: complete task-01-temperature-converter`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest=TemperatureConverterTest test
```

### Manual checks

- [ ] No `TODO(Day07-task01)` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `TemperatureConverter` / `celsiusToFahrenheit` | `TODO(Day07-task01)` | return c * 9/5 + 32 |
| `TemperatureConverter` / `fahrenheitToCelsius` | `TODO(Day07-task01)` | return (f - 32) * 5/9 |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `TemperatureConverterTest` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 07: Temperature Converter`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
