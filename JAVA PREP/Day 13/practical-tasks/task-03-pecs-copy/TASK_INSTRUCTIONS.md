# Task 3 — PECS Copy Utilities

**Day:** 13 · **Task ID:** Day13-task03 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Implement collection utilities whose signatures apply PECS correctly, so they accept subtype sources and supertype destinations. Includes a wildcard-capture helper.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day13/task03/Pecs.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day13/task03/PecsTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 13 theory file read

## What you will implement

1. `copy(dst, src)` appends every element of `src` (`List<? extends T>`) to `dst` (`List<? super T>`)
2. `moveAll(src, dst)` moves all elements from `Collection<? extends T>` into `Collection<? super T>` and leaves `src` empty
3. `fill(dst, value, n)` adds `n` copies of `value` to a `List<? super T>`; negative `n` throws `IllegalArgumentException`
4. `firstOrDefault(src, def)` returns the first element of a `List<? extends T>` or `def` when empty
5. `swap(List<?> list, int i, int j)` swaps two elements using a private capture helper

## Constraints

- Do not edit the tests; do not hard-code expected values
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=PecsTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **9 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day13-task03)`).

### Run one test class

```bash
mvn -Dtest=PecsTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `Pecs.java` — `copy` | `TODO(Day13-task03)` | append every element of src to dst; src is a producer (extends), dst a consumer (super) |
| `Pecs.java` — `moveAll` | `TODO(Day13-task03)` | add every element of src to dst, then clear src |
| `Pecs.java` — `fill` | `TODO(Day13-task03)` | add n copies of value to dst; IllegalArgumentException when n is negative |
| `Pecs.java` — `firstOrDefault` | `TODO(Day13-task03)` | return src.get(0), or def when src is empty |
| `Pecs.java` — `swap` | `TODO(Day13-task03)` | delegate to the private generic helper swapHelper(list, i, j) (wildcard capture) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_copyIntegersIntoNumberList`, `r1_copyIntoObjectListAndEmptySource` |
| 2 | `r2_moveAllEmptiesSource`, `r2_moveAllIntoSet` |
| 3 | `r3_fill`, `r3_fillRejectsNegative` |
| 4 | `r4_firstOrDefault` |
| 5 | `r5_swapWorksOnAnyListType`, `r5_swapOutOfRange` |

## Edge cases to handle

- empty source
- negative count in fill
- swap with equal indexes is a no-op
- out-of-range swap index raises `IndexOutOfBoundsException` (from the list)

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 13: PECS Copy Utilities`

## Hints (optional)

<details><summary>Hint 1</summary>

`swap(List<?>, ...)` itself cannot call `list.set(i, list.get(j))` - delegate to a generic helper so the compiler can name the captured type.

</details>

<details><summary>Hint 2</summary>

`moveAll`'s `src.clear()` is legal even though `src` is `? extends T` because `clear` does not take a `T`.

</details>
