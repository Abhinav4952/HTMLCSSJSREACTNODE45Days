package com.javaprep.day43.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Duration;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class ResilientCallerTest {

    private final ResilientCaller caller = new ResilientCaller();
    private static final Duration WAIT = Duration.ofMillis(10);

    @Test
    void succeedsAfterTransientFailures() {
        FlakyDownstream downstream = new FlakyDownstream(2);
        assertThat(caller.callWithRetry(downstream::call, 3, WAIT, DownstreamException.class)).isEqualTo("ok");
        assertThat(downstream.calls()).isEqualTo(3);
    }

    @Test
    void givesUpAfterMaxAttemptsAndRethrowsLastFailure() {
        FlakyDownstream downstream = new FlakyDownstream(5);
        assertThatThrownBy(() -> caller.callWithRetry(downstream::call, 2, WAIT, DownstreamException.class))
                .isInstanceOf(DownstreamException.class).hasMessage("downstream failure #2");
        assertThat(downstream.calls()).isEqualTo(2);
    }

    @Test
    void nonRetryableExceptionsAreNotRetried() {
        AtomicInteger calls = new AtomicInteger();
        assertThatThrownBy(() -> caller.callWithRetry(() -> {
            calls.incrementAndGet();
            throw new IllegalArgumentException("bad input");
        }, 5, WAIT, DownstreamException.class)).isInstanceOf(IllegalArgumentException.class);
        assertThat(calls.get()).isEqualTo(1);
    }

    @Test
    void firstSuccessIsNotRepeated() {
        FlakyDownstream downstream = new FlakyDownstream(0);
        caller.callWithRetry(downstream::call, 4, WAIT, DownstreamException.class);
        assertThat(downstream.calls()).isEqualTo(1);
    }

    @Test
    void waitsBetweenAttempts() {
        FlakyDownstream downstream = new FlakyDownstream(2);
        long start = System.nanoTime();
        caller.callWithRetry(downstream::call, 3, Duration.ofMillis(50), DownstreamException.class);
        long elapsedMs = (System.nanoTime() - start) / 1_000_000;
        assertThat(elapsedMs).isGreaterThanOrEqualTo(90);
    }

    @Test
    void rejectsInvalidAttemptCount() {
        assertThatThrownBy(() -> caller.callWithRetry(() -> "x", 0, WAIT, DownstreamException.class))
                .isInstanceOf(IllegalArgumentException.class);
    }
}
