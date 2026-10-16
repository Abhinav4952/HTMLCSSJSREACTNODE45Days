# Evaluation Criteria — Day 50 — Task 02 — Timed Round 2 (60 min): Spring + JPA Bug Hunt

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 50 Task 02 (`timed-spring-jpa-bug-hunt-60min`).

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

- Fix BUG-1 (comparison), BUG-2 (integer math + validation) and BUG-3 (input normalisation).
- Implement `reserve` per the Javadoc SPEC (transactional, validated, no partial change).
- Do not change the tests.

### Edge cases

- Boundary value for `lowStock`.
- Rounding down in the discount.
- Null SKU.
- Failed reservation must not decrease stock.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day50-task02)`

## AI grading prompt (paste into your grader)

```
You are grading Day 50 Task 02 (Timed Round 2 (60 min): Spring + JPA Bug Hunt) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
