# Day 21 — Concurrency II: ExecutorService, Callable/Future, CompletableFuture, Atomics, Locks, Concurrent Collections

**Phase:** Core Java  
**Primary theme:** Replace raw threads with executors and futures, compose async work, and share state safely with atomics, locks, and concurrent collections.  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-executor-sum`, `task-02-future-timeout`, `task-03-completable-pipeline`, `task-04-atomic-counter`  
**Instruction alignment:** Maps to the Day 21 entry of the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21 (no Spring today)

## Overview

Day 20 gave you the primitives; production code almost never uses them directly. **Executors** decouple *what* to run from *how/where* it runs (pool size, queueing, naming, shutdown). **Futures** let you get a result back (or a timeout, cancellation, or the exception). **`CompletableFuture`** lets you compose non-blocking pipelines (fetch user -> fetch orders -> combine -> fallback on error), which is how most async Java code is written outside reactive frameworks.

For shared state, prefer **atomics** (lock-free CAS), **`ConcurrentHashMap`** (atomic `merge`/`compute`), and **explicit locks** when you need `tryLock`, fairness, or read/write splitting. Interviews ask: *how do you size a thread pool*, *Runnable vs Callable*, *what does `future.get()` do on failure*, *thenApply vs thenCompose*, *why LongAdder over AtomicLong*, *ConcurrentHashMap vs synchronizedMap*.

## Day roadmap

1. ExecutorService, Callable, and Future
2. CompletableFuture: composing asynchronous pipelines
3. Atomics, locks, and concurrent collections
4. Interview angles
5. Common mistakes & debugging
6. Further reading, glossary, answers

### ExecutorService, Callable, and Future

#### What it is

An **`Executor`** runs submitted tasks; an **`ExecutorService`** adds lifecycle (`shutdown`, `shutdownNow`, `awaitTermination`) and `submit` returning a **`Future<T>`**. `Runnable` returns nothing and cannot throw checked exceptions; **`Callable<V>`** returns a value and may throw. Factory pools: `newFixedThreadPool(n)`, `newCachedThreadPool()`, `newSingleThreadExecutor()`, `newScheduledThreadPool(n)`, and (Java 21) `newVirtualThreadPerTaskExecutor()`. Underneath is `ThreadPoolExecutor` (core/max size, work queue, `RejectedExecutionHandler`, `ThreadFactory`). `Future.get()` blocks until done, returning the value or throwing `ExecutionException` (wrapping the task's exception); `get(timeout, unit)` adds `TimeoutException`; `cancel(true)` interrupts a running task. `invokeAll` runs a batch and returns completed futures in input order; `invokeAny` returns the first success.

#### Why it exists / why it matters

Creating a thread per task is expensive and unbounded. Pools reuse threads, bound concurrency (protect the database!), queue excess work, and give one place to name threads, handle rejection, and shut down. Futures standardize result retrieval and failure propagation across threads.

#### Pros and cons

**Pros**

- Thread reuse and bounded concurrency
- Clean separation of task submission from execution policy
- Results, timeouts, cancellation, and exception propagation via `Future`
- `invokeAll/invokeAny` cover common batch patterns

**Cons / tradeoffs**

- Wrong pool size/queue choices cause latency or `RejectedExecutionException`
- `Future.get()` is blocking - easy to reintroduce sequential behavior
- Cancellation is cooperative: `cancel(true)` only interrupts

#### What happens without it / when misused

**Not shutting down** a pool keeps non-daemon threads alive and the JVM never exits. `newCachedThreadPool` with bursts creates unbounded threads (`OutOfMemoryError: unable to create native thread`); `newFixedThreadPool` uses an **unbounded** queue, so a slow consumer causes unbounded memory growth. Calling `future.get()` inside a task running in the same fixed pool can **deadlock** (thread starvation). Ignoring the returned `Future` of `submit` silently swallows exceptions (unlike `execute`, which reports uncaught exceptions). Swallowing `InterruptedException` in a task prevents cancellation. Sizing: CPU-bound ~ cores (+1); I/O-bound ~ cores x (1 + wait/compute ratio) - or use virtual threads (Day 22).

#### Syntax and rules

- `ExecutorService pool = Executors.newFixedThreadPool(4);` ... `pool.shutdown();` (no new tasks; running tasks finish) then `awaitTermination(timeout, unit)`; if it times out, `shutdownNow()` (interrupts).
- `Future<Integer> f = pool.submit(() -> compute());` `f.get()`, `f.get(1, SECONDS)`, `f.cancel(true)`, `f.isDone()`.
- `List<Future<T>> fs = pool.invokeAll(callables);` (waits for all) / `T first = pool.invokeAny(callables);`.
- Always `try { ... } finally { pool.shutdown(); }` (Java 19+: `ExecutorService` is `AutoCloseable`, so try-with-resources works).
- `ThreadPoolExecutor(core, max, keepAlive, unit, new ArrayBlockingQueue<>(n), threadFactory, new CallerRunsPolicy())` for explicit bounded queues and back-pressure.
- Name threads with a `ThreadFactory` so thread dumps are readable.

#### Examples

**Example 1.1 — Tiny — submit a Callable and get the result**

```java
ExecutorService pool = Executors.newFixedThreadPool(2);
try {
    Future<Integer> f = pool.submit(() -> 6 * 7);
    System.out.println(f.get());            // 42
} finally {
    pool.shutdown();
}
```

**Example 1.2 — Tiny — failure and timeout handling**

```java
ExecutorService pool = Executors.newSingleThreadExecutor();
Future<String> bad = pool.submit(() -> { throw new IllegalStateException("boom"); });
try { bad.get(); }
catch (ExecutionException e) { System.out.println(e.getCause().getMessage()); }   // boom

