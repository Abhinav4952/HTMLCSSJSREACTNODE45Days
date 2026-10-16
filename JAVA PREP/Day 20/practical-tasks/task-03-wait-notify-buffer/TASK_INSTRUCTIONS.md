# Task 3 — Producer/Consumer Bounded Buffer

**Day:** 20 · **Task ID:** Day20-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Implement a classic bounded blocking buffer with `synchronized`, `wait()` and `notifyAll()`: `put` blocks while full, `take` blocks while empty, FIFO order is preserved, and interruption is propagated. The tests check blocking behavior by observing `Thread.State.WAITING` - no sleeps.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day20/task03/BoundedBuffer.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day20/task03/BoundedBufferTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 20 theory file read

## What you will implement

1. `BoundedBuffer(capacity)` rejects capacity <= 0 with `IllegalArgumentException`
2. `put(item)` rejects `null` with `NullPointerException`; blocks (WAITING) while the buffer is full
3. `take()` blocks (WAITING) while the buffer is empty and returns items in FIFO order
4. `size()` returns the current number of items; `capacity()` the configured limit
5. Both blocking methods wait in a **loop** and use `notifyAll()` after changing state; `InterruptedException` is propagated
6. A producer and a consumer thread can transfer 10_000 items through a capacity-3 buffer in order without loss

## Constraints

- Use `synchronized`/`wait`/`notifyAll` - no `BlockingQueue`, `Lock`, or `Condition`
- No `Thread.sleep`
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=BoundedBufferTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day20-task03)`).

### Run one test class

```bash
mvn -Dtest=BoundedBufferTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `BoundedBuffer.java` — `constructor` | `TODO(Day20-task03)` | IllegalArgumentException when capacity <= 0; allocate the circular array |
| `BoundedBuffer.java` — `put` | `TODO(Day20-task03)` | NullPointerException for null; while the buffer is full wait(); then store at tail (circular), count++ and notifyAll() |
| `BoundedBuffer.java` — `take` | `TODO(Day20-task03)` | while the buffer is empty wait(); then remove from head (circular, clear the slot), count-- and notifyAll() |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_constructorValidation` |
| 2 | `r2_fifoSingleThread`, `r2_nullRejected` |
| 3 | `r3_takeBlocksUntilAnItemArrives` |
| 4 | `r4_putBlocksWhileFull` |
| 5 | `r5_interruptWhileWaitingPropagates` |
| 6 | `r6_producerConsumerTransfersEverythingInOrder` |

## Edge cases to handle

- capacity 1
- interrupt while waiting
- null items
- wake-ups after state changes (loop, not `if`)

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 20: Producer/Consumer Bounded Buffer`

## Hints (optional)

<details><summary>Hint 1</summary>

Keep the condition in shared state (`count`) and re-test it in the `while` loop after every wake-up.

</details>

<details><summary>Hint 2</summary>

`notifyAll()` wakes both producers and consumers; each rechecks its own condition.

</details>
