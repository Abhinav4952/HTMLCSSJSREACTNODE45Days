package com.javaprep.day21.task04;

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
