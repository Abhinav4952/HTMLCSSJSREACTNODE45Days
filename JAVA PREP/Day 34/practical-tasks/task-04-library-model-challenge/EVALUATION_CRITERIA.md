# Evaluation Criteria — Day 34 — Task 04 — Library Model: 1:1, 1:N and N:M Together

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 34 Task 04 (`library-model-challenge`).

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

- Map `Author.books`, `Book.author`, `Book.detail`, `Book.tags` and `Tag.books`.
- Implement `addBook`, `removeBook`, `tag`.
- Decide where cascade is safe (author->book->detail) and where it is not (tags).

### Edge cases

- Removing an author must not remove shared tags.
- All associations must be LAZY at runtime.
- `orphanRemoval` on Book.detail removes details together with removed books.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day34-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 34 Task 04 (Library Model: 1:1, 1:N and N:M Together) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
