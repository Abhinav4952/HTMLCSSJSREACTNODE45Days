# Day 20 — Threads I: Thread, Runnable, synchronized, volatile, wait/notify, and Deadlock

**Phase:** Core Java  
**Primary theme:** Create threads, protect shared state with `synchronized`/`volatile`, coordinate with `wait`/`notify`, and recognize deadlock.  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-runnable-counter`, `task-02-synchronized-bank`, `task-03-wait-notify-buffer`, `task-04-deadlock-detector-doc`  
**Instruction alignment:** Maps to the Day 20 entry of the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21 (no Spring today)

## Overview

Every server is concurrent: each request runs on a thread, and those threads share caches, counters, connection pools, and configuration. Concurrency bugs are the hardest to reproduce - they depend on timing - so the discipline is to **reason**, not to test-and-hope. Today you learn the foundations that `ExecutorService` and `java.util.concurrent` (Day 21) are built on.

The key ideas: a *race condition* happens when correctness depends on timing; `count++` is **not atomic**; the JVM may cache values per thread unless you create a *happens-before* edge (`synchronized`, `volatile`, `Thread.start/join`); `wait/notify` implement guarded waiting; and two threads taking two locks in opposite order can **deadlock**. Interviews ask all of these, usually with a code sample to critique.

## Day roadmap

1. Threads, Runnable, and the thread lifecycle
2. Races, synchronized, volatile, and the Java Memory Model
3. wait/notify, producer-consumer, and deadlock
4. Interview angles
5. Common mistakes & debugging
6. Further reading, glossary, answers

### Threads, Runnable, and the thread lifecycle

#### What it is

A **thread** is an independent path of execution inside the JVM that shares the heap with other threads but has its own stack. You supply the work as a `Runnable` (`() -> ...`) and start it with `new Thread(runnable, "name").start()`. **`start()` creates a new OS-level thread that then calls `run()`; calling `run()` directly just executes the code on the *current* thread** (a very common bug). States (`Thread.State`): `NEW`, `RUNNABLE`, `BLOCKED` (waiting for a monitor), `WAITING` (`wait()`, `join()`, `park`), `TIMED_WAITING` (`sleep`, timed waits), `TERMINATED`. `join()` waits for a thread to finish **and creates a happens-before edge**. `interrupt()` sets an interrupt flag / wakes blocking calls with `InterruptedException`; cooperative cancellation is the only safe way to stop a thread (`Thread.stop` is removed). Daemon threads do not keep the JVM alive.

#### Why it exists / why it matters

Threads let one process serve many requests, overlap I/O waits, and use multiple cores. Understanding `start/run/join/interrupt` and thread states is required to read thread dumps (`jstack`, `jcmd Thread.print`, Day 22) and to know why a service is hung. In production you rarely create raw threads (use executors, Day 21), but every abstraction is built on these primitives.

#### Pros and cons

**Pros**

- Parallelism on multi-core hardware
- Overlap blocking I/O with computation
- Simple mental model: `Runnable` is the unit of work
- Thread names and states make dumps readable

**Cons / tradeoffs**

- Shared mutable state needs careful synchronization
- Threads are expensive (~1 MB stack each) and non-trivial to cancel
- Exceptions in a thread do not propagate to the creator (use an `UncaughtExceptionHandler` or `Future`)

#### What happens without it / when misused

Calling `thread.run()` instead of `start()` silently runs the task on the caller's thread (no concurrency). Calling `start()` twice throws `IllegalThreadStateException`. Swallowing `InterruptedException` (`catch (InterruptedException e) {}`) loses the cancellation signal - restore it with `Thread.currentThread().interrupt()`. A non-daemon thread stuck in a loop prevents JVM shutdown. An unhandled exception kills only that thread and prints a stack trace to stderr - the rest of the app continues in a degraded state. Creating a thread per request without bounds exhausts memory (`OutOfMemoryError: unable to create native thread`).

#### Syntax and rules

- Create: `Thread t = new Thread(runnable, "worker-1"); t.start();` or `Thread.ofPlatform().name("w").start(r)` (Java 21).
- `t.join()` / `t.join(millis)`; `t.isAlive()`; `t.getState()`; `Thread.currentThread()`.
- Interrupt protocol: loop on `!Thread.currentThread().isInterrupted()`; blocking methods throw `InterruptedException` (clearing the flag) - either propagate it or re-set the flag.
- `setDaemon(true)` must be called **before** `start()`.
- `Thread.sleep(ms)` is for demos, not for synchronization - never use it to "wait for the other thread".
- Uncaught exceptions: `t.setUncaughtExceptionHandler((th, ex) -> log.error(...))`.

#### Examples

**Example 1.1 — Tiny — start() vs run()**

```java
Runnable who = () -> System.out.println(Thread.currentThread().getName());
Thread t = new Thread(who, "worker");
t.run();                  // prints "main"   (no new thread!)
t.start(); t.join();      // prints "worker" (new thread)
```

**Example 1.2 — Tiny — join gives you the result safely**

```java
int[] box = new int[1];
Thread t = new Thread(() -> box[0] = 6 * 7);
t.start();
t.join();                  // happens-before: the write to box[0] is visible after join
System.out.println(box[0]);   // 42
```

**Example 1.3 — Medium — cooperative cancellation**

```java
public class Worker implements Runnable {
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
}
```

#### Quick checks

1. What is the difference between `start()` and `run()`?
2. What happens if you call `start()` twice on the same Thread?
3. Why re-set the interrupt flag after catching `InterruptedException`?
4. Which state is a thread in while blocked trying to enter a `synchronized` block?

### Races, synchronized, volatile, and the Java Memory Model

#### What it is

A **race condition** occurs when the result depends on thread interleaving. `count++` is three steps (read, add, write), so two threads can both read `5` and both write `6` (a *lost update*). **Atomicity** (indivisible compound actions), **visibility** (one thread's write becomes visible to another), and **ordering** (the compiler/CPU may reorder) are the three problems. The **Java Memory Model** defines *happens-before*: unlock of a monitor happens-before every later lock of the same monitor; a write to a `volatile` field happens-before every later read of it; `Thread.start()` happens-before the first action of the started thread; the last action of a thread happens-before a successful `join()`. `synchronized` (method or block) gives **mutual exclusion + visibility** via the object's intrinsic lock (monitor), which is **reentrant**. `volatile` gives visibility and ordering but **no atomicity** for compound actions.

#### Why it exists / why it matters

Without these guarantees correct-looking code fails on real hardware: loops that never see a `stop` flag, counters that lose updates, objects seen half-constructed. Choosing the right tool matters: `volatile` for a simple status flag or safe publication of an immutable object, `synchronized` for check-then-act and multi-field invariants, atomics/locks (Day 21) for finer control.

#### Pros and cons

**Pros**

- `synchronized` is simple, built in, reentrant, and releases the lock on exceptions
- `volatile` is cheap and ideal for flags and publishing immutable snapshots
- A clear happens-before model lets you reason about correctness
- Immutable objects need no synchronization at all

**Cons / tradeoffs**

- Locks serialize work (contention reduces throughput)
- `synchronized` offers no timeout, no fairness control, and no interruptible acquisition
- `volatile` is misused for compound actions (`volatile int n; n++` is still a race)

#### What happens without it / when misused

A non-volatile `boolean running` read in a `while (running)` loop may be hoisted by the JIT so the loop never ends. `volatile int count; count++` loses updates. Synchronizing on different lock objects for the same data gives no protection (`synchronized(new Object())` is useless). Synchronizing on a *public* object or `String`/boxed values (`synchronized ("lock")`, `synchronized (Integer)`) lets unrelated code interfere. **Check-then-act** (`if (!map.containsKey(k)) map.put(k, v)`) is a race even with a thread-safe map. Holding a lock while calling unknown (alien) code risks deadlock. `double-checked locking` without `volatile` can publish a partially constructed object.

#### Syntax and rules

- Synchronized method: locks `this` (instance) or the `Class` object (static).
- Synchronized block: `synchronized (lock) { ... }` with a **private final** lock object.
- Reentrancy: a thread already holding a monitor can acquire it again.
- Guard **all** accesses (reads and writes) of shared state with the **same** lock.
- `volatile` guarantees: visibility of writes, no reordering across the volatile access; **not** atomic read-modify-write.
- Safe publication: static initializer, `final` fields, `volatile` field, lock-protected field, or `Thread.start/join` edges.
- Prefer immutability, thread confinement, or `java.util.concurrent` classes over hand-rolled locking.

#### Examples

**Example 2.1 — Tiny — the lost update**

```java
class Counter {
    int value;                          // shared, unprotected
    void inc() { value++; }             // read-modify-write: NOT atomic
}
// 4 threads x 100_000 inc() -> usually less than 400_000

