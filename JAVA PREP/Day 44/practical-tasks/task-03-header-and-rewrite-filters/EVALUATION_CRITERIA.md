# Evaluation Criteria — Day 44 — Task 03 — Strip-Prefix, Header and Rewrite Filters

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 44 Task 03 (`header-and-rewrite-filters`).

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

- `StripPrefixFilter` removes N leading segments and keeps the query string.
- `AddRequestHeaderFilter` sets/overwrites a header.
- `RewritePathFilter` applies a regex replacement to the path.
- Every filter must call `next` with the modified request and return its response.

### Edge cases

- More segments than available.
- Header already present.
- Non-matching rewrite.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day44-task03)`

## AI grading prompt (paste into your grader)

```
You are grading Day 44 Task 03 (Strip-Prefix, Header and Rewrite Filters) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
