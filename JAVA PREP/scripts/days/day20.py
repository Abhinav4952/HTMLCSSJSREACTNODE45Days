from gen_helpers import sec, task

DAY = dict(
    num=20,
    title="Threads I: Thread, Runnable, synchronized, volatile, wait/notify, and Deadlock",
    theme="Create threads, protect shared state with `synchronized`/`volatile`, coordinate with `wait`/`notify`, and recognize deadlock.",
    objectives=[
        "Create and start threads with `Thread` and `Runnable`; explain `start()` vs `run()`, `join()`, daemon threads and thread states",
        "Explain race conditions, atomicity, visibility, and ordering using the Java Memory Model (happens-before)",
        "Protect invariants with `synchronized` (methods/blocks, intrinsic locks, reentrancy)",
        "Use `volatile` correctly (visibility, no atomicity) and know when it is not enough",
        "Implement a producer/consumer buffer with `wait()`/`notifyAll()` guarded by a `while` loop",
        "Identify the four deadlock conditions and prevent deadlock with a global lock ordering",
    ],
    prereqs=["Day 16 — lambdas (`Runnable` as a lambda)", "Day 11 — exceptions (`InterruptedException`)", "Day 14 — collections (not thread-safe by default)"],
    overview="""Every server is concurrent: each request runs on a thread, and those threads share caches, counters, connection pools, and configuration. Concurrency bugs are the hardest to reproduce - they depend on timing - so the discipline is to **reason**, not to test-and-hope. Today you learn the foundations that `ExecutorService` and `java.util.concurrent` (Day 21) are built on.

The key ideas: a *race condition* happens when correctness depends on timing; `count++` is **not atomic**; the JVM may cache values per thread unless you create a *happens-before* edge (`synchronized`, `volatile`, `Thread.start/join`); `wait/notify` implement guarded waiting; and two threads taking two locks in opposite order can **deadlock**. Interviews ask all of these, usually with a code sample to critique.""",
    sections=[
        sec(
            "Threads, Runnable, and the thread lifecycle",
            "A **thread** is an independent path of execution inside the JVM that shares the heap with other threads but has its own stack. You supply the work as a `Runnable` (`() -> ...`) and start it with `new Thread(runnable, \"name\").start()`. **`start()` creates a new OS-level thread that then calls `run()`; calling `run()` directly just executes the code on the *current* thread** (a very common bug). States (`Thread.State`): `NEW`, `RUNNABLE`, `BLOCKED` (waiting for a monitor), `WAITING` (`wait()`, `join()`, `park`), `TIMED_WAITING` (`sleep`, timed waits), `TERMINATED`. `join()` waits for a thread to finish **and creates a happens-before edge**. `interrupt()` sets an interrupt flag / wakes blocking calls with `InterruptedException`; cooperative cancellation is the only safe way to stop a thread (`Thread.stop` is removed). Daemon threads do not keep the JVM alive.",
            "Threads let one process serve many requests, overlap I/O waits, and use multiple cores. Understanding `start/run/join/interrupt` and thread states is required to read thread dumps (`jstack`, `jcmd Thread.print`, Day 22) and to know why a service is hung. In production you rarely create raw threads (use executors, Day 21), but every abstraction is built on these primitives.",
            ["Parallelism on multi-core hardware", "Overlap blocking I/O with computation", "Simple mental model: `Runnable` is the unit of work", "Thread names and states make dumps readable"],
            ["Shared mutable state needs careful synchronization", "Threads are expensive (~1 MB stack each) and non-trivial to cancel", "Exceptions in a thread do not propagate to the creator (use an `UncaughtExceptionHandler` or `Future`)"],
            "Calling `thread.run()` instead of `start()` silently runs the task on the caller's thread (no concurrency). Calling `start()` twice throws `IllegalThreadStateException`. Swallowing `InterruptedException` (`catch (InterruptedException e) {}`) loses the cancellation signal - restore it with `Thread.currentThread().interrupt()`. A non-daemon thread stuck in a loop prevents JVM shutdown. An unhandled exception kills only that thread and prints a stack trace to stderr - the rest of the app continues in a degraded state. Creating a thread per request without bounds exhausts memory (`OutOfMemoryError: unable to create native thread`).",
            """- Create: `Thread t = new Thread(runnable, \"worker-1\"); t.start();` or `Thread.ofPlatform().name(\"w\").start(r)` (Java 21).
- `t.join()` / `t.join(millis)`; `t.isAlive()`; `t.getState()`; `Thread.currentThread()`.
- Interrupt protocol: loop on `!Thread.currentThread().isInterrupted()`; blocking methods throw `InterruptedException` (clearing the flag) - either propagate it or re-set the flag.
- `setDaemon(true)` must be called **before** `start()`.
- `Thread.sleep(ms)` is for demos, not for synchronization - never use it to \"wait for the other thread\".
- Uncaught exceptions: `t.setUncaughtExceptionHandler((th, ex) -> log.error(...))`.""",
            [
                ("Tiny — start() vs run()", """Runnable who = () -> System.out.println(Thread.currentThread().getName());
Thread t = new Thread(who, "worker");
t.run();                  // prints "main"   (no new thread!)
t.start(); t.join();      // prints "worker" (new thread)"""),
                ("Tiny — join gives you the result safely", """int[] box = new int[1];
Thread t = new Thread(() -> box[0] = 6 * 7);
t.start();
t.join();                  // happens-before: the write to box[0] is visible after join
System.out.println(box[0]);   // 42"""),
                ("Medium — cooperative cancellation", """public class Worker implements Runnable {
    private int loops;

    @Override public void run() {
        try {
            while (!Thread.currentThread().isInterrupted()) {
                loops++;
                Thread.sleep(10);               // blocking call: throws if interrupted
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt(); // restore the flag for callers
        }
        System.out.println("stopped after some loops");
    }

    public static void main(String[] args) throws Exception {
        Thread t = new Thread(new Worker(), "worker");
        t.start();
        Thread.sleep(50);
        t.interrupt();                           // ask politely
        t.join(1_000);
        System.out.println(t.getState());        // TERMINATED
    }
}"""),
            ],
            [
                ("What is the difference between `start()` and `run()`?", "`start()` spawns a new thread which invokes `run()`; calling `run()` executes it synchronously in the calling thread."),
                ("What happens if you call `start()` twice on the same Thread?", "`IllegalThreadStateException`; a thread can be started only once."),
                ("Why re-set the interrupt flag after catching `InterruptedException`?", "Catching clears the flag; restoring it lets callers up the stack observe the cancellation request."),
                ("Which state is a thread in while blocked trying to enter a `synchronized` block?", "`BLOCKED` (whereas `Object.wait()` and `join()` give `WAITING`)."),
            ],
        ),
        sec(
            "Races, synchronized, volatile, and the Java Memory Model",
            "A **race condition** occurs when the result depends on thread interleaving. `count++` is three steps (read, add, write), so two threads can both read `5` and both write `6` (a *lost update*). **Atomicity** (indivisible compound actions), **visibility** (one thread's write becomes visible to another), and **ordering** (the compiler/CPU may reorder) are the three problems. The **Java Memory Model** defines *happens-before*: unlock of a monitor happens-before every later lock of the same monitor; a write to a `volatile` field happens-before every later read of it; `Thread.start()` happens-before the first action of the started thread; the last action of a thread happens-before a successful `join()`. `synchronized` (method or block) gives **mutual exclusion + visibility** via the object's intrinsic lock (monitor), which is **reentrant**. `volatile` gives visibility and ordering but **no atomicity** for compound actions.",
            "Without these guarantees correct-looking code fails on real hardware: loops that never see a `stop` flag, counters that lose updates, objects seen half-constructed. Choosing the right tool matters: `volatile` for a simple status flag or safe publication of an immutable object, `synchronized` for check-then-act and multi-field invariants, atomics/locks (Day 21) for finer control.",
            ["`synchronized` is simple, built in, reentrant, and releases the lock on exceptions", "`volatile` is cheap and ideal for flags and publishing immutable snapshots", "A clear happens-before model lets you reason about correctness", "Immutable objects need no synchronization at all"],
            ["Locks serialize work (contention reduces throughput)", "`synchronized` offers no timeout, no fairness control, and no interruptible acquisition", "`volatile` is misused for compound actions (`volatile int n; n++` is still a race)"],
            "A non-volatile `boolean running` read in a `while (running)` loop may be hoisted by the JIT so the loop never ends. `volatile int count; count++` loses updates. Synchronizing on different lock objects for the same data gives no protection (`synchronized(new Object())` is useless). Synchronizing on a *public* object or `String`/boxed values (`synchronized (\"lock\")`, `synchronized (Integer)`) lets unrelated code interfere. **Check-then-act** (`if (!map.containsKey(k)) map.put(k, v)`) is a race even with a thread-safe map. Holding a lock while calling unknown (alien) code risks deadlock. `double-checked locking` without `volatile` can publish a partially constructed object.",
            """- Synchronized method: locks `this` (instance) or the `Class` object (static).
- Synchronized block: `synchronized (lock) { ... }` with a **private final** lock object.
- Reentrancy: a thread already holding a monitor can acquire it again.
- Guard **all** accesses (reads and writes) of shared state with the **same** lock.
- `volatile` guarantees: visibility of writes, no reordering across the volatile access; **not** atomic read-modify-write.
- Safe publication: static initializer, `final` fields, `volatile` field, lock-protected field, or `Thread.start/join` edges.
- Prefer immutability, thread confinement, or `java.util.concurrent` classes over hand-rolled locking.""",
            [
                ("Tiny — the lost update", """class Counter {
    int value;                          // shared, unprotected
    void inc() { value++; }             // read-modify-write: NOT atomic
}
// 4 threads x 100_000 inc() -> usually less than 400_000

class SafeCounter {
    private int value;
    synchronized void inc() { value++; }
    synchronized int get() { return value; }   // reads must be guarded too (visibility)
}"""),
                ("Tiny — volatile stop flag", """class Spinner implements Runnable {
    private volatile boolean running = true;     // without volatile the loop might never see false
    public void stop() { running = false; }
    @Override public void run() { while (running) { /* work */ } }
}"""),
                ("Medium — block-level locking of related fields", """public final class Stats {
    private final Object lock = new Object();   // private final lock object
    private long count;
    private long sum;

    public void record(long value) {
        synchronized (lock) {                    // both fields change together: one invariant
            count++;
            sum += value;
        }
    }

    public double average() {
        synchronized (lock) {                    // consistent snapshot of both fields
            return count == 0 ? 0 : (double) sum / count;
        }
    }
}"""),
            ],
            [
                ("Why is `volatile int n; n++;` not thread-safe?", "`n++` is read, add, write; `volatile` makes each access visible but does not make the three steps atomic."),
                ("Which two locks guard a class's static synchronized method and an instance synchronized method?", "The `Class` object monitor and the instance's monitor respectively - they are different locks."),
                ("What does happens-before guarantee for `join()`?", "Everything the joined thread did is visible to the thread that returns from `join()`."),
                ("Why should a lock object be `private final`?", "So no outside code can synchronize on it (or replace it) and break your locking discipline."),
            ],
        ),
        sec(
            "wait/notify, producer-consumer, and deadlock",
            "`Object.wait()` releases the monitor and parks the thread until another thread calls `notify()`/`notifyAll()` on the **same** object; it must be called while holding that object's monitor (else `IllegalMonitorStateException`). Because of **spurious wakeups** and shared conditions, always wait in a **loop**: `while (!condition) wait();`. `notifyAll` is safer than `notify` unless all waiters are equivalent. A **bounded buffer** (producer-consumer) is the classic use: producers wait when full, consumers wait when empty. **Deadlock** is a cycle of threads each holding a lock another needs. It requires the four **Coffman conditions**: mutual exclusion, hold and wait, no preemption, and circular wait. Break any one - most practically circular wait by acquiring locks in a **global order**.",
            "Guarded waiting is how threads coordinate without burning CPU. Deadlocks, unlike races, are *visible* (the app hangs) but intermittent: they appear under load when interleavings line up. You diagnose them with thread dumps (`jstack`, `jcmd <pid> Thread.print`), which report \"Found one Java-level deadlock\". The prevention rules (lock ordering, avoid nested locks, `tryLock` with timeouts, open calls) are interview staples.",
            ["`wait/notify` allow efficient blocking coordination with no polling", "Bounded buffers provide back-pressure between producers and consumers", "Lock ordering is a simple, effective deadlock prevention", "Deadlocks are detectable in thread dumps"],
            ["Easy to misuse: forgetting the loop, wrong monitor, lost notifications, `notify` waking the wrong thread", "Low-level; `BlockingQueue` and `Condition` are higher-level replacements", "Deadlock is non-deterministic and may only appear in production"],
            "`if (queue.isEmpty()) wait();` (an `if`, not a `while`) lets a spuriously woken or racing consumer proceed on an empty queue and fail with `NoSuchElementException`. Calling `notify()` before the waiter has started waiting loses the signal (the condition state must live in shared variables). Waiting on one object but notifying another means no one wakes. Two transfer methods that lock `from` then `to` deadlock when called as `transfer(a,b)` and `transfer(b,a)` simultaneously. Holding a lock while doing I/O or calling listeners (alien methods) stalls every other thread that needs the lock. `Thread.sleep` inside `synchronized` keeps the monitor held (unlike `wait`).",
            """- Pattern: `synchronized (this) { while (!ready()) wait(); consume(); notifyAll(); }`.
- `wait()` throws `InterruptedException`; do not swallow it.
- `wait(timeoutMillis)` returns on timeout - recheck the condition in the loop anyway.
- Producer: `while (full) wait(); add(); notifyAll();` Consumer: `while (empty) wait(); take(); notifyAll();`.
- Deadlock prevention: global lock ordering (e.g. by account id), lock coarsening, `ReentrantLock.tryLock(timeout)`, avoid calling foreign code while holding a lock.
- Detect: `jstack <pid>` / `jcmd <pid> Thread.print`, `ThreadMXBean.findDeadlockedThreads()`.""",
            [
                ("Tiny — minimal guarded wait", """class Gate {
    private boolean open;
    synchronized void await() throws InterruptedException {
        while (!open) wait();            // loop, never if
    }
    synchronized void open() {
        open = true;
        notifyAll();
    }
}"""),
                ("Tiny — deadlock-prone vs ordered locking", """// DEADLOCK RISK: thread 1: transfer(a, b)   thread 2: transfer(b, a)
void transferBad(Account from, Account to, long amt) {
    synchronized (from) { synchronized (to) { from.debit(amt); to.credit(amt); } }
}
// SAFE: always lock the lower id first
void transferOrdered(Account from, Account to, long amt) {
    Account first = from.id < to.id ? from : to, second = first == from ? to : from;
    synchronized (first) { synchronized (second) { from.debit(amt); to.credit(amt); } }
}"""),
                ("Medium — a bounded buffer", """import java.util.*;

public final class BoundedBuffer<T> {
    private final Queue<T> items = new ArrayDeque<>();
    private final int capacity;

    public BoundedBuffer(int capacity) { this.capacity = capacity; }

    public synchronized void put(T item) throws InterruptedException {
        while (items.size() == capacity) wait();     // full -> wait
        items.add(item);
        notifyAll();                                 // wake consumers
    }

    public synchronized T take() throws InterruptedException {
        while (items.isEmpty()) wait();              // empty -> wait
        T item = items.remove();
        notifyAll();                                 // wake producers
        return item;
    }
}"""),
            ],
            [
                ("Why must `wait()` be called in a `while` loop?", "To recheck the condition after wake-ups: spurious wakeups, multiple waiters, and `notifyAll` mean the condition may no longer hold."),
                ("Name the four conditions required for deadlock and the one you usually break.", "Mutual exclusion, hold and wait, no preemption, circular wait; you usually break circular wait with a global lock order."),
                ("What is the difference between `sleep` and `wait` regarding locks?", "`sleep` keeps held monitors; `wait` releases the monitor it is called on while waiting."),
                ("How do you find a deadlock in a running JVM?", "Take a thread dump (`jstack <pid>` or `jcmd <pid> Thread.print`) which prints \"Found one Java-level deadlock\"; or use `ThreadMXBean.findDeadlockedThreads()`."),
            ],
        ),
    ],
    interview=[
        ("What is a race condition? Give an example.", "Correctness depends on timing. `count++` from two threads can lose an update because it is read-modify-write, not atomic."),
        ("synchronized vs volatile?", "`synchronized` gives mutual exclusion and visibility for blocks of code; `volatile` gives visibility/ordering for a single variable but no atomic compound operations."),
        ("What is a deadlock and how do you prevent it?", "A circular wait among threads holding locks. Prevent with consistent lock ordering, timeouts (`tryLock`), fewer nested locks, and not calling alien code under locks."),
        ("wait/notify vs sleep/interrupt?", "`wait/notify` coordinate via an object's monitor and release it while waiting; `sleep` just pauses (monitors stay held); `interrupt` is a cancellation request that wakes blocking calls."),
        ("What does the `Thread.State` BLOCKED mean versus WAITING?", "BLOCKED: waiting to acquire a monitor. WAITING: waiting indefinitely for another thread's action (`wait`, `join`, `park`)."),
        ("Why is double-checked locking broken without volatile?", "Without `volatile` another thread can see a non-null reference to a partially constructed object due to reordering."),
    ],
    mistakes=[
        "`run()` instead of `start()`; or `start()` twice (`IllegalThreadStateException`).",
        "Synchronizing writes but not reads of the same data (visibility bug).",
        "Different lock objects for the same state, or synchronizing on `String`/`Integer`/`this` exposed to outsiders.",
        "`if` instead of `while` around `wait()`; notifying a different object than the one waited on.",
        "Nested locks in inconsistent order (deadlock); sleeping inside synchronized blocks.",
        "Swallowing `InterruptedException`; using `Thread.sleep` as \"synchronization\" in tests.",
    ],
    reading=[
        "JLS ch. 17 (Threads and Locks) - especially 17.4 (Memory Model) and 17.2 (Wait Sets and Notification)",
        "Oracle Java Tutorials - *Concurrency* (Processes and Threads, Synchronization, Liveness)",
        "*Java Concurrency in Practice* (Goetz et al.) ch. 1-3, 10 (avoiding liveness hazards)",
        "Javadoc: `java.lang.Thread`, `Thread.State`, `Object#wait`, `java.lang.management.ThreadMXBean`",
    ],
    glossary=[
        ("Race condition", "Outcome depends on unsynchronized timing of threads"),
        ("Atomic", "Indivisible; appears to happen instantly to other threads"),
        ("Monitor / intrinsic lock", "Per-object lock used by `synchronized`, `wait`, `notify`"),
        ("Happens-before", "JMM ordering guarantee that makes one action's effects visible to another"),
        ("Spurious wakeup", "A waiting thread returns from `wait()` without a notify"),
        ("Deadlock", "Circular wait: each thread holds a lock another needs"),
        ("Livelock / starvation", "Threads active but making no progress / one thread never gets the resource"),
        ("Coffman conditions", "The four necessary conditions for deadlock"),
    ],
    tasks=[
        task(
            "runnable-counter", "Runnable Counter", "Warm-up", "RunnableCounter",
            "Start threads that increment a shared counter and prove the final count is exact by making the counter's methods `synchronized`. Also demonstrate the difference between calling `run()` and `start()` by reporting which thread executed the task.",
            [
                "`Counter.increment()` and `Counter.get()` are thread-safe (`synchronized`)",
                "`incrementTask(counter, times)` returns a `Runnable` that calls `increment()` `times` times",
                "`runConcurrently(counter, threads, perThread)` starts `threads` named threads (`counter-0`, `counter-1`, ...), joins them all, and returns the counter value (`threads <= 0` or `perThread < 0` -> `IllegalArgumentException`)",
                "`startNamed(name, runnable)` returns a **started** thread having that name",
                "`executedByWithRun()` runs a task via `Thread.run()` and returns the name of the thread that executed it (the **calling** thread)",
                "`executedByWithStart(name)` runs a task via `start()`, joins, and returns the executing thread's name (the new thread's name)",
            ],
            ["zero increments", "invalid thread counts", "join all threads before reading the result", "never swallow `InterruptedException` (declare it)"],
            {"Counter.java": r'''package @PKG@;

/** Shared counter; must be safe for concurrent increments. */
public final class Counter {

    private int value;

    public void increment() {
        //@TODO increment | make this method thread-safe: mark it synchronized (or lock a private final monitor) and increment value
        synchronized (this) {
            value++;
        }
        //@END
    }

    public int get() {
        //@TODO get | return value using the SAME lock as increment so that the latest value is visible
        synchronized (this) {
            return value;
        }
        //@END
    }
}
''',
             "RunnableCounter.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;

/** Thread basics. */
public final class RunnableCounter {

    private RunnableCounter() {
    }

    public static Runnable incrementTask(Counter counter, int times) {
        //@TODO incrementTask | return a Runnable that calls counter.increment() exactly times times
        return () -> {
            for (int i = 0; i < times; i++) {
                counter.increment();
            }
        };
        //@END
    }

    public static int runConcurrently(Counter counter, int threads, int perThread) throws InterruptedException {
        //@TODO runConcurrently | validate (threads > 0, perThread >= 0), start threads named counter-0.. each running incrementTask, join ALL of them, then return counter.get()
        if (threads <= 0 || perThread < 0) {
            throw new IllegalArgumentException("threads must be > 0 and perThread >= 0");
        }
        List<Thread> started = new ArrayList<>();
        for (int i = 0; i < threads; i++) {
            Thread t = new Thread(incrementTask(counter, perThread), "counter-" + i);
            started.add(t);
            t.start();
        }
        for (Thread t : started) {
            t.join();
        }
        return counter.get();
        //@END
    }

    public static Thread startNamed(String name, Runnable task) {
        //@TODO startNamed | create a Thread with the given name for the task, start it, and return it
        Thread t = new Thread(task, name);
        t.start();
        return t;
        //@END
    }

    public static String executedByWithRun() {
        //@TODO executedByWithRun | create a thread named "worker" whose task records Thread.currentThread().getName(), call run() directly (NOT start) and return the recorded name
        AtomicReference<String> seen = new AtomicReference<>();
        Thread t = new Thread(() -> seen.set(Thread.currentThread().getName()), "worker");
        t.run();
        return seen.get();
        //@END
    }

    public static String executedByWithStart(String name) throws InterruptedException {
        //@TODO executedByWithStart | same task but on a Thread called name started with start(); join it and return the recorded name
        AtomicReference<String> seen = new AtomicReference<>();
        Thread t = new Thread(() -> seen.set(Thread.currentThread().getName()), name);
        t.start();
        t.join();
        return seen.get();
        //@END
    }
}
'''},
            {"RunnableCounterTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(20)
class RunnableCounterTest {

    @Test
    void r1_counterCountsSequentially() {
        Counter c = new Counter();
        c.increment();
        c.increment();
        assertThat(c.get()).isEqualTo(2);
    }

    @Test
    void r2_incrementTaskRunsExactlyTimes() {
        Counter c = new Counter();
        RunnableCounter.incrementTask(c, 5).run();
        assertThat(c.get()).isEqualTo(5);
        RunnableCounter.incrementTask(c, 0).run();
        assertThat(c.get()).isEqualTo(5);
    }

    @Test
    void r3_concurrentIncrementsAreExact() throws Exception {
        Counter c = new Counter();
        assertThat(RunnableCounter.runConcurrently(c, 8, 50_000)).isEqualTo(400_000);
        assertThat(c.get()).isEqualTo(400_000);
    }

    @Test
    void r3_validation() {
        assertThatThrownBy(() -> RunnableCounter.runConcurrently(new Counter(), 0, 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> RunnableCounter.runConcurrently(new Counter(), 2, -1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r3_zeroIncrementsGivesZero() throws Exception {
        assertThat(RunnableCounter.runConcurrently(new Counter(), 3, 0)).isZero();
    }

    @Test
    void r4_startNamedStartsAThreadWithThatName() throws Exception {
        AtomicReference<String> seen = new AtomicReference<>();
        CountDownLatch done = new CountDownLatch(1);
        Thread t = RunnableCounter.startNamed("my-worker", () -> {
            seen.set(Thread.currentThread().getName());
            done.countDown();
        });
        assertThat(t.getName()).isEqualTo("my-worker");
        assertThat(done.await(5, TimeUnit.SECONDS)).isTrue();
        t.join(5_000);
        assertThat(seen.get()).isEqualTo("my-worker");
        assertThat(t.getState()).isEqualTo(Thread.State.TERMINATED);
    }

    @Test
    void r5_runDirectlyExecutesOnTheCallingThread() {
        assertThat(RunnableCounter.executedByWithRun()).isEqualTo(Thread.currentThread().getName());
        assertThat(RunnableCounter.executedByWithRun()).isNotEqualTo("worker");
    }

    @Test
    void r6_startExecutesOnTheNewThread() throws Exception {
        assertThat(RunnableCounter.executedByWithStart("bg-1")).isEqualTo("bg-1");
        assertThat(RunnableCounter.executedByWithStart("bg-2")).isNotEqualTo(Thread.currentThread().getName());
    }
}
'''},
            ["Both `increment()` and `get()` need the **same** lock: visibility requires the reader to synchronize too.", "Start all threads first, then join them all; joining inside the starting loop serializes the work."],
            ["Same lock for reads and writes of `value`", "No `Thread.sleep` used for coordination", "`InterruptedException` declared, not swallowed"],
            constraints=["Do not use `AtomicInteger` or `java.util.concurrent.locks` in `Counter` (the point is `synchronized`)", "Do not use `Thread.sleep` to wait for threads", "Do not edit the tests"],
        ),
        task(
            "synchronized-bank", "Synchronized Bank Account and Safe Transfer", "Core", "BankAccount",
            "Build a thread-safe `BankAccount` with validated `deposit`/`withdraw` and a `transfer` that is both atomic and **deadlock-free** by locking the two accounts in a global (id) order. The tests hammer the accounts from many threads, including opposing transfers, under a timeout.",
            [
                "`BankAccount(id, initial)` rejects a negative initial balance with `IllegalArgumentException`",
                "`deposit(amount)` and `withdraw(amount)` are thread-safe; non-positive amounts throw `IllegalArgumentException`; withdrawing more than the balance throws `IllegalStateException` and leaves the balance unchanged",
                "`balance()` returns a consistent value even while other threads update the account",
                "`transfer(from, to, amount)` moves money atomically; the sum of both balances is invariant; failure (insufficient funds) leaves both unchanged",
                "`transfer` locks both accounts in ascending `id` order so `transfer(a,b)` and `transfer(b,a)` running concurrently never deadlock",
                "`transfer` to the same account, or with a non-positive amount, throws `IllegalArgumentException`",
            ],
            ["insufficient funds", "same-account transfer", "opposing concurrent transfers (deadlock test)", "validation before any locking side effects"],
            {"BankAccount.java": r'''package @PKG@;

/** Thread-safe account; money is in whole cents. */
public final class BankAccount {

    private final long id;
    private long balance;

    public BankAccount(long id, long initialBalance) {
        //@TODO constructor | store id and initialBalance; IllegalArgumentException when initialBalance is negative
        if (initialBalance < 0) {
            throw new IllegalArgumentException("initial balance must be >= 0");
        }
        this.id = id;
        this.balance = initialBalance;
        //@END
    }

    public long id() {
        return id;
    }

    public void deposit(long amount) {
        //@TODO deposit | IllegalArgumentException when amount <= 0; add to balance under this account's lock
        if (amount <= 0) {
            throw new IllegalArgumentException("amount must be > 0");
        }
        synchronized (this) {
            balance += amount;
        }
        //@END
    }

    public void withdraw(long amount) {
        //@TODO withdraw | IllegalArgumentException when amount <= 0; IllegalStateException (balance unchanged) when amount > balance; subtract under the lock
        if (amount <= 0) {
            throw new IllegalArgumentException("amount must be > 0");
        }
        synchronized (this) {
            if (amount > balance) {
                throw new IllegalStateException("insufficient funds");
            }
            balance -= amount;
        }
        //@END
    }

    public long balance() {
        //@TODO balance | read balance under the same lock used by writers
        synchronized (this) {
            return balance;
        }
        //@END
    }

    public static void transfer(BankAccount from, BankAccount to, long amount) {
        //@TODO transfer | validate (amount > 0, from != to by id) then lock the account with the smaller id first, then the other; withdraw from 'from' and deposit into 'to' while holding both locks
        if (amount <= 0) {
            throw new IllegalArgumentException("amount must be > 0");
        }
        if (from == to || from.id == to.id) {
            throw new IllegalArgumentException("cannot transfer to the same account");
        }
        BankAccount first = from.id < to.id ? from : to;
        BankAccount second = first == from ? to : from;
        synchronized (first) {
            synchronized (second) {
                from.withdraw(amount);
                to.deposit(amount);
            }
        }
        //@END
    }
}
'''},
            {"BankAccountTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(30)
class BankAccountTest {

    @Test
    void r1_constructorValidation() {
        assertThatThrownBy(() -> new BankAccount(1, -1)).isInstanceOf(IllegalArgumentException.class);
        assertThat(new BankAccount(1, 0).balance()).isZero();
        assertThat(new BankAccount(7, 50).id()).isEqualTo(7);
    }

    @Test
    void r2_depositAndWithdraw() {
        BankAccount a = new BankAccount(1, 100);
        a.deposit(50);
        a.withdraw(30);
        assertThat(a.balance()).isEqualTo(120);
    }

    @Test
    void r2_invalidAmountsAndInsufficientFunds() {
        BankAccount a = new BankAccount(1, 100);
        assertThatThrownBy(() -> a.deposit(0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> a.withdraw(-5)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> a.withdraw(101)).isInstanceOf(IllegalStateException.class);
        assertThat(a.balance()).isEqualTo(100);
        a.withdraw(100);
        assertThat(a.balance()).isZero();
    }

    @Test
    void r3_concurrentDepositsAreNotLost() throws Exception {
        BankAccount a = new BankAccount(1, 0);
        runInParallel(8, () -> {
            for (int i = 0; i < 20_000; i++) {
                a.deposit(1);
            }
        });
        assertThat(a.balance()).isEqualTo(160_000);
    }

    @Test
    void r4_transferMovesMoneyAtomically() {
        BankAccount a = new BankAccount(1, 100);
        BankAccount b = new BankAccount(2, 10);
        BankAccount.transfer(a, b, 40);
        assertThat(a.balance()).isEqualTo(60);
        assertThat(b.balance()).isEqualTo(50);
    }

    @Test
    void r4_failedTransferChangesNothing() {
        BankAccount a = new BankAccount(1, 10);
        BankAccount b = new BankAccount(2, 10);
        assertThatThrownBy(() -> BankAccount.transfer(a, b, 11)).isInstanceOf(IllegalStateException.class);
        assertThat(a.balance()).isEqualTo(10);
        assertThat(b.balance()).isEqualTo(10);
    }

    @Test
    void r5_opposingTransfersDoNotDeadlockAndKeepTheTotal() throws Exception {
        BankAccount a = new BankAccount(1, 1_000_000);
        BankAccount b = new BankAccount(2, 1_000_000);
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 20_000; i++) {
                BankAccount.transfer(a, b, 1);
            }
        });
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 20_000; i++) {
                BankAccount.transfer(b, a, 1);
            }
        });
        t1.start();
        t2.start();
        t1.join(20_000);
        t2.join(20_000);
        assertThat(t1.isAlive()).as("thread 1 finished (no deadlock)").isFalse();
        assertThat(t2.isAlive()).as("thread 2 finished (no deadlock)").isFalse();
        assertThat(a.balance() + b.balance()).isEqualTo(2_000_000);
        assertThat(a.balance()).isEqualTo(1_000_000);
    }

    @Test
    void r6_invalidTransfers() {
        BankAccount a = new BankAccount(1, 10);
        assertThatThrownBy(() -> BankAccount.transfer(a, a, 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> BankAccount.transfer(a, new BankAccount(2, 0), 0)).isInstanceOf(IllegalArgumentException.class);
        assertThat(a.balance()).isEqualTo(10);
    }

    private static void runInParallel(int threads, Runnable task) throws InterruptedException {
        List<Thread> all = new ArrayList<>();
        for (int i = 0; i < threads; i++) {
            Thread t = new Thread(task);
            all.add(t);
            t.start();
        }
        for (Thread t : all) {
            t.join();
        }
    }
}
'''},
            ["Lock ordering needs a total order: the account id is perfect because it is unique and immutable.", "`synchronized` is reentrant, so calling `withdraw`/`deposit` while already holding the lock is fine."],
            ["Same lock discipline for reads and writes", "Lock ordering by id explained in a comment", "No `Thread.sleep` or retry loops to \"avoid\" deadlock"],
            constraints=["Use `synchronized` (no `java.util.concurrent.locks` yet)", "Do not edit the tests"],
        ),
        task(
            "wait-notify-buffer", "Producer/Consumer Bounded Buffer", "Stretch", "BoundedBuffer",
            "Implement a classic bounded blocking buffer with `synchronized`, `wait()` and `notifyAll()`: `put` blocks while full, `take` blocks while empty, FIFO order is preserved, and interruption is propagated. The tests check blocking behavior by observing `Thread.State.WAITING` - no sleeps.",
            [
                "`BoundedBuffer(capacity)` rejects capacity <= 0 with `IllegalArgumentException`",
                "`put(item)` rejects `null` with `NullPointerException`; blocks (WAITING) while the buffer is full",
                "`take()` blocks (WAITING) while the buffer is empty and returns items in FIFO order",
                "`size()` returns the current number of items; `capacity()` the configured limit",
                "Both blocking methods wait in a **loop** and use `notifyAll()` after changing state; `InterruptedException` is propagated",
                "A producer and a consumer thread can transfer 10_000 items through a capacity-3 buffer in order without loss",
            ],
            ["capacity 1", "interrupt while waiting", "null items", "wake-ups after state changes (loop, not `if`)"],
            {"BoundedBuffer.java": r'''package @PKG@;

