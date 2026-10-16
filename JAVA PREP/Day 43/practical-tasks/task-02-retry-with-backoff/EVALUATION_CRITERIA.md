# Evaluation Criteria — Day 43 — Task 02 — Retry with Resilience4j

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 43 Task 02 (`retry-with-backoff`).

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

- Build a `RetryConfig` with `maxAttempts`, `waitDuration` and `retryExceptions(retryOn)`.
- Decorate the supplier with `Retry.decorateSupplier` and execute it.
- Rethrow the last exception when attempts are exhausted.
- Do not retry exceptions outside `retryOn`.
- Reject `maxAttempts < 1` with `IllegalArgumentException`.

### Edge cases

- `maxAttempts` counts the first call too.
- Resilience4j requires a wait of at least a few milliseconds.
- Retrying non-idempotent calls is dangerous (discuss in theory).

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day43-task02)`

## AI grading prompt (paste into your grader)

```
You are grading Day 43 Task 02 (Retry with Resilience4j) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