Future<String> slow = pool.submit(() -> { Thread.sleep(10_000); return "late"; });
try { slow.get(100, TimeUnit.MILLISECONDS); }
catch (TimeoutException e) { slow.cancel(true); System.out.println("timed out"); } // timed out
pool.shutdownNow();
```

**Example 1.3 — Medium — chunked parallel sum with graceful shutdown**

```java
import java.util.*;
import java.util.concurrent.*;

public class ChunkedSum {
    static long sum(List<Integer> nums, int chunks, ExecutorService pool) throws Exception {
        int size = nums.size(), step = Math.max(1, (size + chunks - 1) / chunks);
        List<Future<Long>> parts = new ArrayList<>();
        for (int i = 0; i < size; i += step) {
            List<Integer> slice = nums.subList(i, Math.min(size, i + step));
            parts.add(pool.submit(() -> slice.stream().mapToLong(Integer::longValue).sum()));
        }
        long total = 0;
        for (Future<Long> f : parts) total += f.get();   // waits in order; failure -> ExecutionException
        return total;
    }

    public static void main(String[] args) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(4);
        try {
            System.out.println(sum(java.util.stream.IntStream.rangeClosed(1, 100).boxed().toList(), 4, pool)); // 5050
        } finally {
            pool.shutdown();
            if (!pool.awaitTermination(5, TimeUnit.SECONDS)) pool.shutdownNow();
        }
    }
}
```

#### Quick checks

1. Runnable vs Callable?
2. What exception does `future.get()` throw if the task threw `IOException`?
3. Why can a task that calls `future.get()` on another task deadlock a fixed pool?
4. What is the difference between `shutdown()` and `shutdownNow()`?

### CompletableFuture: composing asynchronous pipelines

#### What it is

`CompletableFuture<T>` is a `Future` that you can complete manually and *compose*. Start with `supplyAsync(supplier[, executor])` / `runAsync`. Transform: `thenApply(fn)` (sync map), `thenCompose(fn returning CF)` (flatMap), `thenCombine(other, bifn)` (join two independent results), `thenAccept`, `thenRun`. Fan-in: `allOf(...)` (completes when all do) and `anyOf(...)`. Errors: `exceptionally(fn)` (recover), `handle((value, ex) -> ...)` (both paths), `whenComplete` (observe). Time: `orTimeout`, `completeOnTimeout` (Java 9). Results: `join()` (unchecked `CompletionException`) or `get()` (checked). Methods ending in `Async` hop to another thread; the plain versions run on whichever thread completes the previous stage.

#### Why it exists / why it matters

Real requests fan out to several services (user, orders, recommendations) and combine the results. Sequential `get()` calls add up latencies; `CompletableFuture` runs independent stages concurrently and expresses fallbacks and timeouts declaratively. It is also the bridge to reactive/async APIs in later frameworks.

#### Pros and cons

**Pros**

- Non-blocking composition with clear error handling
- Parallel fan-out/fan-in (`allOf`, `thenCombine`)
- Built-in timeout and fallback operators
- Works with any `Executor` (including virtual threads)

**Cons / tradeoffs**

- Exceptions are wrapped in `CompletionException`, which confuses logging and `handle`
- Default async pool is the shared `ForkJoinPool.commonPool()` (do not run blocking I/O there - pass your own executor)
- Long chains are hard to debug; cancellation does not interrupt the running task

#### What happens without it / when misused

Calling `join()` on every stage immediately turns the pipeline back into blocking code. Using `thenApply` where the function returns a `CompletableFuture` produces `CompletableFuture<CompletableFuture<T>>` (you wanted `thenCompose`). Running blocking JDBC/HTTP calls in `supplyAsync` *without* an executor starves the common pool for the whole JVM. An exception in a stage with no `exceptionally/handle` and no one calling `join/get` is **silently lost**. `allOf` returns `CompletableFuture<Void>` - you must collect the individual results yourself. Catching `Exception` around `join()` without unwrapping `CompletionException` hides the real cause.

#### Syntax and rules

- `CompletableFuture.supplyAsync(() -> load(), executor)`.
- map: `cf.thenApply(String::trim)`; flatMap: `cf.thenCompose(id -> loadUserAsync(id))`; combine: `a.thenCombine(b, (x, y) -> x + y)`.
- Fan-in: `CompletableFuture.allOf(a, b, c).thenApply(v -> List.of(a.join(), b.join(), c.join()))`.
- Recover: `cf.exceptionally(ex -> fallback)`; both paths: `cf.handle((v, ex) -> ex == null ? v : fallback)`.
- Unwrap: `ex instanceof CompletionException && ex.getCause() != null ? ex.getCause() : ex`.
- Time limits: `cf.orTimeout(2, SECONDS)` (fails with `TimeoutException`), `cf.completeOnTimeout(default, 2, SECONDS)`.
- Testing: pass a direct executor (`Runnable::run`) for deterministic single-thread execution.

#### Examples

**Example 2.1 — Tiny — thenApply vs thenCompose**

```java
CompletableFuture<Integer> a = CompletableFuture.supplyAsync(() -> 20);
CompletableFuture<Integer> doubled = a.thenApply(x -> x * 2);                       // value -> value
CompletableFuture<String> viaCompose = a.thenCompose(x -> CompletableFuture.supplyAsync(() -> "id-" + x)); // value -> CF
System.out.println(doubled.join() + " " + viaCompose.join());   // 40 id-20
```

**Example 2.2 — Tiny — fallback and timeout**

```java
CompletableFuture<Integer> risky = CompletableFuture.supplyAsync(() -> { throw new IllegalStateException("x"); });
System.out.println(risky.exceptionally(ex -> -1).join());                 // -1

