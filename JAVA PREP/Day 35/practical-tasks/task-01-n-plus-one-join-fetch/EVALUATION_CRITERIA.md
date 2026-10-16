# Evaluation Criteria — Day 35 — Task 01 — Detect and Fix N+1 Queries

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 35 Task 01 (`n-plus-one-join-fetch`).

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

- Add `findAllWithBooks` (join fetch) and `findAllWithGraph` (entity graph) to the repository.
- Implement the two optimized report methods; observe the statement counts.

### Edge cases

- `distinct` removes duplicate parents caused by the join.
- Never `join fetch` two collections (cartesian product / MultipleBagFetchException) and do not paginate in memory over fetched collections.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day35-task01)`

## AI grading prompt (paste into your grader)

```
You are grading Day 35 Task 01 (Detect and Fix N+1 Queries) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
