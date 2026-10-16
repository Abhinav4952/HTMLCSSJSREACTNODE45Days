# Evaluation Criteria — Day 17 — Task 04 — Challenge: Word Count Analyzer

## Scope

Graded: the behavior and quality of the implementation in `WordCount.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `countWords(text, stopWords)` returns word -> count; words are lower-cased runs of letters/digits; stop words are excluded; `null`/blank text gives an empty map
- Requirement 2: `topN(text, n, stopWords)` returns `"word=count"` strings, most frequent first, ties broken alphabetically; `n <= 0` gives an empty list
- Requirement 3: `lengthHistogram(text)` returns a `SortedMap<Integer, Long>` word length -> number of word occurrences
- Requirement 4: `hapax(text)` returns a `SortedSet<String>` of words that appear exactly once

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- punctuation, apostrophes and newlines split words
- mixed case
- digits are word characters
- stop words are matched case-insensitively (provided lower-case)

### Day-specific checks

- Entire pipelines are expressed with streams and collectors
- Deterministic ordering is produced explicitly
- Private helper `words(...)` reused instead of duplicated splitting logic

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 17 Task 04 (Challenge: Word Count Analyzer) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `WordCount.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
