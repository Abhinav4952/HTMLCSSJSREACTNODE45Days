# Task 4 — Starter Dependency Quiz

**Day:** 29 · **Task ID:** Day29-task04 · **Type:** Spring Boot · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Encode Spring Boot starter knowledge in code: map use cases to starters, validate starter names, and list notable transitive dependencies.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day29/task04/StarterAdvisor.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day29/task04/StarterAdvisorTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 29 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `starterFor` with the documented mapping.
2. Implement `isStarterName` using a regular expression.
3. Implement `typicalTransitives`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day29-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day29-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 29: complete task-04-starter-dependency-quiz`.

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
| `StarterAdvisor.java` | `Day29-task04` | implement the mapping (a Map<String,String> constant is fine |
| `StarterAdvisor.java` | `Day29-task04` | validate with a regex |
| `StarterAdvisor.java` | `Day29-task04` | implement |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `mapsUseCases` |
| 2 | `unknownUseCaseIsRejected` |
| 3 | `recognizesStarterNames` |
| 4 | `transitives` |

## Edge cases to handle

- Input is trimmed and case-insensitive for use cases.
- Starter names are case-sensitive lowercase.
- Non-starter artifact -> `IllegalArgumentException`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 29: Starter Dependency Quiz`

## Hints (optional)

<details><summary>Hint 1</summary>
A `Map.of(...)` constant keeps the mapping readable.
</details>

<details><summary>Hint 2</summary>
`typicalTransitives` can reuse `isStarterName` for validation.
</details>
