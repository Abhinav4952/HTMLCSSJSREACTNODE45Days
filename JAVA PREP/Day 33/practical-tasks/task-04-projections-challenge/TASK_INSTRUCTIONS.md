# Task 4 — Projections: Interface, Open, DTO and Dynamic

**Day:** 33 · **Task ID:** Day33-task04 · **Type:** Spring Boot · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Fetch only the data you need: closed and open interface projections, a constructor-expression DTO and a dynamic projection chosen by the caller.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day33/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task04/Employee.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task04/EmployeeSummary.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task04/EmployeeLabel.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task04/EmployeeRow.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day33/task04/EmployeeRepository.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day33/task04/EmployeeProjections.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day33/task04/ProjectionsTest.java` | Provided helper or test (do not edit) |
| `src/test/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 33 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Declare the four repository methods (closed, open, constructor-expression, dynamic).
2. Implement the facade delegates; `labels` maps the open projection to strings.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day33-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day33-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 33: complete task-04-projections-challenge`.

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
| `EmployeeRepository.java` | `Day33-task04` | declare: |
| `EmployeeProjections.java` | `Day33-task04` | closed projection |
| `EmployeeProjections.java` | `Day33-task04` | open projection labels |
| `EmployeeProjections.java` | `Day33-task04` | DTO projection via constructor expression |
| `EmployeeProjections.java` | `Day33-task04` | dynamic projection |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `seed` |
| 2 | `closedProjectionCarriesOnlyTwoValues` |
| 3 | `openProjectionComputesLabel` |
| 4 | `constructorExpressionBuildsDtos` |
| 5 | `dynamicProjectionChoosesTypeAtCallSite` |

## Edge cases to handle

- Constructor expressions need the fully qualified class name.
- Dynamic projection works with entity, interface and record/class types.
- Open projections load the whole entity; closed projections select fewer columns.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 33: Projections: Interface, Open, DTO and Dynamic`

## Hints (optional)

<details><summary>Hint 1</summary>
Record `EmployeeRow` has a matching constructor `(String, BigDecimal)`.
</details>

<details><summary>Hint 2</summary>
`Class<T>` as the last parameter enables dynamic projections.
</details>
