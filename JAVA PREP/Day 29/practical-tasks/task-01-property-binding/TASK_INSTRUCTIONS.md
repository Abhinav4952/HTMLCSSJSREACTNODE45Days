# Task 1 — @ConfigurationProperties Binding

**Day:** 29 · **Task ID:** Day29-task01 · **Type:** Spring Boot · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Make a typed properties class bindable (getters/setters, nested object, list) and prove relaxed binding with Spring Boot's Binder.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day29/task01/AppProperties.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day29/task01/AppPropertiesTest.java` | Provided helper or test (do not edit) |
| `src/main/resources/application.yml` | Provided helper or test (do not edit) |

## Prerequisites

- Day 29 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Add getters/setters so `Binder` can populate `AppProperties`, including the nested `Security` object and the list.
2. Implement `summary()`.
3. Understand relaxed binding (kebab-case vs camelCase).

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day29-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day29-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 29: complete task-01-property-binding`.

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
| `AppProperties.java` | `Day29-task01` | add getters and setters for name, maxUsers and features (JavaBean binding needs setters), |
| `AppProperties.java` | `Day29-task01` | add getters and setters for enabled and token |
| `AppProperties.java` | `Day29-task01` | build the summary from the bound values |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `bindsScalarsListsAndNestedObjects` |
| 2 | `missingValuesKeepDefaults` |
| 3 | `camelCaseKeysAlsoBind` |
| 4 | `summaryDescribesTheBoundValues` |
| 5 | `prefixIsDeclaredOnTheClass` |

## Edge cases to handle

- Properties that are absent keep their Java defaults (0, empty list, false).
- Both `app.max-users` and `app.maxUsers` bind.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 29: @ConfigurationProperties Binding`

## Hints (optional)

<details><summary>Hint 1</summary>
Nested static classes need their own getters/setters.
</details>

<details><summary>Hint 2</summary>
Boot's `@ConfigurationProperties` + `Binder` is what `@EnableConfigurationProperties` uses internally.
</details>
