# Evaluation Criteria — Day 27 — Task 04 — HikariCP Config Reader

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 27 Task 04 (`hikari-config-reader`).

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

- Implement `read` with defaults and validation (messages must mention the offending key).
- Implement `toHikariConfig`.
- Implement `maskedSummary` with the exact format.
- Open a real HikariCP pool in the last test to prove the config works.

### Edge cases

- Blank or missing `jdbcUrl` is an error.
- `minimumIdle` defaults to `maximumPoolSize`.
- Non-numeric values -> `IllegalArgumentException`.
- The password must never appear in the summary.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day27-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 27 Task 04 (HikariCP Config Reader) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
