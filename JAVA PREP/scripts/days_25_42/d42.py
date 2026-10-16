from sx import *

TYPE = "Spring Boot (Async / Scheduling / Cache)"
S = ["spring-boot-starter"]

# ------------------------------------------------------------ task 1
ACFG = r'''package %PKG%;

import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.context.annotation.Configuration;

//A! switch on @Async processing for the application (@EnableAsync)
@Configuration
@EnableAsync
//E!
public class AsyncConfig {
}
'''
SLOW = r'''package %PKG%;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

@Service
public class SlowService {

    private final AtomicReference<String> lastThread = new AtomicReference<>();

    public String lastThread() {
        return lastThread.get();
    }

    /** Runs on the async executor and reports the name of the thread that executed it. */
    //A! run asynchronously (@Async)
    @Async
    //E!
    public CompletableFuture<String> threadName() {
        //B! return a completed future with Thread.currentThread().getName()
        return CompletableFuture.completedFuture(Thread.currentThread().getName());
        //E!
    }

    /** Simulates slow work (about 50 ms) and returns n * n. */
    //A! run asynchronously (@Async)
    @Async
    //E!
    public CompletableFuture<Integer> square(int n) {
        //B! sleep ~50 ms (restore the interrupt flag when interrupted) and complete with n*n
        try {
            Thread.sleep(50);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return CompletableFuture.failedFuture(e);
        }
        return CompletableFuture.completedFuture(n * n);
        //E!
    }

    /** Returns a FAILED future with IllegalStateException("async boom") (do not throw). */
    //A! run asynchronously (@Async)
    @Async
    //E!
    public CompletableFuture<Integer> failing() {
        //B! failedFuture
        return CompletableFuture.failedFuture(new IllegalStateException("async boom"));
        //E!
    }

    /** Fire-and-forget: stores the executing thread name in lastThread, then counts the latch down. */
    //A! run asynchronously (@Async)
    @Async
    //E!
    public void fireAndForget(CountDownLatch latch) {
        //B! record the thread name and count down
        lastThread.set(Thread.currentThread().getName());
        latch.countDown();
        //E!
    }
}
'''
AGG = r'''package %PKG%;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import org.springframework.stereotype.Component;

/** Calls the async service THROUGH the proxy (separate bean) so @Async really applies. */
@Component
public class Aggregator {

    private final SlowService slow;

    public Aggregator(SlowService slow) {
        this.slow = slow;
    }

    /** Starts all squares first (so they overlap), then waits for all of them and sums the results. */
    public int sumOfSquares(List<Integer> numbers) {
        //B! start every future before joining any; allOf(...).join(); sum
        List<CompletableFuture<Integer>> futures = numbers.stream().map(slow::square).toList();
        CompletableFuture.allOf(futures.toArray(CompletableFuture[]::new)).join();
        return futures.stream().mapToInt(CompletableFuture::join).sum();
        //E!
    }
}
'''
T1 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.Test;
import org.springframework.aop.support.AopUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class AsyncTest {

    @Autowired
    SlowService service;
    @Autowired
    Aggregator aggregator;

    @Test
    void serviceIsProxiedForAsync() {
        assertThat(AopUtils.isAopProxy(service)).isTrue();
    }

    @Test
    void runsOnExecutorThread() throws Exception {
        String caller = Thread.currentThread().getName();
        String worker = service.threadName().get(5, TimeUnit.SECONDS);
        assertThat(worker).isNotEqualTo(caller).startsWith("task-");
    }

    @Test
    void futureCompletesWithValue() throws Exception {
        assertThat(service.square(7).get(5, TimeUnit.SECONDS)).isEqualTo(49);
    }

    @Test
    void failureTravelsInsideTheFuture() {
        assertThatThrownBy(() -> service.failing().get(5, TimeUnit.SECONDS))
                .isInstanceOf(ExecutionException.class).hasCauseInstanceOf(IllegalStateException.class).hasRootCauseMessage("async boom");
    }

    @Test
    void fireAndForgetRunsInBackground() throws Exception {
        CountDownLatch latch = new CountDownLatch(1);
        service.fireAndForget(latch);
        assertThat(latch.await(5, TimeUnit.SECONDS)).isTrue();
        assertThat(service.lastThread()).startsWith("task-").isNotEqualTo(Thread.currentThread().getName());
    }

    @Test
    void aggregatorCombinesFutures() {
        assertThat(aggregator.sumOfSquares(List.of(1, 2, 3, 4))).isEqualTo(30);
        assertThat(aggregator.sumOfSquares(List.of())).isZero();
    }
}
'''
PLAIN_APP = r'''package %PKG%;

