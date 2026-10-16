# Task 2 — JPQL with @Query

**Day:** 33 · **Task ID:** Day33-task02 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Write JPQL by hand: LIKE search, a subquery, a bulk @Modifying update, and an aggregate returned through an interface projection.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day33/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task02/Employee.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task02/DeptTotal.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task02/EmployeeRepository.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day33/task02/EmployeeReports.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day33/task02/JpqlQueriesTest.java` | Provided helper or test (do not edit) |
| `src/test/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 33 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Add four `@Query` methods to `EmployeeRepository` (see the TODO for contracts).
2. Implement the four delegating methods in `EmployeeReports`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day33-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day33-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 33: complete task-02-jpql-query-annotation`.

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
| `EmployeeRepository.java` | `Day33-task02` | add four @Query methods (JPQL, named parameters): |
| `EmployeeReports.java` | `Day33-task02` | delegate to repository.search |
| `EmployeeReports.java` | `Day33-task02` | delegate to repository.aboveAverage |
| `EmployeeReports.java` | `Day33-task02` | delegate to repository.raise |
| `EmployeeReports.java` | `Day33-task02` | delegate to repository.payroll |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `seed` |
| 2 | `searchIgnoresCaseAndOrdersByName` |
| 3 | `aboveAverageUsesSubquery` |
| 4 | `bulkRaiseUpdatesRowsAndRefreshesContext` |
| 5 | `raiseForUnknownDepartmentUpdatesNothing` |
| 6 | `payrollGroupsByDepartment` |

## Edge cases to handle

- JPQL uses entity/field names (`Employee`, `hiredOn`), not table/column names.
- Bulk updates bypass the persistence context: use `clearAutomatically`.
- Aliases in aggregate queries must match projection getter names.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 33: JPQL with @Query`

## Hints (optional)

<details><summary>Hint 1</summary>
`:name` parameters pair with `@Param("name")`.
</details>

<details><summary>Hint 2</summary>
`avg(x.salary)` in a subquery needs a different alias than the outer query.
</details>
