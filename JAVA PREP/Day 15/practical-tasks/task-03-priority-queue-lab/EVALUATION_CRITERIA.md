# Evaluation Criteria — Day 15 — Task 03 — Queues, Deques, and Priority Queues

## Scope

Graded: the behavior and quality of the implementation in `PriorityQueueLab.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `processOrder(List<Job>)` returns job ids in execution order: higher `priority` first, ties broken by id ascending (use a `PriorityQueue`)
- Requirement 2: `kSmallest(List<Integer>, k)` returns the `k` smallest values ascending using a bounded max-heap; `k <= 0` -> empty; `k >= size` -> all values sorted
- Requirement 3: `isBalanced(String)` checks `()`, `[]`, `{}` nesting using an `ArrayDeque` stack; characters other than brackets are ignored
- Requirement 4: `rotateLeft(List<T>, k)` rotates left by `k` (mod size, negative allowed) using an `ArrayDeque`, returning a new list

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty input
- duplicate priorities
- k of 0 / negative / larger than the list
- unbalanced closers (`"]"`), interleaved types (`"(]"`), leftover openers

### Day-specific checks

- Correct data structure for each method (heap, stack, deque)
- `ArrayDeque` used instead of `Stack`/`LinkedList`
- Does not iterate a `PriorityQueue` expecting sorted order

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 15 Task 03 (Queues, Deques, and Priority Queues) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `PriorityQueueLab.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