import org.springframework.boot.autoconfigure.SpringBootApplication;

/** PROVIDED: boot entry point. */
@SpringBootApplication
public class Application {
}
'''
a1 = tk("async-completable-future", "@Async with CompletableFuture", "Warm-up",
    "Run work on Spring's task executor with @Async, return CompletableFuture, handle failures and combine results.",
    {"main/Application.java": PLAIN_APP, "main/AsyncConfig.java": ACFG, "main/SlowService.java": SLOW, "main/Aggregator.java": AGG},
    {"test/AsyncTest.java": T1},
    ["Enable async support and annotate the four service methods with `@Async`.", "Implement the four async methods and `Aggregator.sumOfSquares`."],
    ["Calling an `@Async` method from the same class bypasses the proxy: that is why `Aggregator` is a separate bean.", "Return failures inside the future; `void` async methods lose exceptions (use an AsyncUncaughtExceptionHandler).", "Always restore the interrupt flag after catching `InterruptedException`."],
    ["`@Async` methods must be public and called from another bean.", "`CompletableFuture.allOf(...)` does not return values: join the individual futures."],
    S, ttype=TYPE)

# ------------------------------------------------------------ task 2
SCFG = r'''package %PKG%;

import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;

//A! switch on scheduled task processing (@EnableScheduling)
@Configuration
@EnableScheduling
//E!
public class SchedulingConfig {
}
'''
JOBS = r'''package %PKG%;

