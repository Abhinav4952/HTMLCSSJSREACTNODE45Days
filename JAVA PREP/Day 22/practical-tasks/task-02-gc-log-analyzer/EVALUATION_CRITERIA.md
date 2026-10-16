# Evaluation Criteria — Day 22 — Task 02 — GC Log and JVM Flags Analyzer

## Scope

Graded: the behavior and quality of the implementation in `GcLogAnalyzer.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `parseSize(text)` converts `512K`, `24M`, `2G`, `100B` (case-insensitive, plain digits = bytes) to bytes; anything else -> `IllegalArgumentException`
- Requirement 2: `formatBytes(bytes)` renders human readable binary units with one decimal (`0 B`, `512 B`, `1.5 KiB`, `2.0 MiB`, `1.0 GiB`); negative -> `IllegalArgumentException`
- Requirement 3: `parseLine(line)` parses a line like `[2.345s][info][gc] GC(12) Pause Young (Normal) (G1 Evacuation Pause) 24M->4M(256M) 5.123ms` into a `GcEvent`, or returns empty for lines that do not describe a sized pause; `full` is true for `Pause Full`
- Requirement 4: `parse(log)` returns the events for all matching lines in order (ignore blank/other lines)
- Requirement 5: `summarize(events)` returns event count, number of full GCs, total and maximum pause millis, and total reclaimed bytes (`before - after` summed)
- Requirement 6: `leakSuspected(events, minConsecutive)` is true when at least `minConsecutive` consecutive **full** GC events have a strictly increasing `afterBytes`
- Requirement 7: `heapSettings(args)` reads `-Xms`, `-Xmx` (sizes like `512m`, `2g`) and the collector flag (`UseG1GC`->`G1`, `UseZGC`->`ZGC`, `UseParallelGC`->`Parallel`, `UseSerialGC`->`Serial`; default `G1`); the last occurrence wins; `Xms > Xmx` -> `IllegalArgumentException`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- garbage lines in the log
- no events (summary of nothing)
- events that are young GCs between full GCs when looking for leaks
- missing `-Xms`/`-Xmx` flags

### Day-specific checks

- Garbage input never throws from `parse`/`parseLine`
- Sizes are computed with `long` (no int overflow for GiB values)
- Parsing is separated from analysis (`parse` vs `summarize` vs `leakSuspected`)

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 22 Task 02 (GC Log and JVM Flags Analyzer) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `GcLogAnalyzer.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
