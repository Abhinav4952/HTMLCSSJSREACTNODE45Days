# Evaluation Criteria — Day 15 — Task 02 — Frequency Map Toolkit

## Scope

Graded: the behavior and quality of the implementation in `FrequencyMap.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `count(List<String>)` returns word -> occurrences; words are trimmed and lower-cased; blank/null words are ignored
- Requirement 2: `topN(counts, n)` returns the `n` most frequent words, ordered by count descending then word ascending; `n <= 0` returns an empty list; `n` larger than the number of words returns all
- Requirement 3: `invert(counts)` returns a `SortedMap<Integer, List<String>>` (counts ascending) where each list of words is sorted alphabetically
- Requirement 4: `mergeCounts(a, b)` returns a new map summing counts for shared keys without mutating inputs

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty input
- ties in `topN`
- blank and null words
- inputs left unmodified by `mergeCounts`

### Day-specific checks

- Uses `merge`/`computeIfAbsent` rather than `containsKey`/`get`/`put` boilerplate
- Deterministic ordering is produced by explicit comparators, not by `HashMap` luck

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 15 Task 02 (Frequency Map Toolkit) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `FrequencyMap.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