import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class Jobs {

    private final AtomicInteger beats = new AtomicInteger();
    private final AtomicInteger cleanups = new AtomicInteger();
    private final AtomicInteger refreshes = new AtomicInteger();

    public int beats() {
        return beats.get();
    }

    public int cleanups() {
        return cleanups.get();
    }

    public int refreshes() {
        return refreshes.get();
    }

    /** Every 5 seconds measured from the END of the previous run (fixedDelay = 5000), first run after 60 seconds (initialDelay = 60000). */
    //A! @Scheduled(fixedDelay = 5000, initialDelay = 60000)
    @Scheduled(fixedDelay = 5000, initialDelay = 60000)
    //E!
    public void heartbeat() {
        //B! count a beat
        beats.incrementAndGet();
        //E!
    }

    /** Every day at 02:00 UTC (cron = "0 0 2 * * *", zone = "UTC"). */
    //A! @Scheduled with the cron expression and zone UTC
    @Scheduled(cron = "0 0 2 * * *", zone = "UTC")
    //E!
    public void nightlyCleanup() {
        //B! count a cleanup
        cleanups.incrementAndGet();
        //E!
    }

    /** Fixed RATE taken from the property jobs.refresh-rate (milliseconds, default 60000), first run after 60 seconds. */
    //A! @Scheduled(fixedRateString = "${jobs.refresh-rate:60000}", initialDelay = 60000)
    @Scheduled(fixedRateString = "${jobs.refresh-rate:60000}", initialDelay = 60000)
    //E!
    public void refresh() {
        //B! count a refresh
        refreshes.incrementAndGet();
        //E!
    }
}
'''
T2 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.lang.reflect.Method;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.scheduling.annotation.ScheduledAnnotationBeanPostProcessor;
import org.springframework.scheduling.config.CronTask;
import org.springframework.scheduling.config.FixedDelayTask;
import org.springframework.scheduling.config.FixedRateTask;
import org.springframework.scheduling.config.Task;
import org.springframework.scheduling.support.CronExpression;

@SpringBootTest(properties = "jobs.refresh-rate=120000")
class SchedulingTest {

    @Autowired
    ScheduledAnnotationBeanPostProcessor processor;
    @Autowired
    Jobs jobs;

    private List<Task> tasks() {
        return processor.getScheduledTasks().stream().map(t -> t.getTask()).toList();
    }

    @Test
    void threeTasksAreRegistered() {
        assertThat(tasks()).hasSize(3);
    }

    @Test
    void fixedDelayTask() {
        FixedDelayTask t = tasks().stream().filter(FixedDelayTask.class::isInstance).map(FixedDelayTask.class::cast).findFirst().orElseThrow();
        assertThat(t.getIntervalDuration()).isEqualTo(Duration.ofSeconds(5));
        assertThat(t.getInitialDelayDuration()).isEqualTo(Duration.ofSeconds(60));
        assertThat(t.toString()).contains("heartbeat");
    }

    @Test
    void cronTaskAtTwoAmUtc() {
        CronTask t = tasks().stream().filter(CronTask.class::isInstance).map(CronTask.class::cast).findFirst().orElseThrow();
        assertThat(t.getExpression()).isEqualTo("0 0 2 * * *");
        assertThat(CronExpression.parse(t.getExpression()).next(LocalDateTime.of(2025, 1, 1, 12, 0))).isEqualTo(LocalDateTime.of(2025, 1, 2, 2, 0));
        assertThat(t.toString()).contains("nightlyCleanup");
    }

    @Test
    void fixedRateComesFromThePropertyPlaceholder() {
        FixedRateTask t = tasks().stream().filter(FixedRateTask.class::isInstance).map(FixedRateTask.class::cast).findFirst().orElseThrow();
        assertThat(t.getIntervalDuration()).isEqualTo(Duration.ofMillis(120000));
        assertThat(t.toString()).contains("refresh");
    }

    @Test
    void jobBodiesDoRealWork() {
        int b = jobs.beats();
        int c = jobs.cleanups();
        int r = jobs.refreshes();
        jobs.heartbeat();
        jobs.nightlyCleanup();
        jobs.refresh();
        jobs.refresh();
        assertThat(jobs.beats()).isEqualTo(b + 1);
        assertThat(jobs.cleanups()).isEqualTo(c + 1);
        assertThat(jobs.refreshes()).isEqualTo(r + 2);
    }

    @Test
    void methodsCarryScheduledAnnotations() throws Exception {
        Method m = Jobs.class.getMethod("nightlyCleanup");
        var s = m.getAnnotation(org.springframework.scheduling.annotation.Scheduled.class);
        assertThat(s).isNotNull();
        assertThat(s.zone()).isEqualTo("UTC");
    }
}
'''
a2 = tk("scheduled-jobs", "@Scheduled: Fixed Delay, Cron and Property-Driven Rates", "Core",
    "Declare scheduled jobs with fixedDelay, cron with a time zone and a fixedRate resolved from a property placeholder, and verify them through the scheduler registry.",
    {"main/Application.java": PLAIN_APP, "main/SchedulingConfig.java": SCFG, "main/Jobs.java": JOBS},
    {"test/SchedulingTest.java": T2},
    ["Enable scheduling.", "Add the three `@Scheduled` annotations exactly as documented and implement the three job bodies."],
    ["`fixedDelay` waits after completion; `fixedRate` starts at fixed intervals even if runs overlap.", "Cron has six fields in Spring: second minute hour day month weekday.", "Scheduled methods must be void and take no arguments."],
    ["`fixedRateString` accepts placeholders.", "A long `initialDelay` keeps jobs from firing during the test."],
    S, ttype=TYPE)

