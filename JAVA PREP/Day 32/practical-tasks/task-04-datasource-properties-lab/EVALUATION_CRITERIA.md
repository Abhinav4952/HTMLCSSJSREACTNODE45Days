# Evaluation Criteria — Day 32 — Task 04 — Datasource and JPA Properties

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 32 Task 04 (`datasource-properties-lab`).

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

- Fill `src/main/resources/application.properties` with the seven documented settings.
- Explain in your own words why `open-in-view=false` is preferred for APIs.

### Edge cases

- `DB_CLOSE_DELAY=-1` keeps an in-memory DB alive between connections.
- Without a url, Boot would silently use an embedded default database.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day32-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 32 Task 04 (Datasource and JPA Properties) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
