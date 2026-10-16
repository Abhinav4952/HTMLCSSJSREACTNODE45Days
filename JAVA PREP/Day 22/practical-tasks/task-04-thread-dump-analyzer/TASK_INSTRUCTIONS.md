# Task 4 — Thread Dump Analyzer and Live Deadlock Detector

**Day:** 22 · **Task ID:** Day22-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Be the on-call engineer: parse a `jstack`-style thread dump into structured data, count thread states, locate the hottest `RUNNABLE` frame, find a lock-ordering deadlock from the `waiting to lock` / `locked` lines, and also detect a **real** deadlock inside the running JVM with `ThreadMXBean`.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day22/task04/ThreadDumpAnalyzer.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day22/task04/ThreadDumpAnalyzerTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 22 theory file read

## What you will implement

1. `parse(dump)` returns one `ThreadInfo(name, state, frames, waitingForLock, heldLocks)` per quoted thread header; state comes from `java.lang.Thread.State: X`; frames are the `at ...` lines (trimmed, without `at `); `- waiting to lock <id>` sets `waitingForLock`; each `- locked <id>` is added to `heldLocks` in order
2. `countByState(threads)` returns a sorted map state -> count
3. `hotspot(threads)` returns the most common **top frame** among `RUNNABLE` threads (ties: alphabetically first), or empty when no runnable thread has frames
4. `findDeadlock(threads)` returns the sorted set of thread names that take part in a wait-for cycle (A waits for a lock held by B ... back to A); empty when there is none
5. `liveDeadlockedThreads()` uses `ThreadMXBean.findDeadlockedThreads()` and returns the sorted names of deadlocked threads (empty list when none)

## Constraints

- Use `java.util.regex` and `java.lang.management` only
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=ThreadDumpAnalyzerTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **10 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day22-task04)`).

### Run one test class

```bash
mvn -Dtest=ThreadDumpAnalyzerTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `ThreadDumpAnalyzer.java` — `parse` | `TODO(Day22-task04)` | iterate lines; a HEADER match starts a new thread (flush the previous one); STATE/FRAME/WAITING/LOCKED lines fill the current thread; lines before the first header are ignored; state defaults to UNKNOWN; null/blank dump -> empty list |
| `ThreadDumpAnalyzer.java` — `countByState` | `TODO(Day22-task04)` | sorted map (TreeMap) from state to the number of threads in that state |
| `ThreadDumpAnalyzer.java` — `hotspot` | `TODO(Day22-task04)` | among RUNNABLE threads that have at least one frame count the first frame; return the most frequent (alphabetically first on ties) or Optional.empty() |
| `ThreadDumpAnalyzer.java` — `findDeadlock` | `TODO(Day22-task04)` | map lock id -> holder thread; edge thread -> holder of its waitingForLock; follow edges from each thread, and when you revisit a thread on the current path return the names on the cycle (sorted); none -> empty set |
| `ThreadDumpAnalyzer.java` — `liveDeadlockedThreads` | `TODO(Day22-task04)` | ThreadMXBean bean = ManagementFactory.getThreadMXBean(); long[] ids = bean.findDeadlockedThreads(); null -> empty list; otherwise the sorted thread names from bean.getThreadInfo(ids) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_parseExtractsThreadsInOrder`, `r1_parseReadsLocks`, `r1_parseHandlesEmptyAndNoise` |
| 2 | `r2_countByStateIsSorted` |
| 3 | `r3_hotspotIsTheMostCommonRunnableTopFrame`, `r3_hotspotTieBreaksAlphabetically` |
| 4 | `r4_findsTheTwoThreadDeadlockButNotTheInnocentWaiter`, `r4_findsAThreeThreadCycle`, `r4_aBlockedChainIsNotADeadlock` |
| 5 | `r5_liveDeadlockIsDetectedFromInsideTheJvm` |

## Edge cases to handle

- no threads / empty dump
- threads that wait on a lock nobody holds
- three-thread cycle
- a chain that is blocked but not a cycle
- threads without any frames

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 22: Thread Dump Analyzer and Live Deadlock Detector`

## Hints (optional)

<details><summary>Hint 1</summary>

Parse with one `Pattern` per line kind and a small state machine: *current thread* fields are flushed when a new header appears (and at the end).

</details>

<details><summary>Hint 2</summary>

To detect a cycle, follow `waitsFor` edges from each thread while tracking the path; if you reach a thread already on the path, the cycle is the path suffix starting there.

</details>

<details><summary>Hint 3</summary>

`ThreadMXBean.findDeadlockedThreads()` returns `null` (not an empty array) when nothing is deadlocked.

</details>
