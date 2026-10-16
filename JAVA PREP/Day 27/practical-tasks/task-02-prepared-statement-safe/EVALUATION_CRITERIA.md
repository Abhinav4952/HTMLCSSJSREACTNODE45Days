# Evaluation Criteria — Day 27 — Task 02 — PreparedStatement and SQL Injection

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 27 Task 02 (`prepared-statement-safe`).

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

- Implement `findByName` with a `?` placeholder.
- Implement `findByNamePrefix` so `%` and `_` in user input are literal.
- Implement `insertUser` returning the generated id.
- Never concatenate user input into SQL (the provided `buildUnsafeSql` is the anti-example).

### Edge cases

- Quotes in names (`O'Brien`) must work without escaping by hand.
- Injection payloads match nothing.
- Prefix `%` must not match every row.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day27-task02)`

## AI grading prompt (paste into your grader)

```
You are grading Day 27 Task 02 (PreparedStatement and SQL Injection) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
