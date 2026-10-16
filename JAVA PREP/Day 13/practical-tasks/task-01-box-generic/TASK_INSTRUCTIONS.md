# Task 1 — Generic Box with map/orElse

**Day:** 13 · **Task ID:** Day13-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Implement an immutable generic container `Box<T>` that either holds a non-null value or is empty, with `map`, `orElse`, and value-based equality. A test also proves that `Box<String>` and `Box<Integer>` share one runtime class (erasure).

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day13/task01/Box.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day13/task01/BoxTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 13 theory file read

## What you will implement

1. `Box.of(value)` returns a box holding the value and throws `NullPointerException` for `null`
2. `Box.empty()` returns an empty box; `isEmpty()` reports the state; `get()` on an empty box throws `NoSuchElementException`
3. `orElse(fallback)` returns the value or the fallback
4. `map(fn)` returns a `Box<R>`; an empty box stays empty and a function returning `null` yields an empty box; the signature must be `Function<? super T, ? extends R>`
5. `equals`/`hashCode` are value-based and `toString` is `Box[value]` or `Box.empty`
6. `Box<String>` and `Box<Integer>` have the same runtime class (observable erasure)

## Constraints

- Do not edit the tests; do not hard-code expected values
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=BoxTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **9 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day13-task01)`).

### Run one test class

```bash
mvn -Dtest=BoxTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `Box.java` — `of` | `TODO(Day13-task01)` | return a box holding value; throw NullPointerException when value is null |
| `Box.java` — `empty` | `TODO(Day13-task01)` | return an empty box (a box that holds no value) |
| `Box.java` — `isEmpty` | `TODO(Day13-task01)` | return true when the box holds no value |
| `Box.java` — `get` | `TODO(Day13-task01)` | return the value; throw NoSuchElementException when the box is empty |
| `Box.java` — `orElse` | `TODO(Day13-task01)` | return the value, or fallback when the box is empty |
| `Box.java` — `map` | `TODO(Day13-task01)` | apply fn to the value and wrap the result; empty stays empty; a null result gives an empty box; never call fn on an empty box |
| `Box.java` — `equals` | `TODO(Day13-task01)` | two boxes are equal when both are empty or hold equal values; use pattern matching or getClass |
| `Box.java` — `hashCode` | `TODO(Day13-task01)` | consistent with equals (Objects.hashCode(value)) |
| `Box.java` — `toString` | `TODO(Day13-task01)` | return "Box[value]" for a full box and "Box.empty" for an empty one |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_of` |
| 2 | `r2_emptyBoxBehavior` |
| 3 | `r3_orElse` |
| 4 | `r4_mapTransformsValue`, `r4_mapAcceptsWiderFunction`, `r4_mapOnEmptyNeverCallsFunction`, `r4_mapReturningNullGivesEmpty` |
| 5 | `r5_equalsHashCodeToString` |
| 6 | `r6_erasure` |

## Edge cases to handle

- `of(null)` -> `NullPointerException`
- mapping an empty box never calls the function
- function returning null -> empty box
- `equals` between empty boxes is true; between empty and non-empty is false

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 13: Generic Box with map/orElse`

## Hints (optional)

<details><summary>Hint 1</summary>

Make the constructor private and keep `value` final; use `null` internally to mean empty.

</details>

<details><summary>Hint 2</summary>

`map` can reuse `empty()`; for `equals` compare `Objects.equals(value, other.value)`.

</details>