# ------------------------------------------------------------ task 3
CCFG = r'''package %PKG%;

import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Configuration;

//A! switch on annotation-driven caching (@EnableCaching)
@Configuration
@EnableCaching
//E!
public class CacheConfig {
}
'''
PSVC = r'''package %PKG%;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
public class PriceService {

    private final Map<String, Double> database = new ConcurrentHashMap<>(Map.of("pen", 1.5, "book", 12.0));
    private final AtomicInteger loads = new AtomicInteger();

    /** PROVIDED instrumentation: how many times the "slow" source was really hit. */
    public int loads() {
        return loads.get();
    }

    public void resetLoads() {
        loads.set(0);
    }

    /** Cache "prices", key = sku; unknown skus (null result) must NOT be cached. */
    //A! @Cacheable in cache "prices", skip caching null results (unless = "#result == null")
    @Cacheable(value = "prices", unless = "#result == null")
    //E!
    public Double priceOf(String sku) {
        loads.incrementAndGet();
        return database.get(sku);
    }

    /** Updates the source AND the cache entry for this sku (return value is stored under key sku). */
    //A! @CachePut in cache "prices" with key "#sku"
    @CachePut(value = "prices", key = "#sku")
    //E!
    public Double setPrice(String sku, double price) {
        database.put(sku, price);
        return price;
    }

    /** Removes the cache entry of one sku. */
    //A! @CacheEvict in cache "prices" with key "#sku"
    @CacheEvict(value = "prices", key = "#sku")
    //E!
    public void evict(String sku) {
    }

    /** Removes every entry of the cache "prices". */
    //A! @CacheEvict in cache "prices" with allEntries = true
    @CacheEvict(value = "prices", allEntries = true)
    //E!
    public void evictAll() {
    }

    /** Cache "rates" with the composite key "<from>-><to>" built with SpEL. */
    //A! @Cacheable in cache "rates" with key "#from + '->' + #to"
    @Cacheable(value = "rates", key = "#from + '->' + #to")
    //E!
    public double rate(String from, String to) {
        loads.incrementAndGet();
        return from.equals(to) ? 1.0 : 0.9;
    }
}
'''
T3 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.aop.support.AopUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.cache.CacheManager;

@SpringBootTest
class CachingTest {

    @Autowired
    PriceService service;
    @Autowired
    CacheManager cacheManager;

    @BeforeEach
    void clean() {
        cacheManager.getCacheNames().forEach(n -> cacheManager.getCache(n).clear());
        service.resetLoads();
    }

    @Test
    void cacheInfrastructureIsActive() {
        assertThat(AopUtils.isAopProxy(service)).isTrue();
        assertThat(cacheManager).isNotNull();
    }

    @Test
    void secondCallHitsTheCache() {
        assertThat(service.priceOf("pen")).isEqualTo(1.5);
        assertThat(service.priceOf("pen")).isEqualTo(1.5);
        assertThat(service.loads()).isEqualTo(1);
        assertThat(cacheManager.getCache("prices").get("pen")).isNotNull();
    }

    @Test
    void differentKeysAreCachedSeparately() {
        service.priceOf("pen");
        service.priceOf("book");
        service.priceOf("pen");
        assertThat(service.loads()).isEqualTo(2);
    }

    @Test
    void nullResultsAreNotCached() {
        assertThat(service.priceOf("ghost")).isNull();
        assertThat(service.priceOf("ghost")).isNull();
        assertThat(service.loads()).isEqualTo(2);
    }

    @Test
    void cachePutRefreshesTheEntryWithoutAnotherLoad() {
        service.priceOf("pen");
        service.setPrice("pen", 2.0);
        assertThat(service.priceOf("pen")).isEqualTo(2.0);
        assertThat(service.loads()).isEqualTo(1);
    }

    @Test
    void evictForcesReload() {
        service.priceOf("pen");
        service.evict("pen");
        service.priceOf("pen");
        assertThat(service.loads()).isEqualTo(2);
    }

    @Test
    void evictAllClearsEverything() {
        service.priceOf("pen");
        service.priceOf("book");
        service.evictAll();
        service.priceOf("pen");
        service.priceOf("book");
        assertThat(service.loads()).isEqualTo(4);
    }

