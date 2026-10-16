# Task 2 — @DataJpaTest Slice for Repositories

**Day:** 39 · **Task ID:** Day39-task02 · **Type:** Spring Boot (Testing) · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Turn placeholder default methods into real Spring Data queries and verify them with a repository slice on an embedded database.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day39/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day39/task02/Product.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day39/task02/ProductRepositoryTest.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day39/task02/ProductRepository.java` | Stubs / starter code (edit the TODOs) |

## Prerequisites

- Day 39 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Replace each `default` placeholder with an abstract derived or `@Query` method.
2. Use `@Param` for the named parameters.
3. Write one extra test for a case you think is missing.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day39-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day39-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 39: complete task-02-datajpa-slice`.

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
| `ProductRepository.java` | `Day39-task02` | replace every `default` method below with an abstract Spring Data method: |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `seed` |
| 2 | `ordersByPriceWithinCategory` |
| 3 | `existsBySku` |
| 4 | `priceRangeIsInclusiveAndSorted` |
| 5 | `countsByCategory` |
| 6 | `sliceRollsBackBetweenTests` |

## Edge cases to handle

- `between` is inclusive on both ends.
- The slice rolls each test back, so seeds from one test are not visible in the next.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 39: @DataJpaTest Slice for Repositories`

## Hints (optional)

<details><summary>Hint 1</summary>
`TestEntityManager` is the test-friendly `EntityManager`.
</details>

<details><summary>Hint 2</summary>
Flush and clear to force a real database round trip.
</details>
