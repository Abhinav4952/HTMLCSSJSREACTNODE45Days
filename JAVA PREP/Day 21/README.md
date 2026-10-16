# Day 21 — Concurrency II: ExecutorService, Callable/Future, CompletableFuture, Atomics, Locks, Concurrent Collections

## Learning objectives

- Create and size thread pools with `Executors`/`ThreadPoolExecutor` and shut them down correctly
- Submit `Runnable`/`Callable` tasks and consume results with `Future` (timeouts, cancellation, `invokeAll`, `invokeAny`)
- Compose asynchronous pipelines with `CompletableFuture` (`thenApply`, `thenCompose`, `thenCombine`, `allOf`, `exceptionally`, `handle`)
- Use atomics (`AtomicInteger`, `AtomicLong`, `LongAdder`) and CAS loops instead of locks for simple state
- Use `ReentrantLock`, `ReadWriteLock`, and know the advantages over `synchronized`
- Choose concurrent collections (`ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue`) correctly

## Prerequisites

- Day 20 — threads, synchronized, volatile, wait/notify
- Day 16 — lambdas and functional interfaces
- Day 15 — maps and queues

## How to use this folder

1. Read [`DAY-21-THEORY-AND-REFERENCE.md`](DAY-21-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day21-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-executor-sum` | Plain Java | `mvn test` |
| 2 | `task-02-future-timeout` | Plain Java | `mvn test` |
| 3 | `task-03-completable-pipeline` | Plain Java | `mvn test` |
| 4 | `task-04-atomic-counter` | Plain Java | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Core Java
