# Task 1 — Group Employees by Department

**Day:** 18 · **Task ID:** Day18-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Produce department reports with `groupingBy` and downstream collectors: names per department, total and average salary, headcount, and the top earner per department. All results are sorted maps so output is deterministic.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day18/task01/Emp.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day18/task01/GroupByDept.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day18/task01/GroupByDeptTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 18 theory file read

## What you will implement

1. `namesByDept(emps)` returns a `SortedMap<String, List<String>>` of employee names per department in input order
2. `totalSalaryByDept(emps)` returns the sum of salaries per department (sorted by department)
3. `averageSalaryByDept(emps)` returns the average salary per department
4. `headcountByDept(emps)` returns the number of employees per department as `Long`
5. `topEarnerByDept(emps)` returns the name of the highest-paid employee per department; on a salary tie the **first listed** employee wins

## Constraints

- Use `Collectors.groupingBy` - no hand-written loops or `computeIfAbsent`
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=GroupByDeptTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **6 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day18-task01)`).

### Run one test class

```bash
mvn -Dtest=GroupByDeptTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `GroupByDept.java` — `namesByDept` | `TODO(Day18-task01)` | groupingBy(dept, TreeMap::new, mapping(name, toList())) |
| `GroupByDept.java` — `totalSalaryByDept` | `TODO(Day18-task01)` | groupingBy(dept, TreeMap::new, summingDouble(salary)) |
| `GroupByDept.java` — `averageSalaryByDept` | `TODO(Day18-task01)` | groupingBy(dept, TreeMap::new, averagingDouble(salary)) |
| `GroupByDept.java` — `headcountByDept` | `TODO(Day18-task01)` | groupingBy(dept, TreeMap::new, counting()) |
| `GroupByDept.java` — `topEarnerByDept` | `TODO(Day18-task01)` | groupingBy(dept, TreeMap::new, collectingAndThen(maxBy(by salary), optional -> optional.orElseThrow().name())); first listed wins ties |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_namesByDeptSortedAndInInputOrder` |
| 2 | `r2_totalSalary` |
| 3 | `r3_averageSalary` |
| 4 | `r4_headcount` |
| 5 | `r5_topEarnerFirstWinsTies` |
| general | `emptyInputGivesEmptyMaps` |

## Edge cases to handle

- empty input -> empty map
- single-employee departments
- salary ties
- departments sorted alphabetically

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 18: Group Employees by Department`

## Hints (optional)

<details><summary>Hint 1</summary>

`Collectors.maxBy` returns the *first* of equal elements, which matches the tie rule.

</details>

<details><summary>Hint 2</summary>

Use the three-argument `groupingBy` so the map is a `TreeMap`.

</details>
