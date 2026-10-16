# Task 1 — Inner and Outer Joins

**Day:** 26 · **Task ID:** Day26-task01 · **Type:** SQL script + JDBC test · **Difficulty:** Warm-up

## Summary

Query a small HR schema with INNER, LEFT, anti-join and self-join queries, plus a FULL OUTER row count.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day26/task01/SqlLab.java` | Stubs / starter code (edit the TODOs) |
| `sql/schema.sql` | Provided helper or test (do not edit) |
| `sql/seed.sql` | Provided helper or test (do not edit) |
| `sql/answers.sql` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day26/task01/JoinsTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 26 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Answer the five query blocks in `sql/answers.sql`.
2. Use the correct join type for each question (inner, left, anti-join, self-join).
3. Order results exactly as requested so the tests can compare lists.

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day26-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day26-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 26: complete task-01-inner-outer-joins`.

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
| `answers.sql` | `Day26-task01` | employee name, department name for employees that HAVE a department; ORDER BY employee name |
| `answers.sql` | `Day26-task01` | names of employees with NO department (LEFT JOIN ... WHERE d.id IS NULL); ORDER BY name |
| `answers.sql` | `Day26-task01` | names of departments that have no employees (anti-join); ORDER BY name |
| `answers.sql` | `Day26-task01` | employee name, manager name for employees that have a manager; ORDER BY employee name |
| `answers.sql` | `Day26-task01` | COUNT of rows in the full outer join of employees and departments (UNION of LEFT and RIGHT joins is fine |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `tearDown` |
| 3 | `innerJoinOnlyMatchedPairs` |
| 4 | `leftJoinFindsEmployeesWithoutDepartment` |
| 5 | `departmentsWithoutEmployees` |
| 6 | `selfJoinManagers` |
| 7 | `fullOuterRowCount` |

## Edge cases to handle

- Employees with a NULL `dept_id` must not appear in the inner join.
- The CEO (no manager) must not appear in the self-join result.
- `COUNT` over a UNION needs a subquery.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 26: Inner and Outer Joins`

## Hints (optional)

<details><summary>Hint 1</summary>
Anti-join: `LEFT JOIN ... WHERE right.id IS NULL`.
</details>

<details><summary>Hint 2</summary>
Self join: alias the same table twice (`e` and `m`).
</details>

<details><summary>Hint 3</summary>
Full outer count = matched + unmatched left + unmatched right = 3 + 1 + 1.
</details>
