# Evaluation Criteria — Day 37 — Task 03 — BCrypt Password Hashing

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 37 Task 03 (`bcrypt-password-service`).

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

- Create the encoder with the configurable strength.
- Implement `hash`, `matches` and `needsUpgrade` with the documented null/length rules.

### Edge cases

- Never log or store raw passwords.
- BCrypt only uses the first 72 bytes of input.
- Hash verification must be timing-safe: always use `matches`, never `equals`.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day37-task03)`

## AI grading prompt (paste into your grader)

```
You are grading Day 37 Task 03 (BCrypt Password Hashing) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
