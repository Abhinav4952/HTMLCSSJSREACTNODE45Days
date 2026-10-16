# Evaluation Criteria — Day 46 — Task 01 — Versioned JSON Event Contract

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 46 Task 01 (`json-event-contract`).

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

- Configure the mapper with `FAIL_ON_UNKNOWN_PROPERTIES = false`.
- Implement `toJson` / `fromJson` wrapping Jackson exceptions in `EventFormatException`.
- Normalize version 0 (absent) to 1.
- Reject blank/missing ids and versions above `MAX_SUPPORTED_VERSION`.

### Edge cases

- Missing primitive fields deserialize as 0 in records.
- Null `customerId`.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day46-task01)`

## AI grading prompt (paste into your grader)

```
You are grading Day 46 Task 01 (Versioned JSON Event Contract) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
