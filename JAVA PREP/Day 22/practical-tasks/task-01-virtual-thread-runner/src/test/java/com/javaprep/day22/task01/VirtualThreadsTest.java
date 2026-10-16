package com.javaprep.day22.task01;

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
