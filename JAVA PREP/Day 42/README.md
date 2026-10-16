# Day 42 — Async, Scheduling, Caching and Virtual Threads in Spring Boot

## Learning objectives

- Use @Async with CompletableFuture and understand the proxy pitfalls
- Declare and test @Scheduled jobs
- Apply @Cacheable/@CachePut/@CacheEvict with SpEL keys
- Enable and verify virtual threads in Boot 3.2+
- Reason about thread pools, backpressure and context propagation

## Prerequisites

- Day 40 AOP
- Day 41 observability (MDC)

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-42-THEORY-AND-REFERENCE.md`](DAY-42-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-async-completable-future` | Spring Boot (Async / Scheduling / Cache) | `mvn test` |
| 2 | `task-02-scheduled-jobs` | Spring Boot (Async / Scheduling / Cache) | `mvn test` |
| 3 | `task-03-cache-abstraction` | Spring Boot (Async / Scheduling / Cache) | `mvn test` |
| 4 | `task-04-virtual-threads-in-boot` | Spring Boot (Async / Scheduling / Cache) | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
