# Evaluation Criteria — Day 21 — Task 02 — Future Timeouts, Cancellation, and invokeAny

## Scope

Graded: the behavior and quality of the implementation in `FutureTimeout.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `getWithTimeout(future, timeoutMillis)` returns `Optional.of(value)`; on timeout it **cancels** the future (interrupting) and returns empty; a task failure becomes `IllegalStateException` with the original exception as cause
- Requirement 2: `getOrDefault(future, timeoutMillis, fallback)` returns the value, or `fallback` on timeout or task failure (and cancels on timeout)
- Requirement 3: `firstSuccessful(pool, tasks)` returns the result of the first task that completes successfully (`invokeAny`); if all fail an `ExecutionException` propagates
- Requirement 4: `cancelRunning(future)` returns `true` only if the future was actually cancelled (interrupting a running task); completed futures return `false`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- timeout shorter than the task
- failing task
- all tasks failing in invokeAny
- cancelling an already-finished future

### Day-specific checks

- Timeouts cancel the work (no leaked running tasks)
- Interrupt flag restored in `getOrDefault`
- Original exception preserved as cause

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 21 Task 02 (Future Timeouts, Cancellation, and invokeAny) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `FutureTimeout.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
