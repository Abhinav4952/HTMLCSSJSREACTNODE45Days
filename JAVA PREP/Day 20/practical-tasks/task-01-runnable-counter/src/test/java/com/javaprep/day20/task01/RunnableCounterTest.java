package com.javaprep.day20.task01;

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
