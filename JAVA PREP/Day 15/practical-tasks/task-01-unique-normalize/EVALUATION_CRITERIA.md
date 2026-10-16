# Evaluation Criteria — Day 15 — Task 01 — Unique and Normalize Sets

## Scope

Graded: the behavior and quality of the implementation in `UniqueNormalize.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `normalize(List<String>)` returns a `LinkedHashSet` of trimmed, lower-case, non-blank strings in first-seen order; `null` elements are skipped; a `null` list throws `NullPointerException`
- Requirement 2: `duplicates(List<T>)` returns a `LinkedHashSet` of elements that occur more than once (in order of their second occurrence)
- Requirement 3: `union(a, b)`, `intersection(a, b)`, `difference(a, b)` return new sets and leave `a` and `b` unchanged
- Requirement 4: `sortedCaseInsensitive(Collection<String>)` returns a `TreeSet` using `String.CASE_INSENSITIVE_ORDER` (so "A" and "a" collapse to the first inserted)

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- null and blank elements
- empty inputs
- disjoint sets
- case-insensitive collapse keeps the first inserted spelling

### Day-specific checks

- Set implementation chosen deliberately for each requirement (Linked/Tree)
- Arguments never mutated
- No `contains` on a `List` for membership

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 15 Task 01 (Unique and Normalize Sets) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `UniqueNormalize.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
