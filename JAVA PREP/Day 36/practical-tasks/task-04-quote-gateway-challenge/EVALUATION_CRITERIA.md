# Evaluation Criteria — Day 36 — Task 04 — HTTP Gateway: Retry, Fallback and Headers

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 36 Task 04 (`quote-gateway-challenge`).

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

- Implement all four gateway methods using the injected `RestClient`.
- Retry exactly once on 5xx; never retry 4xx.

### Edge cases

- Build URIs with `uriBuilder`, never string concatenation.
- `toBodilessEntity()` still exposes headers and status.
- Retry loops must be bounded.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day36-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 36 Task 04 (HTTP Gateway: Retry, Fallback and Headers) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
