# Day 42 — Async, Scheduling, Caching and Virtual Threads in Spring Boot

**Phase:** Spring Boot  
**Primary theme:** Running work off the request thread, on a timetable, with caching and with virtual threads  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-async-completable-future`, `task-02-scheduled-jobs`, `task-03-cache-abstraction`, `task-04-virtual-threads-in-boot`  
**Instruction alignment:** Maps to Day 42 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Running work off the request thread, on a timetable, with caching and with virtual threads. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. @Async and the task executor
2. @Scheduled jobs
3. Caching abstraction and virtual threads
4. Interview corner, common mistakes, glossary

## Subtopics

### @Async and the task executor

#### What it is

`@EnableAsync` + `@Async` run a bean method on a separate thread via a proxy. Return `void` (fire-and-forget) or `CompletableFuture<T>` (so callers can compose with `thenApply`, `allOf`, `exceptionally`). Spring Boot auto-configures the `applicationTaskExecutor` (`ThreadPoolTaskExecutor`, thread prefix `task-`) configurable through `spring.task.execution.*` (core-size, max-size, queue-capacity). Unhandled exceptions of `void` methods go to an `AsyncUncaughtExceptionHandler`.

#### Why it exists / why it matters

Slow or independent work (sending mail, calling services in parallel, generating reports) should not block the request thread, and parallel calls cut latency to the slowest instead of the sum.

#### Pros and cons

**Pros**

- Simple to adopt: one annotation
- Composable futures
- Bounded, configurable pool
- Same proxy mechanism as @Transactional

**Cons / trade-offs**

- Self-invocation bypasses the proxy
- Context propagation (security, MDC, transactions) is NOT automatic
- Unbounded queues hide overload
- Errors in `void` methods are easy to lose

#### What happens without it / when misused

Calling `this.asyncMethod()` runs synchronously - no error, just no async. An async method that relies on the caller's transaction or `SecurityContext` fails or runs without it. A tiny queue-capacity with default rejection handling throws `TaskRejectedException` under load.

#### Syntax and rules

```java
@Configuration @EnableAsync class AsyncConfig {}

@Service class Mailer {
  @Async CompletableFuture<Boolean> send(String to) {...}
}
CompletableFuture<Void> all = CompletableFuture.allOf(a, b);   // then join
```
```properties
spring.task.execution.pool.core-size=8
spring.task.execution.pool.queue-capacity=100
spring.task.execution.thread-name-prefix=app-
```

#### Examples

**Example 1 — Handle failure**

```java
service.send(to).exceptionally(ex -> { log.warn("send failed", ex); return false; });
```

**Example 2 — Custom executor**

```java
@Bean("ioExecutor") Executor ioExecutor() { ... }
@Async("ioExecutor") void work() {...}
```

**Example 3 — Propagate MDC**

```java
@Bean TaskDecorator mdcDecorator() { return r -> { var c = MDC.getCopyOfContextMap(); return () -> { MDC.setContextMap(c); r.run(); }; }; }
```

#### Quick checks

1. Why does self-invocation break @Async?
2. Return types allowed for @Async?
3. What thread prefix does Boot's default executor use?

### @Scheduled jobs

#### What it is

`@EnableScheduling` activates `@Scheduled` methods: `fixedDelay` (wait after the previous run ends), `fixedRate` (start every N ms), `cron` (six fields: second minute hour day month weekday, optional `zone`), `initialDelay`, and `...String` variants accepting placeholders (`"${jobs.rate:60000}"`). Methods must be void and parameterless. By default a single scheduler thread runs all jobs (`spring.task.scheduling.pool.size`).

#### Why it exists / why it matters

Housekeeping, polling, report generation and cache refreshes need to run on a timetable without an external scheduler.

#### Pros and cons

**Pros**

- Declarative and tiny
- Externalizable via properties
- Cron with time zones
- Integrates with Boot's scheduler config

**Cons / trade-offs**

- Runs on EVERY instance: multiple replicas run the job multiple times (use ShedLock or Quartz/DB locks)
- A long job blocks others on the single scheduler thread
- No persistence/retry/misfire handling

#### What happens without it / when misused

Two application instances both executing `nightlyCleanup` can double-process data. A job that throws is rescheduled, but errors may go unnoticed without logging. `fixedRate` jobs that run longer than the period pile up.

#### Syntax and rules

```java
@Scheduled(fixedDelay = 5000, initialDelay = 60000) void heartbeat() {...}
@Scheduled(cron = "0 0 2 * * *", zone = "UTC")      void nightly() {...}
@Scheduled(fixedRateString = "${jobs.refresh-rate:60000}") void refresh() {...}
```
```properties
spring.task.scheduling.pool.size=4
spring.task.scheduling.thread-name-prefix=sched-
```
Test by inspecting `ScheduledAnnotationBeanPostProcessor#getScheduledTasks()` or by calling the method directly - not by sleeping.

#### Examples

**Example 1 — Cron examples**