class SafeCounter {
    private int value;
    synchronized void inc() { value++; }
    synchronized int get() { return value; }   // reads must be guarded too (visibility)
}
```

**Example 2.2 — Tiny — volatile stop flag**

```java
class Spinner implements Runnable {
    private volatile boolean running = true;     // without volatile the loop might never see false
    public void stop() { running = false; }
    @Override public void run() { while (running) { /* work */ } }
}
```

**Example 2.3 — Medium — block-level locking of related fields**

```java
public final class Stats {
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
}
```

#### Quick checks

1. Why is `volatile int n; n++;` not thread-safe?
2. Which two locks guard a class's static synchronized method and an instance synchronized method?
3. What does happens-before guarantee for `join()`?
4. Why should a lock object be `private final`?

### wait/notify, producer-consumer, and deadlock

#### What it is

`Object.wait()` releases the monitor and parks the thread until another thread calls `notify()`/`notifyAll()` on the **same** object; it must be called while holding that object's monitor (else `IllegalMonitorStateException`). Because of **spurious wakeups** and shared conditions, always wait in a **loop**: `while (!condition) wait();`. `notifyAll` is safer than `notify` unless all waiters are equivalent. A **bounded buffer** (producer-consumer) is the classic use: producers wait when full, consumers wait when empty. **Deadlock** is a cycle of threads each holding a lock another needs. It requires the four **Coffman conditions**: mutual exclusion, hold and wait, no preemption, and circular wait. Break any one - most practically circular wait by acquiring locks in a **global order**.

#### Why it exists / why it matters

Guarded waiting is how threads coordinate without burning CPU. Deadlocks, unlike races, are *visible* (the app hangs) but intermittent: they appear under load when interleavings line up. You diagnose them with thread dumps (`jstack`, `jcmd <pid> Thread.print`), which report "Found one Java-level deadlock". The prevention rules (lock ordering, avoid nested locks, `tryLock` with timeouts, open calls) are interview staples.

#### Pros and cons

**Pros**

- `wait/notify` allow efficient blocking coordination with no polling
- Bounded buffers provide back-pressure between producers and consumers
- Lock ordering is a simple, effective deadlock prevention
- Deadlocks are detectable in thread dumps

**Cons / tradeoffs**

- Easy to misuse: forgetting the loop, wrong monitor, lost notifications, `notify` waking the wrong thread
- Low-level; `BlockingQueue` and `Condition` are higher-level replacements
- Deadlock is non-deterministic and may only appear in production

#### What happens without it / when misused

`if (queue.isEmpty()) wait();` (an `if`, not a `while`) lets a spuriously woken or racing consumer proceed on an empty queue and fail with `NoSuchElementException`. Calling `notify()` before the waiter has started waiting loses the signal (the condition state must live in shared variables). Waiting on one object but notifying another means no one wakes. Two transfer methods that lock `from` then `to` deadlock when called as `transfer(a,b)` and `transfer(b,a)` simultaneously. Holding a lock while doing I/O or calling listeners (alien methods) stalls every other thread that needs the lock. `Thread.sleep` inside `synchronized` keeps the monitor held (unlike `wait`).

#### Syntax and rules

- Pattern: `synchronized (this) { while (!ready()) wait(); consume(); notifyAll(); }`.
- `wait()` throws `InterruptedException`; do not swallow it.
- `wait(timeoutMillis)` returns on timeout - recheck the condition in the loop anyway.
- Producer: `while (full) wait(); add(); notifyAll();` Consumer: `while (empty) wait(); take(); notifyAll();`.
- Deadlock prevention: global lock ordering (e.g. by account id), lock coarsening, `ReentrantLock.tryLock(timeout)`, avoid calling foreign code while holding a lock.
- Detect: `jstack <pid>` / `jcmd <pid> Thread.print`, `ThreadMXBean.findDeadlockedThreads()`.

#### Examples

**Example 3.1 — Tiny — minimal guarded wait**

```java
class Gate {
    private boolean open;
    synchronized void await() throws InterruptedException {
        while (!open) wait();            // loop, never if
    }
    synchronized void open() {
        open = true;
        notifyAll();
    }
}
```

**Example 3.2 — Tiny — deadlock-prone vs ordered locking**

```java
// DEADLOCK RISK: thread 1: transfer(a, b)   thread 2: transfer(b, a)
void transferBad(Account from, Account to, long amt) {
    synchronized (from) { synchronized (to) { from.debit(amt); to.credit(amt); } }
}
// SAFE: always lock the lower id first
void transferOrdered(Account from, Account to, long amt) {
    Account first = from.id < to.id ? from : to, second = first == from ? to : from;
    synchronized (first) { synchronized (second) { from.debit(amt); to.credit(amt); } }
}
```

**Example 3.3 — Medium — a bounded buffer**

```java
import java.util.*;

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
}
```

#### Quick checks

1. Why must `wait()` be called in a `while` loop?
2. Name the four conditions required for deadlock and the one you usually break.
3. What is the difference between `sleep` and `wait` regarding locks?
4. How do you find a deadlock in a running JVM?

## Interview angles

**Q: What is a race condition? Give an example.**

Correctness depends on timing. `count++` from two threads can lose an update because it is read-modify-write, not atomic.

**Q: synchronized vs volatile?**

`synchronized` gives mutual exclusion and visibility for blocks of code; `volatile` gives visibility/ordering for a single variable but no atomic compound operations.

**Q: What is a deadlock and how do you prevent it?**

A circular wait among threads holding locks. Prevent with consistent lock ordering, timeouts (`tryLock`), fewer nested locks, and not calling alien code under locks.

**Q: wait/notify vs sleep/interrupt?**

`wait/notify` coordinate via an object's monitor and release it while waiting; `sleep` just pauses (monitors stay held); `interrupt` is a cancellation request that wakes blocking calls.

**Q: What does the `Thread.State` BLOCKED mean versus WAITING?**

BLOCKED: waiting to acquire a monitor. WAITING: waiting indefinitely for another thread's action (`wait`, `join`, `park`).

**Q: Why is double-checked locking broken without volatile?**

Without `volatile` another thread can see a non-null reference to a partially constructed object due to reordering.

## Common mistakes & debugging

- `run()` instead of `start()`; or `start()` twice (`IllegalThreadStateException`).
- Synchronizing writes but not reads of the same data (visibility bug).
- Different lock objects for the same state, or synchronizing on `String`/`Integer`/`this` exposed to outsiders.
- `if` instead of `while` around `wait()`; notifying a different object than the one waited on.
- Nested locks in inconsistent order (deadlock); sleeping inside synchronized blocks.
- Swallowing `InterruptedException`; using `Thread.sleep` as "synchronization" in tests.

## Further reading

- JLS ch. 17 (Threads and Locks) - especially 17.4 (Memory Model) and 17.2 (Wait Sets and Notification)
- Oracle Java Tutorials - *Concurrency* (Processes and Threads, Synchronization, Liveness)
- *Java Concurrency in Practice* (Goetz et al.) ch. 1-3, 10 (avoiding liveness hazards)
- Javadoc: `java.lang.Thread`, `Thread.State`, `Object#wait`, `java.lang.management.ThreadMXBean`

