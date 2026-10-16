# Task 4 — Generic Array-Backed Stack

**Day:** 13 · **Task ID:** Day13-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Build `ArrayStack<E>`, a growable LIFO stack on an internal `Object[]`. It must be safe for callers (generics, PECS bulk operations), iterable top-to-bottom, and it contains the one legitimate unchecked cast in the course (reading from `Object[]`). **Challenge:** explain in a comment why the cast is safe.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day13/task04/ArrayStack.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day13/task04/ArrayStackTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 13 theory file read

## What you will implement

1. Constructor `ArrayStack(int initialCapacity)` rejects capacity <= 0 with `IllegalArgumentException`; `ArrayStack()` uses 4
2. `push`, `pop`, `peek`, `size`, `isEmpty` follow LIFO semantics; `pop`/`peek` on an empty stack throw `NoSuchElementException`
3. The backing array grows (doubling) when full, and popped slots are nulled to avoid memory leaks
4. `pushAll(Iterable<? extends E>)` pushes in iteration order
5. `popAll(Collection<? super E>)` pops everything into the sink in pop order and returns the count
6. `iterator()` walks from top to bottom without modifying the stack; calling `next()` past the end throws `NoSuchElementException`

## Constraints

- Do not use `java.util.ArrayList`, `Stack`, `Deque` or any collection as the backing store - use `Object[]`
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=ArrayStackTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **8 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day13-task04)`).

### Run one test class

```bash
mvn -Dtest=ArrayStackTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `ArrayStack.java` — `constructor` | `TODO(Day13-task04)` | reject initialCapacity <= 0 with IllegalArgumentException, else allocate the backing array |
| `ArrayStack.java` — `push` | `TODO(Day13-task04)` | grow the array (double) when full, then store item on top |
| `ArrayStack.java` — `pop` | `TODO(Day13-task04)` | remove and return the top element, null out the slot; NoSuchElementException when empty |
| `ArrayStack.java` — `peek` | `TODO(Day13-task04)` | return the top element without removing it; NoSuchElementException when empty |
| `ArrayStack.java` — `pushAll` | `TODO(Day13-task04)` | push every element of source in iteration order (source is a producer) |
| `ArrayStack.java` — `popAll` | `TODO(Day13-task04)` | pop every element into sink (consumer) in pop order and return how many were moved |
| `ArrayStack.java` — `iterator` | `TODO(Day13-task04)` | return an Iterator that walks top to bottom; next() past the end throws NoSuchElementException; remove() is unsupported |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_constructorValidation` |
| 2 | `r2_lifoOrder`, `r2_emptyStackThrows` |
| 3 | `r3_growsBeyondInitialCapacity` |
| 4 | `r4_pushAllAcceptsSubtypeSource` |
| 5 | `r5_popAllIntoSupertypeSink` |
| 6 | `r6_iteratorWalksTopToBottomWithoutMutating`, `r6_iteratorEdgeCases` |

## Edge cases to handle

- capacity 0 or negative
- growth well beyond initial capacity
- pop on empty
- iterating an empty stack
- pushAll of a `List<Integer>` into `ArrayStack<Number>`

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 13: Generic Array-Backed Stack`

## Hints (optional)

<details><summary>Hint 1</summary>

Nulling `elements[size]` after `pop` prevents *loitering* references (a memory leak).

</details>

<details><summary>Hint 2</summary>

In the iterator, capture `size` at creation or read it live - either passes the tests; explain your choice in a comment.

</details>
