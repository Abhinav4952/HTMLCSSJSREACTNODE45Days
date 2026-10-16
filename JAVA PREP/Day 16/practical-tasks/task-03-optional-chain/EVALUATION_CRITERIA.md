# Evaluation Criteria — Day 16 — Task 03 — Optional Chains Without Null Checks

## Scope

Graded: the behavior and quality of the implementation in `OptionalChain.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `cityOf(user)` returns the trimmed city, or empty when the user, address, or city is null/blank
- Requirement 2: `findByName(users, name)` finds the first user whose name equals `name` ignoring case; `null` name or no match -> empty
- Requirement 3: `parsePositive(text)` returns the parsed positive integer, or empty for null, blank, non-numeric, zero, or negative input
- Requirement 4: `zipOrDefault(user, defaultZip)` returns the zip code or the default (compute lazily using `orElseGet` where it makes sense)
- Requirement 5: `requireCity(user)` returns the city or throws `IllegalStateException` whose message contains the user's name (or `unknown` when the user is null)

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- null user
- null address
- blank city
- whitespace around numbers (`" 42 "` parses)

### Day-specific checks

- No `Optional.get()` and no `isPresent()`/`get()` pairs
- `orElseThrow` supplies a meaningful exception
- No `Optional` fields or parameters

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 16 Task 03 (Optional Chains Without Null Checks) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `OptionalChain.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
