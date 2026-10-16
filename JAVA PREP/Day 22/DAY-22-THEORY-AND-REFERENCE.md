# Day 22 — Virtual Threads (Java 21), JVM Memory & GC, Class Loading, and Troubleshooting

**Phase:** Core Java  
**Primary theme:** Scale blocking code with virtual threads, understand how the JVM lays out memory and loads classes, and diagnose live JVMs with jstack, jcmd, and VisualVM.  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-virtual-thread-runner`, `task-02-gc-log-analyzer`, `task-03-classloader-lab`, `task-04-thread-dump-analyzer`  
**Instruction alignment:** Maps to the Day 22 entry of the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21 (no Spring today)

## Overview

Day 21 showed how to run work on **bounded platform-thread pools**. That model has a ceiling: a platform thread maps 1:1 to an OS thread (about 1 MB of stack reserved, expensive to create and to context-switch), so a server that blocks one thread per request tops out at a few thousand concurrent requests. **Virtual threads** (JEP 444, final in Java 21) are cheap, JVM-scheduled threads multiplexed onto a small pool of carrier threads. When a virtual thread blocks on I/O, `sleep`, a lock, or a queue it is *unmounted* and the carrier runs something else. You keep the simple blocking, thread-per-request style and still scale to hundreds of thousands of concurrent tasks.

Virtual threads sit on top of the JVM, so the second half of the day looks underneath: **where memory lives** (heap young/old, metaspace, stacks, code cache, direct buffers), **how the garbage collectors differ** (throughput vs latency), **how classes get loaded** (bootstrap/platform/app loaders, parent-first delegation, class identity), and **how to troubleshoot a misbehaving JVM** (thread dumps, heap histograms, GC logs, VisualVM). Interviews love these: *why can virtual threads be slow for CPU work*, *what is pinning*, *young vs old generation*, *G1 vs ZGC*, *what causes `OutOfMemoryError: Metaspace`*, *ClassNotFoundException vs NoClassDefFoundError*, *how do you find a deadlock in production*.

## Day roadmap

1. Virtual threads (JEP 444)
2. JVM memory layout and garbage collection
3. Class loading, delegation, and class identity
4. Troubleshooting a live JVM: jstack, jcmd, jstat, VisualVM
5. Interview angles
6. Common mistakes & debugging
7. Further reading, glossary, answers

### Virtual threads (JEP 444)

#### What it is

A **virtual thread** is a `java.lang.Thread` instance whose stack lives on the heap as a growable *continuation* and which is scheduled by the JVM rather than the OS. The JVM mounts it on a **carrier thread** (a platform thread from a `ForkJoinPool`, by default `parallelism = #cores`). When the virtual thread performs a blocking operation that the JDK has made virtual-thread-aware (`Thread.sleep`, `java.util.concurrent` locks and queues, socket and file-channel I/O, `HttpClient`), the continuation is *unmounted* and its stack is parked on the heap; the carrier is free to run another virtual thread. Virtual threads are always daemon threads, have no thread-group of their own, always have priority 5, and cost roughly a few hundred bytes to a few KB instead of ~1 MB. Create them with `Thread.ofVirtual().name("worker-", 0).start(runnable)`, `Thread.startVirtualThread(runnable)`, `Thread.ofVirtual().factory()`, or (the most common) `Executors.newVirtualThreadPerTaskExecutor()` which starts a **new** virtual thread for every submitted task and is `AutoCloseable` (close waits for all tasks). `Thread.currentThread().isVirtual()` tells you which kind you are on.

#### Why it exists / why it matters

