# Evaluation Criteria — Day 21 — Task 04 — Atomics, Locks, and Concurrent Maps

## Scope

Graded: the behavior and quality of the implementation in `AtomicToolkit.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `HitCounter`: `hit()` increments atomically, `count()` returns the total, `reset()` returns the previous count and sets it to 0 atomically (`getAndSet`)
- Requirement 2: `MaxTracker`: `offer(value)` keeps the maximum seen using a **compare-and-set loop**; `get()` returns the maximum (`Integer.MIN_VALUE` before any offer)
- Requirement 3: `WordCounter`: `add(word)` increments atomically using `ConcurrentHashMap.computeIfAbsent` + `LongAdder`; `count(word)` returns 0 for unknown words; `snapshot()` returns an independent `Map<String, Long>`
- Requirement 4: `Registry`: `put`, `get`, `size` are protected by a `ReentrantReadWriteLock` (readers share the read lock; writers use the write lock); always unlock in `finally`
- Requirement 5: All components give exact results under 8 threads x 20_000 operations

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- no updates yet
- unknown words
- concurrent offers with decreasing values
- readers and writers at the same time

### Day-specific checks

- No `synchronized` in `HitCounter`/`MaxTracker`/`WordCounter`
- Every `lock()` is paired with `unlock()` in `finally`
- No check-then-act on the concurrent map

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 21 Task 04 (Atomics, Locks, and Concurrent Maps) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `AtomicToolkit.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
