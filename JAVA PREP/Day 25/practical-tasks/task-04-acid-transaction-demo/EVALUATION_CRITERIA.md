# Evaluation Criteria — Day 25 — Task 04 — ACID Transaction Demo

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 25 Task 04 (`acid-transaction-demo`).

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

- Complete the four named blocks in `sql/answers.sql`.
- Implement `AcidNotes.propertyFor` and `AcidNotes.isolationFor`.
- Be able to explain why the total of 15000 is invariant after commit and after rollback (atomicity + consistency).

### Edge cases

- Unknown ACID letters or anomalies -> `IllegalArgumentException`.
- Anomaly names are case-insensitive and trimmed.
- The overdraft block must fail with a constraint error, not succeed with a negative balance.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day25-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 25 Task 04 (ACID Transaction Demo) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
