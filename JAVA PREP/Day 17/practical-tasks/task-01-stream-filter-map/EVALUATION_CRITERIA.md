# Evaluation Criteria — Day 17 — Task 01 — Filter, Map, Sort, and Page

## Scope

Graded: the behavior and quality of the implementation in `StreamFilterMap.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `upperLongNames(names, minLen)` trims names, drops `null`s and names shorter than `minLen`, and returns them upper-cased in input order
- Requirement 2: `squaresOfOdds(numbers)` returns the squares of the odd numbers (including negative odd numbers)
- Requirement 3: `distinctSortedLower(words)` returns trimmed, lower-cased, non-blank, de-duplicated words sorted alphabetically; `null` entries are ignored
- Requirement 4: `page(items, pageIndex, size)` returns the zero-based page using `skip`/`limit`; `pageIndex < 0` or `size <= 0` throws `IllegalArgumentException`; pages past the end are empty
- Requirement 5: `firstStartingWith(names, prefix)` returns the first name starting with the prefix as an `Optional`
- Requirement 6: `traceLaziness()` runs `filter(len > 1)` then `map(upper)` then `findFirst` over `"a", "bb", "cc"`, recording `filter:<x>` and `map:<x>` events, and returns the trace

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty list
- null elements
- page index past the end
- size 0

### Day-specific checks

- Single pipeline per method, no temporary collections
- No explicit `for`/`while` loops
- `Optional` returned, never `get()`

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 17 Task 01 (Filter, Map, Sort, and Page) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `StreamFilterMap.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
