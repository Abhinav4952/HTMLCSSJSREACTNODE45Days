# Evaluation Criteria — Day 39 — Task 01 — @WebMvcTest Slice with a Mocked Service

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 39 Task 01 (`webmvc-slice-test`).

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

- Implement `get` and `list` in `BookController`.
- Add one more test of your own (e.g. a 404 body check).
- Explain what a slice does and does not load.

### Edge cases

- `list` with an author must never call `findAll()`.
- Type mismatch on `{id}` yields 400 without any code from you.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day39-task01)`

## AI grading prompt (paste into your grader)

```
You are grading Day 39 Task 01 (@WebMvcTest Slice with a Mocked Service) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
