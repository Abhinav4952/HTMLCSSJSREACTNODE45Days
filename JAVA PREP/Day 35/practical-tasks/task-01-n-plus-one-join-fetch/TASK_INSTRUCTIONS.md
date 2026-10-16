# Task 1 — Detect and Fix N+1 Queries

**Day:** 35 · **Task ID:** Day35-task01 · **Type:** Spring Boot · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Measure the N+1 problem with Hibernate statistics and fix it with join fetch and an entity graph.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day35/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day35/task01/Author.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day35/task01/Book.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day35/task01/AuthorRepository.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day35/task01/AuthorReport.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day35/task01/NPlusOneTest.java` | Provided helper or test (do not edit) |
| `src/test/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 35 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Add `findAllWithBooks` (join fetch) and `findAllWithGraph` (entity graph) to the repository.
2. Implement the two optimized report methods; observe the statement counts.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day35-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day35-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 35: complete task-01-n-plus-one-join-fetch`.

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
| `AuthorRepository.java` | `Day35-task01` | declare two methods that load authors TOGETHER with their books in ONE statement: |
| `AuthorReport.java` | `Day35-task01` | use repository.findAllWithBooks( |
| `AuthorReport.java` | `Day35-task01` | use repository.findAllWithGraph( |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `seed` |
| 2 | `naiveVersionExecutesNPlusOneStatements` |
| 3 | `joinFetchUsesOneStatement` |
| 4 | `entityGraphUsesOneStatement` |
| 5 | `bothOptimizedVersionsAgree` |

## Edge cases to handle

- `distinct` removes duplicate parents caused by the join.
- Never `join fetch` two collections (cartesian product / MultipleBagFetchException) and do not paginate in memory over fetched collections.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 35: Detect and Fix N+1 Queries`

## Hints (optional)

<details><summary>Hint 1</summary>
Statistics are cleared after seeding so only the report is counted.
</details>

<details><summary>Hint 2</summary>
`@EntityGraph` can also be put directly on derived query methods.
</details>
