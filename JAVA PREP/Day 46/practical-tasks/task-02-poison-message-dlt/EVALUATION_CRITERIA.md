# Evaluation Criteria — Day 46 — Task 02 — Poison Message and Dead-Letter Topic

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 46 Task 02 (`poison-message-dlt`).

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

- Create a `DeadLetterPublishingRecoverer` from the template (default destination `<topic>.DLT`, same partition).
- Use `FixedBackOff(10L, 2L)`: two retries after the first failure.
- Return a `DefaultErrorHandler(recoverer, backOff)`.

### Edge cases

- The DLT must have at least as many partitions as the source topic.
- Healthy records after the poison one must still be processed.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day46-task02)`

## AI grading prompt (paste into your grader)

```
You are grading Day 46 Task 02 (Poison Message and Dead-Letter Topic) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
