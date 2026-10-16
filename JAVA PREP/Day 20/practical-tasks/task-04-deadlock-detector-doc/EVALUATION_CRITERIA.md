# Evaluation Criteria — Day 20 — Task 04 — Lock-Order Deadlock Detector

## Scope

Graded: the behavior and quality of the implementation in `LockOrderAnalyzer.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `conflictingPairs(orders)` returns a sorted set of strings `"A<->B"` (names in alphabetical order inside each pair) for every two locks that one thread takes as X-then-Y and another as Y-then-X; a lock repeated within one thread (reentrancy) counts at its first position
- Requirement 2: `hasOrderingRisk(orders)` is true exactly when `conflictingPairs` is non-empty
- Requirement 3: `coffmanConditions()` returns, in this order: `Mutual exclusion`, `Hold and wait`, `No preemption`, `Circular wait`
- Requirement 4: `advice(orders)` returns `"No lock-ordering conflicts found."` when safe; otherwise a text that lists every conflicting pair and recommends one global order (all lock names, alphabetical, comma-separated) using the phrase `global order`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- single thread (never a risk)
- same order in all threads (safe)
- reentrant duplicates (`A, A, B`)
- non-adjacent acquisition (`A, C, B` vs `B, A`)

### Day-specific checks

- Conflict detection is order-sensitive but independent of the thread order in the input
- Deterministic (sorted) output
- Explains in a comment how a global lock order breaks the circular-wait condition

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 20 Task 04 (Lock-Order Deadlock Detector) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `LockOrderAnalyzer.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
