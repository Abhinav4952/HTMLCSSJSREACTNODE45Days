# Evaluation Criteria — Day 22 — Task 01 — Virtual Thread Runner

## Scope

Graded: the behavior and quality of the implementation in `VirtualThreads.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `start(name, runnable)` starts and returns a **virtual** thread with exactly that name
- Requirement 2: `isVirtual(thread)` reports whether the thread is virtual
- Requirement 3: `runAll(tasks)` runs every callable on a virtual-thread-per-task executor and returns the results **in input order**; a failing task surfaces as `ExecutionException`; the executor is always closed
- Requirement 4: `factory(prefix)` returns a `ThreadFactory` whose threads are unstarted virtual threads named `prefix0`, `prefix1`, ...
- Requirement 5: `runLimited(tasks, permits, sleepMillis)` runs `tasks` virtual threads that each hold a semaphore permit while sleeping `sleepMillis`, and returns a `Stats(completed, peakConcurrency)` where the peak never exceeds `permits`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty task list
- a failing callable in `runAll`
- permits larger than tasks
- invalid arguments (`permits <= 0`) rejected

### Day-specific checks

- One virtual thread per task - no fixed pools
- Semaphore released in `finally`
- Executor closed on every path (try-with-resources)

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 22 Task 01 (Virtual Thread Runner) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `VirtualThreads.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
