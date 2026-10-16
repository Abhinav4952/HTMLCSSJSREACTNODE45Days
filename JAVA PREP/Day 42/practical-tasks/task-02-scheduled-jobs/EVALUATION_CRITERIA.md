# Evaluation Criteria — Day 42 — Task 02 — @Scheduled: Fixed Delay, Cron and Property-Driven Rates

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 42 Task 02 (`scheduled-jobs`).

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

- Enable scheduling.
- Add the three `@Scheduled` annotations exactly as documented and implement the three job bodies.

### Edge cases

- `fixedDelay` waits after completion; `fixedRate` starts at fixed intervals even if runs overlap.
- Cron has six fields in Spring: second minute hour day month weekday.
- Scheduled methods must be void and take no arguments.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day42-task02)`

## AI grading prompt (paste into your grader)

```
You are grading Day 42 Task 02 (@Scheduled: Fixed Delay, Cron and Property-Driven Rates) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