import java.util.Objects;

/** Bounded FIFO buffer using intrinsic locks and wait/notifyAll. */
public final class BoundedBuffer<T> {

    private final Object[] items;
    private int head;
    private int tail;
    private int count;

    public BoundedBuffer(int capacity) {
        //@TODO constructor | IllegalArgumentException when capacity <= 0; allocate the circular array
        if (capacity <= 0) {
            throw new IllegalArgumentException("capacity must be > 0");
        }
        this.items = new Object[capacity];
        //@END
    }

    public synchronized void put(T item) throws InterruptedException {
        //@TODO put | NullPointerException for null; while the buffer is full wait(); then store at tail (circular), count++ and notifyAll()
        Objects.requireNonNull(item, "item");
        while (count == items.length) {
            wait();
        }
        items[tail] = item;
        tail = (tail + 1) % items.length;
        count++;
        notifyAll();
        //@END
    }

    @SuppressWarnings("unchecked")
    public synchronized T take() throws InterruptedException {
        //@TODO take | while the buffer is empty wait(); then remove from head (circular, clear the slot), count-- and notifyAll()
        while (count == 0) {
            wait();
        }
        T item = (T) items[head];
        items[head] = null;
        head = (head + 1) % items.length;
        count--;
        notifyAll();
        return item;
        //@END
    }

