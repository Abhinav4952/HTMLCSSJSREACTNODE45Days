# Evaluation Criteria — Day 31 — Task 01 — Create User: DTOs and Bean Validation

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 31 Task 01 (`create-user-validation`).

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

- Add constraints to `CreateUserRequest`.
- Enable validation with `@Valid` in `UserController`.
- Map the request to `UserResponse` (trim name, lowercase email, no password).

### Edge cases

- Missing validation -> the handler would run with bad data (NPE or silent success).
- Boundary ages 18 and 120 are valid.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day31-task01)`

## AI grading prompt (paste into your grader)

```
You are grading Day 31 Task 01 (Create User: DTOs and Bean Validation) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