## Glossary

| Term | Meaning |
|------|---------|
| Race condition | Outcome depends on unsynchronized timing of threads |
| Atomic | Indivisible; appears to happen instantly to other threads |
| Monitor / intrinsic lock | Per-object lock used by `synchronized`, `wait`, `notify` |
| Happens-before | JMM ordering guarantee that makes one action's effects visible to another |
| Spurious wakeup | A waiting thread returns from `wait()` without a notify |
| Deadlock | Circular wait: each thread holds a lock another needs |
| Livelock / starvation | Threads active but making no progress / one thread never gets the resource |
| Coffman conditions | The four necessary conditions for deadlock |

## Answers

Answers to every **Quick check** above (numbered `section.question`).

- **1.1** — What is the difference between `start()` and `run()`?  
  `start()` spawns a new thread which invokes `run()`; calling `run()` executes it synchronously in the calling thread.

- **1.2** — What happens if you call `start()` twice on the same Thread?  
  `IllegalThreadStateException`; a thread can be started only once.

- **1.3** — Why re-set the interrupt flag after catching `InterruptedException`?  
  Catching clears the flag; restoring it lets callers up the stack observe the cancellation request.

- **1.4** — Which state is a thread in while blocked trying to enter a `synchronized` block?  
  `BLOCKED` (whereas `Object.wait()` and `join()` give `WAITING`).

