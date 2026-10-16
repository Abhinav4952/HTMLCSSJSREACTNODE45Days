# Evaluation Criteria — Day 39 — Task 04 — Reusable Security Test Helpers

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 39 Task 04 (`security-test-util`).

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

- Implement the four helper methods in `SecurityTestSupport`.
- Notice the stub lives in `src/test/java`: helpers are test code, not production code.
- Add a helper of your own, e.g. `asRole(String...)`.

### Edge cases

- POSTs fail with 403 unless a CSRF token accompanies the request.
- Wrong Basic credentials give 401 (authentication), a missing role gives 403.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day39-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 39 Task 04 (Reusable Security Test Helpers) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
