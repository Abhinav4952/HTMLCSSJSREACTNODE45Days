# Evaluation Criteria — Day 13 — Task 04 — Generic Array-Backed Stack

## Scope

Graded: the behavior and quality of the implementation in `ArrayStack.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: Constructor `ArrayStack(int initialCapacity)` rejects capacity <= 0 with `IllegalArgumentException`; `ArrayStack()` uses 4
- Requirement 2: `push`, `pop`, `peek`, `size`, `isEmpty` follow LIFO semantics; `pop`/`peek` on an empty stack throw `NoSuchElementException`
- Requirement 3: The backing array grows (doubling) when full, and popped slots are nulled to avoid memory leaks
- Requirement 4: `pushAll(Iterable<? extends E>)` pushes in iteration order
- Requirement 5: `popAll(Collection<? super E>)` pops everything into the sink in pop order and returns the count
- Requirement 6: `iterator()` walks from top to bottom without modifying the stack; calling `next()` past the end throws `NoSuchElementException`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- capacity 0 or negative
- growth well beyond initial capacity
- pop on empty
- iterating an empty stack

### Day-specific checks

- Exactly one justified unchecked cast pattern, annotated and commented
- Bulk operations use PECS signatures
- Popped slots are cleared

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 13 Task 04 (Generic Array-Backed Stack) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `ArrayStack.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
