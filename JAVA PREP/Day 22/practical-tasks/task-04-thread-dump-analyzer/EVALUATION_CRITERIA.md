# Evaluation Criteria — Day 22 — Task 04 — Thread Dump Analyzer and Live Deadlock Detector

## Scope

Graded: the behavior and quality of the implementation in `ThreadDumpAnalyzer.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `parse(dump)` returns one `ThreadInfo(name, state, frames, waitingForLock, heldLocks)` per quoted thread header; state comes from `java.lang.Thread.State: X`; frames are the `at ...` lines (trimmed, without `at `); `- waiting to lock <id>` sets `waitingForLock`; each `- locked <id>` is added to `heldLocks` in order
- Requirement 2: `countByState(threads)` returns a sorted map state -> count
- Requirement 3: `hotspot(threads)` returns the most common **top frame** among `RUNNABLE` threads (ties: alphabetically first), or empty when no runnable thread has frames
- Requirement 4: `findDeadlock(threads)` returns the sorted set of thread names that take part in a wait-for cycle (A waits for a lock held by B ... back to A); empty when there is none
- Requirement 5: `liveDeadlockedThreads()` uses `ThreadMXBean.findDeadlockedThreads()` and returns the sorted names of deadlocked threads (empty list when none)

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- no threads / empty dump
- threads that wait on a lock nobody holds
- three-thread cycle
- a chain that is blocked but not a cycle

### Day-specific checks

- Parser never throws on malformed dumps
- Cycle detection terminates (no infinite loop on cycles)
- Live detection returns an empty list rather than null

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 22 Task 04 (Thread Dump Analyzer and Live Deadlock Detector) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `ThreadDumpAnalyzer.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
