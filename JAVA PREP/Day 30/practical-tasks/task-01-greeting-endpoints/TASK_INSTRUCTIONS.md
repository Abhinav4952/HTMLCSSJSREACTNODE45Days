# Task 1 — Greeting Endpoints: Path and Query Parameters

**Day:** 30 · **Task ID:** Day30-task01 · **Type:** Spring Boot · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Turn a plain class into a REST controller using @RestController, @RequestMapping, @GetMapping, @PathVariable and @RequestParam with defaults.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day30/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day30/task01/GreetingController.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day30/task01/GreetingControllerTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 30 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Mark `GreetingController` as a REST controller under `/api/greetings`.
2. Map `greet` to `GET /{name}` and `repeat` to `GET` with query defaults.
3. Implement both bodies; `times < 1` returns an empty string.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day30-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day30-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 30: complete task-01-greeting-endpoints`.

## How to run and verify

```bash
java -version   # 21.x
mvn -v          # 3.9+
mvn test        # expected RED at the start
mvn -Dtest=<TestClass> test
```

## TODO map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `GreetingController.java` | `Day30-task01` | annotate the class as a REST controller mapped under /api/greetings |
| `GreetingController.java` | `Day30-task01` | add the GET mapping for /{name} |
| `GreetingController.java` | `Day30-task01` | return "Hello, <name>! |
| `GreetingController.java` | `Day30-task01` | add the GET mapping for the collection path (no path suffix |
| `GreetingController.java` | `Day30-task01` | join `times` copies of the greeting with single spaces; times < 1 must produce an empty string |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `pathVariableGreeting` |
| 2 | `queryDefaults` |
| 3 | `repeatsGreeting` |
| 4 | `zeroTimesIsEmpty` |
| 5 | `badNumberIs400` |

## Edge cases to handle

- Non-numeric `times` yields 400 automatically (type conversion failure).
- Default values apply when parameters are absent.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 30: Greeting Endpoints: Path and Query Parameters`

## Hints (optional)

<details><summary>Hint 1</summary>
`@RestController` = `@Controller` + `@ResponseBody`.
</details>

<details><summary>Hint 2</summary>
`@RequestParam(defaultValue=...)` makes the parameter optional.
</details>
