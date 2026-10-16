# Evaluation Criteria — Day 18 — Task 04 — Parallel Safety Note (Documentation + Sequential Implementation)

## Scope

Graded: the behavior and quality of the implementation in `ParallelSafety.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `sumOfSquares(values)` computes the sum of squares as a `long` **sequentially** (no `parallel()`), without `int` overflow
- Requirement 2: `squaresInOrder(values)` returns the squares in encounter order (sequential `map`, `toList`)
- Requirement 3: `isSafeToParallelize(stateless, associative, splittable, elementCount, blocking)` returns `true` only when the work is stateless AND associative AND the source is splittable AND it is not blocking AND `elementCount >= 10_000`
- Requirement 4: `parallelCautions()` returns at least 5 non-trivial sentences (each longer than 40 characters) that together mention: `associative`, `stateless`, `side effect`, `common pool`, `blocking`, and `measure` (case-insensitive)

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty input to the numeric methods
- boundary at exactly 10_000 elements
- `int` overflow (`46341 * 46341`)
- documentation sentences must be meaningful, not keyword stuffing

### Day-specific checks

- No `parallel()`/`parallelStream()` in the implementations
- Each caution states a reason, not just a rule
- Decision helper expresses the checklist exactly

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 18 Task 04 (Parallel Safety Note (Documentation + Sequential Implementation)) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `ParallelSafety.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
