package com.javaprep.day50.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class ConcurrencyTest {

    private static <T> List<T> runConcurrently(int threads, Callable<T> task) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(threads);
        CountDownLatch ready = new CountDownLatch(threads);
        CountDownLatch go = new CountDownLatch(1);
        try {
            List<Future<T>> futures = new ArrayList<>();
            for (int i = 0; i < threads; i++) {
                futures.add(pool.submit(() -> {
                    ready.countDown();
                    go.await();
                    return task.call();
                }));
            }
            ready.await();
            go.countDown();
            List<T> results = new ArrayList<>();
            for (Future<T> f : futures) {
                results.add(f.get(20, TimeUnit.SECONDS));
            }
            return results;
        } finally {
            pool.shutdownNow();
        }
    }

    @Test
    void counterDoesNotLoseUpdates() throws Exception {
        SafeCounter counter = new SafeCounter();
        runConcurrently(8, () -> {
            for (int i = 0; i < 10_000; i++) {
                counter.increment();
            }
            return null;
        });
        assertThat(counter.get()).isEqualTo(80_000);
    }

    @Test
    void lazyHolderRunsSupplierOnce() throws Exception {
        AtomicInteger created = new AtomicInteger();
        LazyHolder<Object> holder = new LazyHolder<>(() -> {
            created.incrementAndGet();
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return new Object();
        });
        List<Object> results = runConcurrently(16, holder::get);
        assertThat(created.get()).isEqualTo(1);
        assertThat(results).allSatisfy(o -> assertThat(o).isSameAs(results.get(0)));
    }

    @Test
    void parallelSumMatchesSequentialSum() {
        int[] data = new int[100_000];
        long expected = 0;
        for (int i = 0; i < data.length; i++) {
            data[i] = i + 1;
            expected += data[i];
        }
        assertThat(ParallelSum.sum(data, 1)).isEqualTo(expected);
        assertThat(ParallelSum.sum(data, 4)).isEqualTo(expected);
        assertThat(ParallelSum.sum(data, 7)).isEqualTo(expected);
    }

    @Test
    void parallelSumEdgeCases() {
        assertThat(ParallelSum.sum(new int[0], 4)).isZero();
        assertThat(ParallelSum.sum(new int[] {5, 6}, 8)).isEqualTo(11);
        assertThatThrownBy(() -> ParallelSum.sum(new int[] {1}, 0)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void parallelSumDoesNotLeakThreads() {
        long before = Thread.getAllStackTraces().keySet().stream().filter(t -> t.getName().startsWith("pool-")).count();
        for (int i = 0; i < 20; i++) {
            ParallelSum.sum(new int[] {1, 2, 3, 4}, 4);
        }
        try {
            Thread.sleep(200);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        long after = Thread.getAllStackTraces().keySet().stream().filter(t -> t.getName().startsWith("pool-")).count();
        assertThat(after - before).isLessThan(10);
    }
}