Thread-per-request code is the simplest to write and debug (stack traces, `try/catch`, thread-local context all behave normally), but platform threads make it unscalable. The alternatives (callbacks, reactive streams, `CompletableFuture` chains) scale but are harder to read, debug, and profile. Virtual threads restore the simple model: throughput is bounded by **how many tasks can be in flight** (Little's law: `concurrency = throughput x latency`), and for I/O-bound services that number is limited by memory, not by OS threads.

#### Pros and cons

**Pros**

- Blocking style code scales to 100k+ concurrent tasks with no code restructuring
- Normal stack traces, debugger, `ThreadLocal`, `try/finally` semantics
- Tiny footprint and near-zero creation cost; no need for tuning pool sizes
- Works with existing `ExecutorService`/`Future`/`Thread` APIs; thread dumps via `jcmd Thread.dump_to_file`

**Cons / tradeoffs**

- **No benefit for CPU-bound work** - the carrier pool is only `#cores` wide, so extra virtual threads just queue
- **Pinning**: a virtual thread blocking inside `synchronized` (Java 21) or a native/foreign call keeps its carrier blocked; watch with `-Djdk.tracePinnedThreads=full`
- `ThreadLocal`s are per virtual thread, so millions of tasks with heavy thread-locals waste memory; prefer passing context explicitly (scoped values are a preview feature)
- Unbounded creation can overload downstream resources (DB, remote service) - you must apply back-pressure yourself (`Semaphore`)

#### What happens without it / when misused

Pooling virtual threads (`newFixedThreadPool` with a virtual factory) re-introduces the very concurrency limit you wanted to remove and defeats the design: *virtual threads are cheap, so create one per task and let them die*. Running CPU-heavy loops on virtual threads gives you no speedup and can starve other virtual threads because the JVM does not preempt on time slices. Holding a `synchronized` monitor across blocking I/O pins the carrier; with many such threads the whole carrier pool is pinned and the app appears frozen (replace with `ReentrantLock`). Opening 100_000 virtual threads that each hit a database with a 20-connection pool simply moves the queue into the connection pool and causes timeouts: bound concurrency with a `Semaphore` at the resource boundary. Finally, caching expensive objects in `ThreadLocal` (the old "pooled thread" trick, e.g. `SimpleDateFormat`) now creates one copy *per task*.

#### Syntax and rules

- `Thread t = Thread.ofVirtual().name("worker-", 0).start(runnable);` (`.unstarted(r)` to start later; names `worker-0`, `worker-1`, ...).
- `Thread.startVirtualThread(runnable)` - shortcut without a name.
- `ThreadFactory f = Thread.ofVirtual().name("io-", 0).factory();` - plug into APIs that want a factory.
- `try (ExecutorService ex = Executors.newVirtualThreadPerTaskExecutor()) { futures = ex.invokeAll(tasks); }` - close() waits for completion (Java 19+ `ExecutorService` is `AutoCloseable`).
- `Thread.currentThread().isVirtual()`; `t.join()`; virtual threads ignore `setDaemon(false)` (always daemon) and `setPriority`.
- Limit concurrent access to a scarce resource: `Semaphore permits = new Semaphore(20); permits.acquire(); try { ... } finally { permits.release(); }`.
- Diagnose pinning: `-Djdk.tracePinnedThreads=full` (prints the stack when a virtual thread blocks while pinned); thread dump with `jcmd <pid> Thread.dump_to_file -format=json file.json`.
- Rule of thumb: **one virtual thread per task; platform pools for CPU work; semaphores for limits**.

#### Examples

**Example 1.1 — Tiny — start a virtual thread and inspect it**

```java
Thread t = Thread.ofVirtual().name("greeter-", 0).start(() ->
        System.out.println("hello from " + Thread.currentThread().getName()
                + " virtual=" + Thread.currentThread().isVirtual()));
t.join();       // hello from greeter-0 virtual=true
System.out.println(t.isDaemon());   // true - virtual threads are always daemon
```

**Example 1.2 — Tiny — 10_000 sleeping tasks in about a second**

```java
long start = System.nanoTime();
try (ExecutorService ex = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10_000; i++) {
        ex.submit(() -> { Thread.sleep(Duration.ofSeconds(1)); return null; });
    }
}   // close() waits for every task
System.out.println((System.nanoTime() - start) / 1_000_000 + " ms");   // ~1100 ms (a 200-thread platform pool needs ~50 s)
```

**Example 1.3 — Medium — fan-out with a concurrency limit**

```java
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

public class LimitedFanOut {
    public static void main(String[] args) throws Exception {
        Semaphore dbPermits = new Semaphore(5);           // protect a scarce resource
        AtomicInteger running = new AtomicInteger(), peak = new AtomicInteger();
        try (ExecutorService ex = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Future<Integer>> results = new ArrayList<>();
            for (int i = 0; i < 100; i++) {
                int id = i;
                results.add(ex.submit(() -> {
                    dbPermits.acquire();                  // virtual thread parks here, carrier is free
                    try {
                        peak.accumulateAndGet(running.incrementAndGet(), Math::max);
                        Thread.sleep(20);                 // pretend query
                        running.decrementAndGet();
                        return id * 2;
                    } finally {
                        dbPermits.release();
                    }
                }));
            }
            int sum = 0;
            for (Future<Integer> f : results) sum += f.get();
            System.out.println(sum + " peak=" + peak.get());   // 9900 peak=5
        }
    }
}
```

#### Quick checks

1. Why should you not put virtual threads in a fixed-size pool?
2. Which workloads do virtual threads help, and which do they not?
3. What is pinning?
4. How do you cap concurrent calls to a database when using 50_000 virtual threads?

### JVM memory layout and garbage collection

#### What it is

The JVM splits memory into several areas. The **heap** holds all objects and arrays and is divided (for generational collectors) into the **young generation** (Eden + two Survivor spaces, collected by frequent cheap *minor* GCs) and the **old generation** (long-lived objects, collected by rarer, costlier *major/mixed/full* GCs). **Metaspace** (native memory, replaced PermGen in Java 8) stores class metadata. Each thread has its own **stack** (frames, locals; `-Xss`), the **code cache** holds JIT-compiled code, and **direct buffers/native memory** (NIO, Netty, JNI) live outside the heap. The garbage collector finds objects that are no longer **reachable from GC roots** (thread stacks, static fields, JNI handles) and reclaims them. Collectors: **Serial** (single thread, tiny apps), **Parallel** (max throughput, stop-the-world), **G1** (default since Java 9; region-based, targets a pause goal via `-XX:MaxGCPauseMillis`), **ZGC** (`-XX:+UseZGC`; concurrent, sub-millisecond pauses even on huge heaps; generational by default in newer releases via `-XX:+ZGenerational` in 21). Sizing flags: `-Xms` initial heap, `-Xmx` max heap, `-XX:MaxMetaspaceSize`, `-Xss`, `-XX:+HeapDumpOnOutOfMemoryError`, `-XX:HeapDumpPath`. Logging: `-Xlog:gc*:file=gc.log`.

#### Why it exists / why it matters

Memory is the most common production problem after bugs: pauses spike latency, leaks end in `OutOfMemoryError`, and mis-sized containers get OOM-killed by the kernel. Knowing the layout lets you read GC logs and decide between *give it more heap*, *reduce allocation*, *switch collector*, or *fix the leak*. Almost every GC tuning conversation reduces to **throughput vs pause time vs footprint** - you cannot optimize all three.

#### Pros and cons

**Pros**

- Automatic memory management removes use-after-free and double-free bugs
- Generational collection is cheap because most objects die young
- Modern collectors (G1, ZGC) offer predictable pauses without manual tuning
- Rich tooling: unified GC logging, JFR, heap dumps

**Cons / tradeoffs**

- Stop-the-world pauses (less with G1, minimal with ZGC) and GC CPU overhead
- Memory leaks still exist: unintentionally *reachable* objects are never collected (static maps, listeners, `ThreadLocal`s, caches without eviction)
- Larger heaps mean longer full-GC pauses on non-concurrent collectors
- JVM uses much more than `-Xmx` (metaspace, stacks, direct memory, code cache) - containers need headroom

#### What happens without it / when misused

A **leak** shows up as a post-GC live set that keeps growing across full GCs until `java.lang.OutOfMemoryError: Java heap space` (or `GC overhead limit exceeded`: the JVM spends >98% of time in GC and frees <2%). Setting `-Xmx` equal to the container limit gets the process **OOM-killed** by the kernel because stacks, metaspace, and direct memory sit on top of the heap (exit code 137, no Java stack trace). `OutOfMemoryError: Metaspace` usually means a class-loader leak (redeploys, dynamic proxies). `OutOfMemoryError: unable to create native thread` means too many platform threads or too little native memory. Calling `System.gc()` in application code triggers a full collection and is almost always wrong. Retaining large `String`/`List` results in static caches without a size bound is the classic leak. Reference types matter: **strong** (normal), **soft** (cleared before OOM; memory-sensitive caches), **weak** (cleared at next GC; `WeakHashMap`, canonicalizing maps), **phantom** (post-mortem cleanup; `Cleaner`).

#### Syntax and rules

- Heap: `-Xms512m -Xmx2g` (set equal in servers to avoid resizing); `-XX:+UseG1GC` (default), `-XX:+UseZGC`, `-XX:+UseParallelGC`, `-XX:+UseSerialGC`.
- Pause goal: `-XX:MaxGCPauseMillis=200` (G1 hint, not a guarantee).
- Containers: prefer `-XX:MaxRAMPercentage=75.0` over hard-coding `-Xmx`.
- GC log (unified logging): `-Xlog:gc*:file=gc.log:time,uptime,level,tags`. A typical line: `[2.345s][info][gc] GC(12) Pause Young (Normal) (G1 Evacuation Pause) 24M->4M(256M) 5.123ms` = before->after(committed) and pause.
- Crash evidence: `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/dumps`.
- Runtime numbers: `Runtime.getRuntime().totalMemory()/freeMemory()/maxMemory()`; MXBeans: `ManagementFactory.getMemoryMXBean()`, `getGarbageCollectorMXBeans()`.
- Reading a leak: after each **Full** GC, compare the "after" size; a monotonically rising floor = leak.

#### Examples

**Example 2.1 — Tiny — what the JVM thinks about memory**

```java
Runtime rt = Runtime.getRuntime();
long used = rt.totalMemory() - rt.freeMemory();
System.out.println("used=" + used / (1024 * 1024) + " MiB, max=" + rt.maxMemory() / (1024 * 1024) + " MiB");
```

**Example 2.2 — Tiny — weak vs strong reachability**

```java
Object payload = new Object();
WeakReference<Object> weak = new WeakReference<>(payload);
System.out.println(weak.get() != null);   // true - still strongly referenced by 'payload'
payload = null;
System.gc();                               // only a hint; for demos only
System.out.println(weak.get() == null);    // usually true: only weakly reachable -> collected
```

**Example 2.3 — Medium — a classic leak and its fix**

```java
import java.util.*;

public class LeakDemo {
    // LEAK: static map keeps every session forever
    private static final Map<String, byte[]> CACHE = new HashMap<>();

    static void handle(String sessionId) {
        CACHE.put(sessionId, new byte[1_000_000]);   // never removed -> live set grows after every GC
    }

    // FIX: bounded LRU (evicts eldest) - the post-GC live set now plateaus
    private static final Map<String, byte[]> BOUNDED = new LinkedHashMap<>(16, 0.75f, true) {
        @Override
        protected boolean removeEldestEntry(Map.Entry<String, byte[]> eldest) {
            return size() > 100;
        }
    };

    static void handleFixed(String sessionId) {
        BOUNDED.put(sessionId, new byte[1_000_000]);
    }
}
```

#### Quick checks

1. Why are young-generation collections cheap?
2. What does `24M->4M(256M) 5.1ms` in a GC log mean?
3. Why can a container with `-Xmx` equal to its memory limit still be OOM-killed?
4. What is the signature of a memory leak in GC logs?

### Class loading, delegation, and class identity

#### What it is

A class is loaded **lazily** the first time it is needed, then **linked** (verify bytecode, prepare static fields with default values, resolve symbolic references) and finally **initialized** (static initializers and static field assignments run exactly once, thread-safely). Loading is done by **class loaders** arranged in a hierarchy: the **bootstrap** loader (native, loads `java.base` and other core modules; `getClassLoader()` returns `null`), the **platform** loader (other JDK modules), and the **application** (system) loader (your classpath). `ClassLoader.loadClass` follows **parent-first delegation**: ask the parent, and only if it cannot find the class does the loader call `findClass` itself. That guarantees `java.lang.String` always comes from the JDK and cannot be spoofed. A class's runtime identity is the pair **(fully qualified name, defining class loader)**: the same bytes loaded by two loaders produce two unrelated `Class` objects with separate static state, and instances are *not* assignable to each other (`ClassCastException: X cannot be cast to X`). Custom loaders power plugin systems, application servers (one loader per webapp), hot reload, and frameworks that generate classes. `ServiceLoader` discovers implementations listed in `META-INF/services` or `module-info.java`.

#### Why it exists / why it matters

Understanding loading explains a family of errors (`ClassNotFoundException`, `NoClassDefFoundError`, `NoSuchMethodError`, `LinkageError`, `ExceptionInInitializerError`) and the isolation features of application servers and plugin hosts. It also explains classpath ordering bugs where two versions of a library coexist and the *first one on the classpath wins*.

#### Pros and cons

**Pros**

- Lazy loading keeps startup fast and memory low
- Delegation protects core classes and avoids duplicate loading
- Custom loaders enable isolation, plugins, and hot reload
- Initialization runs once under a lock, giving safe publication of static state

**Cons / tradeoffs**

- Class identity pitfalls (same class, two loaders, `ClassCastException`)
- Leaked loaders keep all their classes alive (metaspace leaks on redeploy)
- Static initializer failures are sticky: the first fails with `ExceptionInInitializerError`, later uses fail with `NoClassDefFoundError`
- Classpath conflicts (jar hell) are resolved by order, not by version

#### What happens without it / when misused

**`ClassNotFoundException`** is a checked exception thrown when code *asks by name* (`Class.forName`, `loadClass`) and no loader can find it. **`NoClassDefFoundError`** is an `Error` thrown when a class that was present at compile time is missing at runtime (or its static initializer previously failed). Two versions of a library on the classpath produce `NoSuchMethodError` at the first call to a method that only exists in the version that lost. A web-app loader that is referenced from a static field in a shared library (JDBC driver registration, `ThreadLocal`, a thread started by the app) can never be collected, so every redeploy leaks the whole class graph until `OutOfMemoryError: Metaspace`. Overriding `loadClass` to be **child-first** for your own packages (as servlet containers do) is legitimate but must never be applied to `java.*`.

#### Syntax and rules

- Introspection: `Foo.class.getClassLoader()` (`null` for bootstrap classes), `ClassLoader.getSystemClassLoader()`, `loader.getParent()`, `loader.getName()` (`app`, `platform`).
- Load by name: `Class.forName("com.acme.Foo")` (initializes), `loader.loadClass("com.acme.Foo")` (does not initialize).
- Custom loader: extend `ClassLoader`, call `super(parent)`, override **`findClass(String)`** to keep delegation (and call `defineClass(name, bytes, 0, len)`), or override `loadClass(String, boolean)` only when you deliberately break parent-first.
- Always synchronize on `getClassLoadingLock(name)` when overriding `loadClass`; check `findLoadedClass(name)` first.
- Read class bytes: `Foo.class.getResourceAsStream("/com/acme/Foo.class")`.
- Compare classes: `a == b` (same `Class` object) - *not* `a.getName().equals(b.getName())`.
- Debug: `-verbose:class` or `-Xlog:class+load` prints every load with its source.

#### Examples

**Example 3.1 — Tiny — who loads what**

```java
System.out.println(String.class.getClassLoader());                // null  (bootstrap)
System.out.println(java.sql.Driver.class.getClassLoader());       // jdk.internal.loader.ClassLoaders$PlatformClassLoader
System.out.println(Main.class.getClassLoader());                  // jdk.internal.loader.ClassLoaders$AppClassLoader
for (ClassLoader l = Main.class.getClassLoader(); l != null; l = l.getParent()) {
    System.out.println(l.getName());                              // app, platform
}
```

**Example 3.2 — Tiny — class identity is name + loader**

```java
// Pseudo: two loaders define the same bytes
Class<?> a = loaderA.loadClass("com.acme.Plugin");
Class<?> b = loaderB.loadClass("com.acme.Plugin");
System.out.println(a == b);                    // false
System.out.println(a.getName().equals(b.getName()));  // true
Object o = a.getDeclaredConstructor().newInstance();
System.out.println(b.isInstance(o));           // false -> ClassCastException if you cast
```

**Example 3.3 — Medium — a loader that defines a class from bytes**

```java
import java.util.Map;

public class BytesLoader extends ClassLoader {
    private final Map<String, byte[]> classes;

    public BytesLoader(ClassLoader parent, Map<String, byte[]> classes) {
        super(parent);                      // parent-first delegation for everything else
        this.classes = Map.copyOf(classes);
    }

    @Override
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        byte[] bytes = classes.get(name);
        if (bytes == null) throw new ClassNotFoundException(name);
        return defineClass(name, bytes, 0, bytes.length);
    }
}
```

#### Quick checks

1. What is the difference between `ClassNotFoundException` and `NoClassDefFoundError`?
2. Why does parent-first delegation exist?
3. Can two classes with the same name coexist in one JVM?
4. `Class.forName(name)` vs `loader.loadClass(name)`?

### Troubleshooting a live JVM: jstack, jcmd, jstat, VisualVM

#### What it is

The JDK ships with diagnostic tools that attach to a running process. **`jps -l`** (or `pgrep java`) lists JVM process ids. **`jstack <pid>`** (or `jcmd <pid> Thread.print`) prints every thread's state, stack, and held/awaited monitors, and reports **Java-level deadlocks** automatically at the end. **`jcmd <pid> help`** lists commands such as `GC.heap_info`, `GC.class_histogram`, `GC.heap_dump file.hprof`, `VM.flags`, `VM.system_properties`, `Thread.dump_to_file -format=json file.json` (includes virtual threads), and `JFR.start`. **`jstat -gcutil <pid> 1000`** prints GC occupancy and counts every second. **VisualVM** (and JDK Mission Control for **JFR** recordings) shows heap, threads, CPU sampling, and opens `.hprof` heap dumps to find the *dominator tree* and *GC roots* that keep objects alive. Thread states you must recognise: `RUNNABLE` (running or in native I/O), `BLOCKED` (waiting for a monitor), `WAITING`/`TIMED_WAITING` (`wait`, `park`, `sleep`, `join`), `NEW`, `TERMINATED`. Inside the JVM, `ManagementFactory.getThreadMXBean().findDeadlockedThreads()` detects monitor *and* lock deadlocks programmatically.

#### Why it exists / why it matters

Production problems rarely reproduce on a laptop. The only evidence you often get is a **thread dump** (what is everyone doing right now?), a **heap histogram or dump** (what is filling memory?), and **GC logs** (when and how long did pauses happen?). Being able to take and read them quickly is a core senior-engineer skill and a standard interview scenario.

#### Pros and cons

**Pros**

- Zero code changes needed; attach to a running JVM
- Thread dumps show lock owners and waiters, making deadlocks and contention obvious
- Class histograms and dumps pinpoint leaks
- JFR has very low overhead and is safe in production

**Cons / tradeoffs**

- A heap dump pauses the JVM and can be as large as the heap (disk, privacy: it contains secrets)
- `jstack` needs the same user as the target process
- A single thread dump is a snapshot; take 3 dumps 5-10 s apart to see what is *stuck* vs *moving*
- Tools differ across JDK vendors/versions; container images often ship only a JRE

#### What happens without it / when misused

Without these tools teams restart the process and lose the evidence. Typical mistakes: taking only one thread dump (cannot tell stuck from busy), forgetting that `top -H` thread ids are **decimal** while `jstack` shows `nid=0x...` in **hex**, analysing a heap dump taken *before* the leak grew, and sharing `.hprof` files that contain passwords and tokens. A CPU spike diagnosed by guessing at code instead of sampling threads wastes hours; a hang that is actually a thread-pool starvation (all workers `WAITING` on futures) looks like a deadlock but is not reported as one.

#### Syntax and rules

- Find the pid: `jps -l`; Linux: `pgrep -f myapp.jar`.
- Thread dump: `jstack -l <pid> > dump1.txt` (repeat 3x, 5 s apart) or `jcmd <pid> Thread.print`.
- Hot thread workflow: `top -H -p <pid>` -> busiest thread id (decimal) -> `printf '%x\n' <tid>` -> search `nid=0x<hex>` in the thread dump.
- Heap quick look: `jcmd <pid> GC.class_histogram | head -20`; `jcmd <pid> GC.heap_info`.
- Heap dump: `jcmd <pid> GC.heap_dump /tmp/heap.hprof` (open in VisualVM/Eclipse MAT; find the dominator tree and path to GC roots).
- GC activity: `jstat -gcutil <pid> 1000 10` (S0 S1 E O M CCS YGC YGCT FGC FGCT GCT).
- Flags and properties: `jcmd <pid> VM.flags`, `jcmd <pid> VM.system_properties`.
- Dump including virtual threads: `jcmd <pid> Thread.dump_to_file -format=json /tmp/threads.json`.
- Deadlock in code: `ThreadMXBean bean = ManagementFactory.getThreadMXBean(); long[] ids = bean.findDeadlockedThreads();` (null when none).
- Thread dump anatomy: header `"name" #id prio=.. nid=0x..`, `java.lang.Thread.State: BLOCKED`, frames `at pkg.Class.method(File.java:12)`, and `- waiting to lock <0x...>` / `- locked <0x...>`.

#### Examples

**Example 4.1 — Tiny — a thread dump excerpt**

```java
"worker-1" #21 prio=5 os_prio=0 tid=0x00007f nid=0x1c03 waiting for monitor entry
   java.lang.Thread.State: BLOCKED (on object monitor)
	at com.acme.Accounts.transfer(Accounts.java:42)
	- waiting to lock <0x000000076ab62208> (a java.lang.Object)
	- locked <0x000000076ab62218> (a java.lang.Object)
```

**Example 4.2 — Tiny — detecting deadlock from inside the JVM**

```java
ThreadMXBean bean = ManagementFactory.getThreadMXBean();
long[] ids = bean.findDeadlockedThreads();       // null when there is no deadlock
if (ids != null) {
    for (ThreadInfo info : bean.getThreadInfo(ids)) {
        System.out.println("deadlocked: " + info.getThreadName() + " waits for " + info.getLockName());
    }
}
```

**Example 4.3 — Medium — a deadlock you can diagnose with jstack**

```java
import java.util.concurrent.locks.ReentrantLock;

public class DeadlockDemo {
    static final ReentrantLock A = new ReentrantLock(), B = new ReentrantLock();

    public static void main(String[] args) throws Exception {
        Thread t1 = new Thread(() -> lockBoth(A, B), "t1");
        Thread t2 = new Thread(() -> lockBoth(B, A), "t2");     // opposite order -> deadlock
        t1.start(); t2.start();
        Thread.sleep(60_000);       // run `jstack <pid>`: it prints "Found one Java-level deadlock:"
    }

    static void lockBoth(ReentrantLock first, ReentrantLock second) {
        first.lock();
        try {
            try { Thread.sleep(100); } catch (InterruptedException e) { return; }
            second.lock();
            try { System.out.println("never reached"); } finally { second.unlock(); }
        } finally {
            first.unlock();
        }
    }
    // Fix: always acquire locks in one global order, or use tryLock with a timeout.
}
```

#### Quick checks

1. Why take several thread dumps instead of one?
2. `top -H` shows thread id 7171; how do you find it in a jstack dump?
3. How do you quickly see which classes fill the heap?
4. How do you fix a lock-ordering deadlock?

## Interview angles

**Q: What are virtual threads and how are they different from platform threads?**

JVM-scheduled lightweight threads (JEP 444) whose stacks live on the heap and that are multiplexed onto a few carrier threads; blocking operations unmount them so a carrier can run others. They allow thread-per-request code to scale to very high concurrency.

**Q: When would you NOT use virtual threads?**

CPU-bound work (no speedup, only `#cores` carriers), code that blocks inside `synchronized` or native calls on Java 21 (pinning), or when you rely on big per-thread caches in `ThreadLocal`.

**Q: Explain young vs old generation and how a minor GC differs from a full GC.**

New objects start in Eden; survivors are copied between survivor spaces and eventually promoted to old. A minor GC collects only the young generation (fast, frequent). A full GC collects the whole heap (slow, ideally rare).

**Q: How do you choose between G1 and ZGC?**

G1 is a balanced default with a pause target of ~100-200 ms; ZGC does most work concurrently for pauses under a millisecond on very large heaps at some throughput/CPU cost. Measure with your workload and GC logs.

**Q: A service slowly gets slower and finally throws OutOfMemoryError. How do you investigate?**

Enable GC logs and `-XX:+HeapDumpOnOutOfMemoryError`, check whether the post-full-GC live set rises, take `GC.class_histogram` snapshots over time, open a heap dump in VisualVM/MAT and follow the path-to-GC-roots of the biggest dominators.

**Q: ClassNotFoundException vs NoClassDefFoundError?**

The first is a checked exception from loading by name; the second is a linkage `Error` for a class that existed at compile time but is missing (or failed static initialization) at runtime.

**Q: An app hangs and CPU is idle. What do you do?**

Take 3 thread dumps with `jstack`, look for `BLOCKED` threads and the `Found one Java-level deadlock` section, check for pool starvation (all workers `WAITING` on futures), and identify lock owners from `- locked <0x...>` lines.

## Common mistakes & debugging

- Pooling virtual threads or caching them; they are meant to be created per task.
- Blocking inside `synchronized` on a virtual thread (pinning) - use `ReentrantLock` instead.
- Using virtual threads for CPU-heavy loops and expecting speedup.
- Setting `-Xmx` to the full container memory and then being OOM-killed with exit code 137.
- Treating `System.gc()` as a performance tool.
- Static caches without eviction; `ThreadLocal`s that are never `remove()`d.
- Confusing `ClassNotFoundException` (name lookup) with `NoClassDefFoundError` (runtime linkage).
- Taking one thread dump and concluding; or mixing decimal thread ids with hex `nid` values.
- Sharing heap dumps without scrubbing; they contain secrets.

## Further reading

- JEP 444: Virtual Threads (openjdk.org/jeps/444) and the *Virtual Threads* chapter of the Oracle Java 21 core libraries guide
- JEP 425/428/453 (preview history): structured concurrency and scoped values - read the motivation sections
- Oracle *HotSpot Virtual Machine Garbage Collection Tuning Guide* (Java 21)
- JEP 333 (ZGC) and JEP 248 (G1 as default); `java -Xlog:help`
- *Java Language Specification* chapter 12 (loading, linking, initialization) and Javadoc of `ClassLoader`
- Oracle *Troubleshooting Guide for JDK*: `jcmd`, `jstack`, `jstat`, JFR; VisualVM documentation (visualvm.github.io)

## Glossary

| Term | Meaning |
|------|---------|
| Virtual thread | JVM-scheduled lightweight thread whose stack lives on the heap |
| Carrier thread | Platform thread on which a virtual thread is currently mounted |
| Pinning | A virtual thread blocking while it cannot be unmounted (monitor, native frame) |
| Young / Old generation | Heap regions for new vs long-lived objects |
| Metaspace | Native memory area holding class metadata |
| GC root | Starting reference (stack, static, JNI) from which reachability is computed |
| Stop-the-world | Pause where all application threads are halted for GC work |
| Class loader | Object that defines classes from bytes; part of a class's identity |
| Parent-first delegation | Loader asks its parent to load a class before trying itself |
| Thread dump | Snapshot of all threads, their states, stacks, and locks |
| Heap dump | Binary snapshot of all live objects (`.hprof`) |
| JFR | Java Flight Recorder: low-overhead event recorder built into the JVM |

## Answers

Answers to every **Quick check** above (numbered `section.question`).

- **1.1** — Why should you not put virtual threads in a fixed-size pool?  
  They are cheap and meant to be created per task; pooling them re-imposes a concurrency cap and gives no reuse benefit.

- **1.2** — Which workloads do virtual threads help, and which do they not?  
  They help blocking, I/O-bound workloads with many concurrent tasks; they do not speed up CPU-bound work because only `#cores` carrier threads run.

- **1.3** — What is pinning?  
  A virtual thread that blocks while holding a monitor (`synchronized` in Java 21) or inside a native call stays mounted and blocks its carrier thread, reducing scalability.

- **1.4** — How do you cap concurrent calls to a database when using 50_000 virtual threads?  
  Guard the call with a `Semaphore` (or a bounded resource pool); the virtual threads simply park while waiting for a permit.

- **2.1** — Why are young-generation collections cheap?  
  Most objects die young, so a minor GC copies only the few survivors and ignores the dead objects entirely.

- **2.2** — What does `24M->4M(256M) 5.1ms` in a GC log mean?  
  Heap usage before the pause was 24 MiB, after it 4 MiB, with 256 MiB committed, and the pause lasted 5.1 ms.

- **2.3** — Why can a container with `-Xmx` equal to its memory limit still be OOM-killed?  
  The JVM also uses native memory (metaspace, thread stacks, code cache, direct buffers), so total usage exceeds `-Xmx`.

- **2.4** — What is the signature of a memory leak in GC logs?  
  The heap size *after* full GCs keeps rising until OutOfMemoryError (a growing live-set floor).

- **3.1** — What is the difference between `ClassNotFoundException` and `NoClassDefFoundError`?  
  The first is a checked exception from an explicit load-by-name that failed; the second is an `Error` raised when a class that was available at compile time cannot be found (or failed to initialize) at runtime.

- **3.2** — Why does parent-first delegation exist?  
  It guarantees core classes like `java.lang.Object` come from the JDK and avoids loading the same class twice.

- **3.3** — Can two classes with the same name coexist in one JVM?  
  Yes, if they are defined by different class loaders; they are distinct types with separate static state.

- **3.4** — `Class.forName(name)` vs `loader.loadClass(name)`?  
  `forName` also initializes the class (runs static initializers); `loadClass` only loads it.

- **4.1** — Why take several thread dumps instead of one?  
  A single dump is a snapshot; comparing dumps over time shows which threads are really stuck versus just busy.

- **4.2** — `top -H` shows thread id 7171; how do you find it in a jstack dump?  
  Convert 7171 to hex (0x1c03) and search for `nid=0x1c03`.

- **4.3** — How do you quickly see which classes fill the heap?  
  `jcmd <pid> GC.class_histogram` (or `jmap -histo`), then a heap dump analysed in VisualVM or MAT for the dominator tree.

- **4.4** — How do you fix a lock-ordering deadlock?  
  Acquire locks in a single global order, or use `tryLock` with a timeout and back off.
