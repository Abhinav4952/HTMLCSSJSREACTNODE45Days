# Evaluation Criteria — Day 20 — Task 01 — Runnable Counter

## Scope

Graded: the behavior and quality of the implementation in `Counter.java`, `RunnableCounter.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `Counter.increment()` and `Counter.get()` are thread-safe (`synchronized`)
- Requirement 2: `incrementTask(counter, times)` returns a `Runnable` that calls `increment()` `times` times
- Requirement 3: `runConcurrently(counter, threads, perThread)` starts `threads` named threads (`counter-0`, `counter-1`, ...), joins them all, and returns the counter value (`threads <= 0` or `perThread < 0` -> `IllegalArgumentException`)
- Requirement 4: `startNamed(name, runnable)` returns a **started** thread having that name
- Requirement 5: `executedByWithRun()` runs a task via `Thread.run()` and returns the name of the thread that executed it (the **calling** thread)
- Requirement 6: `executedByWithStart(name)` runs a task via `start()`, joins, and returns the executing thread's name (the new thread's name)

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- zero increments
- invalid thread counts
- join all threads before reading the result
- never swallow `InterruptedException` (declare it)

### Day-specific checks

- Same lock for reads and writes of `value`
- No `Thread.sleep` used for coordination
- `InterruptedException` declared, not swallowed

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 20 Task 01 (Runnable Counter) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `Counter.java`, `RunnableCounter.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
