# Evaluation Criteria — Day 35 — Task 04 — Flyway Versioned Migrations

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 35 Task 04 (`flyway-migrations`).

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

- Write `V1__create_articles.sql` under `src/main/resources/db/migration`.
- Write `V2__add_article_status.sql` adding the status column with a default.

### Edge cases

- File names follow `V<version>__<description>.sql` (two underscores).
- Applied migrations are immutable: Flyway checksums them.
- `ddl-auto=validate` fails fast when SQL and entity disagree.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day35-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 35 Task 04 (Flyway Versioned Migrations) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
