# Task 3 — Queues, Deques, and Priority Queues

**Day:** 15 · **Task ID:** Day15-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Use a `PriorityQueue` with a custom comparator to schedule jobs, a bounded max-heap to find the K smallest numbers, an `ArrayDeque` as a stack to validate brackets, and a deque to rotate a list.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day15/task03/Job.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day15/task03/PriorityQueueLab.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day15/task03/PriorityQueueLabTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 15 theory file read

## What you will implement

1. `processOrder(List<Job>)` returns job ids in execution order: higher `priority` first, ties broken by id ascending (use a `PriorityQueue`)
2. `kSmallest(List<Integer>, k)` returns the `k` smallest values ascending using a bounded max-heap; `k <= 0` -> empty; `k >= size` -> all values sorted
3. `isBalanced(String)` checks `()`, `[]`, `{}` nesting using an `ArrayDeque` stack; characters other than brackets are ignored
4. `rotateLeft(List<T>, k)` rotates left by `k` (mod size, negative allowed) using an `ArrayDeque`, returning a new list

## Constraints

- Do not use `java.util.Stack`
- Do not sort the whole input list in `kSmallest` (use the bounded heap)
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=PriorityQueueLabTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day15-task03)`).

### Run one test class

```bash
mvn -Dtest=PriorityQueueLabTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `PriorityQueueLab.java` — `processOrder` | `TODO(Day15-task03)` | offer all jobs into a PriorityQueue (priority desc, then id asc) and poll them into a list of ids |
| `PriorityQueueLab.java` — `kSmallest` | `TODO(Day15-task03)` | keep a max-heap of at most k items (evict the largest), then return them in ascending order; k <= 0 gives an empty list |
| `PriorityQueueLab.java` — `isBalanced` | `TODO(Day15-task03)` | use an ArrayDeque as a stack: push openers, pop and match on closers; ignore other characters; true only if the stack ends empty |
| `PriorityQueueLab.java` — `rotateLeft` | `TODO(Day15-task03)` | load items into an ArrayDeque, move the head to the tail (k mod size) times, return a new list; empty list gives empty list |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_processOrderByPriorityThenId`, `r1_processOrderEmptyAndSingle` |
| 2 | `r2_kSmallest`, `r2_kSmallestBoundaries` |
| 3 | `r3_balancedBrackets`, `r3_unbalancedBrackets` |
| 4 | `r4_rotateLeft` |

## Edge cases to handle

- empty input
- duplicate priorities
- k of 0 / negative / larger than the list
- unbalanced closers (`"]"`), interleaved types (`"(]"`), leftover openers
- negative rotation

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 15: Queues, Deques, and Priority Queues`

## Hints (optional)

<details><summary>Hint 1</summary>

Remember `Comparator.comparingInt(Job::priority).reversed().thenComparing(Job::id)`.

</details>

<details><summary>Hint 2</summary>

For top-K *smallest* you need a **max**-heap so the largest candidate is evicted first.

</details>
