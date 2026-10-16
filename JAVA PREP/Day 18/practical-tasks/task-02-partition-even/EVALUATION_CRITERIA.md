# Evaluation Criteria — Day 18 — Task 02 — Partitioning Data

## Scope

Graded: the behavior and quality of the implementation in `PartitionEven.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

## Weighting (100 points unless the instructor overrides)

| Category | Points | Description |
|----------|-------:|-------------|
| Automated tests (`mvn test`) | 40 | Fraction of tests passing; no skipped/@Disabled tests |
| Requirements coverage | 25 | Each "What you will implement" bullet satisfied |
| Code quality | 20 | Naming, structure, idiomatic Java 21, no duplication, correct use of the day's concepts |
| Robustness & safety | 10 | Edge cases, null/validation handling, exceptions, thread-safety/security where relevant |
| Readability & process | 5 | Clear commits, formatting, sensible comments |

## Pass / fail gates (automatic fail if violated)

- Tests modified/disabled to force a pass
- Hard-coded secrets
- Forbidden APIs from Constraints used
- Project does not compile

## Detailed rubric

### Automated tests

- Full marks only when every test passes with no `@Disabled` and no edits to test files.
- Partial credit is proportional to passing tests; a compile failure scores 0 in this category.

### Requirements coverage

- Requirement 1: `partitionEven(numbers)` returns `Map<Boolean, List<Integer>>` with evens under `true` and odds under `false` (input order kept)
- Requirement 2: `partition(items, predicate)` is the generic version for any element type and predicate
- Requirement 3: `countPassFail(scores, passMark)` returns the number of scores `>= passMark` under `true` and `< passMark` under `false` as `Long`
- Requirement 4: `sumEvenOdd(numbers)` returns the sum of evens under `true` and odds under `false`
- Requirement 5: For empty input, **both keys must still be present** with empty/zero results

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty input
- all even / all odd
- negative odd numbers
- pass mark boundary (equal passes)

### Day-specific checks

- Uses `partitioningBy`, not `groupingBy` with a boolean classifier
- No manual null checks for missing keys

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 18 Task 02 (Partitioning Data) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `PartitionEven.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
