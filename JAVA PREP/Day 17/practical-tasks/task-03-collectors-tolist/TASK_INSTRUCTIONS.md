# Task 3 — Collectors Workout

**Day:** 17 · **Task ID:** Day17-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Collect streams into lists, sets, maps and strings with the right collector: handle duplicate keys in `toMap`, preserve insertion order, build bracketed CSV strings, and return an unmodifiable sorted list with `collectingAndThen`.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day17/task03/CollectorsWorkout.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day17/task03/CollectorsWorkoutTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 17 theory file read

## What you will implement

1. `upperNames(names)` collects the upper-cased names into a `List` in input order
2. `uniqueLengths(words)` collects the distinct word lengths into a `Set<Integer>`
3. `lengthByWord(words)` returns a `Map<String,Integer>` word -> length that keeps the **first** value on duplicate words and preserves first-seen order (`LinkedHashMap`)
4. `csv(items)` joins with `", "` and wraps in `[` `]`; an empty list gives `[]`
5. `immutableSorted(items)` returns a naturally sorted list that rejects modification with `UnsupportedOperationException` (use `collectingAndThen`)
6. `toIdsByType(entries)` groups `type:id` strings like `"a:1"` into a `TreeMap<String, List<String>>` of ids per type (sorted by type, ids in input order) using `Collectors.groupingBy` with a `mapping` downstream

## Constraints

- Do not build results with loops or `forEach` into outer collections
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=CollectorsWorkoutTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **6 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day17-task03)`).

### Run one test class

```bash
mvn -Dtest=CollectorsWorkoutTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `CollectorsWorkout.java` — `upperNames` | `TODO(Day17-task03)` | map to upper case and collect with Collectors.toList() |
| `CollectorsWorkout.java` — `uniqueLengths` | `TODO(Day17-task03)` | map to length and collect with Collectors.toSet() |
| `CollectorsWorkout.java` — `lengthByWord` | `TODO(Day17-task03)` | Collectors.toMap with a merge function keeping the first value and LinkedHashMap::new as the map supplier |
| `CollectorsWorkout.java` — `csv` | `TODO(Day17-task03)` | Collectors.joining(", ", "[", "]") - an empty list yields "[]" |
| `CollectorsWorkout.java` — `immutableSorted` | `TODO(Day17-task03)` | sorted() then collectingAndThen(toList(), Collections::unmodifiableList) |
| `CollectorsWorkout.java` — `toIdsByType` | `TODO(Day17-task03)` | entries look like "type:id"; groupingBy(type, TreeMap::new, mapping(id, toList())) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_upperNames` |
| 2 | `r2_uniqueLengths` |
| 3 | `r3_lengthByWordKeepsFirstAndOrder` |
| 4 | `r4_csv` |
| 5 | `r5_immutableSorted` |
| 6 | `r6_toIdsByType` |

## Edge cases to handle

- duplicate words in `toMap`
- empty input
- ids appear in encounter order within each type

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 17: Collectors Workout`

## Hints (optional)

<details><summary>Hint 1</summary>

`toMap`'s 4-argument overload is `(keyFn, valueFn, mergeFn, mapSupplier)`.

</details>

<details><summary>Hint 2</summary>

`groupingBy(classifier, mapFactory, downstream)` is covered in depth on Day 18; use it here as shown in the TODO.

</details>
