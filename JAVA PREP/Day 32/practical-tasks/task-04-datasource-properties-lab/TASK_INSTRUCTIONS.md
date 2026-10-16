# Task 4 — Datasource and JPA Properties

**Day:** 32 · **Task ID:** Day32-task04 · **Type:** Spring Boot · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Configure an H2 (PostgreSQL mode) datasource and the key Hibernate settings in application.properties, then prove them with @SpringBootTest.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day32/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day32/task04/Note.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day32/task04/NoteRepository.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day32/task04/DatasourceConfigTest.java` | Provided helper or test (do not edit) |
| `src/main/resources/application.properties` | Stubs / starter code (edit the TODOs) |

## Prerequisites

- Day 32 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Fill `src/main/resources/application.properties` with the seven documented settings.
2. Explain in your own words why `open-in-view=false` is preferred for APIs.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day32-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day32-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 32: complete task-04-datasource-properties-lab`.

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
| `application.properties` | `Day32-task04` | configure the datasource and JPA/Hibernate for the lab (one key=value per line). |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `datasourceUrlIsH2InPostgresMode` |
| 2 | `credentials` |
| 3 | `hibernateCreatesAndDropsSchema` |
| 4 | `openInViewDisabled` |
| 5 | `sqlLoggingAndFormatting` |
| 6 | `repositoryWorksAgainstConfiguredDatabase` |

## Edge cases to handle

- `DB_CLOSE_DELAY=-1` keeps an in-memory DB alive between connections.
- Without a url, Boot would silently use an embedded default database.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 32: Datasource and JPA Properties`

## Hints (optional)

<details><summary>Hint 1</summary>
Property names are exactly the ones shown in the TODO comments.
</details>

<details><summary>Hint 2</summary>
Environment lookups are relaxed but values must be exact.
</details>
