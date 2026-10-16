# Evaluation Criteria — Day 13 — Task 03 — PECS Copy Utilities

## Scope

Graded: the behavior and quality of the implementation in `Pecs.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `copy(dst, src)` appends every element of `src` (`List<? extends T>`) to `dst` (`List<? super T>`)
- Requirement 2: `moveAll(src, dst)` moves all elements from `Collection<? extends T>` into `Collection<? super T>` and leaves `src` empty
- Requirement 3: `fill(dst, value, n)` adds `n` copies of `value` to a `List<? super T>`; negative `n` throws `IllegalArgumentException`
- Requirement 4: `firstOrDefault(src, def)` returns the first element of a `List<? extends T>` or `def` when empty
- Requirement 5: `swap(List<?> list, int i, int j)` swaps two elements using a private capture helper

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty source
- negative count in fill
- swap with equal indexes is a no-op
- out-of-range swap index raises `IndexOutOfBoundsException` (from the list)

### Day-specific checks

- Producers use `? extends`, consumers `? super` - no unnecessary invariant parameters
- Wildcard capture helper used instead of raw types/casts

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 13 Task 03 (PECS Copy Utilities) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `Pecs.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
