# Task 4 — Challenge: Word Count Analyzer

**Day:** 17 · **Task ID:** Day17-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Build a small text analytics service entirely with streams and collectors: word frequencies (with stop words), the top-N words, a length histogram, and words that occur exactly once. Words are maximal runs of letters or digits, compared case-insensitively. **Challenge:** deliver deterministic ordering from `groupingBy`'s unordered maps.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day17/task04/WordCount.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day17/task04/WordCountTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 17 theory file read

## What you will implement

1. `countWords(text, stopWords)` returns word -> count; words are lower-cased runs of letters/digits; stop words are excluded; `null`/blank text gives an empty map
2. `topN(text, n, stopWords)` returns `"word=count"` strings, most frequent first, ties broken alphabetically; `n <= 0` gives an empty list
3. `lengthHistogram(text)` returns a `SortedMap<Integer, Long>` word length -> number of word occurrences
4. `hapax(text)` returns a `SortedSet<String>` of words that appear exactly once

## Constraints

- No explicit loops in the public methods
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=WordCountTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **6 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day17-task04)`).

### Run one test class

```bash
mvn -Dtest=WordCountTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `WordCount.java` — `countWords` | `TODO(Day17-task04)` | words(text) minus stop words, grouped by identity with Collectors.counting() |
| `WordCount.java` — `topN` | `TODO(Day17-task04)` | sort the entries by count desc then word asc, limit n (n <= 0 -> empty), map to "word=count" |
| `WordCount.java` — `lengthHistogram` | `TODO(Day17-task04)` | group word occurrences by length into a TreeMap with counting() |
| `WordCount.java` — `hapax` | `TODO(Day17-task04)` | words with count exactly 1, collected into a TreeSet |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_countWordsSplitsOnNonLettersAndLowercases`, `r1_stopWordsAndEmptyText` |
| 2 | `r2_topNOrdersByCountThenWord`, `r2_topNBoundaries` |
| 3 | `r3_lengthHistogramIsSortedAndCountsOccurrences` |
| 4 | `r4_hapax` |

## Edge cases to handle

- punctuation, apostrophes and newlines split words
- mixed case
- digits are word characters
- stop words are matched case-insensitively (provided lower-case)
- null/blank text

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 17: Challenge: Word Count Analyzer`

## Hints (optional)

<details><summary>Hint 1</summary>

Ties in `topN` are why a `HashMap` alone is not enough: sort the entries by two keys.

</details>

<details><summary>Hint 2</summary>

A `TreeMap::new` map factory in `groupingBy` gives sorted keys for free.

</details>
