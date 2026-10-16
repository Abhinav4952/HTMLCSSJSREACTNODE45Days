# Evaluation Criteria — Day 25 — Task 02 — Insert, Update, Delete

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 25 Task 02 (`insert-update-delete`).

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

- Write `seed.sql` with exactly the four specified rows.
- Write the four DML blocks and one SELECT block in `answers.sql`.
- Use WHERE clauses precisely — the tests check the affected-row counts returned by `executeUpdate`.

### Edge cases

- An UPDATE/DELETE without WHERE would affect all rows — tests catch this.
- Rely on the column DEFAULT in `insert_eve` rather than repeating the literal.
- `close_zero` must run before `purge_closed` in the test, never in your script.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day25-task02)`

## AI grading prompt (paste into your grader)

```
You are grading Day 25 Task 02 (Insert, Update, Delete) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
