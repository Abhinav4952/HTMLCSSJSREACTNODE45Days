# Evaluation Criteria — Day 13 — Task 01 — Generic Box with map/orElse

## Scope

Graded: the behavior and quality of the implementation in `Box.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `Box.of(value)` returns a box holding the value and throws `NullPointerException` for `null`
- Requirement 2: `Box.empty()` returns an empty box; `isEmpty()` reports the state; `get()` on an empty box throws `NoSuchElementException`
- Requirement 3: `orElse(fallback)` returns the value or the fallback
- Requirement 4: `map(fn)` returns a `Box<R>`; an empty box stays empty and a function returning `null` yields an empty box; the signature must be `Function<? super T, ? extends R>`
- Requirement 5: `equals`/`hashCode` are value-based and `toString` is `Box[value]` or `Box.empty`
- Requirement 6: `Box<String>` and `Box<Integer>` have the same runtime class (observable erasure)

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- `of(null)` -> `NullPointerException`
- mapping an empty box never calls the function
- function returning null -> empty box
- `equals` between empty boxes is true; between empty and non-empty is false

### Day-specific checks

- `map` uses `Function<? super T, ? extends R>` (PECS)
- No raw types or unchecked warnings
- Immutability preserved (no setters)

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 13 Task 01 (Generic Box with map/orElse) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `Box.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
