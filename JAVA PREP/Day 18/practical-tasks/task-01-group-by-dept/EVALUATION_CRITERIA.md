# Evaluation Criteria — Day 18 — Task 01 — Group Employees by Department

## Scope

Graded: the behavior and quality of the implementation in `GroupByDept.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

## Weighting (100 points unless the instructor overrides)

| Category | Points | Description |
|----------|-------:|-------------|
| Automated tests (`mvn test`) | 40 | Fraction of tests passing; no skipped/@Disabled tests |
| Requirements coverage | 25 | Each "What you will implement" bullet satisfied |
| Code quality | 20 | Naming, structure, idiomatic Java 21, no duplication, correct use of the day's concepts |
| Robustness & safety | 10 | Edge cases, null/validation handling, exceptions, thread-safety/security where relevant |
| Readability & process | 5 | Clear commits, formatting, sensible comments |

## Pass / fail gates (automatic fail if violated)

- Tests modified/disabled to force a pass
- Hard-coded secrets
- Forbidden APIs from Constraints used
- Project does not compile

## Detailed rubric

### Automated tests

- Full marks only when every test passes with no `@Disabled` and no edits to test files.
- Partial credit is proportional to passing tests; a compile failure scores 0 in this category.

### Requirements coverage

- Requirement 1: `namesByDept(emps)` returns a `SortedMap<String, List<String>>` of employee names per department in input order
- Requirement 2: `totalSalaryByDept(emps)` returns the sum of salaries per department (sorted by department)
- Requirement 3: `averageSalaryByDept(emps)` returns the average salary per department
- Requirement 4: `headcountByDept(emps)` returns the number of employees per department as `Long`
- Requirement 5: `topEarnerByDept(emps)` returns the name of the highest-paid employee per department; on a salary tie the **first listed** employee wins

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty input -> empty map
- single-employee departments
- salary ties
- departments sorted alphabetically

### Day-specific checks

- One collector expression per method
- Sorted map factory used for deterministic ordering
- Optional unwrapped through `collectingAndThen`, not `get()`

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 18 Task 01 (Group Employees by Department) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `GroupByDept.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