    @Test
    void compositeSpelKey() {
        service.rate("EUR", "USD");
        service.rate("EUR", "USD");
        service.rate("USD", "EUR");
        assertThat(service.loads()).isEqualTo(2);
        assertThat(cacheManager.getCache("rates").get("EUR->USD")).isNotNull();
    }
}
'''
a3 = tk("cache-abstraction", "Spring Cache: @Cacheable, @CachePut and @CacheEvict", "Core",
    "Add caching declaratively: hit/miss behavior, SpEL keys, unless conditions, put and evict semantics.",
    {"main/Application.java": PLAIN_APP, "main/CacheConfig.java": CCFG, "main/PriceService.java": PSVC},
    {"test/CachingTest.java": T3},
    ["Enable caching and annotate the five service methods exactly as documented."],
    ["Cache keys must be stable and cheap: avoid mutable objects.", "`@CachePut` always executes the method; `@Cacheable` skips it on a hit.", "Self-invocation bypasses the cache proxy like every other AOP feature."],
    ["`unless` is evaluated after the call and can use `#result`.", "Default cache manager (no provider on classpath) is a ConcurrentMap - fine for tests, use Caffeine/Redis in production."],
    ["spring-boot-starter-cache"], ttype=TYPE)

# ------------------------------------------------------------ task 4
VAPP = r'''package %PKG%;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class Application {
}
'''
THREAD_SVC = r'''package %PKG%;

import java.util.concurrent.CompletableFuture;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

/** PROVIDED: reports whether @Async work runs on a virtual thread. */
@Service
public class ThreadProbe {

    @Async
    public CompletableFuture<Boolean> runsOnVirtualThread() {
        return CompletableFuture.completedFuture(Thread.currentThread().isVirtual());
    }

    @Async
    public CompletableFuture<String> workerName() {
        return CompletableFuture.completedFuture(Thread.currentThread().getName());
    }
}
'''
RUNNER = r'''package %PKG%;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ThreadFactory;

public final class VirtualThreadRunner {

    private VirtualThreadRunner() {
    }

