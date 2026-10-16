# Task 2 — Frequency Map Toolkit

**Day:** 15 · **Task ID:** Day15-task02 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Build a word-frequency toolkit with the idiomatic Map API (`merge`, `getOrDefault`, `computeIfAbsent`): count words case-insensitively, rank the top N with deterministic tie-breaking, invert counts into a sorted map of groups, and merge two count maps. Tests never depend on `HashMap` iteration order.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day15/task02/FrequencyMap.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day15/task02/FrequencyMapTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 15 theory file read

## What you will implement

1. `count(List<String>)` returns word -> occurrences; words are trimmed and lower-cased; blank/null words are ignored
2. `topN(counts, n)` returns the `n` most frequent words, ordered by count descending then word ascending; `n <= 0` returns an empty list; `n` larger than the number of words returns all
3. `invert(counts)` returns a `SortedMap<Integer, List<String>>` (counts ascending) where each list of words is sorted alphabetically
4. `mergeCounts(a, b)` returns a new map summing counts for shared keys without mutating inputs

## Constraints

- Do not edit the tests; do not hard-code expected values
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=FrequencyMapTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **6 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day15-task02)`).

### Run one test class

```bash
mvn -Dtest=FrequencyMapTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `FrequencyMap.java` — `count` | `TODO(Day15-task02)` | count occurrences of trimmed lower-case words (skip null/blank) using Map.merge |
| `FrequencyMap.java` — `topN` | `TODO(Day15-task02)` | return up to n words ordered by count descending, then word ascending; n <= 0 gives an empty list |
| `FrequencyMap.java` — `invert` | `TODO(Day15-task02)` | group words by count into a TreeMap (counts ascending); each word list sorted alphabetically; use computeIfAbsent |
| `FrequencyMap.java` — `mergeCounts` | `TODO(Day15-task02)` | return a new map with the sum of counts per key; do not mutate a or b |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_countIsCaseInsensitiveAndIgnoresBlanks`, `r1_countEmpty` |
| 2 | `r2_topNOrdersByCountThenAlphabet`, `r2_topNBoundaries` |
| 3 | `r3_invertGroupsAndSorts` |
| 4 | `r4_mergeCountsSumsAndDoesNotMutate` |

## Edge cases to handle

- empty input
- ties in `topN`
- blank and null words
- inputs left unmodified by `mergeCounts`

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 15: Frequency Map Toolkit`

## Hints (optional)

<details><summary>Hint 1</summary>

Sort `Map.Entry` objects with `Map.Entry.comparingByValue()` then `comparingByKey()`.

</details>

<details><summary>Hint 2</summary>

`computeIfAbsent(k, x -> new ArrayList<>()).add(...)` replaces the check-then-put dance.

</details>
