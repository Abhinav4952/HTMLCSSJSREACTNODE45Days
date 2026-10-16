# Evaluation Criteria — Day 42 — Task 01 — @Async with CompletableFuture

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 42 Task 01 (`async-completable-future`).

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

- Enable async support and annotate the four service methods with `@Async`.
- Implement the four async methods and `Aggregator.sumOfSquares`.

### Edge cases

- Calling an `@Async` method from the same class bypasses the proxy: that is why `Aggregator` is a separate bean.
- Return failures inside the future; `void` async methods lose exceptions (use an AsyncUncaughtExceptionHandler).
- Always restore the interrupt flag after catching `InterruptedException`.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day42-task01)`

## AI grading prompt (paste into your grader)

```
You are grading Day 42 Task 01 (@Async with CompletableFuture) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