    /** Runs all callables, each on its OWN virtual thread (newVirtualThreadPerTaskExecutor); results in input order. */
    public static <T> List<T> runAll(List<Callable<T>> tasks) throws InterruptedException, ExecutionException {
        //B! use try-with-resources on the executor, invokeAll, then collect future.get() in order
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            List<T> results = new ArrayList<>();
            for (Future<T> f : executor.invokeAll(tasks)) {
                results.add(f.get());
            }
            return results;
        }
        //E!
    }

    /** ThreadFactory creating UNSTARTED virtual threads named prefix0, prefix1, ... */
    public static ThreadFactory namedFactory(String prefix) {
        //B! Thread.ofVirtual().name(prefix, 0).factory()
        return Thread.ofVirtual().name(prefix, 0).factory();
        //E!
    }

    /** True when the current thread is virtual. */
    public static boolean onVirtualThread() {
        //B! ask the current thread
        return Thread.currentThread().isVirtual();
        //E!
    }
}
'''
VPROPS = '''# TODO(%TAG%): make Spring Boot run its task executors (and Tomcat request threads) on virtual threads (Java 21+).
# Property: spring.threads.virtual.enabled  ->  true
'''
VPROPS_SOL = "spring.threads.virtual.enabled=true\n"
T4 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.TimeUnit;
import java.util.stream.IntStream;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.env.Environment;

@SpringBootTest
class VirtualThreadsTest {

    @Autowired
    ThreadProbe probe;
    @Autowired
    Environment env;

    @Test
    void propertyEnablesVirtualThreads() {
        assertThat(env.getProperty("spring.threads.virtual.enabled", Boolean.class)).isTrue();
    }

    @Test
    void asyncWorkRunsOnVirtualThreads() throws Exception {
        assertThat(probe.runsOnVirtualThread().get(5, TimeUnit.SECONDS)).isTrue();
        assertThat(probe.workerName().get(5, TimeUnit.SECONDS)).startsWith("task-");
    }

    @Test
    void runAllKeepsInputOrderAndUsesVirtualThreads() throws Exception {
        List<Callable<String>> tasks = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            int n = i;
            tasks.add(() -> n + ":" + Thread.currentThread().isVirtual());
        }
        assertThat(VirtualThreadRunner.runAll(tasks)).containsExactly("0:true", "1:true", "2:true", "3:true", "4:true");
    }

    @Test
    void thousandsOfBlockingTasksAreCheap() throws Exception {
        List<Callable<Integer>> tasks = IntStream.range(0, 2000).<Callable<Integer>>mapToObj(i -> () -> {
            Thread.sleep(Duration.ofMillis(200));
            return i;
        }).toList();
        long t0 = System.nanoTime();
        List<Integer> out = VirtualThreadRunner.runAll(tasks);
        long ms = (System.nanoTime() - t0) / 1_000_000;
        assertThat(out).hasSize(2000).startsWith(0, 1, 2);
        assertThat(ms).as("2000 x 200ms sleeps should overlap").isLessThan(5000);
    }

    @Test
    void namedFactoryCreatesNamedVirtualThreads() throws Exception {
        Thread t = VirtualThreadRunner.namedFactory("vt-").newThread(() -> { });
        assertThat(t.isVirtual()).isTrue();
        assertThat(t.getName()).isEqualTo("vt-0");
        assertThat(t.getState()).isEqualTo(Thread.State.NEW);
        Thread second = VirtualThreadRunner.namedFactory("vt-").newThread(() -> { });
        assertThat(second.getName()).isEqualTo("vt-0");
    }

    @Test
    void testThreadIsPlatformThread() {
        assertThat(VirtualThreadRunner.onVirtualThread()).isFalse();
    }
}
'''
a4 = tk("virtual-threads-in-boot", "Virtual Threads in Spring Boot", "Challenge",
    "Turn on virtual threads with one property, prove it through an @Async probe, and use Java 21 virtual-thread executors and factories directly.",
    {"main/Application.java": VAPP, "main/ThreadProbe.java": THREAD_SVC, "main/VirtualThreadRunner.java": RUNNER},
    {"test/VirtualThreadsTest.java": T4},
    ["Set the Spring Boot property in `src/main/resources/application.properties`.", "Implement `runAll`, `namedFactory` and `onVirtualThread` with Java 21 APIs."],
    ["Virtual threads help with blocking I/O, not CPU-bound work.", "Do not pool virtual threads; create one per task.", "`synchronized` blocks around blocking calls can pin carrier threads in Java 21 (prefer `ReentrantLock`)."],
    ["`Executors.newVirtualThreadPerTaskExecutor()` is an `AutoCloseable` ExecutorService.", "`Thread.ofVirtual().name(prefix, start).factory()`."],
    S, ttype=TYPE, extra={"res/application.properties": VPROPS})
a4["sol"]["res/application.properties"] = VPROPS_SOL