- **2.1** — Why is `volatile int n; n++;` not thread-safe?  
  `n++` is read, add, write; `volatile` makes each access visible but does not make the three steps atomic.

- **2.2** — Which two locks guard a class's static synchronized method and an instance synchronized method?  
  The `Class` object monitor and the instance's monitor respectively - they are different locks.

- **2.3** — What does happens-before guarantee for `join()`?  
  Everything the joined thread did is visible to the thread that returns from `join()`.

- **2.4** — Why should a lock object be `private final`?  
  So no outside code can synchronize on it (or replace it) and break your locking discipline.

- **3.1** — Why must `wait()` be called in a `while` loop?  
  To recheck the condition after wake-ups: spurious wakeups, multiple waiters, and `notifyAll` mean the condition may no longer hold.

- **3.2** — Name the four conditions required for deadlock and the one you usually break.  
  Mutual exclusion, hold and wait, no preemption, circular wait; you usually break circular wait with a global lock order.

- **3.3** — What is the difference between `sleep` and `wait` regarding locks?  
  `sleep` keeps held monitors; `wait` releases the monitor it is called on while waiting.

- **3.4** — How do you find a deadlock in a running JVM?  
  Take a thread dump (`jstack <pid>` or `jcmd <pid> Thread.print`) which prints "Found one Java-level deadlock"; or use `ThreadMXBean.findDeadlockedThreads()`.
