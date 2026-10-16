# Evaluation Criteria — Day 33 — Task 01 — Derived Query Methods

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 33 Task 01 (`derived-query-methods`).

## Weighting (100 points)

| Category | Points |
|----------|-------:|
| Correctness (all tests green, requirements met) | 60 |
| Edge cases and error contracts | 20 |
| Code clarity (naming, simplicity, idiomatic Spring/SQL) | 15 |
| Git / hygiene (no `target/`, no secrets, only intended files changed) | 5 |

## Pass / fail gates (automatic fail if violated)

- Project does not compile or `mvn test` fails
- Tests, `pom.xml`, or provided helpers modified to force a pass
- Hard-coded answers that special-case test inputs
- Secrets or `target/` committed

## Detailed rubric

### Correctness

- Declare nine derived query methods on `EmployeeRepository` (names are listed in the TODO).
- Implement every `EmployeeQueries` method as a delegate.

### Edge cases

- `Between` is inclusive on both bounds.
- Derived delete methods need a transaction; the facade method is `@Transactional`.
- A misspelled property name makes the context fail at startup.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day33-task01)`

## AI grading prompt (paste into your grader)

```
You are grading Day 33 Task 01 (Derived Query Methods) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
