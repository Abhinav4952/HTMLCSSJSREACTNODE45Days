# Task 1 — List Operations Toolkit

**Day:** 14 · **Task ID:** Day14-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Implement four everyday list utilities: order-preserving de-duplication, rotation, chunking, and removal of the first occurrence of a value (not an index). Each returns a **new** list and never mutates the argument. The tests deliberately use both `ArrayList` and `LinkedList` inputs and include the `remove(int)` vs `remove(Object)` trap.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day14/task01/ListOps.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day14/task01/ListOpsTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 14 theory file read

## What you will implement

1. `dedupe(list)` returns a new list without duplicates, keeping the first occurrence order; `null` input throws `NullPointerException`
2. `rotate(list, k)` returns a new list rotated right by `k` (negative `k` rotates left, `|k|` larger than size wraps, empty list returns empty)
3. `chunk(list, size)` splits into consecutive sub-lists of `size` (last may be shorter); chunks are independent copies; `size <= 0` throws `IllegalArgumentException`
4. `removeFirstOccurrence(list, value)` returns a copy with the first element **equal to** `value` removed (value semantics, not index), or an unchanged copy when absent; the argument is never mutated

## Constraints

- Do not edit the tests; do not hard-code expected values
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=ListOpsTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **8 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day14-task01)`).

### Run one test class

```bash
mvn -Dtest=ListOpsTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `ListOps.java` — `dedupe` | `TODO(Day14-task01)` | return a new list with duplicates removed, first occurrences kept in order; NullPointerException for null input |
| `ListOps.java` — `rotate` | `TODO(Day14-task01)` | return a new list rotated right by k; negative k rotates left; |k| may exceed size; empty list gives empty list |
| `ListOps.java` — `chunk` | `TODO(Day14-task01)` | split into consecutive copies of at most size elements; IllegalArgumentException when size <= 0 |
| `ListOps.java` — `removeFirstOccurrence` | `TODO(Day14-task01)` | return a copy without the first element equal to value (NOT index value); unchanged copy if absent; do not mutate input |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_dedupeKeepsFirstOccurrenceOrder`, `r1_dedupeReturnsNewMutableListAndRejectsNull` |
| 2 | `r2_rotateRight`, `r2_rotateLeftAndEmpty` |
| 3 | `r3_chunk`, `r3_chunksAreIndependentCopiesAndSizeIsValidated` |
| 4 | `r4_removeFirstOccurrenceByValue`, `r4_removeOnlyFirstAndMissingValue` |

## Edge cases to handle

- empty lists
- rotation by multiples of the size
- negative rotation
- chunk size larger than list
- list containing duplicate and `null`-free values

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 14: List Operations Toolkit`

## Hints (optional)

<details><summary>Hint 1</summary>

`new ArrayList<>(new LinkedHashSet<>(input))` is a compact dedupe.

</details>

<details><summary>Hint 2</summary>

For `rotate`, compute `shift = ((k % n) + n) % n` so negatives behave.

</details>

<details><summary>Hint 3</summary>

`list.remove(Integer.valueOf(v))` removes by value.

</details>
