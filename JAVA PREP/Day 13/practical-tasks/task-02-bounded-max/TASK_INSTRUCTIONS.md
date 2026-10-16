# Task 2 — Bounded Max/Min/Clamp

**Day:** 13 · **Task ID:** Day13-task02 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Write generic numeric and ordering helpers using bounded type parameters: `max`, `min` over lists of comparables (including subclasses of a comparable parent), `clamp` for number-and-comparable types, and a `sum` over any `Collection<? extends Number>`.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day13/task02/BoundedMath.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day13/task02/BoundedMathTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 13 theory file read

## What you will implement

1. `max(List)` returns the greatest element by natural order; empty or null list throws `IllegalArgumentException`
2. `min(List)` returns the smallest element; same validation
3. `max`/`min` signatures use `T extends Comparable<? super T>` so `List<Dog>` works when `Dog extends Animal implements Comparable<Animal>`
4. `clamp(value, lo, hi)` constrains a value into `[lo, hi]` for `T extends Number & Comparable<T>`; `lo > hi` throws `IllegalArgumentException`
5. `sum(Collection<? extends Number>)` adds `doubleValue()`s and treats an empty collection as `0.0`

## Constraints

- Do not edit the tests; do not hard-code expected values
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=BoundedMathTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day13-task02)`).

### Run one test class

```bash
mvn -Dtest=BoundedMathTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `BoundedMath.java` — `max` | `TODO(Day13-task02)` | return the greatest element (compareTo); IllegalArgumentException when items is null or empty |
| `BoundedMath.java` — `min` | `TODO(Day13-task02)` | return the smallest element (compareTo); IllegalArgumentException when items is null or empty |
| `BoundedMath.java` — `clamp` | `TODO(Day13-task02)` | return lo if value < lo, hi if value > hi, else value; IllegalArgumentException when lo > hi |
| `BoundedMath.java` — `sum` | `TODO(Day13-task02)` | add doubleValue() of every element; empty collection gives 0.0 |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_maxOfStringsAndIntegers`, `r1_maxRejectsNullAndEmpty` |
| 2 | `r2_minOfStringsAndDoubles` |
| 3 | `r3_worksForSubclassOfComparableParent` |
| 4 | `r4_clamp`, `r4_clampRejectsInvertedRange` |
| 5 | `r5_sumAcceptsAnyNumberCollection` |

## Edge cases to handle

- empty list, null list
- single-element list
- lo == hi in clamp
- a `List<Integer>` and a `List<Double>` both accepted by `sum`

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 13: Bounded Max/Min/Clamp`

## Hints (optional)

<details><summary>Hint 1</summary>

Seed `best` with the first element, then scan with `compareTo`.

</details>

<details><summary>Hint 2</summary>

For `clamp`, validate the range first so `lo > hi` fails even when `value` is in range.

</details>
