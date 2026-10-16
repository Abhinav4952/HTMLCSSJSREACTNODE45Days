# Task 3 — Pagination, Slices and Native Queries

**Day:** 33 · **Task ID:** Day33-task03 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Return Page and Slice results with Pageable/Sort, and write native SQL queries (with countQuery) when JPQL is not enough.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day33/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task03/Employee.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task03/DeptCount.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task03/EmployeeRepository.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day33/task03/EmployeePaging.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day33/task03/PagingAndNativeTest.java` | Provided helper or test (do not edit) |
| `src/test/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 33 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Declare the four repository methods.
2. Implement the delegating facade methods and `describe`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day33-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day33-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 33: complete task-03-native-and-pagination`.

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
| `EmployeeRepository.java` | `Day33-task03` | declare four methods: |
| `EmployeePaging.java` | `Day33-task03` | delegate to findByDepartment |
| `EmployeePaging.java` | `Day33-task03` | delegate to findByActiveTrue |
| `EmployeePaging.java` | `Day33-task03` | delegate to headcountNative |
| `EmployeePaging.java` | `Day33-task03` | delegate to wellPaid |
| `EmployeePaging.java` | `Day33-task03` | return page <number+1>/<totalPages> (<totalElements> items total |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `seed` |
| 2 | `firstPageSortedBySalaryDescending` |
| 3 | `lastPage` |
| 4 | `sliceKnowsOnlyWhetherThereIsMore` |
| 5 | `nativeAggregateThroughProjection` |
| 6 | `nativePagedQueryUsesCountQuery` |
| 7 | `describeFormatsPageInfo` |

## Edge cases to handle

- Page numbers are zero-based; `describe` shows one-based.
- Native paged queries need a `countQuery`.
- `Slice` skips the count query: cheaper, but no totals.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 33: Pagination, Slices and Native Queries`

## Hints (optional)

<details><summary>Hint 1</summary>
`PageRequest.of(page, size, Sort)`.
</details>

<details><summary>Hint 2</summary>
Native SQL uses table and column names (`employees`, `hired_on`).
</details>