CompletableFuture<Integer> never = new CompletableFuture<>();
System.out.println(never.completeOnTimeout(0, 50, TimeUnit.MILLISECONDS).join());  // 0
```

**Example 2.3 — Medium — fan-out and combine**

```java
import java.util.*;
import java.util.concurrent.*;

public class Dashboard {
    record View(String user, int orders) {}

    static CompletableFuture<View> load(ExecutorService io) {
        CompletableFuture<String> user = CompletableFuture.supplyAsync(() -> "ada", io);
        CompletableFuture<Integer> orders = CompletableFuture.supplyAsync(() -> 3, io);
        return user.thenCombine(orders, View::new)                   // runs both in parallel, then combines
                .orTimeout(2, TimeUnit.SECONDS)
                .exceptionally(ex -> new View("unknown", 0));         // degrade gracefully
    }

    public static void main(String[] args) {
        ExecutorService io = Executors.newFixedThreadPool(2);
        try { System.out.println(load(io).join()); }                  // View[user=ada, orders=3]
        finally { io.shutdown(); }
    }
}
```

#### Quick checks

1. What is the difference between `thenApply` and `thenCompose`?
2. What does `join()` throw on failure vs `get()`?
3. Why pass your own executor to `supplyAsync` for I/O?
4. How do you wait for several futures and keep their results?

### Atomics, locks, and concurrent collections

#### What it is

**Atomics** (`AtomicInteger`, `AtomicLong`, `AtomicReference`, `AtomicBoolean`) provide lock-free thread-safe updates via **compare-and-set (CAS)**: `incrementAndGet`, `getAndSet`, `updateAndGet(fn)`, `accumulateAndGet(x, fn)`, or an explicit loop `do { cur = get(); next = f(cur); } while (!compareAndSet(cur, next));`. `LongAdder`/`LongAccumulator` stripe the counter across cells to reduce contention under heavy writes (sum is computed on read). **Locks** (`java.util.concurrent.locks`): `ReentrantLock` (`lock/unlock` in `try/finally`, `tryLock(timeout)`, `lockInterruptibly`, fairness, multiple `Condition`s) and `ReentrantReadWriteLock` (many readers or one writer). **Concurrent collections**: `ConcurrentHashMap` (atomic `putIfAbsent/compute/merge`, no null keys/values, weakly consistent iterators), `CopyOnWriteArrayList/Set` (snapshot iteration, writes copy the array), `ConcurrentLinkedQueue`, and `BlockingQueue` implementations (`ArrayBlockingQueue`, `LinkedBlockingQueue`, `PriorityBlockingQueue`) for producer/consumer.

#### Why it exists / why it matters

Simple counters and flags do not need a lock - atomics are faster and cannot deadlock. Compound invariants need locks. `Collections.synchronizedMap` serializes all access and still requires external locking for compound operations and iteration; `ConcurrentHashMap` scales with fine-grained locking/CAS and offers atomic compound operations. These are the building blocks of caches, metrics, rate limiters, and work queues.

#### Pros and cons

**Pros**

- Atomics: lock-free, no deadlock, simple
- `LongAdder` scales for write-heavy counters
- `tryLock` and interruptible locking avoid hangs; read/write locks boost read-mostly workloads
- `ConcurrentHashMap` offers atomic compound operations and high concurrency

**Cons / tradeoffs**

- Atomics only protect a **single variable**; multi-field invariants still need a lock
- CAS loops can spin under high contention (use `LongAdder` or a lock)
- Forgetting `unlock()` in `finally` leaks the lock; `ReadWriteLock` can starve writers or be slower for short critical sections
- Concurrent iterators are weakly consistent (may or may not reflect concurrent updates)

#### What happens without it / when misused

`if (!map.containsKey(k)) map.put(k, v)` on a `ConcurrentHashMap` is still a **check-then-act race** (use `putIfAbsent`/`computeIfAbsent`). Two separate atomic updates (`balance.addAndGet(-x); other.addAndGet(x)`) are not atomic *together*. Using `AtomicInteger` for a value that must stay within `[0, max]` needs a CAS loop (an unconditional `incrementAndGet` overshoots). Forgetting `lock.unlock()` in `finally` leaves the lock held forever after an exception. Mutating the value objects stored in a `ConcurrentHashMap` (e.g. `ArrayList`) is still unsafe. Using `CopyOnWriteArrayList` for write-heavy workloads copies the whole array on every write. `ConcurrentHashMap.size()` is only an estimate under concurrent updates.

#### Syntax and rules

- Atomic counter: `AtomicLong hits = new AtomicLong(); hits.incrementAndGet(); hits.getAndSet(0);`.
- CAS loop: `int cur; do { cur = max.get(); if (v <= cur) return; } while (!max.compareAndSet(cur, v));` or `max.accumulateAndGet(v, Math::max)`.
- Lock idiom: `lock.lock(); try { ... } finally { lock.unlock(); }`; `if (lock.tryLock(50, MILLISECONDS)) { try { ... } finally { lock.unlock(); } }`.
- Read/write: `rw.readLock().lock()` for lookups, `rw.writeLock().lock()` for updates (always unlock in `finally`).
- Frequency map: `ConcurrentHashMap<String, LongAdder> m; m.computeIfAbsent(w, k -> new LongAdder()).increment();` or `m.merge(w, 1L, Long::sum)`.
- Prefer `BlockingQueue.put/take` over hand-written wait/notify for producer/consumer.

#### Examples

**Example 3.1 — Tiny — atomic counter and CAS-based maximum**

```java
AtomicLong hits = new AtomicLong();
hits.incrementAndGet();
System.out.println(hits.getAndSet(0));       // 1  (and resets)

