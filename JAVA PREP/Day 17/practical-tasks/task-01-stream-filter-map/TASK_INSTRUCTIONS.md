# Task 1 — Filter, Map, Sort, and Page

**Day:** 17 · **Task ID:** Day17-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Practice the core intermediate operations: filter, map, distinct, sorted, skip/limit, and findFirst - plus one *predict the output* method that reveals how streams process elements lazily, one at a time.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day17/task01/StreamFilterMap.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day17/task01/StreamFilterMapTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 17 theory file read

## What you will implement

1. `upperLongNames(names, minLen)` trims names, drops `null`s and names shorter than `minLen`, and returns them upper-cased in input order
2. `squaresOfOdds(numbers)` returns the squares of the odd numbers (including negative odd numbers)
3. `distinctSortedLower(words)` returns trimmed, lower-cased, non-blank, de-duplicated words sorted alphabetically; `null` entries are ignored
4. `page(items, pageIndex, size)` returns the zero-based page using `skip`/`limit`; `pageIndex < 0` or `size <= 0` throws `IllegalArgumentException`; pages past the end are empty
5. `firstStartingWith(names, prefix)` returns the first name starting with the prefix as an `Optional`
6. `traceLaziness()` runs `filter(len > 1)` then `map(upper)` then `findFirst` over `"a", "bb", "cc"`, recording `filter:<x>` and `map:<x>` events, and returns the trace

## Constraints

- Use the Stream API - no explicit `for`/`while` loops (except none are needed)
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=StreamFilterMapTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day17-task01)`).

### Run one test class

```bash
mvn -Dtest=StreamFilterMapTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `StreamFilterMap.java` — `upperLongNames` | `TODO(Day17-task01)` | stream: drop nulls, trim, keep length >= minLen, upper-case, toList (input order) |
| `StreamFilterMap.java` — `squaresOfOdds` | `TODO(Day17-task01)` | keep odd numbers (negative ones too) and map each to its square |
| `StreamFilterMap.java` — `distinctSortedLower` | `TODO(Day17-task01)` | drop nulls, trim, lower-case, drop blank, distinct, sorted alphabetically |
| `StreamFilterMap.java` — `page` | `TODO(Day17-task01)` | validate (pageIndex >= 0, size > 0 else IllegalArgumentException), then skip(pageIndex * size) and limit(size); use long arithmetic |
| `StreamFilterMap.java` — `firstStartingWith` | `TODO(Day17-task01)` | findFirst among non-null names that start with prefix |
| `StreamFilterMap.java` — `traceLaziness` | `TODO(Day17-task01)` | pipeline over "a","bb","cc": filter(length>1) logging "filter:<s>", map(upper) logging "map:<s>", then findFirst(); return the log (it shows per-element, short-circuited processing) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_upperLongNames` |
| 2 | `r2_squaresOfOdds` |
| 3 | `r3_distinctSortedLower` |
| 4 | `r4_page`, `r4_pageValidatesArguments` |
| 5 | `r5_firstStartingWith` |
| 6 | `r6_traceLaziness` |

## Edge cases to handle

- empty list
- null elements
- page index past the end
- size 0
- negative odd numbers (`-3 % 2 == -1`)

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 17: Filter, Map, Sort, and Page`

## Hints (optional)

<details><summary>Hint 1</summary>

`Stream.skip` takes a `long`: cast before multiplying to avoid `int` overflow.

</details>

<details><summary>Hint 2</summary>

In `traceLaziness`, remember the log is mutated from inside lambdas (acceptable for a demo; never in production pipelines).

</details>
