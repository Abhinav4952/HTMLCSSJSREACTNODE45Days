# Evaluation Criteria — Day 39 — Task 02 — @DataJpaTest Slice for Repositories

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 39 Task 02 (`datajpa-slice`).

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

- Replace each `default` placeholder with an abstract derived or `@Query` method.
- Use `@Param` for the named parameters.
- Write one extra test for a case you think is missing.

### Edge cases

- `between` is inclusive on both ends.
- The slice rolls each test back, so seeds from one test are not visible in the next.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day39-task02)`

## AI grading prompt (paste into your grader)

```
You are grading Day 39 Task 02 (@DataJpaTest Slice for Repositories) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
