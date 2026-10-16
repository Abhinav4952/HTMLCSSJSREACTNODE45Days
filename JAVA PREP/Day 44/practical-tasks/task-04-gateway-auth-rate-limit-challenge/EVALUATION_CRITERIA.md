# Evaluation Criteria — Day 44 — Task 04 — Edge Gateway: API Key + Rate Limit (Challenge)

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 44 Task 04 (`gateway-auth-rate-limit-challenge`).

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

- `ApiKeyFilter`: 401 for missing/unknown keys, otherwise continue.
- `RateLimitFilter`: per-client fixed window using the injected `Clock`; 429 when exceeded.
- `Gateway.handle`: 404 for unknown route, 502 when no backend, else filters around backend.
- Filter order matters: authentication happens before rate limiting.

### Edge cases

- Window expiry.
- Anonymous clients.
- Unauthenticated requests must not consume quota.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day44-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 44 Task 04 (Edge Gateway: API Key + Rate Limit (Challenge)) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
