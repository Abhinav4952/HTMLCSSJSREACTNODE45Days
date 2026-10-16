# Task 1 — Lambda Filter, Map, and Closures

**Day:** 16 · **Task ID:** Day16-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Implement generic higher-order helpers that accept lambdas, then three small closure exercises: applying a unary operator twice, creating independent counters, and generating adders without falling into the loop-variable capture trap.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day16/task01/LambdaFilter.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day16/task01/LambdaFilterTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 16 theory file read

## What you will implement

1. `filter(list, predicate)` returns a new list of elements matching the predicate (accepts `Predicate<? super T>`)
2. `mapAll(list, fn)` returns a new list of transformed elements (accepts `Function<? super T, ? extends R>`)
3. `applyTwice(f, x)` applies an `IntUnaryOperator` two times
4. `counter()` returns a `Supplier<Integer>`; each supplier yields 1, 2, 3, ... independently of other suppliers
5. `adders(n)` returns `n` `IntUnaryOperator`s where the operator at index `i` adds `i` to its argument

## Constraints

- Do not use streams (Day 17)
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=LambdaFilterTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day16-task01)`).

### Run one test class

```bash
mvn -Dtest=LambdaFilterTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `LambdaFilter.java` — `filter` | `TODO(Day16-task01)` | return a new list containing only the elements for which predicate.test is true |
| `LambdaFilter.java` — `mapAll` | `TODO(Day16-task01)` | return a new list with fn applied to every element, preserving order |
| `LambdaFilter.java` — `applyTwice` | `TODO(Day16-task01)` | return f(f(x)) |
| `LambdaFilter.java` — `counter` | `TODO(Day16-task01)` | return a Supplier whose successive calls return 1, 2, 3, ...; every counter() call gets its own state (captured AtomicInteger) |
| `LambdaFilter.java` — `adders` | `TODO(Day16-task01)` | return n operators; operator i adds i to its input; IllegalArgumentException when n is negative (watch effectively-final capture in the loop) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_filter`, `r1_filterAcceptsSupertypePredicate` |
| 2 | `r2_mapAll` |
| 3 | `r3_applyTwice` |
| 4 | `r4_countersAreIndependent` |
| 5 | `r5_addersCaptureTheRightValue`, `r5_addersEdgeCases` |

## Edge cases to handle

- empty list
- predicate matching nothing/everything
- `adders(0)` is empty; negative `n` throws `IllegalArgumentException`
- two counters do not share state

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 16: Lambda Filter, Map, and Closures`

## Hints (optional)

<details><summary>Hint 1</summary>

`counter()` needs mutable state inside a lambda: capture an `AtomicInteger` (a reference that is itself effectively final).

</details>

<details><summary>Hint 2</summary>

Create a fresh `final int` per loop iteration before capturing it.

</details>
