# Task 1 — Parameterized Conversions: Roman Numerals and Slugs

**Day:** 23 · **Task ID:** Day23-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Implement `RomanNumerals` (to/from Roman) and `Slugs.slugify`. The provided test classes demonstrate `@ParameterizedTest` with `@CsvSource`, `@ValueSource`, `@MethodSource`, `@NullAndEmptySource`, and a full round-trip property check - read them to learn the JUnit 5 style you will use for your own tests.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day23/task01/RomanNumerals.java` | Stubs with TODOs |
| `src/main/java/com/javaprep/day23/task01/Slugs.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day23/task01/RomanNumeralsTest.java` | Specification tests (read-only) |
| `src/test/java/com/javaprep/day23/task01/SlugsTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 23 theory file read

## What you will implement

1. `toRoman(n)` converts 1..3999 to canonical Roman numerals using subtractive notation (`IV`, `IX`, `XL`, `XC`, `CD`, `CM`); outside the range -> `IllegalArgumentException`
2. `fromRoman(text)` converts canonical numerals back to an int; lower case is accepted; null, blank, invalid characters, or **non-canonical** forms (`IIII`, `VX`, `IC`) -> `IllegalArgumentException`
3. `Slugs.slugify(text)` lower-cases, strips accents (`Normalizer` NFD + remove combining marks), collapses every run of non-alphanumeric characters into a single `-`, and trims leading/trailing dashes; blank input -> empty string; `null` -> `IllegalArgumentException`
4. `Slugs.isValidSlug(text)` is true for non-empty strings made of `[a-z0-9]` groups separated by single dashes

## Constraints

- Use plain Java (`java.text.Normalizer`, `java.util.regex`) - no third-party libraries
- Do not edit the tests; read them as examples of parameterized testing
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=RomanNumeralsTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **12 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day23-task01)`).

### Run one test class

```bash
mvn -Dtest=RomanNumeralsTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `RomanNumerals.java` — `toRoman` | `TODO(Day23-task01)` | IllegalArgumentException outside 1..3999; greedily subtract the largest VALUES entry and append its SYMBOLS entry |
| `RomanNumerals.java` — `fromRoman` | `TODO(Day23-task01)` | null/blank -> IllegalArgumentException; upper-case (Locale.ROOT); parse greedily using SYMBOLS/VALUES; the leftover must be empty and toRoman(result) must equal the input (rejects IIII, VX, IC) otherwise IllegalArgumentException |
| `Slugs.java` — `slugify` | `TODO(Day23-task01)` | null -> IllegalArgumentException; Normalizer.normalize(NFD), remove COMBINING_MARKS, toLowerCase(Locale.ROOT), replace NON_ALNUM runs with "-", strip leading/trailing "-" |
| `Slugs.java` — `isValidSlug` | `TODO(Day23-task01)` | true only for non-null text matching VALID (lowercase alphanumerics separated by single dashes) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_toRomanRejectsOutOfRange` |
| 2 | `r2_fromRoman`, `r2_fromRomanRejectsInvalid`, `r2_fromRomanRejectsNull`, `r2_roundTrip`, `r2_differentNumbersGiveDifferentNumerals` |
| 3 | `r3_blankOrEmptyBecomesEmptyExceptNull`, `r3_slugifyIsIdempotent` |
| 4 | `r4_validSlugs`, `r4_invalidSlugs`, `r4_nullIsNotAValidSlug`, `r4_everySlugifiedValueIsValidOrEmpty` |

## Edge cases to handle

- 0, 4000, negative numbers
- non-canonical Roman strings
- accents, emoji, and punctuation only input
- leading/trailing/multiple separators

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 23: Parameterized Conversions: Roman Numerals and Slugs`

## Hints (optional)

<details><summary>Hint 1</summary>

Roman numerals: loop over parallel `VALUES`/`SYMBOLS` arrays from large to small.

</details>

<details><summary>Hint 2</summary>

For `fromRoman`, a cheap way to reject non-canonical input is to convert back with `toRoman` and compare.

</details>

<details><summary>Hint 3</summary>

`Normalizer.normalize(text, Normalizer.Form.NFD)` splits `é` into `e` + a combining mark that `\p{M}` matches.

</details>
