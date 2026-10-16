# Evaluation Criteria — Day 32 — Task 03 — ddl-auto=validate with Your Own schema.sql

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 32 Task 03 (`schema-sql-validate`).

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

- Write `src/main/resources/schema.sql` creating `products` with exactly the columns the entity expects.
- Understand why `validate` fails fast on mismatches while `create-drop` hides them.

### Edge cases

- Types must be compatible (`numeric(10,2)` vs `BigDecimal`, `timestamp` vs `LocalDateTime`).
- Column names follow Spring's snake_case naming strategy (`createdAt` -> `created_at` is set explicitly here).

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day32-task03)`

## AI grading prompt (paste into your grader)

```
You are grading Day 32 Task 03 (ddl-auto=validate with Your Own schema.sql) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
