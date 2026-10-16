# Task 1 — Unique and Normalize Sets

**Day:** 15 · **Task ID:** Day15-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Use `Set` implementations deliberately: normalize raw strings into an insertion-ordered unique set, find duplicates, and implement set algebra (union, intersection, difference) that returns **new** sets and never mutates its arguments.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day15/task01/UniqueNormalize.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day15/task01/UniqueNormalizeTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 15 theory file read

## What you will implement

1. `normalize(List<String>)` returns a `LinkedHashSet` of trimmed, lower-case, non-blank strings in first-seen order; `null` elements are skipped; a `null` list throws `NullPointerException`
2. `duplicates(List<T>)` returns a `LinkedHashSet` of elements that occur more than once (in order of their second occurrence)
3. `union(a, b)`, `intersection(a, b)`, `difference(a, b)` return new sets and leave `a` and `b` unchanged
4. `sortedCaseInsensitive(Collection<String>)` returns a `TreeSet` using `String.CASE_INSENSITIVE_ORDER` (so "A" and "a" collapse to the first inserted)

## Constraints

- Do not edit the tests; do not hard-code expected values
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=UniqueNormalizeTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day15-task01)`).

### Run one test class

```bash
mvn -Dtest=UniqueNormalizeTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `UniqueNormalize.java` — `normalize` | `TODO(Day15-task01)` | trim + lower-case each element, skip null and blank, keep first-seen order in a LinkedHashSet; NullPointerException for null list |
| `UniqueNormalize.java` — `duplicates` | `TODO(Day15-task01)` | return the elements seen more than once, ordered by when the repeat was detected (use the boolean result of Set.add) |
| `UniqueNormalize.java` — `union` | `TODO(Day15-task01)` | new set containing every element of a and b; do not mutate a or b |
| `UniqueNormalize.java` — `intersection` | `TODO(Day15-task01)` | new set of the elements present in both; do not mutate a or b |
| `UniqueNormalize.java` — `difference` | `TODO(Day15-task01)` | new set of the elements in a that are not in b; do not mutate a or b |
| `UniqueNormalize.java` — `sortedCaseInsensitive` | `TODO(Day15-task01)` | TreeSet with String.CASE_INSENSITIVE_ORDER containing words; the first inserted spelling wins |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_normalizeTrimsLowercasesAndKeepsOrder`, `r1_normalizeEdgeCases` |
| 2 | `r2_duplicates` |
| 3 | `r3_setAlgebra`, `r3_argumentsAreNeverMutated`, `r3_disjointAndEmpty` |
| 4 | `r4_caseInsensitiveSortedSet` |

## Edge cases to handle

- null and blank elements
- empty inputs
- disjoint sets
- case-insensitive collapse keeps the first inserted spelling

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 15: Unique and Normalize Sets`

## Hints (optional)

<details><summary>Hint 1</summary>

`Set.add` returns false for an element that is already present - use that in `duplicates`.

</details>

<details><summary>Hint 2</summary>

Copy first (`new LinkedHashSet<>(a)`), then `addAll`/`retainAll`/`removeAll` the copy.

</details>
