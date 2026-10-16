# Evaluation Criteria — Day 13 — Task 02 — Bounded Max/Min/Clamp

## Scope

Graded: the behavior and quality of the implementation in `BoundedMath.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `max(List)` returns the greatest element by natural order; empty or null list throws `IllegalArgumentException`
- Requirement 2: `min(List)` returns the smallest element; same validation
- Requirement 3: `max`/`min` signatures use `T extends Comparable<? super T>` so `List<Dog>` works when `Dog extends Animal implements Comparable<Animal>`
- Requirement 4: `clamp(value, lo, hi)` constrains a value into `[lo, hi]` for `T extends Number & Comparable<T>`; `lo > hi` throws `IllegalArgumentException`
- Requirement 5: `sum(Collection<? extends Number>)` adds `doubleValue()`s and treats an empty collection as `0.0`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty list, null list
- single-element list
- lo == hi in clamp
- a `List<Integer>` and a `List<Double>` both accepted by `sum`

### Day-specific checks

- Signatures use `Comparable<? super T>` and `List<? extends T>` exactly as described
- No casts to `Comparable` or `Object`

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 13 Task 02 (Bounded Max/Min/Clamp) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `BoundedMath.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