    public synchronized int size() {
        return count;
    }

    public int capacity() {
        return items.length;
    }
}
'''},
            {"BoundedBufferTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(30)
class BoundedBufferTest {

    private static void awaitState(Thread t, Thread.State expected) throws InterruptedException {
        long deadline = System.nanoTime() + 5_000_000_000L;
        while (t.getState() != expected) {
            if (System.nanoTime() > deadline) {
                throw new AssertionError("thread never reached " + expected + " (was " + t.getState() + ")");
            }
            Thread.onSpinWait();
        }
    }

    @Test
    void r1_constructorValidation() {
        assertThatThrownBy(() -> new BoundedBuffer<String>(0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new BoundedBuffer<String>(-1)).isInstanceOf(IllegalArgumentException.class);
        BoundedBuffer<String> b = new BoundedBuffer<>(3);
        assertThat(b.capacity()).isEqualTo(3);
        assertThat(b.size()).isZero();
    }

    @Test
    void r2_fifoSingleThread() throws Exception {
        BoundedBuffer<Integer> b = new BoundedBuffer<>(3);
        b.put(1);
        b.put(2);
        b.put(3);
        assertThat(b.size()).isEqualTo(3);
        assertThat(b.take()).isEqualTo(1);
        b.put(4);
        assertThat(b.take()).isEqualTo(2);
        assertThat(b.take()).isEqualTo(3);
        assertThat(b.take()).isEqualTo(4);
        assertThat(b.size()).isZero();
    }

    @Test
    void r2_nullRejected() {
        BoundedBuffer<String> b = new BoundedBuffer<>(1);
        assertThatThrownBy(() -> b.put(null)).isInstanceOf(NullPointerException.class);
    }

    @Test
    void r3_takeBlocksUntilAnItemArrives() throws Exception {
        BoundedBuffer<String> b = new BoundedBuffer<>(2);
        AtomicReference<String> got = new AtomicReference<>();
        Thread consumer = new Thread(() -> {
            try {
                got.set(b.take());
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        consumer.start();
        awaitState(consumer, Thread.State.WAITING);
        assertThat(got.get()).isNull();
        b.put("hello");
        consumer.join(5_000);
        assertThat(consumer.isAlive()).isFalse();
        assertThat(got.get()).isEqualTo("hello");
    }

    @Test
    void r4_putBlocksWhileFull() throws Exception {
        BoundedBuffer<String> b = new BoundedBuffer<>(1);
        b.put("a");
        Thread producer = new Thread(() -> {
            try {
                b.put("b");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        producer.start();
        awaitState(producer, Thread.State.WAITING);
        assertThat(b.size()).isEqualTo(1);
        assertThat(b.take()).isEqualTo("a");
        producer.join(5_000);
        assertThat(producer.isAlive()).isFalse();
        assertThat(b.take()).isEqualTo("b");
    }

    @Test
    void r5_interruptWhileWaitingPropagates() throws Exception {
        BoundedBuffer<String> b = new BoundedBuffer<>(1);
        AtomicReference<Throwable> thrown = new AtomicReference<>();
        Thread consumer = new Thread(() -> {
            try {
                b.take();
            } catch (Throwable t) {
                thrown.set(t);
            }
        });
        consumer.start();
        awaitState(consumer, Thread.State.WAITING);
        consumer.interrupt();
        consumer.join(5_000);
        assertThat(consumer.isAlive()).isFalse();
        assertThat(thrown.get()).isInstanceOf(InterruptedException.class);
    }

    @Test
    void r6_producerConsumerTransfersEverythingInOrder() throws Exception {
        BoundedBuffer<Integer> b = new BoundedBuffer<>(3);
        int total = 10_000;
        List<Integer> received = new ArrayList<>();
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < total; i++) {
                    b.put(i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        Thread consumer = new Thread(() -> {
            try {
                for (int i = 0; i < total; i++) {
                    received.add(b.take());
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        producer.start();
        consumer.start();
        producer.join(20_000);
        consumer.join(20_000);
        assertThat(received).hasSize(total);
        for (int i = 0; i < total; i++) {
            assertThat(received.get(i)).isEqualTo(i);
        }
        assertThat(b.size()).isZero();
    }
}
'''},
            ["Keep the condition in shared state (`count`) and re-test it in the `while` loop after every wake-up.", "`notifyAll()` wakes both producers and consumers; each rechecks its own condition."],
            ["`while` loops (never `if`) around `wait()`", "All state accessed under the same monitor", "Interrupt propagated, not swallowed"],
            constraints=["Use `synchronized`/`wait`/`notifyAll` - no `BlockingQueue`, `Lock`, or `Condition`", "No `Thread.sleep`", "Do not edit the tests"],
        ),
        task(
            "deadlock-detector-doc", "Lock-Order Deadlock Detector", "Challenge", "LockOrderAnalyzer",
            "Analyze lock acquisition orders statically: each thread is described by the ordered list of lock names it acquires. Detect pairs of locks acquired in **opposite orders** by different threads (a classic deadlock risk), produce a human-readable recommendation, and document the four Coffman conditions in code.",
            [
                "`conflictingPairs(orders)` returns a sorted set of strings `\"A<->B\"` (names in alphabetical order inside each pair) for every two locks that one thread takes as X-then-Y and another as Y-then-X; a lock repeated within one thread (reentrancy) counts at its first position",
                "`hasOrderingRisk(orders)` is true exactly when `conflictingPairs` is non-empty",
                "`coffmanConditions()` returns, in this order: `Mutual exclusion`, `Hold and wait`, `No preemption`, `Circular wait`",
                "`advice(orders)` returns `\"No lock-ordering conflicts found.\"` when safe; otherwise a text that lists every conflicting pair and recommends one global order (all lock names, alphabetical, comma-separated) using the phrase `global order`",
            ],
            ["single thread (never a risk)", "same order in all threads (safe)", "reentrant duplicates (`A, A, B`)", "non-adjacent acquisition (`A, C, B` vs `B, A`)", "empty input"],
            {"LockOrderAnalyzer.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.SortedSet;
import java.util.TreeSet;

/** Static analysis of lock acquisition orders. Each inner list is one thread's lock order. */
public final class LockOrderAnalyzer {

    private LockOrderAnalyzer() {
    }

    public static SortedSet<String> conflictingPairs(List<List<String>> threadLockOrders) {
        //@TODO conflictingPairs | collect every (x before y) relation per thread (first occurrence only); report "A<->B" (A < B alphabetically) when both (x,y) and (y,x) occur in different threads
        Set<List<String>> before = new HashSet<>();
        for (List<String> order : threadLockOrders) {
            List<String> distinct = new ArrayList<>(new LinkedHashSet<>(order));
            for (int i = 0; i < distinct.size(); i++) {
                for (int j = i + 1; j < distinct.size(); j++) {
                    before.add(List.of(distinct.get(i), distinct.get(j)));
                }
            }
        }
        SortedSet<String> pairs = new TreeSet<>();
        for (List<String> relation : before) {
            String x = relation.get(0);
            String y = relation.get(1);
            if (before.contains(List.of(y, x))) {
                String low = x.compareTo(y) < 0 ? x : y;
                String high = x.compareTo(y) < 0 ? y : x;
                pairs.add(low + "<->" + high);
            }
        }
        return pairs;
        //@END
    }

    public static boolean hasOrderingRisk(List<List<String>> threadLockOrders) {
        //@TODO hasOrderingRisk | true when conflictingPairs is not empty
        return !conflictingPairs(threadLockOrders).isEmpty();
        //@END
    }

    public static List<String> coffmanConditions() {
        //@TODO coffmanConditions | return exactly: "Mutual exclusion", "Hold and wait", "No preemption", "Circular wait" (in this order)
        return List.of("Mutual exclusion", "Hold and wait", "No preemption", "Circular wait");
        //@END
    }

    public static String advice(List<List<String>> threadLockOrders) {
        //@TODO advice | "No lock-ordering conflicts found." when safe; otherwise mention each pair and recommend a "global order" listing all lock names alphabetically
        SortedSet<String> pairs = conflictingPairs(threadLockOrders);
        if (pairs.isEmpty()) {
            return "No lock-ordering conflicts found.";
        }
        SortedSet<String> allLocks = new TreeSet<>();
        for (List<String> order : threadLockOrders) {
            allLocks.addAll(order);
        }
        return "Lock-ordering risk: " + String.join("; ", pairs)
                + ". Fix: acquire locks in one global order, for example " + String.join(", ", allLocks) + ".";
        //@END
    }
}
'''},
            {"LockOrderAnalyzerTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.Test;

class LockOrderAnalyzerTest {

    @Test
    void r1_oppositeOrdersAreConflicting() {
        var pairs = LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "B"), List.of("B", "A")));
        assertThat(pairs).containsExactly("A<->B");
    }

    @Test
    void r1_sameOrderIsSafe() {
        assertThat(LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "B"), List.of("A", "B"), List.of("A", "B")))).isEmpty();
        assertThat(LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "B", "C"), List.of("A", "C")))).isEmpty();
    }

    @Test
    void r1_singleThreadIsNeverAConflict() {
        assertThat(LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "B", "A")))).isEmpty();
        assertThat(LockOrderAnalyzer.conflictingPairs(List.of())).isEmpty();
    }

    @Test
    void r1_nonAdjacentAndMultiplePairs() {
        var pairs = LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "C", "B"), List.of("B", "A"), List.of("C", "X")));
        assertThat(pairs).containsExactly("A<->B");
        var more = LockOrderAnalyzer.conflictingPairs(List.of(List.of("L1", "L2", "L3"), List.of("L3", "L2"), List.of("L2", "L1")));
        assertThat(more).containsExactly("L1<->L2", "L2<->L3");
    }

    @Test
    void r1_reentrantDuplicatesUseFirstPosition() {
        assertThat(LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "A", "B"), List.of("A", "B")))).isEmpty();
        assertThat(LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "A", "B"), List.of("B", "A")))).containsExactly("A<->B");
    }

    @Test
    void r2_hasOrderingRisk() {
        assertThat(LockOrderAnalyzer.hasOrderingRisk(List.of(List.of("lockX", "lockY"), List.of("lockY", "lockX")))).isTrue();
        assertThat(LockOrderAnalyzer.hasOrderingRisk(List.of(List.of("lockX", "lockY"), List.of("lockX")))).isFalse();
    }

    @Test
    void r3_coffmanConditions() {
        assertThat(LockOrderAnalyzer.coffmanConditions())
                .containsExactly("Mutual exclusion", "Hold and wait", "No preemption", "Circular wait");
    }

    @Test
    void r4_adviceWhenSafe() {
        assertThat(LockOrderAnalyzer.advice(List.of(List.of("A", "B"), List.of("A", "B"))))
                .isEqualTo("No lock-ordering conflicts found.");
    }

    @Test
    void r4_adviceWhenRisky() {
        String text = LockOrderAnalyzer.advice(List.of(List.of("accounts", "audit"), List.of("audit", "accounts"), List.of("zeta")));
        assertThat(text).contains("accounts<->audit").contains("global order");
        assertThat(text).contains("accounts, audit, zeta");
    }
}
'''},
            ["Think of each thread as producing \"X before Y\" facts; a conflict is a fact and its mirror image from some thread.", "Use `List.of(x, y)` as a hash key for a pair - lists have value-based `equals`/`hashCode`."],
            ["Conflict detection is order-sensitive but independent of the thread order in the input", "Deterministic (sorted) output", "Explains in a comment how a global lock order breaks the circular-wait condition"],
            constraints=["No actual threads or locks are needed - this is an analysis task", "Do not edit the tests"],
        ),
    ],
)