AtomicInteger max = new AtomicInteger(Integer.MIN_VALUE);
for (int v : new int[] {3, 9, 4}) max.accumulateAndGet(v, Math::max);
System.out.println(max.get());               // 9
```

**Example 3.2 — Tiny — ConcurrentHashMap atomic compound operations**

```java
ConcurrentHashMap<String, Long> counts = new ConcurrentHashMap<>();
for (String w : List.of("a", "b", "a")) counts.merge(w, 1L, Long::sum);
System.out.println(new TreeMap<>(counts));    // {a=2, b=1}
counts.putIfAbsent("c", 0L);                  // atomic, unlike containsKey + put
```

**Example 3.3 — Medium — read-mostly registry with ReadWriteLock**

```java
import java.util.*;
import java.util.concurrent.locks.*;

public final class Registry {
    private final Map<String, String> map = new HashMap<>();
    private final ReentrantReadWriteLock lock = new ReentrantReadWriteLock();

    public void put(String k, String v) {
        lock.writeLock().lock();
        try { map.put(k, v); }
        finally { lock.writeLock().unlock(); }
    }

    public String get(String k) {
        lock.readLock().lock();                  // many readers may hold this at once
        try { return map.get(k); }
        finally { lock.readLock().unlock(); }
    }
}
```

#### Quick checks

1. Why is `LongAdder` preferred over `AtomicLong` for hot counters?
2. Why is `containsKey` then `put` unsafe on a `ConcurrentHashMap`?
3. Why must `unlock()` be in a `finally` block?
4. When is `CopyOnWriteArrayList` a good fit?

## Interview angles

**Q: How do you choose a thread pool size?**

CPU-bound: about the number of cores (+1). I/O-bound: cores x (1 + wait time / compute time), or measure; consider virtual threads for blocking I/O. Bound the queue to apply back-pressure.

**Q: What are the dangers of `Executors.newFixedThreadPool` and `newCachedThreadPool`?**

Fixed uses an unbounded queue (memory growth); cached has unbounded thread creation. Prefer an explicit `ThreadPoolExecutor` with a bounded queue and rejection policy.

**Q: Callable vs Runnable vs Supplier?**

`Callable` returns a value and may throw checked exceptions (used with `ExecutorService`); `Runnable` returns nothing; `Supplier` returns a value but cannot throw checked exceptions (used with `CompletableFuture.supplyAsync`).

**Q: How does CAS work and what is the ABA problem?**

Compare-and-set atomically updates a value only if it still equals the expected one; ABA is when a value changes A->B->A so CAS cannot see the intermediate change (`AtomicStampedReference` adds a version).

**Q: ConcurrentHashMap vs Collections.synchronizedMap vs Hashtable?**

CHM uses fine-grained locking/CAS with atomic compound operations and weakly consistent iterators; the others use one lock for every operation and still need external locking for compound actions and iteration.

**Q: What happens to exceptions in CompletableFuture stages?**

They complete the stage exceptionally and propagate to dependents wrapped in `CompletionException`; handle with `exceptionally`/`handle`, otherwise they are silent until `join/get`.

## Common mistakes & debugging

- Forgetting to `shutdown()` the pool (JVM never exits) or leaking pools per request.
- Ignoring `Future`s or `CompletableFuture`s so failures are never noticed.
- Blocking calls (`get()`/`join()`) inside tasks of the same bounded pool (deadlock).
- Running blocking I/O on the common ForkJoinPool via `supplyAsync` without a custom executor.
- Check-then-act on concurrent collections; two atomic variables treated as one invariant.
- `lock()` without `try/finally unlock()`.

## Further reading

- Javadoc: `java.util.concurrent` package summary, `ExecutorService`, `ThreadPoolExecutor`, `CompletableFuture`, `ConcurrentHashMap`, `LongAdder`
- *Java Concurrency in Practice* (Goetz) ch. 5-8 (building blocks, task execution, pool sizing)
- Oracle Java Tutorials - *Concurrency: High Level Concurrency Objects*
- JEP 444 (virtual threads) for the alternative to large I/O thread pools (see Day 22)

## Glossary

| Term | Meaning |
|------|---------|
| Executor | Abstraction that runs submitted tasks |
| Future | Handle to the result of an asynchronous computation |
| CompletableFuture | Composable, manually completable future |
| CAS | Compare-and-set: atomic conditional update (hardware-supported) |
| Back-pressure | Slowing producers when consumers/queues are saturated |
| Thread starvation deadlock | All pool threads blocked on tasks that cannot start |
| Weakly consistent iterator | Iterator that tolerates concurrent modification without throwing |
| Common pool | `ForkJoinPool.commonPool()` default for async stages and parallel streams |

## Answers

Answers to every **Quick check** above (numbered `section.question`).

- **1.1** — Runnable vs Callable?  
  `Runnable.run()` returns nothing and cannot throw checked exceptions; `Callable<V>.call()` returns a value and may throw `Exception`.

- **1.2** — What exception does `future.get()` throw if the task threw `IOException`?  
  `ExecutionException` whose `getCause()` is the `IOException`.

- **1.3** — Why can a task that calls `future.get()` on another task deadlock a fixed pool?  
  All pool threads can end up blocked waiting for tasks that are queued behind them (thread starvation deadlock).

- **1.4** — What is the difference between `shutdown()` and `shutdownNow()`?  
  `shutdown` stops accepting tasks and lets queued/running ones finish; `shutdownNow` also interrupts running tasks and returns the never-started ones.

- **2.1** — What is the difference between `thenApply` and `thenCompose`?  
  `thenApply` maps the value with a plain function; `thenCompose` flattens a function that itself returns a `CompletableFuture` (like `flatMap`).

- **2.2** — What does `join()` throw on failure vs `get()`?  
  `join()` throws unchecked `CompletionException`; `get()` throws checked `ExecutionException`; both wrap the original cause.

- **2.3** — Why pass your own executor to `supplyAsync` for I/O?  
  The default is the shared common pool sized for CPU work; blocking calls would starve unrelated parallel streams and async tasks.

- **2.4** — How do you wait for several futures and keep their results?  
  `allOf(...)` then collect each future's `join()` in a `thenApply`.

- **3.1** — Why is `LongAdder` preferred over `AtomicLong` for hot counters?  
  It spreads updates across cells to reduce CAS contention; `sum()` aggregates on read.

- **3.2** — Why is `containsKey` then `put` unsafe on a `ConcurrentHashMap`?  
  Another thread can insert between the two calls (check-then-act race); use `putIfAbsent`, `computeIfAbsent`, or `merge`.

- **3.3** — Why must `unlock()` be in a `finally` block?  
  Otherwise an exception between `lock()` and `unlock()` leaves the lock held forever.

- **3.4** — When is `CopyOnWriteArrayList` a good fit?  
  Read-mostly, small lists with rare writes (listeners, config), where iterators need snapshot semantics.