```text
0 0/15 * * * *   every 15 minutes
0 0 9-17 * * MON-FRI   hourly on weekdays 9-17
0 0 0 1 * *   first day of month
```

**Example 2 — Disable in tests**

```properties
spring.task.scheduling.enabled=false   # or use a profile guard
```

**Example 3 — Distributed lock (idea)**

```java
@SchedulerLock(name = "nightlyCleanup", lockAtMostFor = "10m")
```

#### Quick checks

1. fixedDelay vs fixedRate?
2. What happens with several app instances?
3. How many fields does a Spring cron have?

### Caching abstraction and virtual threads

#### What it is

**Cache abstraction**: `@EnableCaching`; `@Cacheable` (skip the method on a hit), `@CachePut` (always run, update cache), `@CacheEvict` (remove entries, `allEntries = true`), `key` (SpEL), `condition` (before), `unless` (after, can use `#result`). Providers: ConcurrentMap by default; Caffeine, Redis, EhCache via starters/properties. **Virtual threads** (Java 21, JEP 444): cheap threads for blocking code; Boot 3.2+ enables them for Tomcat/Jetty, `@Async`, `@Scheduled` and more with `spring.threads.virtual.enabled=true`.

#### Why it exists / why it matters

Caching removes repeated expensive work; virtual threads let a thread-per-request style scale to many concurrent blocking calls (database, HTTP) without reactive code.

#### Pros and cons

**Pros**

- Declarative caching with minimal code
- Swappable providers
- Virtual threads keep simple imperative code scalable
- One property to adopt in Boot

**Cons / trade-offs**

- Stale data and invalidation are hard
- Memory growth without eviction/TTL (configure Caffeine `maximumSize`, `expireAfterWrite`)
- Virtual threads do not speed up CPU-bound code and `synchronized` + blocking can pin carrier threads
- Thread-local heavy code needs review

#### What happens without it / when misused

Caching mutable objects or user-specific data under shared keys leaks data. Forgetting eviction on updates serves stale values. Creating a fixed thread pool of virtual threads defeats their purpose - use one per task.

#### Syntax and rules

```java
@Cacheable(value = "prices", unless = "#result == null") Double priceOf(String sku)
@CachePut(value = "prices", key = "#sku") Double setPrice(String sku, double p)
@CacheEvict(value = "prices", allEntries = true) void evictAll()

try (var ex = Executors.newVirtualThreadPerTaskExecutor()) { ex.invokeAll(tasks); }
```
```properties
spring.cache.type=caffeine
spring.cache.caffeine.spec=maximumSize=1000,expireAfterWrite=10m
spring.threads.virtual.enabled=true
```

#### Examples

**Example 1 — Conditional caching**

```java
@Cacheable(value = "users", condition = "#id > 0", key = "#id")
```

**Example 2 — Thread check**

```java
Thread.currentThread().isVirtual()
```

**Example 3 — Thread builder**

```java
Thread t = Thread.ofVirtual().name("worker-", 0).start(() -> work());
```

#### Quick checks

1. @Cacheable vs @CachePut?
2. When do virtual threads help?
3. What pins a virtual thread (Java 21)?

## Interview corner

**Q1. How does @Async work?**

A proxy submits the method call to a TaskExecutor.

**Q2. How do you run a job once in a cluster?**

A distributed lock (ShedLock), a leader election, or an external scheduler.

**Q3. Cacheable vs CachePut vs CacheEvict?**

Read-through, write-through refresh, invalidate.

**Q4. What are virtual threads?**

JVM-managed lightweight threads scheduled onto carrier threads; ideal for blocking I/O.

**Q5. What can go wrong with @Async and security/transactions?**

Context is thread-bound and not propagated automatically.

## Common mistakes & debugging

- Self-invocation of @Async/@Cacheable methods.
- Assuming scheduled jobs run once per cluster.
- Unbounded caches.
- Pooling virtual threads.
- Ignoring context propagation.

## Further reading

- Spring Framework Reference: Task Execution and Scheduling, Cache Abstraction
- JEP 444: Virtual Threads
- Spring Boot Reference: Task Execution, Virtual Threads

## Glossary

| Term | Meaning |
|------|---------|
| @Async | Run a method on another thread |
| fixedDelay | Wait N ms after the previous run finished |
| Cache eviction | Removing cached entries |
| Virtual thread | Lightweight JVM thread |
| Carrier thread | Platform thread that runs virtual threads |

## Answers

### @Async and the task executor

1. The call does not go through the Spring proxy.
2. void, Future, CompletableFuture (and ListenableFuture in older versions).
3. `task-`.

### @Scheduled jobs

1. fixedDelay waits after completion; fixedRate starts at fixed intervals.
2. Each runs the job unless you add a distributed lock.
3. Six: second, minute, hour, day-of-month, month, day-of-week.

### Caching abstraction and virtual threads

1. Cacheable skips the method on a hit; CachePut always runs and refreshes the cache.
2. With many concurrent blocking I/O operations.
3. Blocking inside `synchronized` blocks or native calls.
