# Evaluation Criteria — Day 17 — Task 03 — Collectors Workout

## Scope

Graded: the behavior and quality of the implementation in `CollectorsWorkout.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `upperNames(names)` collects the upper-cased names into a `List` in input order
- Requirement 2: `uniqueLengths(words)` collects the distinct word lengths into a `Set<Integer>`
- Requirement 3: `lengthByWord(words)` returns a `Map<String,Integer>` word -> length that keeps the **first** value on duplicate words and preserves first-seen order (`LinkedHashMap`)
- Requirement 4: `csv(items)` joins with `", "` and wraps in `[` `]`; an empty list gives `[]`
- Requirement 5: `immutableSorted(items)` returns a naturally sorted list that rejects modification with `UnsupportedOperationException` (use `collectingAndThen`)
- Requirement 6: `toIdsByType(entries)` groups `type:id` strings like `"a:1"` into a `TreeMap<String, List<String>>` of ids per type (sorted by type, ids in input order) using `Collectors.groupingBy` with a `mapping` downstream

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- duplicate words in `toMap`
- empty input
- ids appear in encounter order within each type

### Day-specific checks

- Chooses the collector overload that fits (merge function, map supplier)
- No intermediate mutable collections built by hand
- Result mutability matches the requirements

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 17 Task 03 (Collectors Workout) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `CollectorsWorkout.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
