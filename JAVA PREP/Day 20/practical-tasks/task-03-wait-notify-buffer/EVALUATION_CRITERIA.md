# Evaluation Criteria — Day 20 — Task 03 — Producer/Consumer Bounded Buffer

## Scope

Graded: the behavior and quality of the implementation in `BoundedBuffer.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `BoundedBuffer(capacity)` rejects capacity <= 0 with `IllegalArgumentException`
- Requirement 2: `put(item)` rejects `null` with `NullPointerException`; blocks (WAITING) while the buffer is full
- Requirement 3: `take()` blocks (WAITING) while the buffer is empty and returns items in FIFO order
- Requirement 4: `size()` returns the current number of items; `capacity()` the configured limit
- Requirement 5: Both blocking methods wait in a **loop** and use `notifyAll()` after changing state; `InterruptedException` is propagated
- Requirement 6: A producer and a consumer thread can transfer 10_000 items through a capacity-3 buffer in order without loss

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- capacity 1
- interrupt while waiting
- null items
- wake-ups after state changes (loop, not `if`)

### Day-specific checks

- `while` loops (never `if`) around `wait()`
- All state accessed under the same monitor
- Interrupt propagated, not swallowed

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 20 Task 03 (Producer/Consumer Bounded Buffer) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `BoundedBuffer.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
