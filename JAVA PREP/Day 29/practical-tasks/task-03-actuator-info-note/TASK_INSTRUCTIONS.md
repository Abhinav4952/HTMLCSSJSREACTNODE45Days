# Task 3 — Actuator Info Contributor

**Day:** 29 · **Task ID:** Day29-task03 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Implement an InfoContributor that adds app name/version to /actuator/info and record the properties that expose the endpoint.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day29/task03/AppInfoContributor.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day29/task03/AppInfoContributorTest.java` | Provided helper or test (do not edit) |
| `src/main/resources/application.yml` | Provided helper or test (do not edit) |

## Prerequisites

- Day 29 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `contribute` using `Info.Builder#withDetail`.
2. Implement the two static helper methods.
3. Describe in a sentence why Actuator endpoints are not all exposed over HTTP by default.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day29-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day29-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 29: complete task-03-actuator-info-note`.

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
| `AppInfoContributor.java` | `Day29-task03` | add a detail "app" whose value is a Map with keys "name" and "version |
| `AppInfoContributor.java` | `Day29-task03` | return "/actuator/info |
| `AppInfoContributor.java` | `Day29-task03` | return the property line |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `contributesAppSection` |
| 2 | `keepsExistingDetails` |
| 3 | `endpointAndExposureProperties` |

## Edge cases to handle

- Existing details contributed by other InfoContributors must be preserved.
- The value of `app` must be a Map with exactly `name` and `version`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 29: Actuator Info Contributor`

## Hints (optional)

<details><summary>Hint 1</summary>
`builder.withDetail(String, Object)` returns the builder.
</details>

<details><summary>Hint 2</summary>
In a real app, register the contributor as a `@Bean`.
</details>
