# Task 1 — Derived Query Methods

**Day:** 33 · **Task ID:** Day33-task01 · **Type:** Spring Boot · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Express queries purely through repository method names: And, Containing, IgnoreCase, OrderBy, Top, Between, count/exists/delete.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day33/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task01/Employee.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task01/EmployeeRepository.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day33/task01/EmployeeQueries.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day33/task01/DerivedQueriesTest.java` | Provided helper or test (do not edit) |
| `src/test/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 33 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Declare nine derived query methods on `EmployeeRepository` (names are listed in the TODO).
2. Implement every `EmployeeQueries` method as a delegate.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day33-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day33-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 33: complete task-01-derived-query-methods`.

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
| `EmployeeRepository.java` | `Day33-task01` | declare DERIVED query methods (names matter!), the facade EmployeeQueries documents the contract: |
| `EmployeeQueries.java` | `Day33-task01` | delegate to findByDepartment |
| `EmployeeQueries.java` | `Day33-task01` | delegate to findByDepartmentAndActiveTrue |
| `EmployeeQueries.java` | `Day33-task01` | delegate to findBySalaryGreaterThanEqualOrderBySalaryDesc |
| `EmployeeQueries.java` | `Day33-task01` | delegate to findByNameContainingIgnoreCase |
| `EmployeeQueries.java` | `Day33-task01` | delegate to countByDepartment |
| `EmployeeQueries.java` | `Day33-task01` | delegate to existsByNameIgnoreCase |
| `EmployeeQueries.java` | `Day33-task01` | delegate to findTop2ByOrderBySalaryDesc |
| `EmployeeQueries.java` | `Day33-task01` | delegate to findByHiredOnBetween |
| `EmployeeQueries.java` | `Day33-task01` | delegate to deleteByActiveFalse and return the number of deleted rows |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `seed` |
| 2 | `byDepartment` |
| 3 | `byDepartmentAndActive` |
| 4 | `salaryThresholdOrderedDescending` |
| 5 | `nameContainsIgnoresCase` |
| 6 | `countAndExists` |
| 7 | `topTwo` |
| 8 | `hiredBetweenIsInclusive` |
| 9 | `purgeInactiveReturnsCount` |

## Edge cases to handle

- `Between` is inclusive on both bounds.
- Derived delete methods need a transaction; the facade method is `@Transactional`.
- A misspelled property name makes the context fail at startup.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 33: Derived Query Methods`

## Hints (optional)

<details><summary>Hint 1</summary>
Property names come from the entity fields (`hiredOn`, not `hired_on`).
</details>

<details><summary>Hint 2</summary>
`Top2` limits the result count; combine with `OrderBy...Desc`.
</details>
