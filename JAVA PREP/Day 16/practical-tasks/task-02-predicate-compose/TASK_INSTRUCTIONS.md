# Task 2 — Composing Predicates and Functions

**Day:** 16 · **Task ID:** Day16-task02 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Combine small predicates into richer rules (`allOf`, `anyOf`, `noneOf`), make predicates null-safe, build a realistic username validator from composed predicates, and chain `UnaryOperator`s into a pipeline.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day16/task02/PredicateCompose.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day16/task02/PredicateComposeTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 16 theory file read

## What you will implement

1. `allOf(predicates)` is true only if every predicate matches (empty list -> `true`)
2. `anyOf(predicates)` is true if at least one matches (empty list -> `false`)
3. `noneOf(predicates)` is true if no predicate matches (empty list -> `true`)
4. `nullSafe(predicate)` returns `false` for `null` input instead of calling the delegate
5. `validUsername()` accepts names that are 3-12 characters, start with a letter, and contain only letters, digits, or `_`; it returns `false` for `null`
6. `pipeline(operators)` composes unary operators left-to-right; an empty list is the identity

## Constraints

- Do not use regular expressions in `validUsername` (compose predicates instead)
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=PredicateComposeTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **8 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day16-task02)`).

### Run one test class

```bash
mvn -Dtest=PredicateComposeTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `PredicateCompose.java` — `allOf` | `TODO(Day16-task02)` | combine with Predicate.and; empty list yields a predicate that is always true |
| `PredicateCompose.java` — `anyOf` | `TODO(Day16-task02)` | combine with Predicate.or; empty list yields a predicate that is always false |
| `PredicateCompose.java` — `noneOf` | `TODO(Day16-task02)` | true when no predicate matches (negate anyOf); empty list is always true |
| `PredicateCompose.java` — `nullSafe` | `TODO(Day16-task02)` | return a predicate that is false for null input and otherwise delegates |
| `PredicateCompose.java` — `validUsername` | `TODO(Day16-task02)` | build from composed predicates: not null, length 3..12, first char is a letter, all chars letter/digit/underscore |
| `PredicateCompose.java` — `pipeline` | `TODO(Day16-task02)` | apply operators left to right using Function.andThen; empty list returns the identity function |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_allOf` |
| 2 | `r2_anyOf` |
| 3 | `r3_noneOf` |
| 4 | `r4_nullSafe` |
| 5 | `r5_validUsernameAccepts`, `r5_validUsernameRejects` |
| 6 | `r6_pipelineAppliesLeftToRight`, `r6_emptyPipelineIsIdentity` |

## Edge cases to handle

- empty predicate lists
- null input
- boundary lengths 2/3/12/13
- start with digit or underscore

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 16: Composing Predicates and Functions`

## Hints (optional)

<details><summary>Hint 1</summary>

`Predicate.and/or/negate` already do the heavy lifting; start from a neutral element.

</details>

<details><summary>Hint 2</summary>

`String.chars()` gives an `IntStream` - using it for `allMatch` is fine here (character check), or write a loop.

</details>
