package com.javaprep.day43.task03;

import static org.assertj.core.api.Assertions.assertThat;

import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import java.time.Duration;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class BreakerFacadeTest {

    private final AtomicInteger calls = new AtomicInteger();
    private final AtomicBoolean healthy = new AtomicBoolean(false);

    private String downstream() {
        calls.incrementAndGet();
        if (!healthy.get()) {
            throw new IllegalStateException("down");
        }
        return "OK";
    }

    @Test
    void opensAfterFourFailuresAndStopsCallingDownstream() {
        BreakerFacade facade = new BreakerFacade(this::downstream, Duration.ofMillis(100));
        for (int i = 0; i < 4; i++) {
            assertThat(facade.call()).isEqualTo("FALLBACK");
        }
        assertThat(facade.state()).isEqualTo(CircuitBreaker.State.OPEN);
        int before = calls.get();
        assertThat(facade.call()).isEqualTo("FALLBACK");
        assertThat(calls.get()).isEqualTo(before);
    }

    @Test
    void recoversThroughHalfOpenWhenDownstreamIsHealthyAgain() throws Exception {
        BreakerFacade facade = new BreakerFacade(this::downstream, Duration.ofMillis(100));
        for (int i = 0; i < 4; i++) {
            facade.call();
        }
        healthy.set(true);
        Thread.sleep(250);
        assertThat(facade.call()).isEqualTo("OK");
        assertThat(facade.state()).isEqualTo(CircuitBreaker.State.CLOSED);
    }

    @Test
    void staysClosedBelowTheFailureThreshold() {
        BreakerFacade facade = new BreakerFacade(this::downstream, Duration.ofMillis(100));
        healthy.set(true);
        facade.call();
        facade.call();
        facade.call();
        healthy.set(false);
        assertThat(facade.call()).isEqualTo("FALLBACK");
        assertThat(facade.state()).isEqualTo(CircuitBreaker.State.CLOSED);
    }

    @Test
    void healthyCallsReturnTheRealValue() {
        healthy.set(true);
        BreakerFacade facade = new BreakerFacade(this::downstream, Duration.ofMillis(100));
        assertThat(facade.call()).isEqualTo("OK");
    }
}
