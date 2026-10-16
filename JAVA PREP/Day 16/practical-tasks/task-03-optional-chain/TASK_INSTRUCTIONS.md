# Task 3 — Optional Chains Without Null Checks

**Day:** 16 · **Task ID:** Day16-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Model absent data with `Optional`: navigate a nullable `User -> Address -> city` chain, search a list, parse input safely, and convert absence into a meaningful exception - all without writing `if (x == null)` in the main logic path (null checks are allowed only at the API boundary through `Optional.ofNullable`).

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day16/task03/Address.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day16/task03/User.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day16/task03/OptionalChain.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day16/task03/OptionalChainTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 16 theory file read

## What you will implement

1. `cityOf(user)` returns the trimmed city, or empty when the user, address, or city is null/blank
2. `findByName(users, name)` finds the first user whose name equals `name` ignoring case; `null` name or no match -> empty
3. `parsePositive(text)` returns the parsed positive integer, or empty for null, blank, non-numeric, zero, or negative input
4. `zipOrDefault(user, defaultZip)` returns the zip code or the default (compute lazily using `orElseGet` where it makes sense)
5. `requireCity(user)` returns the city or throws `IllegalStateException` whose message contains the user's name (or `unknown` when the user is null)

## Constraints

- Do not call `Optional.get()` or `isPresent()`
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=OptionalChainTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **6 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day16-task03)`).

### Run one test class

```bash
mvn -Dtest=OptionalChainTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `OptionalChain.java` — `cityOf` | `TODO(Day16-task03)` | Optional.ofNullable(user) -> map address -> map city -> map trim -> filter non-empty |
| `OptionalChain.java` — `findByName` | `TODO(Day16-task03)` | first user whose name equalsIgnoreCase name; empty if name is null or none matches (loop or later-day streams are both fine) |
| `OptionalChain.java` — `parsePositive` | `TODO(Day16-task03)` | parse a trimmed int; empty for null/blank/non-numeric/overflow/zero/negative (catch NumberFormatException) |
| `OptionalChain.java` — `zipOrDefault` | `TODO(Day16-task03)` | return the address zip, or defaultZip when the user, address, or zip is missing |
| `OptionalChain.java` — `requireCity` | `TODO(Day16-task03)` | return cityOf(user) or throw IllegalStateException with a message containing the user's name ("unknown" for a null user) via orElseThrow |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_cityOf` |
| 2 | `r2_findByName` |
| 3 | `r3_parsePositive`, `r3_parsePositiveRejects` |
| 4 | `r4_zipOrDefault` |
| 5 | `r5_requireCity` |

## Edge cases to handle

- null user
- null address
- blank city
- whitespace around numbers (`" 42 "` parses)
- overflow like `99999999999` returns empty

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 16: Optional Chains Without Null Checks`

## Hints (optional)

<details><summary>Hint 1</summary>

`flatMap` is the right tool when your lambda itself returns an `Optional` (e.g. a safe parse).

</details>

<details><summary>Hint 2</summary>

A `try/catch` for `NumberFormatException` inside the `flatMap` lambda is a clean way to turn parsing failure into `Optional.empty()`.

</details>