topics = [
    T("@Async and the task executor",
      "`@EnableAsync` + `@Async` run a bean method on a separate thread via a proxy. Return `void` (fire-and-forget) or `CompletableFuture<T>` (so callers can compose with `thenApply`, `allOf`, `exceptionally`). Spring Boot auto-configures the `applicationTaskExecutor` (`ThreadPoolTaskExecutor`, thread prefix `task-`) configurable through `spring.task.execution.*` (core-size, max-size, queue-capacity). Unhandled exceptions of `void` methods go to an `AsyncUncaughtExceptionHandler`.",
      "Slow or independent work (sending mail, calling services in parallel, generating reports) should not block the request thread, and parallel calls cut latency to the slowest instead of the sum.",
      ["Simple to adopt: one annotation", "Composable futures", "Bounded, configurable pool", "Same proxy mechanism as @Transactional"],
      ["Self-invocation bypasses the proxy", "Context propagation (security, MDC, transactions) is NOT automatic", "Unbounded queues hide overload", "Errors in `void` methods are easy to lose"],
      "Calling `this.asyncMethod()` runs synchronously - no error, just no async. An async method that relies on the caller's transaction or `SecurityContext` fails or runs without it. A tiny queue-capacity with default rejection handling throws `TaskRejectedException` under load.",
      "```java\n@Configuration @EnableAsync class AsyncConfig {}\n\n@Service class Mailer {\n  @Async CompletableFuture<Boolean> send(String to) {...}\n}\nCompletableFuture<Void> all = CompletableFuture.allOf(a, b);   // then join\n```\n```properties\nspring.task.execution.pool.core-size=8\nspring.task.execution.pool.queue-capacity=100\nspring.task.execution.thread-name-prefix=app-\n```",
      [("Handle failure", "java", "service.send(to).exceptionally(ex -> { log.warn(\"send failed\", ex); return false; });"),
       ("Custom executor", "java", "@Bean(\"ioExecutor\") Executor ioExecutor() { ... }\n@Async(\"ioExecutor\") void work() {...}"),
       ("Propagate MDC", "java", "@Bean TaskDecorator mdcDecorator() { return r -> { var c = MDC.getCopyOfContextMap(); return () -> { MDC.setContextMap(c); r.run(); }; }; }")],
      [("Why does self-invocation break @Async?", "The call does not go through the Spring proxy."),
       ("Return types allowed for @Async?", "void, Future, CompletableFuture (and ListenableFuture in older versions)."),
       ("What thread prefix does Boot's default executor use?", "`task-`.")]),
    T("@Scheduled jobs",
      "`@EnableScheduling` activates `@Scheduled` methods: `fixedDelay` (wait after the previous run ends), `fixedRate` (start every N ms), `cron` (six fields: second minute hour day month weekday, optional `zone`), `initialDelay`, and `...String` variants accepting placeholders (`\"${jobs.rate:60000}\"`). Methods must be void and parameterless. By default a single scheduler thread runs all jobs (`spring.task.scheduling.pool.size`).",
      "Housekeeping, polling, report generation and cache refreshes need to run on a timetable without an external scheduler.",
      ["Declarative and tiny", "Externalizable via properties", "Cron with time zones", "Integrates with Boot's scheduler config"],
      ["Runs on EVERY instance: multiple replicas run the job multiple times (use ShedLock or Quartz/DB locks)", "A long job blocks others on the single scheduler thread", "No persistence/retry/misfire handling"],
      "Two application instances both executing `nightlyCleanup` can double-process data. A job that throws is rescheduled, but errors may go unnoticed without logging. `fixedRate` jobs that run longer than the period pile up.",
      "```java\n@Scheduled(fixedDelay = 5000, initialDelay = 60000) void heartbeat() {...}\n@Scheduled(cron = \"0 0 2 * * *\", zone = \"UTC\")      void nightly() {...}\n@Scheduled(fixedRateString = \"${jobs.refresh-rate:60000}\") void refresh() {...}\n```\n```properties\nspring.task.scheduling.pool.size=4\nspring.task.scheduling.thread-name-prefix=sched-\n```\nTest by inspecting `ScheduledAnnotationBeanPostProcessor#getScheduledTasks()` or by calling the method directly - not by sleeping.",
      [("Cron examples", "text", "0 0/15 * * * *   every 15 minutes\n0 0 9-17 * * MON-FRI   hourly on weekdays 9-17\n0 0 0 1 * *   first day of month"),
       ("Disable in tests", "properties", "spring.task.scheduling.enabled=false   # or use a profile guard"),
       ("Distributed lock (idea)", "java", "@SchedulerLock(name = \"nightlyCleanup\", lockAtMostFor = \"10m\")")],
      [("fixedDelay vs fixedRate?", "fixedDelay waits after completion; fixedRate starts at fixed intervals."),
       ("What happens with several app instances?", "Each runs the job unless you add a distributed lock."),
       ("How many fields does a Spring cron have?", "Six: second, minute, hour, day-of-month, month, day-of-week.")]),
    T("Caching abstraction and virtual threads",
      "**Cache abstraction**: `@EnableCaching`; `@Cacheable` (skip the method on a hit), `@CachePut` (always run, update cache), `@CacheEvict` (remove entries, `allEntries = true`), `key` (SpEL), `condition` (before), `unless` (after, can use `#result`). Providers: ConcurrentMap by default; Caffeine, Redis, EhCache via starters/properties. **Virtual threads** (Java 21, JEP 444): cheap threads for blocking code; Boot 3.2+ enables them for Tomcat/Jetty, `@Async`, `@Scheduled` and more with `spring.threads.virtual.enabled=true`.",
      "Caching removes repeated expensive work; virtual threads let a thread-per-request style scale to many concurrent blocking calls (database, HTTP) without reactive code.",
      ["Declarative caching with minimal code", "Swappable providers", "Virtual threads keep simple imperative code scalable", "One property to adopt in Boot"],
      ["Stale data and invalidation are hard", "Memory growth without eviction/TTL (configure Caffeine `maximumSize`, `expireAfterWrite`)", "Virtual threads do not speed up CPU-bound code and `synchronized` + blocking can pin carrier threads", "Thread-local heavy code needs review"],
      "Caching mutable objects or user-specific data under shared keys leaks data. Forgetting eviction on updates serves stale values. Creating a fixed thread pool of virtual threads defeats their purpose - use one per task.",
      "```java\n@Cacheable(value = \"prices\", unless = \"#result == null\") Double priceOf(String sku)\n@CachePut(value = \"prices\", key = \"#sku\") Double setPrice(String sku, double p)\n@CacheEvict(value = \"prices\", allEntries = true) void evictAll()\n\ntry (var ex = Executors.newVirtualThreadPerTaskExecutor()) { ex.invokeAll(tasks); }\n```\n```properties\nspring.cache.type=caffeine\nspring.cache.caffeine.spec=maximumSize=1000,expireAfterWrite=10m\nspring.threads.virtual.enabled=true\n```",
      [("Conditional caching", "java", "@Cacheable(value = \"users\", condition = \"#id > 0\", key = \"#id\")"),
       ("Thread check", "java", "Thread.currentThread().isVirtual()"),
       ("Thread builder", "java", "Thread t = Thread.ofVirtual().name(\"worker-\", 0).start(() -> work());")],
      [("@Cacheable vs @CachePut?", "Cacheable skips the method on a hit; CachePut always runs and refreshes the cache."),
       ("When do virtual threads help?", "With many concurrent blocking I/O operations."),
       ("What pins a virtual thread (Java 21)?", "Blocking inside `synchronized` blocks or native calls.")]),
]

