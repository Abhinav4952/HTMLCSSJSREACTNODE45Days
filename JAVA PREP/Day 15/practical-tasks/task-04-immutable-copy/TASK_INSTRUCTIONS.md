# Task 4 — Immutable Roster with Defensive Copies

**Day:** 15 · **Task ID:** Day15-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Create an immutable `Roster` value object that defensively copies its inputs, exposes only immutable collections, and offers a wither that returns a new instance. Add helper methods demonstrating the difference between an unmodifiable **view** and an immutable **copy**. **Challenge:** explain in a comment why `Collections.unmodifiableList(internal)` would be a bug here.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day15/task04/Roster.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day15/task04/RosterTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 15 theory file read

## What you will implement

1. `new Roster(names, scores)` stores immutable copies (`List.copyOf`, `Map.copyOf`); null arguments or null elements throw `NullPointerException`
2. Changes to the caller's original collections after construction do not affect the roster
3. `names()` and `scores()` return collections that throw `UnsupportedOperationException` on mutation
4. `withName(String)` returns a **new** roster that has one more name (appended) and the same scores; the original is unchanged
5. `safeCopy(Collection<? extends T>)` returns an immutable `List<T>` snapshot
6. `viewReflectsChanges(base)` returns `true` (an unmodifiable view shows later changes to its base) and `copyIgnoresChanges(base)` returns `true` (an immutable copy does not); both must actually perform the experiment on a **copy** of `base` and not mutate `base`

## Constraints

- Do not edit the tests; do not hard-code expected values
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=RosterTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **6 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day15-task04)`).

### Run one test class

```bash
mvn -Dtest=RosterTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `Roster.java` — `constructor` | `TODO(Day15-task04)` | store List.copyOf(names) and Map.copyOf(scores) (null arguments or elements -> NullPointerException) |
| `Roster.java` — `withName` | `TODO(Day15-task04)` | return a NEW Roster whose names are this.names plus name appended; scores unchanged; this stays unchanged |
| `Roster.java` — `safeCopy` | `TODO(Day15-task04)` | return an immutable snapshot list of source (List.copyOf) |
| `Roster.java` — `viewReflectsChanges` | `TODO(Day15-task04)` | on a mutable COPY of base: wrap it in Collections.unmodifiableList, add an element to the copy, return whether the view's size grew (true); never mutate base |
| `Roster.java` — `copyIgnoresChanges` | `TODO(Day15-task04)` | on a mutable COPY of base: take List.copyOf, add an element to the copy, return whether the snapshot's size stayed the same (true); never mutate base |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_constructorCopiesAndRejectsNulls` |
| 2 | `r2_callerChangesDoNotLeakIn` |
| 3 | `r3_exposedCollectionsAreImmutable` |
| 4 | `r4_withNameReturnsNewInstance` |
| 5 | `r5_safeCopyIsAnImmutableSnapshot` |
| 6 | `r6_viewVersusCopyExperiments` |

## Edge cases to handle

- null list, null element, null map
- mutating the original after construction
- wither leaves original untouched
- `Map.copyOf` iteration order is unspecified - do not depend on it

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 15: Immutable Roster with Defensive Copies`

## Hints (optional)

<details><summary>Hint 1</summary>

`List.copyOf` and `Map.copyOf` already throw `NullPointerException` for nulls - no manual checks needed.

</details>

<details><summary>Hint 2</summary>

The wither can build a mutable `ArrayList`, append, and pass it to the constructor (which copies again).

</details>
