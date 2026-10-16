# Evaluation Criteria — Day 26 — Task 01 — Inner and Outer Joins

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 26 Task 01 (`inner-outer-joins`).

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

- Answer the five query blocks in `sql/answers.sql`.
- Use the correct join type for each question (inner, left, anti-join, self-join).
- Order results exactly as requested so the tests can compare lists.

### Edge cases

- Employees with a NULL `dept_id` must not appear in the inner join.
- The CEO (no manager) must not appear in the self-join result.
- `COUNT` over a UNION needs a subquery.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day26-task01)`

## AI grading prompt (paste into your grader)

```
You are grading Day 26 Task 01 (Inner and Outer Joins) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
