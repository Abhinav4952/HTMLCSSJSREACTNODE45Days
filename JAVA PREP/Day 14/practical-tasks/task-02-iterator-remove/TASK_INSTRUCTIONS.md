# Task 2 — Iterator Removal Lab

**Day:** 14 · **Task ID:** Day14-task02 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Practice safe in-place mutation with `Iterator` and `ListIterator`, and prove you understand the fail-fast quirk by writing a method that reports whether a for-each removal throws `ConcurrentModificationException` (including the silent second-to-last case).

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day14/task02/IteratorOps.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day14/task02/IteratorOpsTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 14 theory file read

## What you will implement

1. `removeNegatives(List<Integer>)` removes negative values **in place** using `Iterator.remove()` and returns how many were removed
2. `removeMatching(Collection<T>, Predicate<? super T>)` removes matching elements in place and returns the count (use an iterator, not `removeIf`)
3. `duplicateEvens(List<Integer>)` inserts a copy right after each even number using `ListIterator.add`
4. `forEachRemovalThrows(input, toRemove)` copies the list, removes `toRemove` inside a for-each loop, and returns `true` if `ConcurrentModificationException` was thrown, else `false`

## Constraints

- Do not call `Collection.removeIf` or `List.remove(...)` inside loops (except in `forEachRemovalThrows`, which intentionally does)
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=IteratorOpsTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day14-task02)`).

### Run one test class

```bash
mvn -Dtest=IteratorOpsTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `IteratorOps.java` — `removeNegatives` | `TODO(Day14-task02)` | remove every negative value in place via Iterator.remove() and return the number removed |
| `IteratorOps.java` — `removeMatching` | `TODO(Day14-task02)` | remove every element matching predicate in place using an explicit Iterator (not removeIf); return the count |
| `IteratorOps.java` — `duplicateEvens` | `TODO(Day14-task02)` | using a ListIterator, insert a copy immediately after every even value (e.g. [1,2,3,4] -> [1,2,2,3,4,4]) |
| `IteratorOps.java` — `forEachRemovalThrows` | `TODO(Day14-task02)` | copy input into an ArrayList, remove toRemove inside a for-each, return true if ConcurrentModificationException was thrown else false |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_removeNegativesInPlace`, `r1_removeNegativesEdgeCases` |
| 2 | `r2_removeMatchingWorksOnAnyCollection` |
| 3 | `r3_duplicateEvens` |
| 4 | `r4_removeFirstThrows`, `r4_secondToLastDoesNotThrow`, `r4_doesNotMutateTheInput` |

## Edge cases to handle

- empty collection
- all elements match / none match
- `LinkedList` and `ArrayList` both supported
- removing the second-to-last element does not throw
- value not present

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 14: Iterator Removal Lab`

## Hints (optional)

<details><summary>Hint 1</summary>

Always call `it.next()` before `it.remove()`.

</details>

<details><summary>Hint 2</summary>

`ListIterator.add` inserts before the implicit cursor, so after `next()` it lands right after the element you just read and the cursor skips it automatically.

</details>
