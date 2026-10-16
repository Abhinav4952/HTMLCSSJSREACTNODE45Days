# Evaluation Criteria — Day 17 — Task 02 — Reduce, Sum, and Statistics

## Scope

Graded: the behavior and quality of the implementation in `ReduceSum.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `sum(numbers)` adds all values with `reduce(0, Integer::sum)`; empty list -> 0
- Requirement 2: `product(numbers)` returns the product as a `long` (empty list -> 1)
- Requirement 3: `max(numbers)` returns an `Optional<Integer>`; empty -> empty
- Requirement 4: `average(numbers)` returns an `OptionalDouble` using a primitive stream; empty -> empty
- Requirement 5: `longest(words)` returns the longest word as `Optional`; when several have the same maximum length the **first** wins; `null` words are ignored
- Requirement 6: `stats(numbers)` returns an `IntSummaryStatistics` (count, sum, min, max)
- Requirement 7: `sumLong(numbers)` sums as `long` so large inputs do not overflow `int`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty list
- negative numbers
- ties for longest
- overflow (`Integer.MAX_VALUE` twice)

### Day-specific checks

- Correct identities and associative accumulators
- Primitive streams used where boxing is pointless
- No mutable external accumulators

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 17 Task 02 (Reduce, Sum, and Statistics) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `ReduceSum.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
