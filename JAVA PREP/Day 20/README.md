# Day 20 — Threads I: Thread, Runnable, synchronized, volatile, wait/notify, and Deadlock

## Learning objectives

- Create and start threads with `Thread` and `Runnable`; explain `start()` vs `run()`, `join()`, daemon threads and thread states
- Explain race conditions, atomicity, visibility, and ordering using the Java Memory Model (happens-before)
- Protect invariants with `synchronized` (methods/blocks, intrinsic locks, reentrancy)
- Use `volatile` correctly (visibility, no atomicity) and know when it is not enough
- Implement a producer/consumer buffer with `wait()`/`notifyAll()` guarded by a `while` loop
- Identify the four deadlock conditions and prevent deadlock with a global lock ordering

## Prerequisites

- Day 16 — lambdas (`Runnable` as a lambda)
- Day 11 — exceptions (`InterruptedException`)
- Day 14 — collections (not thread-safe by default)

## How to use this folder

1. Read [`DAY-20-THEORY-AND-REFERENCE.md`](DAY-20-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day20-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-runnable-counter` | Plain Java | `mvn test` |
| 2 | `task-02-synchronized-bank` | Plain Java | `mvn test` |
| 3 | `task-03-wait-notify-buffer` | Plain Java | `mvn test` |
| 4 | `task-04-deadlock-detector-doc` | Plain Java | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Core Java
