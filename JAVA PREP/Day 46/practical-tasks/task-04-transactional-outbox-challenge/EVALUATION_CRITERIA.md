# Evaluation Criteria — Day 46 — Task 04 — Transactional Outbox Simulation (Challenge)

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 46 Task 04 (`transactional-outbox-challenge`).

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

- `placeOrder` inserts order + outbox row atomically.
- Any failure rolls back both rows; restore auto-commit.
- `pollOnce` publishes unpublished rows in id order and marks each after success.
- Stop at the first publisher failure and return the count so far.

### Edge cases

- Null payload (outbox constraint).
- Publisher fails mid-batch.
- Second poll republishes only what remains.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day46-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 46 Task 04 (Transactional Outbox Simulation (Challenge)) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
