package com.javaprep.day21.task02;

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
