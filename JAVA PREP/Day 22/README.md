# Day 22 — Virtual Threads (Java 21), JVM Memory & GC, Class Loading, and Troubleshooting

## Learning objectives

- Create virtual threads with `Thread.ofVirtual()`, `Thread.startVirtualThread`, and `Executors.newVirtualThreadPerTaskExecutor()` and explain when they help (blocking I/O) and when they do not (CPU-bound work)
- Explain pinning, `ThreadLocal` cost, and why virtual threads must never be pooled; limit concurrency with a `Semaphore` instead
- Describe heap generations, metaspace, thread stacks, and direct memory, and pick a collector (Serial, Parallel, G1, ZGC) with the right `-Xms/-Xmx/-XX` flags
- Read unified GC logs (`-Xlog:gc*`) and spot a leak from a rising post-GC live set
- Explain parent-first delegation, class identity (`name + defining loader`), and the difference between `ClassNotFoundException` and `NoClassDefFoundError`
- Diagnose hangs, deadlocks, high CPU, and `OutOfMemoryError` with `jps`, `jstack`, `jcmd`, `jstat`, heap dumps, and VisualVM

## Prerequisites

- Day 20 — threads, synchronized, volatile
- Day 21 — ExecutorService, CompletableFuture, locks
- Day 13 — exceptions and stack traces

## How to use this folder

1. Read [`DAY-22-THEORY-AND-REFERENCE.md`](DAY-22-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day22-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-virtual-thread-runner` | Plain Java | `mvn test` |
| 2 | `task-02-gc-log-analyzer` | Plain Java | `mvn test` |
| 3 | `task-03-classloader-lab` | Plain Java | `mvn test` |
| 4 | `task-04-thread-dump-analyzer` | Plain Java | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Core Java
