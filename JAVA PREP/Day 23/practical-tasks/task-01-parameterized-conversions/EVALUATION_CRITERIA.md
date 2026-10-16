# Evaluation Criteria — Day 23 — Task 01 — Parameterized Conversions: Roman Numerals and Slugs

## Scope

Graded: the behavior and quality of the implementation in `RomanNumerals.java`, `Slugs.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `toRoman(n)` converts 1..3999 to canonical Roman numerals using subtractive notation (`IV`, `IX`, `XL`, `XC`, `CD`, `CM`); outside the range -> `IllegalArgumentException`
- Requirement 2: `fromRoman(text)` converts canonical numerals back to an int; lower case is accepted; null, blank, invalid characters, or **non-canonical** forms (`IIII`, `VX`, `IC`) -> `IllegalArgumentException`
- Requirement 3: `Slugs.slugify(text)` lower-cases, strips accents (`Normalizer` NFD + remove combining marks), collapses every run of non-alphanumeric characters into a single `-`, and trims leading/trailing dashes; blank input -> empty string; `null` -> `IllegalArgumentException`
- Requirement 4: `Slugs.isValidSlug(text)` is true for non-empty strings made of `[a-z0-9]` groups separated by single dashes

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- 0, 4000, negative numbers
- non-canonical Roman strings
- accents, emoji, and punctuation only input
- leading/trailing/multiple separators

### Day-specific checks

- Edge cases are handled before the main algorithm
- No duplicated tables (single source of truth for symbols)
- `Locale.ROOT` used for case conversion

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`, JaCoCo summary (`target/site/jacoco/index.html`)

## AI-assisted grading prompt (optional)

```
You are grading Day 23 Task 01 (Parameterized Conversions: Roman Numerals and Slugs) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `RomanNumerals.java`, `Slugs.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
