# Task 4 — Lock-Order Deadlock Detector

**Day:** 20 · **Task ID:** Day20-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Analyze lock acquisition orders statically: each thread is described by the ordered list of lock names it acquires. Detect pairs of locks acquired in **opposite orders** by different threads (a classic deadlock risk), produce a human-readable recommendation, and document the four Coffman conditions in code.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day20/task04/LockOrderAnalyzer.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day20/task04/LockOrderAnalyzerTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 20 theory file read

## What you will implement

1. `conflictingPairs(orders)` returns a sorted set of strings `"A<->B"` (names in alphabetical order inside each pair) for every two locks that one thread takes as X-then-Y and another as Y-then-X; a lock repeated within one thread (reentrancy) counts at its first position
2. `hasOrderingRisk(orders)` is true exactly when `conflictingPairs` is non-empty
3. `coffmanConditions()` returns, in this order: `Mutual exclusion`, `Hold and wait`, `No preemption`, `Circular wait`
4. `advice(orders)` returns `"No lock-ordering conflicts found."` when safe; otherwise a text that lists every conflicting pair and recommends one global order (all lock names, alphabetical, comma-separated) using the phrase `global order`

## Constraints

- No actual threads or locks are needed - this is an analysis task
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=LockOrderAnalyzerTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **9 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day20-task04)`).

### Run one test class

```bash
mvn -Dtest=LockOrderAnalyzerTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `LockOrderAnalyzer.java` — `conflictingPairs` | `TODO(Day20-task04)` | collect every (x before y) relation per thread (first occurrence only); report "A<->B" (A < B alphabetically) when both (x,y) and (y,x) occur in different threads |
| `LockOrderAnalyzer.java` — `hasOrderingRisk` | `TODO(Day20-task04)` | true when conflictingPairs is not empty |
| `LockOrderAnalyzer.java` — `coffmanConditions` | `TODO(Day20-task04)` | return exactly: "Mutual exclusion", "Hold and wait", "No preemption", "Circular wait" (in this order) |
| `LockOrderAnalyzer.java` — `advice` | `TODO(Day20-task04)` | "No lock-ordering conflicts found." when safe; otherwise mention each pair and recommend a "global order" listing all lock names alphabetically |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_oppositeOrdersAreConflicting`, `r1_sameOrderIsSafe`, `r1_singleThreadIsNeverAConflict`, `r1_nonAdjacentAndMultiplePairs`, `r1_reentrantDuplicatesUseFirstPosition` |
| 2 | `r2_hasOrderingRisk` |
| 3 | `r3_coffmanConditions` |
| 4 | `r4_adviceWhenSafe`, `r4_adviceWhenRisky` |

## Edge cases to handle

- single thread (never a risk)
- same order in all threads (safe)
- reentrant duplicates (`A, A, B`)
- non-adjacent acquisition (`A, C, B` vs `B, A`)
- empty input

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 20: Lock-Order Deadlock Detector`

## Hints (optional)

<details><summary>Hint 1</summary>

Think of each thread as producing "X before Y" facts; a conflict is a fact and its mirror image from some thread.

</details>

<details><summary>Hint 2</summary>

Use `List.of(x, y)` as a hash key for a pair - lists have value-based `equals`/`hashCode`.

</details>
