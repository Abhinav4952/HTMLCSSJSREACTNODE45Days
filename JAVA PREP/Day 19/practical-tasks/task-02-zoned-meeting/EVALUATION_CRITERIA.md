# Evaluation Criteria — Day 19 — Task 02 — Zoned Meeting Scheduler

## Scope

Graded: the behavior and quality of the implementation in `ZonedMeeting.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `convert(local, from, to)` returns the `ZonedDateTime` in zone `to` for the instant described by `local` in zone `from`
- Requirement 2: `localTimes(instant, zoneIds)` returns `"yyyy-MM-dd HH:mm"` strings in the order of `zoneIds`; an unknown zone id throws `java.time.DateTimeException`
- Requirement 3: `isDuringWorkHours(t)` is true for Monday-Friday from 09:00 (inclusive) to 17:00 (exclusive) in `t`'s own zone
- Requirement 4: `minutesBetween(a, b)` returns the **elapsed** minutes (DST aware): on 2024-03-10 in `America/New_York`, 01:30 -> 03:30 is 60 minutes
- Requirement 5: `plusWeeksWallClock(start, weeks)` keeps the local time across DST changes
- Requirement 6: `formatUtc(t)` returns the ISO-8601 instant string such as `2024-05-20T09:00:00Z`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- DST spring-forward day
- boundaries 08:59/09:00/16:59/17:00
- weekends
- unknown zone id

### Day-specific checks

- Zone IDs, never fixed offsets, for region-based logic
- Understands wall-clock vs elapsed arithmetic and can explain the test on DST
- No `ZoneId.systemDefault()` in logic

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 19 Task 02 (Zoned Meeting Scheduler) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `ZonedMeeting.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
