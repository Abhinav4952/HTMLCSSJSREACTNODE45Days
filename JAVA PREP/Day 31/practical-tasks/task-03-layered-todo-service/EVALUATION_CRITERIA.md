# Evaluation Criteria — Day 31 — Task 03 — Layered Architecture: Controller, Service, Repository, Mapper

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 31 Task 03 (`layered-todo-service`).

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

- Implement `TodoMapper.toDto`.
- Implement `TodoService.create`, `complete`, `list` with the documented rules and exceptions.

### Edge cases

- Duplicate detection ignores case and surrounding whitespace.
- A second `complete` fails with `IllegalStateException`.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day31-task03)`

## AI grading prompt (paste into your grader)

```
You are grading Day 31 Task 03 (Layered Architecture: Controller, Service, Repository, Mapper) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
