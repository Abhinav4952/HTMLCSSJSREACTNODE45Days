# Evaluation Criteria — Day 43 — Task 03 — Circuit Breaker Facade

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 43 Task 03 (`circuit-breaker-facade`).

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

- Configure the breaker: COUNT_BASED window 4, minimum 4 calls, 50 % failure threshold, wait in OPEN = `openWait`, 1 permitted call in HALF_OPEN.
- `call()` returns the downstream value or `"FALLBACK"` for any failure and for `CallNotPermittedException`.
- While OPEN the downstream supplier must not be invoked.
- `state()` exposes the current `CircuitBreaker.State`.

### Edge cases

- Transition OPEN -> HALF_OPEN happens on the first call after the wait elapsed.
- A single failure in a window of 4 stays below 50 %.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day43-task03)`

## AI grading prompt (paste into your grader)

```
You are grading Day 43 Task 03 (Circuit Breaker Facade) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
