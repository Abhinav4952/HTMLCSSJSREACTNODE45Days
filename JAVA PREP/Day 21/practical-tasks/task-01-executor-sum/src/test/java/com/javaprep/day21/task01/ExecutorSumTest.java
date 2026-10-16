package com.javaprep.day21.task01;

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
