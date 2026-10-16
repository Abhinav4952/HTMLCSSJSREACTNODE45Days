from gen_helpers import sec, task

DAY = dict(
    num=21,
    title="Concurrency II: ExecutorService, Callable/Future, CompletableFuture, Atomics, Locks, Concurrent Collections",
    theme="Replace raw threads with executors and futures, compose async work, and share state safely with atomics, locks, and concurrent collections.",
    objectives=[
        "Create and size thread pools with `Executors`/`ThreadPoolExecutor` and shut them down correctly",
        "Submit `Runnable`/`Callable` tasks and consume results with `Future` (timeouts, cancellation, `invokeAll`, `invokeAny`)",
        "Compose asynchronous pipelines with `CompletableFuture` (`thenApply`, `thenCompose`, `thenCombine`, `allOf`, `exceptionally`, `handle`)",
        "Use atomics (`AtomicInteger`, `AtomicLong`, `LongAdder`) and CAS loops instead of locks for simple state",
        "Use `ReentrantLock`, `ReadWriteLock`, and know the advantages over `synchronized`",
        "Choose concurrent collections (`ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue`) correctly",
    ],
    prereqs=["Day 20 — threads, synchronized, volatile, wait/notify", "Day 16 — lambdas and functional interfaces", "Day 15 — maps and queues"],
    overview="""Day 20 gave you the primitives; production code almost never uses them directly. **Executors** decouple *what* to run from *how/where* it runs (pool size, queueing, naming, shutdown). **Futures** let you get a result back (or a timeout, cancellation, or the exception). **`CompletableFuture`** lets you compose non-blocking pipelines (fetch user -> fetch orders -> combine -> fallback on error), which is how most async Java code is written outside reactive frameworks.

For shared state, prefer **atomics** (lock-free CAS), **`ConcurrentHashMap`** (atomic `merge`/`compute`), and **explicit locks** when you need `tryLock`, fairness, or read/write splitting. Interviews ask: *how do you size a thread pool*, *Runnable vs Callable*, *what does `future.get()` do on failure*, *thenApply vs thenCompose*, *why LongAdder over AtomicLong*, *ConcurrentHashMap vs synchronizedMap*.""",
    sections=[
        sec(
            "ExecutorService, Callable, and Future",
            "An **`Executor`** runs submitted tasks; an **`ExecutorService`** adds lifecycle (`shutdown`, `shutdownNow`, `awaitTermination`) and `submit` returning a **`Future<T>`**. `Runnable` returns nothing and cannot throw checked exceptions; **`Callable<V>`** returns a value and may throw. Factory pools: `newFixedThreadPool(n)`, `newCachedThreadPool()`, `newSingleThreadExecutor()`, `newScheduledThreadPool(n)`, and (Java 21) `newVirtualThreadPerTaskExecutor()`. Underneath is `ThreadPoolExecutor` (core/max size, work queue, `RejectedExecutionHandler`, `ThreadFactory`). `Future.get()` blocks until done, returning the value or throwing `ExecutionException` (wrapping the task's exception); `get(timeout, unit)` adds `TimeoutException`; `cancel(true)` interrupts a running task. `invokeAll` runs a batch and returns completed futures in input order; `invokeAny` returns the first success.",
            "Creating a thread per task is expensive and unbounded. Pools reuse threads, bound concurrency (protect the database!), queue excess work, and give one place to name threads, handle rejection, and shut down. Futures standardize result retrieval and failure propagation across threads.",
            ["Thread reuse and bounded concurrency", "Clean separation of task submission from execution policy", "Results, timeouts, cancellation, and exception propagation via `Future`", "`invokeAll/invokeAny` cover common batch patterns"],
            ["Wrong pool size/queue choices cause latency or `RejectedExecutionException`", "`Future.get()` is blocking - easy to reintroduce sequential behavior", "Cancellation is cooperative: `cancel(true)` only interrupts"],
            "**Not shutting down** a pool keeps non-daemon threads alive and the JVM never exits. `newCachedThreadPool` with bursts creates unbounded threads (`OutOfMemoryError: unable to create native thread`); `newFixedThreadPool` uses an **unbounded** queue, so a slow consumer causes unbounded memory growth. Calling `future.get()` inside a task running in the same fixed pool can **deadlock** (thread starvation). Ignoring the returned `Future` of `submit` silently swallows exceptions (unlike `execute`, which reports uncaught exceptions). Swallowing `InterruptedException` in a task prevents cancellation. Sizing: CPU-bound ~ cores (+1); I/O-bound ~ cores x (1 + wait/compute ratio) - or use virtual threads (Day 22).",
            """- `ExecutorService pool = Executors.newFixedThreadPool(4);` ... `pool.shutdown();` (no new tasks; running tasks finish) then `awaitTermination(timeout, unit)`; if it times out, `shutdownNow()` (interrupts).
- `Future<Integer> f = pool.submit(() -> compute());` `f.get()`, `f.get(1, SECONDS)`, `f.cancel(true)`, `f.isDone()`.
- `List<Future<T>> fs = pool.invokeAll(callables);` (waits for all) / `T first = pool.invokeAny(callables);`.
- Always `try { ... } finally { pool.shutdown(); }` (Java 19+: `ExecutorService` is `AutoCloseable`, so try-with-resources works).
- `ThreadPoolExecutor(core, max, keepAlive, unit, new ArrayBlockingQueue<>(n), threadFactory, new CallerRunsPolicy())` for explicit bounded queues and back-pressure.
- Name threads with a `ThreadFactory` so thread dumps are readable.""",
            [
                ("Tiny — submit a Callable and get the result", """ExecutorService pool = Executors.newFixedThreadPool(2);
try {
    Future<Integer> f = pool.submit(() -> 6 * 7);
    System.out.println(f.get());            // 42
} finally {
    pool.shutdown();
}"""),
                ("Tiny — failure and timeout handling", """ExecutorService pool = Executors.newSingleThreadExecutor();
Future<String> bad = pool.submit(() -> { throw new IllegalStateException("boom"); });
try { bad.get(); }
catch (ExecutionException e) { System.out.println(e.getCause().getMessage()); }   // boom

Future<String> slow = pool.submit(() -> { Thread.sleep(10_000); return "late"; });
try { slow.get(100, TimeUnit.MILLISECONDS); }
catch (TimeoutException e) { slow.cancel(true); System.out.println("timed out"); } // timed out
pool.shutdownNow();"""),
                ("Medium — chunked parallel sum with graceful shutdown", """import java.util.*;
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
}"""),
            ],
            [
                ("Runnable vs Callable?", "`Runnable.run()` returns nothing and cannot throw checked exceptions; `Callable<V>.call()` returns a value and may throw `Exception`."),
                ("What exception does `future.get()` throw if the task threw `IOException`?", "`ExecutionException` whose `getCause()` is the `IOException`."),
                ("Why can a task that calls `future.get()` on another task deadlock a fixed pool?", "All pool threads can end up blocked waiting for tasks that are queued behind them (thread starvation deadlock)."),
                ("What is the difference between `shutdown()` and `shutdownNow()`?", "`shutdown` stops accepting tasks and lets queued/running ones finish; `shutdownNow` also interrupts running tasks and returns the never-started ones."),
            ],
        ),
        sec(
            "CompletableFuture: composing asynchronous pipelines",
            "`CompletableFuture<T>` is a `Future` that you can complete manually and *compose*. Start with `supplyAsync(supplier[, executor])` / `runAsync`. Transform: `thenApply(fn)` (sync map), `thenCompose(fn returning CF)` (flatMap), `thenCombine(other, bifn)` (join two independent results), `thenAccept`, `thenRun`. Fan-in: `allOf(...)` (completes when all do) and `anyOf(...)`. Errors: `exceptionally(fn)` (recover), `handle((value, ex) -> ...)` (both paths), `whenComplete` (observe). Time: `orTimeout`, `completeOnTimeout` (Java 9). Results: `join()` (unchecked `CompletionException`) or `get()` (checked). Methods ending in `Async` hop to another thread; the plain versions run on whichever thread completes the previous stage.",
            "Real requests fan out to several services (user, orders, recommendations) and combine the results. Sequential `get()` calls add up latencies; `CompletableFuture` runs independent stages concurrently and expresses fallbacks and timeouts declaratively. It is also the bridge to reactive/async APIs in later frameworks.",
            ["Non-blocking composition with clear error handling", "Parallel fan-out/fan-in (`allOf`, `thenCombine`)", "Built-in timeout and fallback operators", "Works with any `Executor` (including virtual threads)"],
            ["Exceptions are wrapped in `CompletionException`, which confuses logging and `handle`", "Default async pool is the shared `ForkJoinPool.commonPool()` (do not run blocking I/O there - pass your own executor)", "Long chains are hard to debug; cancellation does not interrupt the running task"],
            "Calling `join()` on every stage immediately turns the pipeline back into blocking code. Using `thenApply` where the function returns a `CompletableFuture` produces `CompletableFuture<CompletableFuture<T>>` (you wanted `thenCompose`). Running blocking JDBC/HTTP calls in `supplyAsync` *without* an executor starves the common pool for the whole JVM. An exception in a stage with no `exceptionally/handle` and no one calling `join/get` is **silently lost**. `allOf` returns `CompletableFuture<Void>` - you must collect the individual results yourself. Catching `Exception` around `join()` without unwrapping `CompletionException` hides the real cause.",
            """- `CompletableFuture.supplyAsync(() -> load(), executor)`.
- map: `cf.thenApply(String::trim)`; flatMap: `cf.thenCompose(id -> loadUserAsync(id))`; combine: `a.thenCombine(b, (x, y) -> x + y)`.
- Fan-in: `CompletableFuture.allOf(a, b, c).thenApply(v -> List.of(a.join(), b.join(), c.join()))`.
- Recover: `cf.exceptionally(ex -> fallback)`; both paths: `cf.handle((v, ex) -> ex == null ? v : fallback)`.
- Unwrap: `ex instanceof CompletionException && ex.getCause() != null ? ex.getCause() : ex`.
- Time limits: `cf.orTimeout(2, SECONDS)` (fails with `TimeoutException`), `cf.completeOnTimeout(default, 2, SECONDS)`.
- Testing: pass a direct executor (`Runnable::run`) for deterministic single-thread execution.""",
            [
                ("Tiny — thenApply vs thenCompose", """CompletableFuture<Integer> a = CompletableFuture.supplyAsync(() -> 20);
CompletableFuture<Integer> doubled = a.thenApply(x -> x * 2);                       // value -> value
CompletableFuture<String> viaCompose = a.thenCompose(x -> CompletableFuture.supplyAsync(() -> "id-" + x)); // value -> CF
System.out.println(doubled.join() + " " + viaCompose.join());   // 40 id-20"""),
                ("Tiny — fallback and timeout", """CompletableFuture<Integer> risky = CompletableFuture.supplyAsync(() -> { throw new IllegalStateException("x"); });
System.out.println(risky.exceptionally(ex -> -1).join());                 // -1

CompletableFuture<Integer> never = new CompletableFuture<>();
System.out.println(never.completeOnTimeout(0, 50, TimeUnit.MILLISECONDS).join());  // 0"""),
                ("Medium — fan-out and combine", """import java.util.*;
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
}"""),
            ],
            [
                ("What is the difference between `thenApply` and `thenCompose`?", "`thenApply` maps the value with a plain function; `thenCompose` flattens a function that itself returns a `CompletableFuture` (like `flatMap`)."),
                ("What does `join()` throw on failure vs `get()`?", "`join()` throws unchecked `CompletionException`; `get()` throws checked `ExecutionException`; both wrap the original cause."),
                ("Why pass your own executor to `supplyAsync` for I/O?", "The default is the shared common pool sized for CPU work; blocking calls would starve unrelated parallel streams and async tasks."),
                ("How do you wait for several futures and keep their results?", "`allOf(...)` then collect each future's `join()` in a `thenApply`."),
            ],
        ),
        sec(
            "Atomics, locks, and concurrent collections",
            "**Atomics** (`AtomicInteger`, `AtomicLong`, `AtomicReference`, `AtomicBoolean`) provide lock-free thread-safe updates via **compare-and-set (CAS)**: `incrementAndGet`, `getAndSet`, `updateAndGet(fn)`, `accumulateAndGet(x, fn)`, or an explicit loop `do { cur = get(); next = f(cur); } while (!compareAndSet(cur, next));`. `LongAdder`/`LongAccumulator` stripe the counter across cells to reduce contention under heavy writes (sum is computed on read). **Locks** (`java.util.concurrent.locks`): `ReentrantLock` (`lock/unlock` in `try/finally`, `tryLock(timeout)`, `lockInterruptibly`, fairness, multiple `Condition`s) and `ReentrantReadWriteLock` (many readers or one writer). **Concurrent collections**: `ConcurrentHashMap` (atomic `putIfAbsent/compute/merge`, no null keys/values, weakly consistent iterators), `CopyOnWriteArrayList/Set` (snapshot iteration, writes copy the array), `ConcurrentLinkedQueue`, and `BlockingQueue` implementations (`ArrayBlockingQueue`, `LinkedBlockingQueue`, `PriorityBlockingQueue`) for producer/consumer.",
            "Simple counters and flags do not need a lock - atomics are faster and cannot deadlock. Compound invariants need locks. `Collections.synchronizedMap` serializes all access and still requires external locking for compound operations and iteration; `ConcurrentHashMap` scales with fine-grained locking/CAS and offers atomic compound operations. These are the building blocks of caches, metrics, rate limiters, and work queues.",
            ["Atomics: lock-free, no deadlock, simple", "`LongAdder` scales for write-heavy counters", "`tryLock` and interruptible locking avoid hangs; read/write locks boost read-mostly workloads", "`ConcurrentHashMap` offers atomic compound operations and high concurrency"],
            ["Atomics only protect a **single variable**; multi-field invariants still need a lock", "CAS loops can spin under high contention (use `LongAdder` or a lock)", "Forgetting `unlock()` in `finally` leaks the lock; `ReadWriteLock` can starve writers or be slower for short critical sections", "Concurrent iterators are weakly consistent (may or may not reflect concurrent updates)"],
            "`if (!map.containsKey(k)) map.put(k, v)` on a `ConcurrentHashMap` is still a **check-then-act race** (use `putIfAbsent`/`computeIfAbsent`). Two separate atomic updates (`balance.addAndGet(-x); other.addAndGet(x)`) are not atomic *together*. Using `AtomicInteger` for a value that must stay within `[0, max]` needs a CAS loop (an unconditional `incrementAndGet` overshoots). Forgetting `lock.unlock()` in `finally` leaves the lock held forever after an exception. Mutating the value objects stored in a `ConcurrentHashMap` (e.g. `ArrayList`) is still unsafe. Using `CopyOnWriteArrayList` for write-heavy workloads copies the whole array on every write. `ConcurrentHashMap.size()` is only an estimate under concurrent updates.",
            """- Atomic counter: `AtomicLong hits = new AtomicLong(); hits.incrementAndGet(); hits.getAndSet(0);`.
- CAS loop: `int cur; do { cur = max.get(); if (v <= cur) return; } while (!max.compareAndSet(cur, v));` or `max.accumulateAndGet(v, Math::max)`.
- Lock idiom: `lock.lock(); try { ... } finally { lock.unlock(); }`; `if (lock.tryLock(50, MILLISECONDS)) { try { ... } finally { lock.unlock(); } }`.
- Read/write: `rw.readLock().lock()` for lookups, `rw.writeLock().lock()` for updates (always unlock in `finally`).
- Frequency map: `ConcurrentHashMap<String, LongAdder> m; m.computeIfAbsent(w, k -> new LongAdder()).increment();` or `m.merge(w, 1L, Long::sum)`.
- Prefer `BlockingQueue.put/take` over hand-written wait/notify for producer/consumer.""",
            [
                ("Tiny — atomic counter and CAS-based maximum", """AtomicLong hits = new AtomicLong();
hits.incrementAndGet();
System.out.println(hits.getAndSet(0));       // 1  (and resets)

AtomicInteger max = new AtomicInteger(Integer.MIN_VALUE);
for (int v : new int[] {3, 9, 4}) max.accumulateAndGet(v, Math::max);
System.out.println(max.get());               // 9"""),
                ("Tiny — ConcurrentHashMap atomic compound operations", """ConcurrentHashMap<String, Long> counts = new ConcurrentHashMap<>();
for (String w : List.of("a", "b", "a")) counts.merge(w, 1L, Long::sum);
System.out.println(new TreeMap<>(counts));    // {a=2, b=1}
counts.putIfAbsent("c", 0L);                  // atomic, unlike containsKey + put"""),
                ("Medium — read-mostly registry with ReadWriteLock", """import java.util.*;
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
}"""),
            ],
            [
                ("Why is `LongAdder` preferred over `AtomicLong` for hot counters?", "It spreads updates across cells to reduce CAS contention; `sum()` aggregates on read."),
                ("Why is `containsKey` then `put` unsafe on a `ConcurrentHashMap`?", "Another thread can insert between the two calls (check-then-act race); use `putIfAbsent`, `computeIfAbsent`, or `merge`."),
                ("Why must `unlock()` be in a `finally` block?", "Otherwise an exception between `lock()` and `unlock()` leaves the lock held forever."),
                ("When is `CopyOnWriteArrayList` a good fit?", "Read-mostly, small lists with rare writes (listeners, config), where iterators need snapshot semantics."),
            ],
        ),
    ],
    interview=[
        ("How do you choose a thread pool size?", "CPU-bound: about the number of cores (+1). I/O-bound: cores x (1 + wait time / compute time), or measure; consider virtual threads for blocking I/O. Bound the queue to apply back-pressure."),
        ("What are the dangers of `Executors.newFixedThreadPool` and `newCachedThreadPool`?", "Fixed uses an unbounded queue (memory growth); cached has unbounded thread creation. Prefer an explicit `ThreadPoolExecutor` with a bounded queue and rejection policy."),
        ("Callable vs Runnable vs Supplier?", "`Callable` returns a value and may throw checked exceptions (used with `ExecutorService`); `Runnable` returns nothing; `Supplier` returns a value but cannot throw checked exceptions (used with `CompletableFuture.supplyAsync`)."),
        ("How does CAS work and what is the ABA problem?", "Compare-and-set atomically updates a value only if it still equals the expected one; ABA is when a value changes A->B->A so CAS cannot see the intermediate change (`AtomicStampedReference` adds a version)."),
        ("ConcurrentHashMap vs Collections.synchronizedMap vs Hashtable?", "CHM uses fine-grained locking/CAS with atomic compound operations and weakly consistent iterators; the others use one lock for every operation and still need external locking for compound actions and iteration."),
        ("What happens to exceptions in CompletableFuture stages?", "They complete the stage exceptionally and propagate to dependents wrapped in `CompletionException`; handle with `exceptionally`/`handle`, otherwise they are silent until `join/get`."),
    ],
    mistakes=[
        "Forgetting to `shutdown()` the pool (JVM never exits) or leaking pools per request.",
        "Ignoring `Future`s or `CompletableFuture`s so failures are never noticed.",
        "Blocking calls (`get()`/`join()`) inside tasks of the same bounded pool (deadlock).",
        "Running blocking I/O on the common ForkJoinPool via `supplyAsync` without a custom executor.",
        "Check-then-act on concurrent collections; two atomic variables treated as one invariant.",
        "`lock()` without `try/finally unlock()`.",
    ],
    reading=[
        "Javadoc: `java.util.concurrent` package summary, `ExecutorService`, `ThreadPoolExecutor`, `CompletableFuture`, `ConcurrentHashMap`, `LongAdder`",
        "*Java Concurrency in Practice* (Goetz) ch. 5-8 (building blocks, task execution, pool sizing)",
        "Oracle Java Tutorials - *Concurrency: High Level Concurrency Objects*",
        "JEP 444 (virtual threads) for the alternative to large I/O thread pools (see Day 22)",
    ],
    glossary=[
        ("Executor", "Abstraction that runs submitted tasks"),
        ("Future", "Handle to the result of an asynchronous computation"),
        ("CompletableFuture", "Composable, manually completable future"),
        ("CAS", "Compare-and-set: atomic conditional update (hardware-supported)"),
        ("Back-pressure", "Slowing producers when consumers/queues are saturated"),
        ("Thread starvation deadlock", "All pool threads blocked on tasks that cannot start"),
        ("Weakly consistent iterator", "Iterator that tolerates concurrent modification without throwing"),
        ("Common pool", "`ForkJoinPool.commonPool()` default for async stages and parallel streams"),
    ],
    tasks=[
        task(
            "executor-sum", "Executor Chunked Sum", "Warm-up", "ExecutorSum",
            "Use an `ExecutorService` to sum a list in parallel chunks with `Callable`/`Future`, run a batch with `invokeAll` preserving order, and implement a correct graceful shutdown (shutdown, await, then `shutdownNow`).",
            [
                "`parallelSum(numbers, chunks, pool)` splits the list into at most `chunks` consecutive slices, sums each in the pool, and returns the total as a `long`; `chunks <= 0` -> `IllegalArgumentException`; empty list -> 0",
                "`runAll(pool, tasks)` runs all callables with `invokeAll` and returns their results **in input order**; if a task failed, the `ExecutionException` (with its cause) propagates",
                "`shutdownGracefully(pool, timeoutMillis)` calls `shutdown`, waits up to the timeout, then `shutdownNow`; returns `true` if the pool terminated on its own, `false` if it had to be forced",
            ],
            ["more chunks than elements", "empty list", "a failing task in `runAll`", "pool with a task that never finishes (forced shutdown)"],
            {"ExecutorSum.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

/** ExecutorService practice. */
public final class ExecutorSum {

    private ExecutorSum() {
    }

    public static long parallelSum(List<Integer> numbers, int chunks, ExecutorService pool)
            throws InterruptedException, ExecutionException {
        //@TODO parallelSum | IllegalArgumentException if chunks <= 0; empty list -> 0; split into <= chunks consecutive slices, submit one Callable<Long> per slice, then add up future.get() results
        if (chunks <= 0) {
            throw new IllegalArgumentException("chunks must be > 0");
        }
        int size = numbers.size();
        if (size == 0) {
            return 0L;
        }
        int step = (size + chunks - 1) / chunks;
        List<Future<Long>> parts = new ArrayList<>();
        for (int start = 0; start < size; start += step) {
            List<Integer> slice = numbers.subList(start, Math.min(size, start + step));
            parts.add(pool.submit(() -> {
                long sum = 0;
                for (int value : slice) {
                    sum += value;
                }
                return sum;
            }));
        }
        long total = 0;
        for (Future<Long> part : parts) {
            total += part.get();
        }
        return total;
        //@END
    }

    public static <T> List<T> runAll(ExecutorService pool, List<Callable<T>> tasks)
            throws InterruptedException, ExecutionException {
        //@TODO runAll | pool.invokeAll(tasks) then collect future.get() values in input order; a failed task propagates ExecutionException
        List<Future<T>> futures = pool.invokeAll(tasks);
        List<T> results = new ArrayList<>();
        for (Future<T> future : futures) {
            results.add(future.get());
        }
        return results;
        //@END
    }

    public static boolean shutdownGracefully(ExecutorService pool, long timeoutMillis) {
        //@TODO shutdownGracefully | shutdown(); awaitTermination(timeoutMillis); if not terminated call shutdownNow() (and wait briefly) and return false; restore the interrupt flag if interrupted; return true when it terminated by itself
        pool.shutdown();
        try {
            if (pool.awaitTermination(timeoutMillis, TimeUnit.MILLISECONDS)) {
                return true;
            }
            pool.shutdownNow();
            pool.awaitTermination(timeoutMillis, TimeUnit.MILLISECONDS);
            return false;
        } catch (InterruptedException e) {
            pool.shutdownNow();
            Thread.currentThread().interrupt();
            return false;
        }
        //@END
    }
}
'''},
            {"ExecutorSumTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.stream.IntStream;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(30)
class ExecutorSumTest {

    @Test
    void r1_parallelSumMatchesSequentialSum() throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(4);
        try {
            List<Integer> nums = IntStream.rangeClosed(1, 1_000).boxed().toList();
            assertThat(ExecutorSum.parallelSum(nums, 4, pool)).isEqualTo(500_500L);
            assertThat(ExecutorSum.parallelSum(nums, 7, pool)).isEqualTo(500_500L);
            assertThat(ExecutorSum.parallelSum(nums, 5_000, pool)).isEqualTo(500_500L);
            assertThat(ExecutorSum.parallelSum(List.of(Integer.MAX_VALUE, Integer.MAX_VALUE), 2, pool)).isEqualTo(4_294_967_294L);
        } finally {
            pool.shutdownNow();
        }
    }

    @Test
    void r1_edgeCases() throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        try {
            assertThat(ExecutorSum.parallelSum(List.of(), 3, pool)).isZero();
            assertThat(ExecutorSum.parallelSum(List.of(42), 1, pool)).isEqualTo(42L);
            assertThatThrownBy(() -> ExecutorSum.parallelSum(List.of(1), 0, pool)).isInstanceOf(IllegalArgumentException.class);
            assertThatThrownBy(() -> ExecutorSum.parallelSum(List.of(1), -2, pool)).isInstanceOf(IllegalArgumentException.class);
        } finally {
            pool.shutdownNow();
        }
    }

    @Test
    void r1_usesThePoolThreads() throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(2, r -> {
            Thread t = new Thread(r, "sum-pool-thread");
            t.setDaemon(true);
            return t;
        });
        try {
            java.util.concurrent.atomic.AtomicBoolean sawPoolThread = new java.util.concurrent.atomic.AtomicBoolean();
            List<Callable<Integer>> probe = List.of(() -> {
                sawPoolThread.set(Thread.currentThread().getName().equals("sum-pool-thread"));
                return 1;
            });
            assertThat(ExecutorSum.runAll(pool, probe)).containsExactly(1);
            assertThat(sawPoolThread).isTrue();
        } finally {
            pool.shutdownNow();
        }
    }

    @Test
    void r2_runAllKeepsInputOrder() throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(3);
        try {
            List<Callable<String>> tasks = new ArrayList<>();
            for (int i = 0; i < 6; i++) {
                int n = i;
                tasks.add(() -> "task-" + n);
            }
            assertThat(ExecutorSum.runAll(pool, tasks)).containsExactly("task-0", "task-1", "task-2", "task-3", "task-4", "task-5");
            assertThat(ExecutorSum.runAll(pool, List.<Callable<String>>of())).isEmpty();
        } finally {
            pool.shutdownNow();
        }
    }

    @Test
    void r2_failureKeepsItsCause() {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        try {
            List<Callable<Integer>> tasks = List.of(() -> 1, () -> {
                throw new IllegalStateException("boom");
            });
            assertThatThrownBy(() -> ExecutorSum.runAll(pool, tasks))
                    .isInstanceOf(ExecutionException.class)
                    .hasRootCauseInstanceOf(IllegalStateException.class)
                    .hasRootCauseMessage("boom");
        } finally {
            pool.shutdownNow();
        }
    }

    @Test
    void r3_gracefulShutdownWhenIdle() {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        pool.submit(() -> 1);
        assertThat(ExecutorSum.shutdownGracefully(pool, 2_000)).isTrue();
        assertThat(pool.isShutdown()).isTrue();
        assertThat(pool.isTerminated()).isTrue();
    }

    @Test
    void r3_forcedShutdownWhenATaskNeverFinishes() throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(1);
        CountDownLatch started = new CountDownLatch(1);
        CountDownLatch interrupted = new CountDownLatch(1);
        pool.submit(() -> {
            started.countDown();
            try {
                new CountDownLatch(1).await();
            } catch (InterruptedException e) {
                interrupted.countDown();
            }
        });
        assertThat(started.await(5, TimeUnit.SECONDS)).isTrue();
        assertThat(ExecutorSum.shutdownGracefully(pool, 100)).isFalse();
        assertThat(interrupted.await(5, TimeUnit.SECONDS)).as("shutdownNow interrupted the task").isTrue();
        assertThat(pool.awaitTermination(5, TimeUnit.SECONDS)).isTrue();
    }
}
'''},
            ["Compute the slice size with ceiling division, then loop with `start += step`; the last slice may be shorter.", "`shutdownNow()` interrupts running tasks - your graceful method must return `false` when it had to use it."],
            ["Pool is never created/owned by the helper (caller decides lifecycle) except for shutdown helper", "Futures are consumed (failures are not lost)", "Interrupt flag restored when `InterruptedException` is caught"],
            constraints=["Use only the provided `ExecutorService` - do not create threads or pools inside `parallelSum`/`runAll`", "No `parallelStream`", "Do not edit the tests"],
        ),
        task(
            "future-timeout", "Future Timeouts, Cancellation, and invokeAny", "Core", "FutureTimeout",
            "Wrap `Future` usage in safe helpers: get a result within a deadline (cancelling on timeout), fall back to a default on any failure, take the first successful result of several redundant tasks (`invokeAny`), and cancel a running task while verifying it was interrupted.",
            [
                "`getWithTimeout(future, timeoutMillis)` returns `Optional.of(value)`; on timeout it **cancels** the future (interrupting) and returns empty; a task failure becomes `IllegalStateException` with the original exception as cause",
                "`getOrDefault(future, timeoutMillis, fallback)` returns the value, or `fallback` on timeout or task failure (and cancels on timeout)",
                "`firstSuccessful(pool, tasks)` returns the result of the first task that completes successfully (`invokeAny`); if all fail an `ExecutionException` propagates",
                "`cancelRunning(future)` returns `true` only if the future was actually cancelled (interrupting a running task); completed futures return `false`",
            ],
            ["timeout shorter than the task", "failing task", "all tasks failing in invokeAny", "cancelling an already-finished future"],
            {"FutureTimeout.java": r'''package @PKG@;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/** Future helpers. */
public final class FutureTimeout {

    private FutureTimeout() {
    }

    public static <T> Optional<T> getWithTimeout(Future<T> future, long timeoutMillis) throws InterruptedException {
        //@TODO getWithTimeout | future.get(timeout, MILLISECONDS) -> Optional.ofNullable; on TimeoutException cancel(true) and return empty; on ExecutionException throw IllegalStateException with the cause
        try {
            return Optional.ofNullable(future.get(timeoutMillis, TimeUnit.MILLISECONDS));
        } catch (TimeoutException e) {
            future.cancel(true);
            return Optional.empty();
        } catch (ExecutionException e) {
            throw new IllegalStateException("task failed", e.getCause());
        }
        //@END
    }

    public static <T> T getOrDefault(Future<T> future, long timeoutMillis, T fallback) {
        //@TODO getOrDefault | value within the timeout, otherwise fallback on timeout (cancel the future) or task failure; if the calling thread is interrupted restore its flag and return fallback
        try {
            return future.get(timeoutMillis, TimeUnit.MILLISECONDS);
        } catch (TimeoutException e) {
            future.cancel(true);
            return fallback;
        } catch (ExecutionException e) {
            return fallback;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return fallback;
        }
        //@END
    }

    public static <T> T firstSuccessful(ExecutorService pool, List<Callable<T>> tasks)
            throws InterruptedException, ExecutionException {
        //@TODO firstSuccessful | return pool.invokeAny(tasks): the first successful result; ExecutionException when every task fails
        return pool.invokeAny(tasks);
        //@END
    }

    public static boolean cancelRunning(Future<?> future) {
        //@TODO cancelRunning | cancel(true) and report whether the future is now cancelled (false for futures that already completed)
        return future.cancel(true) && future.isCancelled();
        //@END
    }
}
'''},
            {"FutureTimeoutTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(30)
class FutureTimeoutTest {

    private ExecutorService pool;

    @BeforeEach
    void start() {
        pool = Executors.newFixedThreadPool(4);
    }

    @AfterEach
    void stop() {
        pool.shutdownNow();
    }

    private static void blockForever() throws InterruptedException {
        new CountDownLatch(1).await();
    }

    @Test
    void r1_returnsValueWhenFastEnough() throws Exception {
        Future<String> f = pool.submit(() -> "ready");
        assertThat(FutureTimeout.getWithTimeout(f, 5_000)).contains("ready");
    }

    @Test
    void r1_timeoutCancelsAndReturnsEmpty() throws Exception {
        CountDownLatch interrupted = new CountDownLatch(1);
        Future<String> slow = pool.submit(() -> {
            try {
                blockForever();
            } catch (InterruptedException e) {
                interrupted.countDown();
            }
            return "never";
        });
        assertThat(FutureTimeout.getWithTimeout(slow, 50)).isEmpty();
        assertThat(slow.isCancelled()).isTrue();
        assertThat(interrupted.await(5, TimeUnit.SECONDS)).as("the running task was interrupted").isTrue();
    }

    @Test
    void r1_failureBecomesIllegalStateWithCause() {
        Future<String> bad = pool.submit(() -> {
            throw new java.io.IOException("disk");
        });
        assertThatThrownBy(() -> FutureTimeout.getWithTimeout(bad, 5_000))
                .isInstanceOf(IllegalStateException.class)
                .hasCauseInstanceOf(java.io.IOException.class);
    }

    @Test
    void r2_getOrDefault() {
        Future<Integer> ok = pool.submit(() -> 7);
        assertThat(FutureTimeout.getOrDefault(ok, 5_000, -1)).isEqualTo(7);
        Future<Integer> failing = pool.submit(() -> {
            throw new IllegalStateException("x");
        });
        assertThat(FutureTimeout.getOrDefault(failing, 5_000, -1)).isEqualTo(-1);
        Future<Integer> slow = pool.submit(() -> {
            blockForever();
            return 1;
        });
        assertThat(FutureTimeout.getOrDefault(slow, 50, -2)).isEqualTo(-2);
        assertThat(slow.isCancelled()).isTrue();
    }

    @Test
    void r3_firstSuccessfulIgnoresFailures() throws Exception {
        List<Callable<String>> tasks = List.of(
                () -> {
                    throw new IllegalStateException("replica-1 down");
                },
                () -> "replica-2",
                () -> {
                    throw new IllegalStateException("replica-3 down");
                });
        assertThat(FutureTimeout.firstSuccessful(pool, tasks)).isEqualTo("replica-2");
    }

    @Test
    void r3_allFailingPropagatesExecutionException() {
        List<Callable<String>> tasks = List.of(
                () -> {
                    throw new IllegalStateException("a");
                },
                () -> {
                    throw new IllegalStateException("b");
                });
        assertThatThrownBy(() -> FutureTimeout.firstSuccessful(pool, tasks)).isInstanceOf(ExecutionException.class);
    }

    @Test
    void r4_cancelRunningInterruptsTheTask() throws Exception {
        CountDownLatch started = new CountDownLatch(1);
        CountDownLatch interrupted = new CountDownLatch(1);
        Future<?> running = pool.submit(() -> {
            started.countDown();
            try {
                blockForever();
            } catch (InterruptedException e) {
                interrupted.countDown();
            }
        });
        assertThat(started.await(5, TimeUnit.SECONDS)).isTrue();
        assertThat(FutureTimeout.cancelRunning(running)).isTrue();
        assertThat(interrupted.await(5, TimeUnit.SECONDS)).isTrue();
    }

    @Test
    void r4_cancellingACompletedFutureReturnsFalse() throws Exception {
        Future<Integer> done = pool.submit(() -> 1);
        assertThat(done.get(5, TimeUnit.SECONDS)).isEqualTo(1);
        assertThat(FutureTimeout.cancelRunning(done)).isFalse();
    }
}
'''},
            ["`Future.cancel(true)` returns `false` for tasks that already completed - make sure your helper reports exactly that.", "Wrap `ExecutionException#getCause()` to preserve the original failure for callers."],
            ["Timeouts cancel the work (no leaked running tasks)", "Interrupt flag restored in `getOrDefault`", "Original exception preserved as cause"],
            constraints=["Do not create threads or executors in the helpers (use the given future/pool)", "Do not use `Thread.sleep`", "Do not edit the tests"],
        ),
        task(
            "completable-pipeline", "CompletableFuture Pipeline", "Stretch", "CompletablePipeline",
            "Compose asynchronous work with `CompletableFuture`: a transform pipeline, combining two results, collecting a list of futures in order, a fallback on failure, dependent calls with `thenCompose`, a default-on-timeout, and a `describe` function that unwraps `CompletionException`.",
            [
                "`pipeline(source, executor)` runs `source` asynchronously on `executor`, trims the text, then upper-cases it",
                "`combine(a, b)` completes with the sum of both results (`thenCombine`)",
                "`allInOrder(futures)` completes with the list of all results in the **input order** (`allOf` + `join`)",
                "`withFallback(risky, executor, fallback)` runs `risky` asynchronously and completes with `fallback` if it throws",
                "`chain(id, lookupUser, lookupEmail)` runs `lookupUser(id)` then `lookupEmail(user)` using `thenCompose`",
                "`withTimeout(future, millis, defaultValue)` completes with `defaultValue` when the future is not done in time (`completeOnTimeout`)",
                "`describe(future)` returns `\"ok:<value>\"` or `\"error:<root exception simple name>\"`, unwrapping a `CompletionException`",
            ],
            ["failure in the middle of a chain", "future that never completes", "empty list in `allInOrder`", "wrapped vs direct exceptions in `describe`"],
            {"CompletablePipeline.java": r'''package @PKG@;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.Executor;
import java.util.concurrent.TimeUnit;
import java.util.function.Function;
import java.util.function.Supplier;

/** CompletableFuture composition. */
public final class CompletablePipeline {

    private CompletablePipeline() {
    }

    public static CompletableFuture<String> pipeline(Supplier<String> source, Executor executor) {
        //@TODO pipeline | supplyAsync(source, executor) then thenApply(trim) then thenApply(toUpperCase)
        return CompletableFuture.supplyAsync(source, executor)
                .thenApply(String::trim)
                .thenApply(String::toUpperCase);
        //@END
    }

    public static CompletableFuture<Integer> combine(CompletableFuture<Integer> a, CompletableFuture<Integer> b) {
        //@TODO combine | a.thenCombine(b, Integer::sum)
        return a.thenCombine(b, Integer::sum);
        //@END
    }

    public static CompletableFuture<List<Integer>> allInOrder(List<CompletableFuture<Integer>> futures) {
        //@TODO allInOrder | CompletableFuture.allOf(...) then collect each future's join() preserving the input order (empty list gives an already completed empty result)
        return CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
                .thenApply(ignored -> futures.stream().map(CompletableFuture::join).toList());
        //@END
    }

    public static CompletableFuture<Integer> withFallback(Supplier<Integer> risky, Executor executor, int fallback) {
        //@TODO withFallback | supplyAsync(risky, executor).exceptionally(ex -> fallback)
        return CompletableFuture.supplyAsync(risky, executor).exceptionally(ex -> fallback);
        //@END
    }

    public static CompletableFuture<String> chain(String id,
                                                  Function<String, CompletableFuture<String>> lookupUser,
                                                  Function<String, CompletableFuture<String>> lookupEmail) {
        //@TODO chain | lookupUser.apply(id) then thenCompose(lookupEmail) - NOT thenApply (that would nest futures)
        return lookupUser.apply(id).thenCompose(lookupEmail);
        //@END
    }

    public static CompletableFuture<Integer> withTimeout(CompletableFuture<Integer> future, long millis, int defaultValue) {
        //@TODO withTimeout | future.completeOnTimeout(defaultValue, millis, MILLISECONDS)
        return future.completeOnTimeout(defaultValue, millis, TimeUnit.MILLISECONDS);
        //@END
    }

    public static CompletableFuture<String> describe(CompletableFuture<Integer> future) {
        //@TODO describe | handle((value, ex) -> ...): "ok:<value>" or "error:<SimpleName of the root exception>" unwrapping CompletionException
        return future.handle((value, error) -> {
            if (error == null) {
                return "ok:" + value;
            }
            Throwable root = error instanceof CompletionException && error.getCause() != null ? error.getCause() : error;
            return "error:" + root.getClass().getSimpleName();
        });
        //@END
    }
}
'''},
            {"CompletablePipelineTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(20)
class CompletablePipelineTest {

    /** Runs tasks on the calling thread so the tests are deterministic. */
    private static final Executor DIRECT = Runnable::run;

    @Test
    void r1_pipelineTransformsText() throws Exception {
        assertThat(CompletablePipeline.pipeline(() -> "  hello ", DIRECT).get(5, TimeUnit.SECONDS)).isEqualTo("HELLO");
    }

    @Test
    void r1_pipelinePropagatesSourceFailure() {
        CompletableFuture<String> f = CompletablePipeline.pipeline(() -> {
            throw new IllegalStateException("source down");
        }, DIRECT);
        assertThat(f.isCompletedExceptionally()).isTrue();
    }

    @Test
    void r2_combineSums() {
        CompletableFuture<Integer> a = CompletableFuture.completedFuture(20);
        CompletableFuture<Integer> b = CompletableFuture.supplyAsync(() -> 22);
        assertThat(CompletablePipeline.combine(a, b).join()).isEqualTo(42);
    }

    @Test
    void r2_combineWaitsForBoth() {
        CompletableFuture<Integer> a = new CompletableFuture<>();
        CompletableFuture<Integer> b = CompletableFuture.completedFuture(1);
        CompletableFuture<Integer> sum = CompletablePipeline.combine(a, b);
        assertThat(sum.isDone()).isFalse();
        a.complete(9);
        assertThat(sum.join()).isEqualTo(10);
    }

    @Test
    void r3_allInOrderKeepsInputOrder() {
        CompletableFuture<Integer> first = new CompletableFuture<>();
        CompletableFuture<Integer> second = CompletableFuture.completedFuture(2);
        CompletableFuture<Integer> third = CompletableFuture.completedFuture(3);
        CompletableFuture<List<Integer>> all = CompletablePipeline.allInOrder(List.of(first, second, third));
        assertThat(all.isDone()).isFalse();
        first.complete(1);
        assertThat(all.join()).containsExactly(1, 2, 3);
    }

    @Test
    void r3_allInOrderEmpty() {
        assertThat(CompletablePipeline.allInOrder(List.of()).join()).isEmpty();
    }

    @Test
    void r4_fallbackOnFailureAndNoFallbackOnSuccess() {
        assertThat(CompletablePipeline.withFallback(() -> 5, DIRECT, -1).join()).isEqualTo(5);
        assertThat(CompletablePipeline.withFallback(() -> {
            throw new IllegalStateException("x");
        }, DIRECT, -1).join()).isEqualTo(-1);
    }

    @Test
    void r5_chainComposesDependentCalls() {
        CompletableFuture<String> email = CompletablePipeline.chain("42",
                id -> CompletableFuture.completedFuture("user-" + id),
                user -> CompletableFuture.completedFuture(user + "@example.org"));
        assertThat(email.join()).isEqualTo("user-42@example.org");
    }

    @Test
    void r5_chainFailsWhenFirstLookupFails() {
        CompletableFuture<String> email = CompletablePipeline.chain("x",
                id -> CompletableFuture.failedFuture(new IllegalArgumentException("no such user")),
                user -> CompletableFuture.completedFuture(user + "@example.org"));
        assertThat(email.isCompletedExceptionally()).isTrue();
    }

    @Test
    void r6_timeoutUsesTheDefault() {
        CompletableFuture<Integer> never = new CompletableFuture<>();
        assertThat(CompletablePipeline.withTimeout(never, 50, -1).join()).isEqualTo(-1);
        CompletableFuture<Integer> quick = CompletableFuture.completedFuture(8);
        assertThat(CompletablePipeline.withTimeout(quick, 50, -1).join()).isEqualTo(8);
    }

    @Test
    void r7_describeUnwrapsCompletionException() {
        assertThat(CompletablePipeline.describe(CompletableFuture.completedFuture(5)).join()).isEqualTo("ok:5");
        CompletableFuture<Integer> direct = CompletableFuture.failedFuture(new IllegalStateException("x"));
        assertThat(CompletablePipeline.describe(direct).join()).isEqualTo("error:IllegalStateException");
        CompletableFuture<Integer> derived = CompletableFuture.<Integer>supplyAsync(() -> {
            throw new IllegalArgumentException("y");
        }, DIRECT).thenApply(v -> v + 1);
        assertThat(CompletablePipeline.describe(derived).join()).isEqualTo("error:IllegalArgumentException");
    }
}
'''},
            ["`allOf` returns `CompletableFuture<Void>`: gather results in a `thenApply` after it completes (calling `join()` there never blocks).", "A failed derived stage hands `handle` a `CompletionException`; a directly failed future does not."],
            ["No blocking `join()`/`get()` before the pipeline is composed (except inside already-completed stages)", "Correct operator choice: `thenCompose` vs `thenApply`", "Error handling unwraps `CompletionException`"],
            constraints=["Return `CompletableFuture`s - do not block the calling thread in any method", "Do not edit the tests"],
        ),
        task(
            "atomic-counter", "Atomics, Locks, and Concurrent Maps", "Challenge", "AtomicToolkit",
            "Build four small thread-safe components, each using the right tool: a hit counter with `AtomicLong`, a running maximum with a CAS loop, a word counter with `ConcurrentHashMap` + `LongAdder`, and a read-mostly registry guarded by a `ReentrantReadWriteLock`. The tests hammer each from many threads.",
            [
                "`HitCounter`: `hit()` increments atomically, `count()` returns the total, `reset()` returns the previous count and sets it to 0 atomically (`getAndSet`)",
                "`MaxTracker`: `offer(value)` keeps the maximum seen using a **compare-and-set loop**; `get()` returns the maximum (`Integer.MIN_VALUE` before any offer)",
                "`WordCounter`: `add(word)` increments atomically using `ConcurrentHashMap.computeIfAbsent` + `LongAdder`; `count(word)` returns 0 for unknown words; `snapshot()` returns an independent `Map<String, Long>`",
                "`Registry`: `put`, `get`, `size` are protected by a `ReentrantReadWriteLock` (readers share the read lock; writers use the write lock); always unlock in `finally`",
                "All components give exact results under 8 threads x 20_000 operations",
            ],
            ["no updates yet", "unknown words", "concurrent offers with decreasing values", "readers and writers at the same time"],
            {"AtomicToolkit.java": r'''package @PKG@;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.LongAdder;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/** Small thread-safe building blocks. */
public final class AtomicToolkit {

    private AtomicToolkit() {
    }

    /** Counts hits using an AtomicLong. */
    public static final class HitCounter {
        private final AtomicLong hits = new AtomicLong();

        public void hit() {
            //@TODO hit | atomically increment the counter (incrementAndGet / getAndIncrement)
            hits.incrementAndGet();
            //@END
        }

        public long count() {
            //@TODO count | return the current number of hits
            return hits.get();
            //@END
        }

        public long reset() {
            //@TODO reset | atomically set the counter to 0 and return the previous value (getAndSet)
            return hits.getAndSet(0);
            //@END
        }
    }

    /** Tracks the maximum value using a compare-and-set loop. */
    public static final class MaxTracker {
        private final AtomicInteger max = new AtomicInteger(Integer.MIN_VALUE);

        public void offer(int value) {
            //@TODO offer | CAS loop: read current, return if value <= current, else compareAndSet(current, value) and retry on failure
            int current;
            do {
                current = max.get();
                if (value <= current) {
                    return;
                }
            } while (!max.compareAndSet(current, value));
            //@END
        }

        public int get() {
            //@TODO get | return the maximum seen so far (Integer.MIN_VALUE when nothing was offered)
            return max.get();
            //@END
        }
    }

    /** Counts words from many threads using ConcurrentHashMap + LongAdder. */
    public static final class WordCounter {
        private final ConcurrentHashMap<String, LongAdder> counts = new ConcurrentHashMap<>();

        public void add(String word) {
            //@TODO add | counts.computeIfAbsent(word, k -> new LongAdder()).increment() - no containsKey/put race
            counts.computeIfAbsent(word, key -> new LongAdder()).increment();
            //@END
        }

        public long count(String word) {
            //@TODO count | the adder's sum for the word, or 0 when the word is unknown
            LongAdder adder = counts.get(word);
            return adder == null ? 0L : adder.sum();
            //@END
        }

        public Map<String, Long> snapshot() {
            //@TODO snapshot | return a NEW HashMap word -> sum() (a point-in-time copy, not a view)
            Map<String, Long> copy = new HashMap<>();
            counts.forEach((word, adder) -> copy.put(word, adder.sum()));
            return copy;
            //@END
        }
    }

    /** Read-mostly string registry guarded by a read/write lock. */
    public static final class Registry {
        private final Map<String, String> map = new HashMap<>();
        private final ReentrantReadWriteLock lock = new ReentrantReadWriteLock();

        public void put(String key, String value) {
            //@TODO put | take the WRITE lock, put into the map, release in finally
            lock.writeLock().lock();
            try {
                map.put(key, value);
            } finally {
                lock.writeLock().unlock();
            }
            //@END
        }

        public String get(String key) {
            //@TODO get | take the READ lock, read, release in finally
            lock.readLock().lock();
            try {
                return map.get(key);
            } finally {
                lock.readLock().unlock();
            }
            //@END
        }

        public int size() {
            //@TODO size | take the READ lock, return map.size(), release in finally
            lock.readLock().lock();
            try {
                return map.size();
            } finally {
                lock.readLock().unlock();
            }
            //@END
        }
    }
}
'''},
            {"AtomicToolkitTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(60)
class AtomicToolkitTest {

    private static final int THREADS = 8;
    private static final int OPS = 20_000;

    /** Runs the task body on THREADS threads that all start at the same moment; the body receives its thread index. */
    private static void inParallel(java.util.function.IntConsumer body) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(THREADS);
        try {
            CountDownLatch go = new CountDownLatch(1);
            List<Future<?>> futures = new ArrayList<>();
            for (int i = 0; i < THREADS; i++) {
                int index = i;
                futures.add(pool.submit(() -> {
                    go.await();
                    body.accept(index);
                    return null;
                }));
            }
            go.countDown();
            for (Future<?> f : futures) {
                f.get(30, TimeUnit.SECONDS);
            }
        } finally {
            pool.shutdownNow();
        }
    }

    @Test
    void r1_hitCounterIsExactAndResetReturnsPrevious() throws Exception {
        AtomicToolkit.HitCounter counter = new AtomicToolkit.HitCounter();
        assertThat(counter.count()).isZero();
        inParallel(i -> {
            for (int k = 0; k < OPS; k++) {
                counter.hit();
            }
        });
        assertThat(counter.count()).isEqualTo((long) THREADS * OPS);
        assertThat(counter.reset()).isEqualTo((long) THREADS * OPS);
        assertThat(counter.count()).isZero();
        assertThat(counter.reset()).isZero();
    }

    @Test
    void r2_maxTrackerStartsAtMinValue() {
        AtomicToolkit.MaxTracker tracker = new AtomicToolkit.MaxTracker();
        assertThat(tracker.get()).isEqualTo(Integer.MIN_VALUE);
        tracker.offer(-5);
        assertThat(tracker.get()).isEqualTo(-5);
        tracker.offer(-9);
        assertThat(tracker.get()).isEqualTo(-5);
        tracker.offer(12);
        assertThat(tracker.get()).isEqualTo(12);
    }

    @Test
    void r2_maxTrackerUnderContention() throws Exception {
        AtomicToolkit.MaxTracker tracker = new AtomicToolkit.MaxTracker();
        inParallel(i -> {
            for (int k = 0; k < OPS; k++) {
                tracker.offer(i * OPS + k);
            }
        });
        assertThat(tracker.get()).isEqualTo(THREADS * OPS - 1);
    }

    @Test
    void r3_wordCounterBasics() {
        AtomicToolkit.WordCounter counter = new AtomicToolkit.WordCounter();
        counter.add("a");
        counter.add("b");
        counter.add("a");
        assertThat(counter.count("a")).isEqualTo(2L);
        assertThat(counter.count("b")).isEqualTo(1L);
        assertThat(counter.count("zzz")).isZero();
        var snap = counter.snapshot();
        assertThat(snap).containsOnlyKeys("a", "b").containsEntry("a", 2L);
        counter.add("a");
        assertThat(snap).containsEntry("a", 2L);
    }

    @Test
    void r3_wordCounterUnderContention() throws Exception {
        AtomicToolkit.WordCounter counter = new AtomicToolkit.WordCounter();
        inParallel(i -> {
            for (int k = 0; k < OPS; k++) {
                counter.add(k % 2 == 0 ? "even" : "odd");
                counter.add("shared");
            }
        });
        assertThat(counter.count("even")).isEqualTo((long) THREADS * OPS / 2);
        assertThat(counter.count("odd")).isEqualTo((long) THREADS * OPS / 2);
        assertThat(counter.count("shared")).isEqualTo((long) THREADS * OPS);
    }

    @Test
    void r4_registryBasics() {
        AtomicToolkit.Registry registry = new AtomicToolkit.Registry();
        assertThat(registry.size()).isZero();
        assertThat(registry.get("k")).isNull();
        registry.put("k", "v");
        registry.put("k2", "v2");
        registry.put("k", "v3");
        assertThat(registry.get("k")).isEqualTo("v3");
        assertThat(registry.size()).isEqualTo(2);
    }

    @Test
    void r5_registryWithConcurrentReadersAndWriters() throws Exception {
        AtomicToolkit.Registry registry = new AtomicToolkit.Registry();
        AtomicInteger readHits = new AtomicInteger();
        inParallel(i -> {
            for (int k = 0; k < 2_000; k++) {
                if (i % 2 == 0) {
                    registry.put("key-" + i + "-" + k, "v");
                } else if (registry.get("key-0-0") != null || registry.size() >= 0) {
                    readHits.incrementAndGet();
                }
            }
        });
        assertThat(registry.size()).isEqualTo((THREADS / 2) * 2_000);
        assertThat(readHits.get()).isEqualTo((THREADS / 2) * 2_000);
        assertThat(registry.get("key-2-1999")).isEqualTo("v");
    }
}
'''},
            ["Use `AtomicInteger.compareAndSet(expected, update)` inside a `do/while`; if it fails, another thread won - re-read and retry.", "`LongAdder.sum()` is a snapshot: that is exactly what `snapshot()` should expose."],
            ["No `synchronized` in `HitCounter`/`MaxTracker`/`WordCounter`", "Every `lock()` is paired with `unlock()` in `finally`", "No check-then-act on the concurrent map"],
            constraints=["`HitCounter`, `MaxTracker` and `WordCounter` must be lock-free (atomics/concurrent collections only)", "Do not edit the tests"],
        ),
    ],
)