day(42, "Async, Scheduling, Caching and Virtual Threads in Spring Boot", "Spring Boot",
    "Running work off the request thread, on a timetable, with caching and with virtual threads",
    ["Use @Async with CompletableFuture and understand the proxy pitfalls", "Declare and test @Scheduled jobs", "Apply @Cacheable/@CachePut/@CacheEvict with SpEL keys", "Enable and verify virtual threads in Boot 3.2+", "Reason about thread pools, backpressure and context propagation"],
    ["Day 40 AOP", "Day 41 observability (MDC)"],
    topics, [a1, a2, a3, a4],
    [("How does @Async work?", "A proxy submits the method call to a TaskExecutor."),
     ("How do you run a job once in a cluster?", "A distributed lock (ShedLock), a leader election, or an external scheduler."),
     ("Cacheable vs CachePut vs CacheEvict?", "Read-through, write-through refresh, invalidate."),
     ("What are virtual threads?", "JVM-managed lightweight threads scheduled onto carrier threads; ideal for blocking I/O."),
     ("What can go wrong with @Async and security/transactions?", "Context is thread-bound and not propagated automatically.")],
    ["Self-invocation of @Async/@Cacheable methods.", "Assuming scheduled jobs run once per cluster.", "Unbounded caches.", "Pooling virtual threads.", "Ignoring context propagation."],
    ["Spring Framework Reference: Task Execution and Scheduling, Cache Abstraction", "JEP 444: Virtual Threads", "Spring Boot Reference: Task Execution, Virtual Threads"],
    [("@Async", "Run a method on another thread"), ("fixedDelay", "Wait N ms after the previous run finished"), ("Cache eviction", "Removing cached entries"),
     ("Virtual thread", "Lightweight JVM thread"), ("Carrier thread", "Platform thread that runs virtual threads")],
    "2–3 h theory + 3–5 h tasks", spring=True)
