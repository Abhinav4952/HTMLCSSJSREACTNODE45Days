# Evaluation Criteria — Day 45 — Task 04 — Independent Consumer Groups (Challenge)

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 45 Task 04 (`consumer-groups-challenge`).

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

- Make `BillingListener.onMessage` a listener in group `billing` that records the record value.
- Make `ShippingListener.onMessage` a listener in group `shipping` doing the same.
- Explain in your commit message (or a short comment) what would happen if both used the same group id.

### Edge cases

- Same group = messages are split between members (competing consumers); different groups = each group gets all messages.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day45-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 45 Task 04 (Independent Consumer Groups (Challenge)) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
