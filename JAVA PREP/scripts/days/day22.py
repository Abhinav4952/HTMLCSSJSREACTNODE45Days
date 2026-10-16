from gen_helpers import sec, task

DAY = dict(
    num=22,
    title="Virtual Threads (Java 21), JVM Memory & GC, Class Loading, and Troubleshooting",
    theme="Scale blocking code with virtual threads, understand how the JVM lays out memory and loads classes, and diagnose live JVMs with jstack, jcmd, and VisualVM.",
    objectives=[
        "Create virtual threads with `Thread.ofVirtual()`, `Thread.startVirtualThread`, and `Executors.newVirtualThreadPerTaskExecutor()` and explain when they help (blocking I/O) and when they do not (CPU-bound work)",
        "Explain pinning, `ThreadLocal` cost, and why virtual threads must never be pooled; limit concurrency with a `Semaphore` instead",
        "Describe heap generations, metaspace, thread stacks, and direct memory, and pick a collector (Serial, Parallel, G1, ZGC) with the right `-Xms/-Xmx/-XX` flags",
        "Read unified GC logs (`-Xlog:gc*`) and spot a leak from a rising post-GC live set",
        "Explain parent-first delegation, class identity (`name + defining loader`), and the difference between `ClassNotFoundException` and `NoClassDefFoundError`",
        "Diagnose hangs, deadlocks, high CPU, and `OutOfMemoryError` with `jps`, `jstack`, `jcmd`, `jstat`, heap dumps, and VisualVM",
    ],
    prereqs=["Day 20 — threads, synchronized, volatile", "Day 21 — ExecutorService, CompletableFuture, locks", "Day 13 — exceptions and stack traces"],
    overview="""Day 21 showed how to run work on **bounded platform-thread pools**. That model has a ceiling: a platform thread maps 1:1 to an OS thread (about 1 MB of stack reserved, expensive to create and to context-switch), so a server that blocks one thread per request tops out at a few thousand concurrent requests. **Virtual threads** (JEP 444, final in Java 21) are cheap, JVM-scheduled threads multiplexed onto a small pool of carrier threads. When a virtual thread blocks on I/O, `sleep`, a lock, or a queue it is *unmounted* and the carrier runs something else. You keep the simple blocking, thread-per-request style and still scale to hundreds of thousands of concurrent tasks.

Virtual threads sit on top of the JVM, so the second half of the day looks underneath: **where memory lives** (heap young/old, metaspace, stacks, code cache, direct buffers), **how the garbage collectors differ** (throughput vs latency), **how classes get loaded** (bootstrap/platform/app loaders, parent-first delegation, class identity), and **how to troubleshoot a misbehaving JVM** (thread dumps, heap histograms, GC logs, VisualVM). Interviews love these: *why can virtual threads be slow for CPU work*, *what is pinning*, *young vs old generation*, *G1 vs ZGC*, *what causes `OutOfMemoryError: Metaspace`*, *ClassNotFoundException vs NoClassDefFoundError*, *how do you find a deadlock in production*.""",
    sections=[
        sec(
            "Virtual threads (JEP 444)",
            "A **virtual thread** is a `java.lang.Thread` instance whose stack lives on the heap as a growable *continuation* and which is scheduled by the JVM rather than the OS. The JVM mounts it on a **carrier thread** (a platform thread from a `ForkJoinPool`, by default `parallelism = #cores`). When the virtual thread performs a blocking operation that the JDK has made virtual-thread-aware (`Thread.sleep`, `java.util.concurrent` locks and queues, socket and file-channel I/O, `HttpClient`), the continuation is *unmounted* and its stack is parked on the heap; the carrier is free to run another virtual thread. Virtual threads are always daemon threads, have no thread-group of their own, always have priority 5, and cost roughly a few hundred bytes to a few KB instead of ~1 MB. Create them with `Thread.ofVirtual().name(\"worker-\", 0).start(runnable)`, `Thread.startVirtualThread(runnable)`, `Thread.ofVirtual().factory()`, or (the most common) `Executors.newVirtualThreadPerTaskExecutor()` which starts a **new** virtual thread for every submitted task and is `AutoCloseable` (close waits for all tasks). `Thread.currentThread().isVirtual()` tells you which kind you are on.",
            "Thread-per-request code is the simplest to write and debug (stack traces, `try/catch`, thread-local context all behave normally), but platform threads make it unscalable. The alternatives (callbacks, reactive streams, `CompletableFuture` chains) scale but are harder to read, debug, and profile. Virtual threads restore the simple model: throughput is bounded by **how many tasks can be in flight** (Little's law: `concurrency = throughput x latency`), and for I/O-bound services that number is limited by memory, not by OS threads.",
            ["Blocking style code scales to 100k+ concurrent tasks with no code restructuring", "Normal stack traces, debugger, `ThreadLocal`, `try/finally` semantics", "Tiny footprint and near-zero creation cost; no need for tuning pool sizes", "Works with existing `ExecutorService`/`Future`/`Thread` APIs; thread dumps via `jcmd Thread.dump_to_file`"],
            ["**No benefit for CPU-bound work** - the carrier pool is only `#cores` wide, so extra virtual threads just queue", "**Pinning**: a virtual thread blocking inside `synchronized` (Java 21) or a native/foreign call keeps its carrier blocked; watch with `-Djdk.tracePinnedThreads=full`", "`ThreadLocal`s are per virtual thread, so millions of tasks with heavy thread-locals waste memory; prefer passing context explicitly (scoped values are a preview feature)", "Unbounded creation can overload downstream resources (DB, remote service) - you must apply back-pressure yourself (`Semaphore`)"],
            "Pooling virtual threads (`newFixedThreadPool` with a virtual factory) re-introduces the very concurrency limit you wanted to remove and defeats the design: *virtual threads are cheap, so create one per task and let them die*. Running CPU-heavy loops on virtual threads gives you no speedup and can starve other virtual threads because the JVM does not preempt on time slices. Holding a `synchronized` monitor across blocking I/O pins the carrier; with many such threads the whole carrier pool is pinned and the app appears frozen (replace with `ReentrantLock`). Opening 100_000 virtual threads that each hit a database with a 20-connection pool simply moves the queue into the connection pool and causes timeouts: bound concurrency with a `Semaphore` at the resource boundary. Finally, caching expensive objects in `ThreadLocal` (the old \"pooled thread\" trick, e.g. `SimpleDateFormat`) now creates one copy *per task*.",
            """- `Thread t = Thread.ofVirtual().name("worker-", 0).start(runnable);` (`.unstarted(r)` to start later; names `worker-0`, `worker-1`, ...).
- `Thread.startVirtualThread(runnable)` - shortcut without a name.
- `ThreadFactory f = Thread.ofVirtual().name("io-", 0).factory();` - plug into APIs that want a factory.
- `try (ExecutorService ex = Executors.newVirtualThreadPerTaskExecutor()) { futures = ex.invokeAll(tasks); }` - close() waits for completion (Java 19+ `ExecutorService` is `AutoCloseable`).
- `Thread.currentThread().isVirtual()`; `t.join()`; virtual threads ignore `setDaemon(false)` (always daemon) and `setPriority`.
- Limit concurrent access to a scarce resource: `Semaphore permits = new Semaphore(20); permits.acquire(); try { ... } finally { permits.release(); }`.
- Diagnose pinning: `-Djdk.tracePinnedThreads=full` (prints the stack when a virtual thread blocks while pinned); thread dump with `jcmd <pid> Thread.dump_to_file -format=json file.json`.
- Rule of thumb: **one virtual thread per task; platform pools for CPU work; semaphores for limits**.""",
            [
                ("Tiny — start a virtual thread and inspect it", """Thread t = Thread.ofVirtual().name("greeter-", 0).start(() ->
        System.out.println("hello from " + Thread.currentThread().getName()
                + " virtual=" + Thread.currentThread().isVirtual()));
t.join();       // hello from greeter-0 virtual=true
System.out.println(t.isDaemon());   // true - virtual threads are always daemon"""),
                ("Tiny — 10_000 sleeping tasks in about a second", """long start = System.nanoTime();
try (ExecutorService ex = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10_000; i++) {
        ex.submit(() -> { Thread.sleep(Duration.ofSeconds(1)); return null; });
    }
}   // close() waits for every task
System.out.println((System.nanoTime() - start) / 1_000_000 + " ms");   // ~1100 ms (a 200-thread platform pool needs ~50 s)"""),
                ("Medium — fan-out with a concurrency limit", """import java.util.*;
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
}"""),
            ],
            [
                ("Why should you not put virtual threads in a fixed-size pool?", "They are cheap and meant to be created per task; pooling them re-imposes a concurrency cap and gives no reuse benefit."),
                ("Which workloads do virtual threads help, and which do they not?", "They help blocking, I/O-bound workloads with many concurrent tasks; they do not speed up CPU-bound work because only `#cores` carrier threads run."),
                ("What is pinning?", "A virtual thread that blocks while holding a monitor (`synchronized` in Java 21) or inside a native call stays mounted and blocks its carrier thread, reducing scalability."),
                ("How do you cap concurrent calls to a database when using 50_000 virtual threads?", "Guard the call with a `Semaphore` (or a bounded resource pool); the virtual threads simply park while waiting for a permit."),
            ],
        ),
        sec(
            "JVM memory layout and garbage collection",
            "The JVM splits memory into several areas. The **heap** holds all objects and arrays and is divided (for generational collectors) into the **young generation** (Eden + two Survivor spaces, collected by frequent cheap *minor* GCs) and the **old generation** (long-lived objects, collected by rarer, costlier *major/mixed/full* GCs). **Metaspace** (native memory, replaced PermGen in Java 8) stores class metadata. Each thread has its own **stack** (frames, locals; `-Xss`), the **code cache** holds JIT-compiled code, and **direct buffers/native memory** (NIO, Netty, JNI) live outside the heap. The garbage collector finds objects that are no longer **reachable from GC roots** (thread stacks, static fields, JNI handles) and reclaims them. Collectors: **Serial** (single thread, tiny apps), **Parallel** (max throughput, stop-the-world), **G1** (default since Java 9; region-based, targets a pause goal via `-XX:MaxGCPauseMillis`), **ZGC** (`-XX:+UseZGC`; concurrent, sub-millisecond pauses even on huge heaps; generational by default in newer releases via `-XX:+ZGenerational` in 21). Sizing flags: `-Xms` initial heap, `-Xmx` max heap, `-XX:MaxMetaspaceSize`, `-Xss`, `-XX:+HeapDumpOnOutOfMemoryError`, `-XX:HeapDumpPath`. Logging: `-Xlog:gc*:file=gc.log`.",
            "Memory is the most common production problem after bugs: pauses spike latency, leaks end in `OutOfMemoryError`, and mis-sized containers get OOM-killed by the kernel. Knowing the layout lets you read GC logs and decide between *give it more heap*, *reduce allocation*, *switch collector*, or *fix the leak*. Almost every GC tuning conversation reduces to **throughput vs pause time vs footprint** - you cannot optimize all three.",
            ["Automatic memory management removes use-after-free and double-free bugs", "Generational collection is cheap because most objects die young", "Modern collectors (G1, ZGC) offer predictable pauses without manual tuning", "Rich tooling: unified GC logging, JFR, heap dumps"],
            ["Stop-the-world pauses (less with G1, minimal with ZGC) and GC CPU overhead", "Memory leaks still exist: unintentionally *reachable* objects are never collected (static maps, listeners, `ThreadLocal`s, caches without eviction)", "Larger heaps mean longer full-GC pauses on non-concurrent collectors", "JVM uses much more than `-Xmx` (metaspace, stacks, direct memory, code cache) - containers need headroom"],
            "A **leak** shows up as a post-GC live set that keeps growing across full GCs until `java.lang.OutOfMemoryError: Java heap space` (or `GC overhead limit exceeded`: the JVM spends >98% of time in GC and frees <2%). Setting `-Xmx` equal to the container limit gets the process **OOM-killed** by the kernel because stacks, metaspace, and direct memory sit on top of the heap (exit code 137, no Java stack trace). `OutOfMemoryError: Metaspace` usually means a class-loader leak (redeploys, dynamic proxies). `OutOfMemoryError: unable to create native thread` means too many platform threads or too little native memory. Calling `System.gc()` in application code triggers a full collection and is almost always wrong. Retaining large `String`/`List` results in static caches without a size bound is the classic leak. Reference types matter: **strong** (normal), **soft** (cleared before OOM; memory-sensitive caches), **weak** (cleared at next GC; `WeakHashMap`, canonicalizing maps), **phantom** (post-mortem cleanup; `Cleaner`).",
            """- Heap: `-Xms512m -Xmx2g` (set equal in servers to avoid resizing); `-XX:+UseG1GC` (default), `-XX:+UseZGC`, `-XX:+UseParallelGC`, `-XX:+UseSerialGC`.
- Pause goal: `-XX:MaxGCPauseMillis=200` (G1 hint, not a guarantee).
- Containers: prefer `-XX:MaxRAMPercentage=75.0` over hard-coding `-Xmx`.
- GC log (unified logging): `-Xlog:gc*:file=gc.log:time,uptime,level,tags`. A typical line: `[2.345s][info][gc] GC(12) Pause Young (Normal) (G1 Evacuation Pause) 24M->4M(256M) 5.123ms` = before->after(committed) and pause.
- Crash evidence: `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/dumps`.
- Runtime numbers: `Runtime.getRuntime().totalMemory()/freeMemory()/maxMemory()`; MXBeans: `ManagementFactory.getMemoryMXBean()`, `getGarbageCollectorMXBeans()`.
- Reading a leak: after each **Full** GC, compare the "after" size; a monotonically rising floor = leak.""",
            [
                ("Tiny — what the JVM thinks about memory", """Runtime rt = Runtime.getRuntime();
long used = rt.totalMemory() - rt.freeMemory();
System.out.println("used=" + used / (1024 * 1024) + " MiB, max=" + rt.maxMemory() / (1024 * 1024) + " MiB");"""),
                ("Tiny — weak vs strong reachability", """Object payload = new Object();
WeakReference<Object> weak = new WeakReference<>(payload);
System.out.println(weak.get() != null);   // true - still strongly referenced by 'payload'
payload = null;
System.gc();                               // only a hint; for demos only
System.out.println(weak.get() == null);    // usually true: only weakly reachable -> collected"""),
                ("Medium — a classic leak and its fix", """import java.util.*;

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
}"""),
            ],
            [
                ("Why are young-generation collections cheap?", "Most objects die young, so a minor GC copies only the few survivors and ignores the dead objects entirely."),
                ("What does `24M->4M(256M) 5.1ms` in a GC log mean?", "Heap usage before the pause was 24 MiB, after it 4 MiB, with 256 MiB committed, and the pause lasted 5.1 ms."),
                ("Why can a container with `-Xmx` equal to its memory limit still be OOM-killed?", "The JVM also uses native memory (metaspace, thread stacks, code cache, direct buffers), so total usage exceeds `-Xmx`."),
                ("What is the signature of a memory leak in GC logs?", "The heap size *after* full GCs keeps rising until OutOfMemoryError (a growing live-set floor)."),
            ],
        ),
        sec(
            "Class loading, delegation, and class identity",
            "A class is loaded **lazily** the first time it is needed, then **linked** (verify bytecode, prepare static fields with default values, resolve symbolic references) and finally **initialized** (static initializers and static field assignments run exactly once, thread-safely). Loading is done by **class loaders** arranged in a hierarchy: the **bootstrap** loader (native, loads `java.base` and other core modules; `getClassLoader()` returns `null`), the **platform** loader (other JDK modules), and the **application** (system) loader (your classpath). `ClassLoader.loadClass` follows **parent-first delegation**: ask the parent, and only if it cannot find the class does the loader call `findClass` itself. That guarantees `java.lang.String` always comes from the JDK and cannot be spoofed. A class's runtime identity is the pair **(fully qualified name, defining class loader)**: the same bytes loaded by two loaders produce two unrelated `Class` objects with separate static state, and instances are *not* assignable to each other (`ClassCastException: X cannot be cast to X`). Custom loaders power plugin systems, application servers (one loader per webapp), hot reload, and frameworks that generate classes. `ServiceLoader` discovers implementations listed in `META-INF/services` or `module-info.java`.",
            "Understanding loading explains a family of errors (`ClassNotFoundException`, `NoClassDefFoundError`, `NoSuchMethodError`, `LinkageError`, `ExceptionInInitializerError`) and the isolation features of application servers and plugin hosts. It also explains classpath ordering bugs where two versions of a library coexist and the *first one on the classpath wins*.",
            ["Lazy loading keeps startup fast and memory low", "Delegation protects core classes and avoids duplicate loading", "Custom loaders enable isolation, plugins, and hot reload", "Initialization runs once under a lock, giving safe publication of static state"],
            ["Class identity pitfalls (same class, two loaders, `ClassCastException`)", "Leaked loaders keep all their classes alive (metaspace leaks on redeploy)", "Static initializer failures are sticky: the first fails with `ExceptionInInitializerError`, later uses fail with `NoClassDefFoundError`", "Classpath conflicts (jar hell) are resolved by order, not by version"],
            "**`ClassNotFoundException`** is a checked exception thrown when code *asks by name* (`Class.forName`, `loadClass`) and no loader can find it. **`NoClassDefFoundError`** is an `Error` thrown when a class that was present at compile time is missing at runtime (or its static initializer previously failed). Two versions of a library on the classpath produce `NoSuchMethodError` at the first call to a method that only exists in the version that lost. A web-app loader that is referenced from a static field in a shared library (JDBC driver registration, `ThreadLocal`, a thread started by the app) can never be collected, so every redeploy leaks the whole class graph until `OutOfMemoryError: Metaspace`. Overriding `loadClass` to be **child-first** for your own packages (as servlet containers do) is legitimate but must never be applied to `java.*`.",
            """- Introspection: `Foo.class.getClassLoader()` (`null` for bootstrap classes), `ClassLoader.getSystemClassLoader()`, `loader.getParent()`, `loader.getName()` (`app`, `platform`).
- Load by name: `Class.forName("com.acme.Foo")` (initializes), `loader.loadClass("com.acme.Foo")` (does not initialize).
- Custom loader: extend `ClassLoader`, call `super(parent)`, override **`findClass(String)`** to keep delegation (and call `defineClass(name, bytes, 0, len)`), or override `loadClass(String, boolean)` only when you deliberately break parent-first.
- Always synchronize on `getClassLoadingLock(name)` when overriding `loadClass`; check `findLoadedClass(name)` first.
- Read class bytes: `Foo.class.getResourceAsStream("/com/acme/Foo.class")`.
- Compare classes: `a == b` (same `Class` object) - *not* `a.getName().equals(b.getName())`.
- Debug: `-verbose:class` or `-Xlog:class+load` prints every load with its source.""",
            [
                ("Tiny — who loads what", """System.out.println(String.class.getClassLoader());                // null  (bootstrap)
System.out.println(java.sql.Driver.class.getClassLoader());       // jdk.internal.loader.ClassLoaders$PlatformClassLoader
System.out.println(Main.class.getClassLoader());                  // jdk.internal.loader.ClassLoaders$AppClassLoader
for (ClassLoader l = Main.class.getClassLoader(); l != null; l = l.getParent()) {
    System.out.println(l.getName());                              // app, platform
}"""),
                ("Tiny — class identity is name + loader", """// Pseudo: two loaders define the same bytes
Class<?> a = loaderA.loadClass("com.acme.Plugin");
Class<?> b = loaderB.loadClass("com.acme.Plugin");
System.out.println(a == b);                    // false
System.out.println(a.getName().equals(b.getName()));  // true
Object o = a.getDeclaredConstructor().newInstance();
System.out.println(b.isInstance(o));           // false -> ClassCastException if you cast"""),
                ("Medium — a loader that defines a class from bytes", """import java.util.Map;

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
}"""),
            ],
            [
                ("What is the difference between `ClassNotFoundException` and `NoClassDefFoundError`?", "The first is a checked exception from an explicit load-by-name that failed; the second is an `Error` raised when a class that was available at compile time cannot be found (or failed to initialize) at runtime."),
                ("Why does parent-first delegation exist?", "It guarantees core classes like `java.lang.Object` come from the JDK and avoids loading the same class twice."),
                ("Can two classes with the same name coexist in one JVM?", "Yes, if they are defined by different class loaders; they are distinct types with separate static state."),
                ("`Class.forName(name)` vs `loader.loadClass(name)`?", "`forName` also initializes the class (runs static initializers); `loadClass` only loads it."),
            ],
        ),
        sec(
            "Troubleshooting a live JVM: jstack, jcmd, jstat, VisualVM",
            "The JDK ships with diagnostic tools that attach to a running process. **`jps -l`** (or `pgrep java`) lists JVM process ids. **`jstack <pid>`** (or `jcmd <pid> Thread.print`) prints every thread's state, stack, and held/awaited monitors, and reports **Java-level deadlocks** automatically at the end. **`jcmd <pid> help`** lists commands such as `GC.heap_info`, `GC.class_histogram`, `GC.heap_dump file.hprof`, `VM.flags`, `VM.system_properties`, `Thread.dump_to_file -format=json file.json` (includes virtual threads), and `JFR.start`. **`jstat -gcutil <pid> 1000`** prints GC occupancy and counts every second. **VisualVM** (and JDK Mission Control for **JFR** recordings) shows heap, threads, CPU sampling, and opens `.hprof` heap dumps to find the *dominator tree* and *GC roots* that keep objects alive. Thread states you must recognise: `RUNNABLE` (running or in native I/O), `BLOCKED` (waiting for a monitor), `WAITING`/`TIMED_WAITING` (`wait`, `park`, `sleep`, `join`), `NEW`, `TERMINATED`. Inside the JVM, `ManagementFactory.getThreadMXBean().findDeadlockedThreads()` detects monitor *and* lock deadlocks programmatically.",
            "Production problems rarely reproduce on a laptop. The only evidence you often get is a **thread dump** (what is everyone doing right now?), a **heap histogram or dump** (what is filling memory?), and **GC logs** (when and how long did pauses happen?). Being able to take and read them quickly is a core senior-engineer skill and a standard interview scenario.",
            ["Zero code changes needed; attach to a running JVM", "Thread dumps show lock owners and waiters, making deadlocks and contention obvious", "Class histograms and dumps pinpoint leaks", "JFR has very low overhead and is safe in production"],
            ["A heap dump pauses the JVM and can be as large as the heap (disk, privacy: it contains secrets)", "`jstack` needs the same user as the target process", "A single thread dump is a snapshot; take 3 dumps 5-10 s apart to see what is *stuck* vs *moving*", "Tools differ across JDK vendors/versions; container images often ship only a JRE"],
            "Without these tools teams restart the process and lose the evidence. Typical mistakes: taking only one thread dump (cannot tell stuck from busy), forgetting that `top -H` thread ids are **decimal** while `jstack` shows `nid=0x...` in **hex**, analysing a heap dump taken *before* the leak grew, and sharing `.hprof` files that contain passwords and tokens. A CPU spike diagnosed by guessing at code instead of sampling threads wastes hours; a hang that is actually a thread-pool starvation (all workers `WAITING` on futures) looks like a deadlock but is not reported as one.",
            """- Find the pid: `jps -l`; Linux: `pgrep -f myapp.jar`.
- Thread dump: `jstack -l <pid> > dump1.txt` (repeat 3x, 5 s apart) or `jcmd <pid> Thread.print`.
- Hot thread workflow: `top -H -p <pid>` -> busiest thread id (decimal) -> `printf '%x\\n' <tid>` -> search `nid=0x<hex>` in the thread dump.
- Heap quick look: `jcmd <pid> GC.class_histogram | head -20`; `jcmd <pid> GC.heap_info`.
- Heap dump: `jcmd <pid> GC.heap_dump /tmp/heap.hprof` (open in VisualVM/Eclipse MAT; find the dominator tree and path to GC roots).
- GC activity: `jstat -gcutil <pid> 1000 10` (S0 S1 E O M CCS YGC YGCT FGC FGCT GCT).
- Flags and properties: `jcmd <pid> VM.flags`, `jcmd <pid> VM.system_properties`.
- Dump including virtual threads: `jcmd <pid> Thread.dump_to_file -format=json /tmp/threads.json`.
- Deadlock in code: `ThreadMXBean bean = ManagementFactory.getThreadMXBean(); long[] ids = bean.findDeadlockedThreads();` (null when none).
- Thread dump anatomy: header `"name" #id prio=.. nid=0x..`, `java.lang.Thread.State: BLOCKED`, frames `at pkg.Class.method(File.java:12)`, and `- waiting to lock <0x...>` / `- locked <0x...>`.""",
            [
                ("Tiny — a thread dump excerpt", """"worker-1" #21 prio=5 os_prio=0 tid=0x00007f nid=0x1c03 waiting for monitor entry
   java.lang.Thread.State: BLOCKED (on object monitor)
	at com.acme.Accounts.transfer(Accounts.java:42)
	- waiting to lock <0x000000076ab62208> (a java.lang.Object)
	- locked <0x000000076ab62218> (a java.lang.Object)"""),
                ("Tiny — detecting deadlock from inside the JVM", """ThreadMXBean bean = ManagementFactory.getThreadMXBean();
long[] ids = bean.findDeadlockedThreads();       // null when there is no deadlock
if (ids != null) {
    for (ThreadInfo info : bean.getThreadInfo(ids)) {
        System.out.println("deadlocked: " + info.getThreadName() + " waits for " + info.getLockName());
    }
}"""),
                ("Medium — a deadlock you can diagnose with jstack", """import java.util.concurrent.locks.ReentrantLock;

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
}"""),
            ],
            [
                ("Why take several thread dumps instead of one?", "A single dump is a snapshot; comparing dumps over time shows which threads are really stuck versus just busy."),
                ("`top -H` shows thread id 7171; how do you find it in a jstack dump?", "Convert 7171 to hex (0x1c03) and search for `nid=0x1c03`."),
                ("How do you quickly see which classes fill the heap?", "`jcmd <pid> GC.class_histogram` (or `jmap -histo`), then a heap dump analysed in VisualVM or MAT for the dominator tree."),
                ("How do you fix a lock-ordering deadlock?", "Acquire locks in a single global order, or use `tryLock` with a timeout and back off."),
            ],
        ),
    ],
    interview=[
        ("What are virtual threads and how are they different from platform threads?", "JVM-scheduled lightweight threads (JEP 444) whose stacks live on the heap and that are multiplexed onto a few carrier threads; blocking operations unmount them so a carrier can run others. They allow thread-per-request code to scale to very high concurrency."),
        ("When would you NOT use virtual threads?", "CPU-bound work (no speedup, only `#cores` carriers), code that blocks inside `synchronized` or native calls on Java 21 (pinning), or when you rely on big per-thread caches in `ThreadLocal`."),
        ("Explain young vs old generation and how a minor GC differs from a full GC.", "New objects start in Eden; survivors are copied between survivor spaces and eventually promoted to old. A minor GC collects only the young generation (fast, frequent). A full GC collects the whole heap (slow, ideally rare)."),
        ("How do you choose between G1 and ZGC?", "G1 is a balanced default with a pause target of ~100-200 ms; ZGC does most work concurrently for pauses under a millisecond on very large heaps at some throughput/CPU cost. Measure with your workload and GC logs."),
        ("A service slowly gets slower and finally throws OutOfMemoryError. How do you investigate?", "Enable GC logs and `-XX:+HeapDumpOnOutOfMemoryError`, check whether the post-full-GC live set rises, take `GC.class_histogram` snapshots over time, open a heap dump in VisualVM/MAT and follow the path-to-GC-roots of the biggest dominators."),
        ("ClassNotFoundException vs NoClassDefFoundError?", "The first is a checked exception from loading by name; the second is a linkage `Error` for a class that existed at compile time but is missing (or failed static initialization) at runtime."),
        ("An app hangs and CPU is idle. What do you do?", "Take 3 thread dumps with `jstack`, look for `BLOCKED` threads and the `Found one Java-level deadlock` section, check for pool starvation (all workers `WAITING` on futures), and identify lock owners from `- locked <0x...>` lines."),
    ],
    mistakes=[
        "Pooling virtual threads or caching them; they are meant to be created per task.",
        "Blocking inside `synchronized` on a virtual thread (pinning) - use `ReentrantLock` instead.",
        "Using virtual threads for CPU-heavy loops and expecting speedup.",
        "Setting `-Xmx` to the full container memory and then being OOM-killed with exit code 137.",
        "Treating `System.gc()` as a performance tool.",
        "Static caches without eviction; `ThreadLocal`s that are never `remove()`d.",
        "Confusing `ClassNotFoundException` (name lookup) with `NoClassDefFoundError` (runtime linkage).",
        "Taking one thread dump and concluding; or mixing decimal thread ids with hex `nid` values.",
        "Sharing heap dumps without scrubbing; they contain secrets.",
    ],
    reading=[
        "JEP 444: Virtual Threads (openjdk.org/jeps/444) and the *Virtual Threads* chapter of the Oracle Java 21 core libraries guide",
        "JEP 425/428/453 (preview history): structured concurrency and scoped values - read the motivation sections",
        "Oracle *HotSpot Virtual Machine Garbage Collection Tuning Guide* (Java 21)",
        "JEP 333 (ZGC) and JEP 248 (G1 as default); `java -Xlog:help`",
        "*Java Language Specification* chapter 12 (loading, linking, initialization) and Javadoc of `ClassLoader`",
        "Oracle *Troubleshooting Guide for JDK*: `jcmd`, `jstack`, `jstat`, JFR; VisualVM documentation (visualvm.github.io)",
    ],
    glossary=[
        ("Virtual thread", "JVM-scheduled lightweight thread whose stack lives on the heap"),
        ("Carrier thread", "Platform thread on which a virtual thread is currently mounted"),
        ("Pinning", "A virtual thread blocking while it cannot be unmounted (monitor, native frame)"),
        ("Young / Old generation", "Heap regions for new vs long-lived objects"),
        ("Metaspace", "Native memory area holding class metadata"),
        ("GC root", "Starting reference (stack, static, JNI) from which reachability is computed"),
        ("Stop-the-world", "Pause where all application threads are halted for GC work"),
        ("Class loader", "Object that defines classes from bytes; part of a class's identity"),
        ("Parent-first delegation", "Loader asks its parent to load a class before trying itself"),
        ("Thread dump", "Snapshot of all threads, their states, stacks, and locks"),
        ("Heap dump", "Binary snapshot of all live objects (`.hprof`)"),
        ("JFR", "Java Flight Recorder: low-overhead event recorder built into the JVM"),
    ],
    tasks=[
        task(
            "virtual-thread-runner", "Virtual Thread Runner", "Warm-up", "VirtualThreads",
            "Build a tiny toolkit on top of Java 21 virtual threads: start a named virtual thread, detect virtual threads, run a batch of `Callable`s on a virtual-thread-per-task executor with results in input order, create a named virtual `ThreadFactory`, and run many tasks while limiting concurrency with a `Semaphore`.",
            [
                "`start(name, runnable)` starts and returns a **virtual** thread with exactly that name",
                "`isVirtual(thread)` reports whether the thread is virtual",
                "`runAll(tasks)` runs every callable on a virtual-thread-per-task executor and returns the results **in input order**; a failing task surfaces as `ExecutionException`; the executor is always closed",
                "`factory(prefix)` returns a `ThreadFactory` whose threads are unstarted virtual threads named `prefix0`, `prefix1`, ...",
                "`runLimited(tasks, permits, sleepMillis)` runs `tasks` virtual threads that each hold a semaphore permit while sleeping `sleepMillis`, and returns a `Stats(completed, peakConcurrency)` where the peak never exceeds `permits`",
            ],
            ["empty task list", "a failing callable in `runAll`", "permits larger than tasks", "invalid arguments (`permits <= 0`) rejected"],
            {"VirtualThreads.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.Semaphore;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.atomic.AtomicInteger;

/** Helpers around Java 21 virtual threads. */
public final class VirtualThreads {

    /** Result of {@link #runLimited(int, int, long)}. */
    public record Stats(int completed, int peakConcurrency) {
    }

    private VirtualThreads() {
    }

    public static Thread start(String name, Runnable body) {
        //@TODO start | Thread.ofVirtual().name(name).start(body) and return the started thread
        return Thread.ofVirtual().name(name).start(body);
        //@END
    }

    public static boolean isVirtual(Thread thread) {
        //@TODO isVirtual | return thread.isVirtual()
        return thread.isVirtual();
        //@END
    }

    public static <T> List<T> runAll(List<Callable<T>> tasks) throws InterruptedException, ExecutionException {
        //@TODO runAll | try-with-resources on Executors.newVirtualThreadPerTaskExecutor(); submit every task, then collect future.get() in input order
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Future<T>> futures = new ArrayList<>();
            for (Callable<T> task : tasks) {
                futures.add(executor.submit(task));
            }
            List<T> results = new ArrayList<>();
            for (Future<T> future : futures) {
                results.add(future.get());
            }
            return results;
        }
        //@END
    }

    public static ThreadFactory factory(String prefix) {
        //@TODO factory | Thread.ofVirtual().name(prefix, 0).factory() so names are prefix0, prefix1, ...
        return Thread.ofVirtual().name(prefix, 0).factory();
        //@END
    }

    public static Stats runLimited(int tasks, int permits, long sleepMillis) {
        //@TODO runLimited | IllegalArgumentException if permits <= 0 or tasks < 0; Semaphore(permits); one virtual thread per task: acquire, bump running/peak (AtomicInteger), sleep, decrement, completed++, release in finally; close the executor to wait
        if (permits <= 0 || tasks < 0) {
            throw new IllegalArgumentException("permits must be > 0 and tasks >= 0");
        }
        Semaphore semaphore = new Semaphore(permits);
        AtomicInteger running = new AtomicInteger();
        AtomicInteger peak = new AtomicInteger();
        AtomicInteger completed = new AtomicInteger();
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < tasks; i++) {
                executor.submit(() -> {
                    semaphore.acquire();
                    try {
                        peak.accumulateAndGet(running.incrementAndGet(), Math::max);
                        Thread.sleep(sleepMillis);
                        running.decrementAndGet();
                        completed.incrementAndGet();
                    } finally {
                        semaphore.release();
                    }
                    return null;
                });
            }
        }
        return new Stats(completed.get(), peak.get());
        //@END
    }
}
'''},
            {"VirtualThreadsTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(60)
class VirtualThreadsTest {

    @Test
    void r1_startCreatesNamedVirtualThreadThatRunsTheBody() throws Exception {
        AtomicReference<Thread> inside = new AtomicReference<>();
        Thread thread = VirtualThreads.start("greeter-1", () -> inside.set(Thread.currentThread()));
        thread.join(5_000);
        assertThat(thread.getName()).isEqualTo("greeter-1");
        assertThat(thread.isVirtual()).isTrue();
        assertThat(thread.isDaemon()).as("virtual threads are always daemon").isTrue();
        assertThat(inside.get()).isSameAs(thread);
        assertThat(thread.isAlive()).isFalse();
    }

    @Test
    void r2_isVirtualDistinguishesThreadKinds() throws Exception {
        assertThat(VirtualThreads.isVirtual(Thread.currentThread())).isFalse();
        Thread platform = new Thread(() -> { });
        assertThat(VirtualThreads.isVirtual(platform)).isFalse();
        Thread virtual = Thread.ofVirtual().unstarted(() -> { });
        assertThat(VirtualThreads.isVirtual(virtual)).isTrue();
    }

    @Test
    void r3_runAllKeepsInputOrderAndRunsOnVirtualThreads() throws Exception {
        List<Callable<String>> tasks = new ArrayList<>();
        AtomicBoolean allVirtual = new AtomicBoolean(true);
        for (int i = 0; i < 20; i++) {
            int n = i;
            tasks.add(() -> {
                Thread.sleep(20 - n);   // later tasks finish first
                if (!Thread.currentThread().isVirtual()) {
                    allVirtual.set(false);
                }
                return "task-" + n;
            });
        }
        List<String> results = VirtualThreads.runAll(tasks);
        assertThat(results).hasSize(20).startsWith("task-0", "task-1").endsWith("task-19");
        assertThat(allVirtual).isTrue();
        assertThat(VirtualThreads.runAll(List.<Callable<String>>of())).isEmpty();
    }

    @Test
    void r3_runAllScalesToManyBlockingTasks() {
        List<Callable<Integer>> tasks = new ArrayList<>();
        for (int i = 0; i < 10_000; i++) {
            int n = i;
            tasks.add(() -> {
                Thread.sleep(200);
                return n;
            });
        }
        // 10_000 x 200 ms sequentially = 2000 s; a 200-thread pool needs 10 s; virtual threads need ~ 1 s.
        List<Integer> results = org.junit.jupiter.api.Assertions.assertTimeoutPreemptively(Duration.ofSeconds(8), () -> VirtualThreads.runAll(tasks));
        assertThat(results).hasSize(10_000);
        assertThat(results.get(0)).isZero();
        assertThat(results.get(9_999)).isEqualTo(9_999);
    }

    @Test
    void r3_failureSurfacesAsExecutionException() {
        List<Callable<Integer>> tasks = List.of(() -> 1, () -> {
            throw new IllegalStateException("boom");
        });
        assertThatThrownBy(() -> VirtualThreads.runAll(tasks))
                .isInstanceOf(ExecutionException.class)
                .hasRootCauseMessage("boom");
    }

    @Test
    void r4_factoryBuildsUnstartedNamedVirtualThreads() throws Exception {
        ThreadFactory factory = VirtualThreads.factory("io-");
        Thread first = factory.newThread(() -> { });
        Thread second = factory.newThread(() -> { });
        assertThat(first.getName()).isEqualTo("io-0");
        assertThat(second.getName()).isEqualTo("io-1");
        assertThat(first.isVirtual()).isTrue();
        assertThat(first.getState()).isEqualTo(Thread.State.NEW);
        CompletableFuture<String> ran = new CompletableFuture<>();
        Thread third = factory.newThread(() -> ran.complete(Thread.currentThread().getName()));
        third.start();
        assertThat(ran.get(5, TimeUnit.SECONDS)).isEqualTo("io-2");
    }

    @Test
    void r5_runLimitedNeverExceedsPermitsButUsesThem() {
        VirtualThreads.Stats stats = VirtualThreads.runLimited(60, 4, 25);
        assertThat(stats.completed()).isEqualTo(60);
        assertThat(stats.peakConcurrency()).isBetween(2, 4);
    }

    @Test
    void r5_morePermitsThanTasksAndZeroTasks() {
        VirtualThreads.Stats stats = VirtualThreads.runLimited(5, 100, 50);
        assertThat(stats.completed()).isEqualTo(5);
        assertThat(stats.peakConcurrency()).isBetween(1, 5);
        VirtualThreads.Stats none = VirtualThreads.runLimited(0, 3, 10);
        assertThat(none.completed()).isZero();
        assertThat(none.peakConcurrency()).isZero();
    }

    @Test
    void r5_invalidArgumentsAreRejected() {
        assertThatThrownBy(() -> VirtualThreads.runLimited(10, 0, 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> VirtualThreads.runLimited(-1, 2, 1)).isInstanceOf(IllegalArgumentException.class);
    }
}
'''},
            ["`Thread.ofVirtual().name(prefix, 0)` appends an incrementing counter to the prefix.", "`ExecutorService` is `AutoCloseable` in Java 19+: leaving the try block waits for all submitted tasks.", "The semaphore must be released in `finally`, otherwise one failure starves the rest."],
            ["One virtual thread per task - no fixed pools", "Semaphore released in `finally`", "Executor closed on every path (try-with-resources)"],
            constraints=["Use `Thread.ofVirtual()` / `newVirtualThreadPerTaskExecutor()` - no platform thread pools", "Do not edit the tests"],
        ),
        task(
            "gc-log-analyzer", "GC Log and JVM Flags Analyzer", "Core", "GcLogAnalyzer",
            "Parse JDK unified GC log lines (`-Xlog:gc`), summarize pause behaviour, flag a probable memory leak from a rising post-full-GC live set, and interpret heap/collector flags and byte sizes the way you would while triaging a production incident.",
            [
                "`parseSize(text)` converts `512K`, `24M`, `2G`, `100B` (case-insensitive, plain digits = bytes) to bytes; anything else -> `IllegalArgumentException`",
                "`formatBytes(bytes)` renders human readable binary units with one decimal (`0 B`, `512 B`, `1.5 KiB`, `2.0 MiB`, `1.0 GiB`); negative -> `IllegalArgumentException`",
                "`parseLine(line)` parses a line like `[2.345s][info][gc] GC(12) Pause Young (Normal) (G1 Evacuation Pause) 24M->4M(256M) 5.123ms` into a `GcEvent`, or returns empty for lines that do not describe a sized pause; `full` is true for `Pause Full`",
                "`parse(log)` returns the events for all matching lines in order (ignore blank/other lines)",
                "`summarize(events)` returns event count, number of full GCs, total and maximum pause millis, and total reclaimed bytes (`before - after` summed)",
                "`leakSuspected(events, minConsecutive)` is true when at least `minConsecutive` consecutive **full** GC events have a strictly increasing `afterBytes`",
                "`heapSettings(args)` reads `-Xms`, `-Xmx` (sizes like `512m`, `2g`) and the collector flag (`UseG1GC`->`G1`, `UseZGC`->`ZGC`, `UseParallelGC`->`Parallel`, `UseSerialGC`->`Serial`; default `G1`); the last occurrence wins; `Xms > Xmx` -> `IllegalArgumentException`",
            ],
            ["garbage lines in the log", "no events (summary of nothing)", "events that are young GCs between full GCs when looking for leaks", "missing `-Xms`/`-Xmx` flags", "lower-case size suffixes"],
            {"GcLogAnalyzer.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.OptionalLong;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Triage helpers for GC logs and JVM flags. */
public final class GcLogAnalyzer {

    /** One sized GC pause. */
    public record GcEvent(double uptimeSeconds, int gcId, String cause, long beforeBytes, long afterBytes,
                          long committedBytes, double pauseMillis, boolean full) {
    }

    /** Aggregated view of many events. */
    public record Summary(int events, int fullGcs, double totalPauseMillis, double maxPauseMillis, long reclaimedBytes) {
    }

    /** Heap-related flags extracted from a JVM command line. */
    public record HeapSettings(OptionalLong initialBytes, OptionalLong maxBytes, String collector) {
    }

    private static final Pattern SIZE = Pattern.compile("(\\d+)([bBkKmMgG]?)");
    private static final Pattern LINE = Pattern.compile(
            "^\\[(\\d+(?:\\.\\d+)?)s\\]\\[info\\]\\[gc\\s*\\]\\s+GC\\((\\d+)\\)\\s+Pause\\s+(Young|Full|Mixed)(.*?)\\s+"
                    + "(\\d+[BKMG])->(\\d+[BKMG])\\((\\d+[BKMG])\\)\\s+(\\d+(?:\\.\\d+)?)ms\\s*$");

    private GcLogAnalyzer() {
    }

    public static long parseSize(String text) {
        //@TODO parseSize | match digits + optional B/K/M/G (case-insensitive); K=1024, M=1024^2, G=1024^3; null/blank/unknown unit -> IllegalArgumentException
        if (text == null) {
            throw new IllegalArgumentException("size is null");
        }
        Matcher m = SIZE.matcher(text.trim());
        if (!m.matches()) {
            throw new IllegalArgumentException("bad size: " + text);
        }
        long value = Long.parseLong(m.group(1));
        return switch (m.group(2).toUpperCase(Locale.ROOT)) {
            case "K" -> value * 1024L;
            case "M" -> value * 1024L * 1024L;
            case "G" -> value * 1024L * 1024L * 1024L;
            default -> value;
        };
        //@END
    }

    public static String formatBytes(long bytes) {
        //@TODO formatBytes | negative -> IllegalArgumentException; below 1024 print "<n> B"; otherwise divide by 1024 up to TiB and print String.format(Locale.ROOT, "%.1f %s", value, unit) with units KiB, MiB, GiB, TiB
        if (bytes < 0) {
            throw new IllegalArgumentException("negative size");
        }
        if (bytes < 1024) {
            return bytes + " B";
        }
        String[] units = {"KiB", "MiB", "GiB", "TiB"};
        double value = bytes;
        int unit = -1;
        while (value >= 1024 && unit < units.length - 1) {
            value /= 1024;
            unit++;
        }
        return String.format(Locale.ROOT, "%.1f %s", value, units[unit]);
        //@END
    }

    public static Optional<GcEvent> parseLine(String line) {
        //@TODO parseLine | apply the LINE pattern (groups: uptime, id, kind, cause text, before, after, committed, pause); trim the cause text; full == kind equals Full; non-matching or null -> Optional.empty()
        if (line == null) {
            return Optional.empty();
        }
        Matcher m = LINE.matcher(line.trim());
        if (!m.matches()) {
            return Optional.empty();
        }
        return Optional.of(new GcEvent(
                Double.parseDouble(m.group(1)),
                Integer.parseInt(m.group(2)),
                m.group(4).trim(),
                parseSize(m.group(5)),
                parseSize(m.group(6)),
                parseSize(m.group(7)),
                Double.parseDouble(m.group(8)),
                "Full".equals(m.group(3))));
        //@END
    }

    public static List<GcEvent> parse(String log) {
        //@TODO parse | split on line breaks, keep the events produced by parseLine, preserve order; null/blank -> empty list
        List<GcEvent> events = new ArrayList<>();
        if (log == null || log.isBlank()) {
            return events;
        }
        for (String line : log.split("\\R")) {
            parseLine(line).ifPresent(events::add);
        }
        return events;
        //@END
    }

    public static Summary summarize(List<GcEvent> events) {
        //@TODO summarize | count events and full GCs, sum pauses, track max pause, sum (before - after); empty list gives all zeros
        int full = 0;
        double total = 0;
        double max = 0;
        long reclaimed = 0;
        for (GcEvent e : events) {
            if (e.full()) {
                full++;
            }
            total += e.pauseMillis();
            max = Math.max(max, e.pauseMillis());
            reclaimed += e.beforeBytes() - e.afterBytes();
        }
        return new Summary(events.size(), full, total, max, reclaimed);
        //@END
    }

    public static boolean leakSuspected(List<GcEvent> events, int minConsecutive) {
        //@TODO leakSuspected | consider only full GCs in order; true when minConsecutive consecutive full GCs have strictly increasing afterBytes (a run of N events means N-1 increases); minConsecutive < 2 -> IllegalArgumentException
        if (minConsecutive < 2) {
            throw new IllegalArgumentException("minConsecutive must be >= 2");
        }
        int run = 0;
        long previous = -1;
        for (GcEvent e : events) {
            if (!e.full()) {
                continue;
            }
            if (previous >= 0 && e.afterBytes() > previous) {
                run++;
            } else {
                run = 1;
            }
            previous = e.afterBytes();
            if (run >= minConsecutive) {
                return true;
            }
        }
        return false;
        //@END
    }

    public static HeapSettings heapSettings(List<String> args) {
        //@TODO heapSettings | scan args: -Xms<size> / -Xmx<size> via parseSize, -XX:+UseG1GC/UseZGC/UseParallelGC/UseSerialGC set the collector name; last occurrence wins; default collector G1; throw IllegalArgumentException when Xms > Xmx
        OptionalLong initial = OptionalLong.empty();
        OptionalLong max = OptionalLong.empty();
        String collector = "G1";
        for (String arg : args) {
            if (arg.startsWith("-Xms")) {
                initial = OptionalLong.of(parseSize(arg.substring(4)));
            } else if (arg.startsWith("-Xmx")) {
                max = OptionalLong.of(parseSize(arg.substring(4)));
            } else if (arg.equals("-XX:+UseG1GC")) {
                collector = "G1";
            } else if (arg.equals("-XX:+UseZGC")) {
                collector = "ZGC";
            } else if (arg.equals("-XX:+UseParallelGC")) {
                collector = "Parallel";
            } else if (arg.equals("-XX:+UseSerialGC")) {
                collector = "Serial";
            }
        }
        if (initial.isPresent() && max.isPresent() && initial.getAsLong() > max.getAsLong()) {
            throw new IllegalArgumentException("Xms is larger than Xmx");
        }
        return new HeapSettings(initial, max, collector);
        //@END
    }
}
'''},
            {"GcLogAnalyzerTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.assertj.core.api.Assertions.within;

import java.util.List;
import java.util.OptionalLong;
import org.junit.jupiter.api.Test;

class GcLogAnalyzerTest {

    private static final String LOG = """
            [0.012s][info][gc] Using G1
            [1.500s][info][gc] GC(0) Pause Young (Normal) (G1 Evacuation Pause) 24M->4M(256M) 5.123ms
            this is not a gc line
            [2.750s][info][gc] GC(1) Pause Young (Concurrent Start) (G1 Humongous Allocation) 60M->20M(256M) 12.500ms

            [9.000s][info][gc         ] GC(2) Pause Full (System.gc()) 200M->50M(256M) 150.000ms
            [12.000s][info][gc] GC(3) Pause Young (Normal) (G1 Evacuation Pause) 120M->60M(256M) 7.000ms
            [20.000s][info][gc] GC(4) Pause Full (Allocation Failure) 250M->80M(256M) 220.500ms
            [30.000s][info][gc] GC(5) Pause Full (Allocation Failure) 250M->120M(256M) 300.000ms
            """;

    private static GcLogAnalyzer.GcEvent full(int id, long afterMb) {
        return new GcLogAnalyzer.GcEvent(id, id, "x", 250L << 20, afterMb << 20, 256L << 20, 100.0, true);
    }

    private static GcLogAnalyzer.GcEvent young(int id, long afterMb) {
        return new GcLogAnalyzer.GcEvent(id, id, "x", 100L << 20, afterMb << 20, 256L << 20, 5.0, false);
    }

    @Test
    void r1_parseSizeUnits() {
        assertThat(GcLogAnalyzer.parseSize("100")).isEqualTo(100L);
        assertThat(GcLogAnalyzer.parseSize("100B")).isEqualTo(100L);
        assertThat(GcLogAnalyzer.parseSize("512K")).isEqualTo(512L * 1024);
        assertThat(GcLogAnalyzer.parseSize("24M")).isEqualTo(24L * 1024 * 1024);
        assertThat(GcLogAnalyzer.parseSize("2g")).isEqualTo(2L * 1024 * 1024 * 1024);
        assertThat(GcLogAnalyzer.parseSize(" 8m ")).isEqualTo(8L * 1024 * 1024);
    }

    @Test
    void r1_parseSizeRejectsGarbage() {
        assertThatThrownBy(() -> GcLogAnalyzer.parseSize("12X")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GcLogAnalyzer.parseSize("M")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GcLogAnalyzer.parseSize("")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GcLogAnalyzer.parseSize(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r2_formatBytes() {
        assertThat(GcLogAnalyzer.formatBytes(0)).isEqualTo("0 B");
        assertThat(GcLogAnalyzer.formatBytes(512)).isEqualTo("512 B");
        assertThat(GcLogAnalyzer.formatBytes(1023)).isEqualTo("1023 B");
        assertThat(GcLogAnalyzer.formatBytes(1024)).isEqualTo("1.0 KiB");
        assertThat(GcLogAnalyzer.formatBytes(1536)).isEqualTo("1.5 KiB");
        assertThat(GcLogAnalyzer.formatBytes(2L * 1024 * 1024)).isEqualTo("2.0 MiB");
        assertThat(GcLogAnalyzer.formatBytes(1024L * 1024 * 1024)).isEqualTo("1.0 GiB");
        assertThat(GcLogAnalyzer.formatBytes(3L * 1024 * 1024 * 1024 * 1024)).isEqualTo("3.0 TiB");
        assertThatThrownBy(() -> GcLogAnalyzer.formatBytes(-1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r3_parseLineExtractsAllFields() {
        var event = GcLogAnalyzer.parseLine("[2.345s][info][gc] GC(12) Pause Young (Normal) (G1 Evacuation Pause) 24M->4M(256M) 5.123ms").orElseThrow();
        assertThat(event.uptimeSeconds()).isCloseTo(2.345, within(1e-9));
        assertThat(event.gcId()).isEqualTo(12);
        assertThat(event.cause()).isEqualTo("(Normal) (G1 Evacuation Pause)");
        assertThat(event.beforeBytes()).isEqualTo(24L << 20);
        assertThat(event.afterBytes()).isEqualTo(4L << 20);
        assertThat(event.committedBytes()).isEqualTo(256L << 20);
        assertThat(event.pauseMillis()).isCloseTo(5.123, within(1e-9));
        assertThat(event.full()).isFalse();
    }

    @Test
    void r3_parseLineFullAndPaddedTag() {
        var event = GcLogAnalyzer.parseLine("[9.000s][info][gc         ] GC(2) Pause Full (System.gc()) 200M->50M(256M) 150.000ms").orElseThrow();
        assertThat(event.full()).isTrue();
        assertThat(event.cause()).isEqualTo("(System.gc())");
        assertThat(event.pauseMillis()).isCloseTo(150.0, within(1e-9));
    }

    @Test
    void r3_parseLineIgnoresOtherLines() {
        assertThat(GcLogAnalyzer.parseLine("[0.012s][info][gc] Using G1")).isEmpty();
        assertThat(GcLogAnalyzer.parseLine("")).isEmpty();
        assertThat(GcLogAnalyzer.parseLine(null)).isEmpty();
        assertThat(GcLogAnalyzer.parseLine("[1.0s][info][gc,heap] GC(1) Pause Young 1M->1M(2M) 1ms")).isEmpty();
    }

    @Test
    void r4_parseKeepsOrderAndSkipsNoise() {
        var events = GcLogAnalyzer.parse(LOG);
        assertThat(events).extracting(GcLogAnalyzer.GcEvent::gcId).containsExactly(0, 1, 2, 3, 4, 5);
        assertThat(GcLogAnalyzer.parse("")).isEmpty();
        assertThat(GcLogAnalyzer.parse(null)).isEmpty();
        assertThat(GcLogAnalyzer.parse("nothing here\nnor here")).isEmpty();
    }

    @Test
    void r5_summaryOfTheSampleLog() {
        var s = GcLogAnalyzer.summarize(GcLogAnalyzer.parse(LOG));
        assertThat(s.events()).isEqualTo(6);
        assertThat(s.fullGcs()).isEqualTo(3);
        assertThat(s.totalPauseMillis()).isCloseTo(5.123 + 12.5 + 150.0 + 7.0 + 220.5 + 300.0, within(1e-9));
        assertThat(s.maxPauseMillis()).isCloseTo(300.0, within(1e-9));
        // (24-4)+(60-20)+(200-50)+(120-60)+(250-80)+(250-120) MiB
        assertThat(s.reclaimedBytes()).isEqualTo((20L + 40 + 150 + 60 + 170 + 130) << 20);
    }

    @Test
    void r5_summaryOfNothing() {
        var s = GcLogAnalyzer.summarize(List.of());
        assertThat(s).isEqualTo(new GcLogAnalyzer.Summary(0, 0, 0.0, 0.0, 0L));
    }

    @Test
    void r6_leakDetectedOnRisingFloor() {
        // fulls: 50 -> 80 -> 120 MB (rising), with young GCs in between that must be ignored
        var events = List.of(full(1, 50), young(2, 10), full(3, 80), young(4, 5), full(5, 120));
        assertThat(GcLogAnalyzer.leakSuspected(events, 3)).isTrue();
        assertThat(GcLogAnalyzer.leakSuspected(events, 2)).isTrue();
        assertThat(GcLogAnalyzer.leakSuspected(events, 4)).isFalse();
    }

    @Test
    void r6_noLeakWhenFloorDropsOrPlateaus() {
        assertThat(GcLogAnalyzer.leakSuspected(List.of(full(1, 50), full(2, 80), full(3, 60), full(4, 90)), 3)).isFalse();
        assertThat(GcLogAnalyzer.leakSuspected(List.of(full(1, 50), full(2, 50), full(3, 50)), 2)).isFalse();
        assertThat(GcLogAnalyzer.leakSuspected(List.of(), 2)).isFalse();
        assertThat(GcLogAnalyzer.leakSuspected(List.of(young(1, 5), young(2, 9)), 2)).isFalse();
        assertThatThrownBy(() -> GcLogAnalyzer.leakSuspected(List.of(), 1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r6_leakInTheSampleLog() {
        assertThat(GcLogAnalyzer.leakSuspected(GcLogAnalyzer.parse(LOG), 3)).as("50M -> 80M -> 120M after full GCs").isTrue();
    }

    @Test
    void r7_heapSettingsFromFlags() {
        var s = GcLogAnalyzer.heapSettings(List.of("-Xms512m", "-Xmx2g", "-XX:+UseZGC", "-Dfoo=bar"));
        assertThat(s.initialBytes()).isEqualTo(OptionalLong.of(512L << 20));
        assertThat(s.maxBytes()).isEqualTo(OptionalLong.of(2L << 30));
        assertThat(s.collector()).isEqualTo("ZGC");
    }

    @Test
    void r7_defaultsAndLastWins() {
        var none = GcLogAnalyzer.heapSettings(List.of("-Dx=y"));
        assertThat(none.initialBytes()).isEmpty();
        assertThat(none.maxBytes()).isEmpty();
        assertThat(none.collector()).isEqualTo("G1");
        var last = GcLogAnalyzer.heapSettings(List.of("-Xmx1g", "-XX:+UseSerialGC", "-Xmx4g", "-XX:+UseParallelGC"));
        assertThat(last.maxBytes()).isEqualTo(OptionalLong.of(4L << 30));
        assertThat(last.collector()).isEqualTo("Parallel");
    }

    @Test
    void r7_initialLargerThanMaxIsRejected() {
        assertThatThrownBy(() -> GcLogAnalyzer.heapSettings(List.of("-Xms4g", "-Xmx1g"))).isInstanceOf(IllegalArgumentException.class);
        assertThat(GcLogAnalyzer.heapSettings(List.of("-Xms1g", "-Xmx1g")).maxBytes()).isEqualTo(OptionalLong.of(1L << 30));
    }
}
'''},
            ["Use one compiled `Pattern` for log lines; `Matcher.matches()` plus named capture indices keeps parsing readable.", "For `leakSuspected`, a *run length* counter that resets to 1 whenever the floor does not rise is simpler than comparing windows.", "Remember `-XX:+UseG1GC` is a *flag string*, not something to `startsWith`-parse."],
            ["Garbage input never throws from `parse`/`parseLine`", "Sizes are computed with `long` (no int overflow for GiB values)", "Parsing is separated from analysis (`parse` vs `summarize` vs `leakSuspected`)"],
            constraints=["Use `java.util.regex` and plain Java - no external libraries", "Do not edit the tests"],
        ),
        task(
            "classloader-lab", "Class Loader Lab", "Stretch", "ClassLoaderLab",
            "Explore class loading by building an `IsolatedLoader` that defines classes from raw bytes with **child-first** behaviour for the classes you register while still delegating everything else to its parent. Prove class identity rules: two loaders produce two `Class` objects with separate static state, and instances are not assignable across them.",
            [
                "`bytesOf(type)` reads the `.class` bytes of a loaded class from its resource (`/pkg/Name.class`); a missing resource -> `IllegalArgumentException`",
                "`IsolatedLoader(parent, classes)` defines each registered class name **itself** (child-first, once per loader, synchronized on the class-loading lock) and delegates every other name to the parent",
                "`loaderName(type)` returns `bootstrap` when the class loader is `null`, the loader's name when it has one (`app`, `platform`), otherwise the loader's simple class name",
                "`loaderChain(loader)` lists loader names from the given loader up to and including `bootstrap`",
                "`instantiate(type)` creates an instance via the public no-arg constructor, wrapping reflective failures in `IllegalStateException` with the cause",
            ],
            ["unknown class names throw `ClassNotFoundException`", "java.* classes must still come from the parent", "loading the same name twice in one loader returns the same `Class`", "classes without a registered name delegate to the parent (same `Class` as the app loader)"],
            {"SamplePlugin.java": r'''package @PKG@;

/** Provided type: carries static state so class identity is observable. */
public class SamplePlugin {

    private static int counter;

    public String greet() {
        return "hello from plugin";
    }

    public int next() {
        return ++counter;
    }
}
''', "ClassLoaderLab.java": r'''package @PKG@;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** Class loading experiments. */
public final class ClassLoaderLab {

    private ClassLoaderLab() {
    }

    /** Child-first loader for the registered class names; everything else is delegated to the parent. */
    public static final class IsolatedLoader extends ClassLoader {
        private final Map<String, byte[]> classes;

        public IsolatedLoader(ClassLoader parent, Map<String, byte[]> classes) {
            super(parent);
            this.classes = Map.copyOf(classes);
        }

        @Override
        protected Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {
            //@TODO loadClass | synchronized (getClassLoadingLock(name)): when name is registered use findLoadedClass or defineClass(name, bytes, 0, length) (child-first); otherwise return super.loadClass(name, resolve)
            synchronized (getClassLoadingLock(name)) {
                byte[] bytes = classes.get(name);
                if (bytes == null) {
                    return super.loadClass(name, resolve);
                }
                Class<?> loaded = findLoadedClass(name);
                if (loaded == null) {
                    loaded = defineClass(name, bytes, 0, bytes.length);
                }
                if (resolve) {
                    resolveClass(loaded);
                }
                return loaded;
            }
            //@END
        }
    }

    public static byte[] bytesOf(Class<?> type) {
        //@TODO bytesOf | type.getResourceAsStream("/" + name with dots replaced by slashes + ".class"); null stream -> IllegalArgumentException; read all bytes, wrap IOException in UncheckedIOException
        String resource = "/" + type.getName().replace('.', '/') + ".class";
        try (InputStream in = type.getResourceAsStream(resource)) {
            if (in == null) {
                throw new IllegalArgumentException("no class file for " + type.getName());
            }
            return in.readAllBytes();
        } catch (IOException e) {
            throw new java.io.UncheckedIOException(e);
        }
        //@END
    }

    public static String loaderName(Class<?> type) {
        //@TODO loaderName | getClassLoader() == null -> "bootstrap"; loader.getName() when not null; else the loader's getClass().getSimpleName()
        ClassLoader loader = type.getClassLoader();
        if (loader == null) {
            return "bootstrap";
        }
        return loader.getName() != null ? loader.getName() : loader.getClass().getSimpleName();
        //@END
    }

    public static List<String> loaderChain(ClassLoader loader) {
        //@TODO loaderChain | walk getParent() from the given loader collecting a name per loader (same naming rule as loaderName), then append "bootstrap"
        List<String> names = new ArrayList<>();
        for (ClassLoader current = loader; current != null; current = current.getParent()) {
            names.add(current.getName() != null ? current.getName() : current.getClass().getSimpleName());
        }
        names.add("bootstrap");
        return names;
        //@END
    }

    public static Object instantiate(Class<?> type) {
        //@TODO instantiate | type.getDeclaredConstructor().newInstance(); wrap ReflectiveOperationException in IllegalStateException keeping the cause
        try {
            return type.getDeclaredConstructor().newInstance();
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException("cannot instantiate " + type.getName(), e);
        }
        //@END
    }
}
'''},
            {"ClassLoaderLabTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class ClassLoaderLabTest {

    private static final String PLUGIN = SamplePlugin.class.getName();

    private static ClassLoaderLab.IsolatedLoader newLoader() {
        return new ClassLoaderLab.IsolatedLoader(ClassLoaderLabTest.class.getClassLoader(),
                Map.of(PLUGIN, ClassLoaderLab.bytesOf(SamplePlugin.class)));
    }

    private static Object call(Object target, String method) throws Exception {
        return target.getClass().getMethod(method).invoke(target);
    }

    @Test
    void r1_bytesOfReturnsClassFileWithMagicNumber() {
        byte[] bytes = ClassLoaderLab.bytesOf(SamplePlugin.class);
        assertThat(bytes.length).isGreaterThan(100);
        assertThat(bytes[0] & 0xFF).isEqualTo(0xCA);
        assertThat(bytes[1] & 0xFF).isEqualTo(0xFE);
        assertThat(bytes[2] & 0xFF).isEqualTo(0xBA);
        assertThat(bytes[3] & 0xFF).isEqualTo(0xBE);
    }

    @Test
    void r2_registeredClassIsDefinedByTheIsolatedLoader() throws Exception {
        ClassLoaderLab.IsolatedLoader loader = newLoader();
        Class<?> loaded = loader.loadClass(PLUGIN);
        assertThat(loaded.getName()).isEqualTo(PLUGIN);
        assertThat(loaded.getClassLoader()).isSameAs(loader);
        assertThat(loaded).isNotSameAs(SamplePlugin.class);
        assertThat(loader.loadClass(PLUGIN)).as("defined only once per loader").isSameAs(loaded);
    }

    @Test
    void r2_otherClassesAreDelegatedToTheParent() throws Exception {
        ClassLoaderLab.IsolatedLoader loader = newLoader();
        assertThat(loader.loadClass("java.lang.String")).isSameAs(String.class);
        assertThat(loader.loadClass(ClassLoaderLab.class.getName())).isSameAs(ClassLoaderLab.class);
        assertThatThrownBy(() -> loader.loadClass("com.does.not.Exist")).isInstanceOf(ClassNotFoundException.class);
    }

    @Test
    void r2_sameBytesInTwoLoadersAreUnrelatedTypesWithSeparateStatics() throws Exception {
        Object a = ClassLoaderLab.instantiate(newLoader().loadClass(PLUGIN));
        Object b = ClassLoaderLab.instantiate(newLoader().loadClass(PLUGIN));
        assertThat(a.getClass()).isNotSameAs(b.getClass());
        assertThat(a.getClass().getName()).isEqualTo(b.getClass().getName());
        assertThat(a).isNotInstanceOf(SamplePlugin.class);
        assertThat(b.getClass().isInstance(a)).isFalse();
        assertThat(call(a, "next")).isEqualTo(1);
        assertThat(call(a, "next")).isEqualTo(2);
        assertThat(call(b, "next")).as("separate static counter").isEqualTo(1);
        assertThat(call(a, "greet")).isEqualTo("hello from plugin");
        SamplePlugin local = new SamplePlugin();
        assertThat(local.next()).as("the application's own copy is independent too").isEqualTo(1);
    }

    @Test
    void r3_loaderNames() {
        assertThat(ClassLoaderLab.loaderName(String.class)).isEqualTo("bootstrap");
        assertThat(ClassLoaderLab.loaderName(java.sql.Driver.class)).isEqualTo("platform");
        assertThat(ClassLoaderLab.loaderName(ClassLoaderLab.class)).isEqualTo(ClassLoaderLabTest.class.getClassLoader().getName() == null
                ? ClassLoaderLabTest.class.getClassLoader().getClass().getSimpleName()
                : ClassLoaderLabTest.class.getClassLoader().getName());
    }

    @Test
    void r3_loaderNameOfAnIsolatedClass() throws Exception {
        Class<?> loaded = newLoader().loadClass(PLUGIN);
        assertThat(ClassLoaderLab.loaderName(loaded)).isEqualTo("IsolatedLoader");
    }

    @Test
    void r4_loaderChainEndsAtBootstrap() {
        List<String> chain = ClassLoaderLab.loaderChain(newLoader());
        assertThat(chain).startsWith("IsolatedLoader").endsWith("platform", "bootstrap");
        assertThat(chain.size()).isGreaterThanOrEqualTo(4);
        assertThat(ClassLoaderLab.loaderChain(ClassLoader.getPlatformClassLoader())).containsExactly("platform", "bootstrap");
    }

    @Test
    void r5_instantiateWrapsFailures() {
        assertThat(ClassLoaderLab.instantiate(SamplePlugin.class)).isInstanceOf(SamplePlugin.class);
        assertThatThrownBy(() -> ClassLoaderLab.instantiate(Integer.class))
                .isInstanceOf(IllegalStateException.class)
                .hasCauseInstanceOf(ReflectiveOperationException.class);
        assertThatThrownBy(() -> ClassLoaderLab.instantiate(Runnable.class))
                .isInstanceOf(IllegalStateException.class);
    }
}
'''},
            ["Override `loadClass(String, boolean)`, not `loadClass(String)`: the one-argument version just calls it.", "`defineClass` can only be called once per name per loader - check `findLoadedClass` first (inside the class-loading lock).", "A class whose `getClassLoader()` is `null` came from the bootstrap loader."],
            ["Delegation preserved for everything that is not registered", "Class identity reasoning is correct (name + loader)", "Locking on `getClassLoadingLock(name)`"],
            constraints=["Extend `ClassLoader` only - no `URLClassLoader`, no third-party bytecode libraries", "Do not edit the tests"],
        ),
        task(
            "thread-dump-analyzer", "Thread Dump Analyzer and Live Deadlock Detector", "Challenge", "ThreadDumpAnalyzer",
            "Be the on-call engineer: parse a `jstack`-style thread dump into structured data, count thread states, locate the hottest `RUNNABLE` frame, find a lock-ordering deadlock from the `waiting to lock` / `locked` lines, and also detect a **real** deadlock inside the running JVM with `ThreadMXBean`.",
            [
                "`parse(dump)` returns one `ThreadInfo(name, state, frames, waitingForLock, heldLocks)` per quoted thread header; state comes from `java.lang.Thread.State: X`; frames are the `at ...` lines (trimmed, without `at `); `- waiting to lock <id>` sets `waitingForLock`; each `- locked <id>` is added to `heldLocks` in order",
                "`countByState(threads)` returns a sorted map state -> count",
                "`hotspot(threads)` returns the most common **top frame** among `RUNNABLE` threads (ties: alphabetically first), or empty when no runnable thread has frames",
                "`findDeadlock(threads)` returns the sorted set of thread names that take part in a wait-for cycle (A waits for a lock held by B ... back to A); empty when there is none",
                "`liveDeadlockedThreads()` uses `ThreadMXBean.findDeadlockedThreads()` and returns the sorted names of deadlocked threads (empty list when none)",
            ],
            ["no threads / empty dump", "threads that wait on a lock nobody holds", "three-thread cycle", "a chain that is blocked but not a cycle", "threads without any frames"],
            {"ThreadDumpAnalyzer.java": r'''package @PKG@;

import java.lang.management.ManagementFactory;
import java.lang.management.ThreadInfo;
import java.lang.management.ThreadMXBean;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** jstack-style thread dump triage. */
public final class ThreadDumpAnalyzer {

    /** One parsed thread. */
    public record ThreadEntry(String name, String state, List<String> frames, String waitingForLock, List<String> heldLocks) {
    }

    private static final Pattern HEADER = Pattern.compile("^\"(.+?)\"\\s.*$");
    private static final Pattern STATE = Pattern.compile("^\\s*java\\.lang\\.Thread\\.State:\\s+(\\w+).*$");
    private static final Pattern FRAME = Pattern.compile("^\\s*at\\s+(.+?)\\s*$");
    private static final Pattern WAITING = Pattern.compile("^\\s*-\\s+waiting to lock\\s+<(0x[0-9a-fA-F]+)>.*$");
    private static final Pattern LOCKED = Pattern.compile("^\\s*-\\s+locked\\s+<(0x[0-9a-fA-F]+)>.*$");

    private ThreadDumpAnalyzer() {
    }

    public static List<ThreadEntry> parse(String dump) {
        //@TODO parse | iterate lines; a HEADER match starts a new thread (flush the previous one); STATE/FRAME/WAITING/LOCKED lines fill the current thread; lines before the first header are ignored; state defaults to UNKNOWN; null/blank dump -> empty list
        List<ThreadEntry> threads = new ArrayList<>();
        if (dump == null || dump.isBlank()) {
            return threads;
        }
        String name = null;
        String state = "UNKNOWN";
        List<String> frames = new ArrayList<>();
        String waiting = null;
        List<String> held = new ArrayList<>();
        for (String line : dump.split("\\R")) {
            Matcher header = HEADER.matcher(line);
            if (header.matches()) {
                if (name != null) {
                    threads.add(new ThreadEntry(name, state, frames, waiting, held));
                }
                name = header.group(1);
                state = "UNKNOWN";
                frames = new ArrayList<>();
                waiting = null;
                held = new ArrayList<>();
                continue;
            }
            if (name == null) {
                continue;
            }
            Matcher m;
            if ((m = STATE.matcher(line)).matches()) {
                state = m.group(1);
            } else if ((m = FRAME.matcher(line)).matches()) {
                frames.add(m.group(1));
            } else if ((m = WAITING.matcher(line)).matches()) {
                waiting = m.group(1);
            } else if ((m = LOCKED.matcher(line)).matches()) {
                held.add(m.group(1));
            }
        }
        if (name != null) {
            threads.add(new ThreadEntry(name, state, frames, waiting, held));
        }
        return threads;
        //@END
    }

    public static Map<String, Long> countByState(List<ThreadEntry> threads) {
        //@TODO countByState | sorted map (TreeMap) from state to the number of threads in that state
        Map<String, Long> counts = new TreeMap<>();
        for (ThreadEntry t : threads) {
            counts.merge(t.state(), 1L, Long::sum);
        }
        return counts;
        //@END
    }

    public static Optional<String> hotspot(List<ThreadEntry> threads) {
        //@TODO hotspot | among RUNNABLE threads that have at least one frame count the first frame; return the most frequent (alphabetically first on ties) or Optional.empty()
        Map<String, Integer> counts = new TreeMap<>();
        for (ThreadEntry t : threads) {
            if ("RUNNABLE".equals(t.state()) && !t.frames().isEmpty()) {
                counts.merge(t.frames().get(0), 1, Integer::sum);
            }
        }
        String best = null;
        int bestCount = 0;
        for (Map.Entry<String, Integer> e : counts.entrySet()) {
            if (e.getValue() > bestCount) {
                best = e.getKey();
                bestCount = e.getValue();
            }
        }
        return Optional.ofNullable(best);
        //@END
    }

    public static Set<String> findDeadlock(List<ThreadEntry> threads) {
        //@TODO findDeadlock | map lock id -> holder thread; edge thread -> holder of its waitingForLock; follow edges from each thread, and when you revisit a thread on the current path return the names on the cycle (sorted); none -> empty set
        Map<String, String> holderOf = new HashMap<>();
        for (ThreadEntry t : threads) {
            for (String lock : t.heldLocks()) {
                holderOf.put(lock, t.name());
            }
        }
        Map<String, String> waitsFor = new HashMap<>();
        for (ThreadEntry t : threads) {
            if (t.waitingForLock() != null && holderOf.containsKey(t.waitingForLock())) {
                waitsFor.put(t.name(), holderOf.get(t.waitingForLock()));
            }
        }
        for (ThreadEntry start : threads) {
            List<String> path = new ArrayList<>();
            Set<String> seen = new HashSet<>();
            String current = start.name();
            while (current != null && seen.add(current)) {
                path.add(current);
                current = waitsFor.get(current);
            }
            if (current != null && path.contains(current)) {
                return new TreeSet<>(path.subList(path.indexOf(current), path.size()));
            }
        }
        return new TreeSet<>();
        //@END
    }

    public static List<String> liveDeadlockedThreads() {
        //@TODO liveDeadlockedThreads | ThreadMXBean bean = ManagementFactory.getThreadMXBean(); long[] ids = bean.findDeadlockedThreads(); null -> empty list; otherwise the sorted thread names from bean.getThreadInfo(ids)
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        long[] ids = bean.findDeadlockedThreads();
        List<String> names = new ArrayList<>();
        if (ids == null) {
            return names;
        }
        for (ThreadInfo info : bean.getThreadInfo(ids)) {
            if (info != null) {
                names.add(info.getThreadName());
            }
        }
        names.sort(null);
        return names;
        //@END
    }
}
'''},
            {"ThreadDumpAnalyzerTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.locks.ReentrantLock;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(60)
class ThreadDumpAnalyzerTest {

    private static final String DUMP = """
            2026-10-16 18:00:00
            Full thread dump OpenJDK 64-Bit Server VM (21.0.5+11 mixed mode):

            "main" #1 [1234] prio=5 os_prio=31 cpu=45.2ms elapsed=10.3s tid=0x00007f1 nid=0x1c03 waiting on condition  [0x000070000]
               java.lang.Thread.State: TIMED_WAITING (sleeping)
            \tat java.lang.Thread.sleep(java.base@21.0.5/Native Method)
            \tat com.acme.Main.main(Main.java:10)

            "pool-1-thread-1" #21 [2001] prio=5 os_prio=31 tid=0x00007f2 nid=0x2003 runnable  [0x000070100]
               java.lang.Thread.State: RUNNABLE
            \tat com.acme.Hash.compute(Hash.java:77)
            \tat com.acme.Worker.run(Worker.java:12)

            "pool-1-thread-2" #22 [2002] prio=5 os_prio=31 tid=0x00007f3 nid=0x2004 runnable  [0x000070200]
               java.lang.Thread.State: RUNNABLE
            \tat com.acme.Hash.compute(Hash.java:77)
            \tat com.acme.Worker.run(Worker.java:12)

            "pool-1-thread-3" #23 [2003] prio=5 os_prio=31 tid=0x00007f4 nid=0x2005 runnable  [0x000070300]
               java.lang.Thread.State: RUNNABLE
            \tat com.acme.Parser.next(Parser.java:5)

            "transfer-A" #31 [3001] prio=5 os_prio=31 tid=0x00007f5 nid=0x3001 waiting for monitor entry  [0x000070400]
               java.lang.Thread.State: BLOCKED (on object monitor)
            \tat com.acme.Accounts.transfer(Accounts.java:42)
            \t- waiting to lock <0x000000076ab62208> (a java.lang.Object)
            \t- locked <0x000000076ab62218> (a java.lang.Object)

            "transfer-B" #32 [3002] prio=5 os_prio=31 tid=0x00007f6 nid=0x3002 waiting for monitor entry  [0x000070500]
               java.lang.Thread.State: BLOCKED (on object monitor)
            \tat com.acme.Accounts.transfer(Accounts.java:42)
            \t- waiting to lock <0x000000076ab62218> (a java.lang.Object)
            \t- locked <0x000000076ab62208> (a java.lang.Object)

            "innocent-waiter" #33 [3003] prio=5 os_prio=31 tid=0x00007f7 nid=0x3003 waiting for monitor entry  [0x000070600]
               java.lang.Thread.State: BLOCKED (on object monitor)
            \tat com.acme.Accounts.audit(Accounts.java:90)
            \t- waiting to lock <0x000000076ab62208> (a java.lang.Object)
            """;

    private static String dumpOf(String... blocks) {
        return String.join("\n\n", blocks);
    }

    private static String thread(String name, String waiting, String... held) {
        StringBuilder sb = new StringBuilder("\"" + name + "\" #1 prio=5 nid=0x1 blocked\n   java.lang.Thread.State: BLOCKED (on object monitor)\n\tat com.acme.X.y(X.java:1)\n");
        if (waiting != null) {
            sb.append("\t- waiting to lock <").append(waiting).append("> (a java.lang.Object)\n");
        }
        for (String h : held) {
            sb.append("\t- locked <").append(h).append("> (a java.lang.Object)\n");
        }
        return sb.toString();
    }

    @Test
    void r1_parseExtractsThreadsInOrder() {
        List<ThreadDumpAnalyzer.ThreadEntry> threads = ThreadDumpAnalyzer.parse(DUMP);
        assertThat(threads).extracting(ThreadDumpAnalyzer.ThreadEntry::name)
                .containsExactly("main", "pool-1-thread-1", "pool-1-thread-2", "pool-1-thread-3", "transfer-A", "transfer-B", "innocent-waiter");
        ThreadDumpAnalyzer.ThreadEntry main = threads.get(0);
        assertThat(main.state()).isEqualTo("TIMED_WAITING");
        assertThat(main.frames()).containsExactly("java.lang.Thread.sleep(java.base@21.0.5/Native Method)", "com.acme.Main.main(Main.java:10)");
        assertThat(main.waitingForLock()).isNull();
        assertThat(main.heldLocks()).isEmpty();
    }

    @Test
    void r1_parseReadsLocks() {
        List<ThreadDumpAnalyzer.ThreadEntry> threads = ThreadDumpAnalyzer.parse(DUMP);
        ThreadDumpAnalyzer.ThreadEntry a = threads.get(4);
        assertThat(a.state()).isEqualTo("BLOCKED");
        assertThat(a.waitingForLock()).isEqualTo("0x000000076ab62208");
        assertThat(a.heldLocks()).containsExactly("0x000000076ab62218");
        assertThat(threads.get(6).heldLocks()).isEmpty();
    }

    @Test
    void r1_parseHandlesEmptyAndNoise() {
        assertThat(ThreadDumpAnalyzer.parse("")).isEmpty();
        assertThat(ThreadDumpAnalyzer.parse(null)).isEmpty();
        assertThat(ThreadDumpAnalyzer.parse("Full thread dump\nnothing quoted here")).isEmpty();
        List<ThreadDumpAnalyzer.ThreadEntry> bare = ThreadDumpAnalyzer.parse("\"lonely\" #5 prio=5\n");
        assertThat(bare).hasSize(1);
        assertThat(bare.get(0).state()).isEqualTo("UNKNOWN");
        assertThat(bare.get(0).frames()).isEmpty();
    }

    @Test
    void r2_countByStateIsSorted() {
        var counts = ThreadDumpAnalyzer.countByState(ThreadDumpAnalyzer.parse(DUMP));
        assertThat(counts).containsExactly(
                java.util.Map.entry("BLOCKED", 3L),
                java.util.Map.entry("RUNNABLE", 3L),
                java.util.Map.entry("TIMED_WAITING", 1L));
        assertThat(ThreadDumpAnalyzer.countByState(List.of())).isEmpty();
    }

    @Test
    void r3_hotspotIsTheMostCommonRunnableTopFrame() {
        assertThat(ThreadDumpAnalyzer.hotspot(ThreadDumpAnalyzer.parse(DUMP))).contains("com.acme.Hash.compute(Hash.java:77)");
        assertThat(ThreadDumpAnalyzer.hotspot(ThreadDumpAnalyzer.parse(thread("t", null)))).as("only BLOCKED threads").isEmpty();
        assertThat(ThreadDumpAnalyzer.hotspot(List.of())).isEmpty();
    }

    @Test
    void r3_hotspotTieBreaksAlphabetically() {
        String dump = "\"a\" #1 x\n   java.lang.Thread.State: RUNNABLE\n\tat zeta.Z.run(Z.java:1)\n\n"
                + "\"b\" #2 x\n   java.lang.Thread.State: RUNNABLE\n\tat alpha.A.run(A.java:1)\n";
        assertThat(ThreadDumpAnalyzer.hotspot(ThreadDumpAnalyzer.parse(dump))).contains("alpha.A.run(A.java:1)");
    }

    @Test
    void r4_findsTheTwoThreadDeadlockButNotTheInnocentWaiter() {
        assertThat(ThreadDumpAnalyzer.findDeadlock(ThreadDumpAnalyzer.parse(DUMP))).containsExactly("transfer-A", "transfer-B");
    }

    @Test
    void r4_findsAThreeThreadCycle() {
        String dump = dumpOf(thread("t1", "0xB", "0xA"), thread("t2", "0xC", "0xB"), thread("t3", "0xA", "0xC"), thread("bystander", "0xA"));
        assertThat(ThreadDumpAnalyzer.findDeadlock(ThreadDumpAnalyzer.parse(dump))).containsExactly("t1", "t2", "t3");
    }

    @Test
    void r4_aBlockedChainIsNotADeadlock() {
        String dump = dumpOf(thread("t1", "0xB", "0xA"), thread("t2", null, "0xB"));
        assertThat(ThreadDumpAnalyzer.findDeadlock(ThreadDumpAnalyzer.parse(dump))).isEmpty();
        assertThat(ThreadDumpAnalyzer.findDeadlock(ThreadDumpAnalyzer.parse(thread("t", "0xZ")))).as("lock held by nobody").isEmpty();
        assertThat(ThreadDumpAnalyzer.findDeadlock(List.of())).isEmpty();
    }

    @Test
    void r5_liveDeadlockIsDetectedFromInsideTheJvm() throws Exception {
        assertThat(ThreadDumpAnalyzer.liveDeadlockedThreads()).isEmpty();
        ReentrantLock a = new ReentrantLock();
        ReentrantLock b = new ReentrantLock();
        CyclicBarrier bothHoldFirstLock = new CyclicBarrier(2);
        Thread t1 = deadlocker("dl-1", a, b, bothHoldFirstLock);
        Thread t2 = deadlocker("dl-2", b, a, bothHoldFirstLock);
        try {
            t1.start();
            t2.start();
            List<String> found = List.of();
            long deadline = System.nanoTime() + 20_000_000_000L;
            while (System.nanoTime() < deadline) {
                found = ThreadDumpAnalyzer.liveDeadlockedThreads();
                if (!found.isEmpty()) {
                    break;
                }
                Thread.sleep(50);
            }
            assertThat(found).containsExactly("dl-1", "dl-2");
        } finally {
            t1.interrupt();
            t2.interrupt();
            t1.join(5_000);
            t2.join(5_000);
        }
        assertThat(ThreadDumpAnalyzer.liveDeadlockedThreads()).as("cleaned up").isEmpty();
    }

    private static Thread deadlocker(String name, ReentrantLock first, ReentrantLock second, CyclicBarrier barrier) {
        Thread t = new Thread(() -> {
            first.lock();
            try {
                barrier.await();
                second.lockInterruptibly();
                second.unlock();
            } catch (Exception interruptedOrBroken) {
                // the test interrupts us to clean up
            } finally {
                first.unlock();
            }
        }, name);
        t.setDaemon(true);
        return t;
    }
}
'''},
            ["Parse with one `Pattern` per line kind and a small state machine: *current thread* fields are flushed when a new header appears (and at the end).", "To detect a cycle, follow `waitsFor` edges from each thread while tracking the path; if you reach a thread already on the path, the cycle is the path suffix starting there.", "`ThreadMXBean.findDeadlockedThreads()` returns `null` (not an empty array) when nothing is deadlocked."],
            ["Parser never throws on malformed dumps", "Cycle detection terminates (no infinite loop on cycles)", "Live detection returns an empty list rather than null"],
            constraints=["Use `java.util.regex` and `java.lang.management` only", "Do not edit the tests"],
        ),
    ],
)
