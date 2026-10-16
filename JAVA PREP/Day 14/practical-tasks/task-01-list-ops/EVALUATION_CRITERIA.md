# Evaluation Criteria — Day 14 — Task 01 — List Operations Toolkit

## Scope

Graded: the behavior and quality of the implementation in `ListOps.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `dedupe(list)` returns a new list without duplicates, keeping the first occurrence order; `null` input throws `NullPointerException`
- Requirement 2: `rotate(list, k)` returns a new list rotated right by `k` (negative `k` rotates left, `|k|` larger than size wraps, empty list returns empty)
- Requirement 3: `chunk(list, size)` splits into consecutive sub-lists of `size` (last may be shorter); chunks are independent copies; `size <= 0` throws `IllegalArgumentException`
- Requirement 4: `removeFirstOccurrence(list, value)` returns a copy with the first element **equal to** `value` removed (value semantics, not index), or an unchanged copy when absent; the argument is never mutated

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty lists
- rotation by multiples of the size
- negative rotation
- chunk size larger than list

### Day-specific checks

- Argument lists are never mutated
- The `remove(Object)` vs `remove(int)` trap is handled explicitly
- No O(n^2) work on `LinkedList` inputs beyond what is required

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 14 Task 01 (List Operations Toolkit) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `ListOps.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
