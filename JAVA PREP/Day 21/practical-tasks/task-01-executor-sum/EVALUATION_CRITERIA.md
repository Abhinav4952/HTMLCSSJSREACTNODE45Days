# Evaluation Criteria — Day 21 — Task 01 — Executor Chunked Sum

## Scope

Graded: the behavior and quality of the implementation in `ExecutorSum.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `parallelSum(numbers, chunks, pool)` splits the list into at most `chunks` consecutive slices, sums each in the pool, and returns the total as a `long`; `chunks <= 0` -> `IllegalArgumentException`; empty list -> 0
- Requirement 2: `runAll(pool, tasks)` runs all callables with `invokeAll` and returns their results **in input order**; if a task failed, the `ExecutionException` (with its cause) propagates
- Requirement 3: `shutdownGracefully(pool, timeoutMillis)` calls `shutdown`, waits up to the timeout, then `shutdownNow`; returns `true` if the pool terminated on its own, `false` if it had to be forced

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- more chunks than elements
- empty list
- a failing task in `runAll`
- pool with a task that never finishes (forced shutdown)

### Day-specific checks

- Pool is never created/owned by the helper (caller decides lifecycle) except for shutdown helper
- Futures are consumed (failures are not lost)
- Interrupt flag restored when `InterruptedException` is caught

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 21 Task 01 (Executor Chunked Sum) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `ExecutorSum.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
