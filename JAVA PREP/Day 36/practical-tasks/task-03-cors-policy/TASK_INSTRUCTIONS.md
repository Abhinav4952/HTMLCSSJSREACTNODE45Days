# Task 3 — CORS Policy

**Day:** 36 · **Task ID:** Day36-task03 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Configure a global CORS policy with WebMvcConfigurer and open a single endpoint with @CrossOrigin, then verify preflight behavior.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day36/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day36/task03/DataController.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day36/task03/CorsConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day36/task03/CorsTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 36 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `CorsConfig.addCorsMappings` for `/api/**`.
2. Add `@CrossOrigin(origins = "*")` to the ping endpoint.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day36-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day36-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 36: complete task-03-cors-policy`.

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
| `DataController.java` | `Day36-task03` | allow ANY origin for this single endpoint with @CrossOrigin(origins = |
| `CorsConfig.java` | `Day36-task03` | registry.addMapping on /api/** with origins, methods, headers, credentials and maxAge |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `preflightFromAllowedOrigin` |
| 2 | `deleteIsAllowedButPatchIsNot` |
| 3 | `preflightFromOtherOriginIsForbidden` |
| 4 | `simpleRequestGetsAllowOriginHeader` |
| 5 | `noOriginNoCorsHeaders` |
| 6 | `pathsOutsideTheMappingGetNoCorsHeaders` |
| 7 | `crossOriginAnnotationOpensOnlyThePingEndpoint` |

## Edge cases to handle

- `allowedOrigins("*")` cannot be combined with `allowCredentials(true)`.
- CORS is enforced by browsers; it is not authentication.
- Preflight is an `OPTIONS` request with `Origin` and `Access-Control-Request-Method` headers.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 36: CORS Policy`

## Hints (optional)

<details><summary>Hint 1</summary>
`maxAge` is in seconds.
</details>

<details><summary>Hint 2</summary>
Forbidden (403) is how Spring rejects an invalid CORS request.
</details>
