# Evaluation Criteria — Day 26 — Task 04 — Views, Functions and Transactions

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 26 Task 04 (`view-and-txn`).

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

- Define the `order_totals` view with columns `order_id` and `total_cents`.
- Query the view for big orders and compute customer counts per email domain with SQL functions.

### Edge cases

- The view must update automatically when new items are inserted.
- Rolled-back inserts must not appear in the view.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day26-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 26 Task 04 (Views, Functions and Transactions) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
