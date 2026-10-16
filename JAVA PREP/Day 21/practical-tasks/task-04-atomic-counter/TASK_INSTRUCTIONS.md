# Task 4 — Atomics, Locks, and Concurrent Maps

**Day:** 21 · **Task ID:** Day21-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Build four small thread-safe components, each using the right tool: a hit counter with `AtomicLong`, a running maximum with a CAS loop, a word counter with `ConcurrentHashMap` + `LongAdder`, and a read-mostly registry guarded by a `ReentrantReadWriteLock`. The tests hammer each from many threads.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day21/task04/AtomicToolkit.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day21/task04/AtomicToolkitTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 21 theory file read

## What you will implement

1. `HitCounter`: `hit()` increments atomically, `count()` returns the total, `reset()` returns the previous count and sets it to 0 atomically (`getAndSet`)
2. `MaxTracker`: `offer(value)` keeps the maximum seen using a **compare-and-set loop**; `get()` returns the maximum (`Integer.MIN_VALUE` before any offer)
3. `WordCounter`: `add(word)` increments atomically using `ConcurrentHashMap.computeIfAbsent` + `LongAdder`; `count(word)` returns 0 for unknown words; `snapshot()` returns an independent `Map<String, Long>`
4. `Registry`: `put`, `get`, `size` are protected by a `ReentrantReadWriteLock` (readers share the read lock; writers use the write lock); always unlock in `finally`
5. All components give exact results under 8 threads x 20_000 operations

## Constraints

- `HitCounter`, `MaxTracker` and `WordCounter` must be lock-free (atomics/concurrent collections only)
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=AtomicToolkitTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day21-task04)`).

### Run one test class

```bash
mvn -Dtest=AtomicToolkitTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `AtomicToolkit.java` — `hit` | `TODO(Day21-task04)` | atomically increment the counter (incrementAndGet / getAndIncrement) |
| `AtomicToolkit.java` — `count` | `TODO(Day21-task04)` | return the current number of hits |
| `AtomicToolkit.java` — `reset` | `TODO(Day21-task04)` | atomically set the counter to 0 and return the previous value (getAndSet) |
| `AtomicToolkit.java` — `offer` | `TODO(Day21-task04)` | CAS loop: read current, return if value <= current, else compareAndSet(current, value) and retry on failure |
| `AtomicToolkit.java` — `get` | `TODO(Day21-task04)` | return the maximum seen so far (Integer.MIN_VALUE when nothing was offered) |
| `AtomicToolkit.java` — `add` | `TODO(Day21-task04)` | counts.computeIfAbsent(word, k -> new LongAdder()).increment() - no containsKey/put race |
| `AtomicToolkit.java` — `count` | `TODO(Day21-task04)` | the adder's sum for the word, or 0 when the word is unknown |
| `AtomicToolkit.java` — `snapshot` | `TODO(Day21-task04)` | return a NEW HashMap word -> sum() (a point-in-time copy, not a view) |
| `AtomicToolkit.java` — `put` | `TODO(Day21-task04)` | take the WRITE lock, put into the map, release in finally |
| `AtomicToolkit.java` — `get` | `TODO(Day21-task04)` | take the READ lock, read, release in finally |
| `AtomicToolkit.java` — `size` | `TODO(Day21-task04)` | take the READ lock, return map.size(), release in finally |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_hitCounterIsExactAndResetReturnsPrevious` |
| 2 | `r2_maxTrackerStartsAtMinValue`, `r2_maxTrackerUnderContention` |
| 3 | `r3_wordCounterBasics`, `r3_wordCounterUnderContention` |
| 4 | `r4_registryBasics` |
| 5 | `r5_registryWithConcurrentReadersAndWriters` |

## Edge cases to handle

- no updates yet
- unknown words
- concurrent offers with decreasing values
- readers and writers at the same time

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 21: Atomics, Locks, and Concurrent Maps`

## Hints (optional)

<details><summary>Hint 1</summary>

Use `AtomicInteger.compareAndSet(expected, update)` inside a `do/while`; if it fails, another thread won - re-read and retry.

</details>

<details><summary>Hint 2</summary>

`LongAdder.sum()` is a snapshot: that is exactly what `snapshot()` should expose.

</details>
