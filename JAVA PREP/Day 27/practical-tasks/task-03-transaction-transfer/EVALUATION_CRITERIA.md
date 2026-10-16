# Evaluation Criteria — Day 27 — Task 03 — JDBC Transaction Transfer

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 27 Task 03 (`transaction-transfer`).

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

- Implement `balanceOf`.
- Implement `transfer` in one transaction: validate, check funds, debit, credit, commit.
- Roll back on any failure and rethrow the original unchecked exception.
- Always restore `autoCommit(true)` in a finally block.

### Edge cases

- Unknown destination: the debit must be undone.
- `amount <= 0` or same account: reject before opening a transaction.
- Total money is invariant.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day27-task03)`

## AI grading prompt (paste into your grader)

```
You are grading Day 27 Task 03 (JDBC Transaction Transfer) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
