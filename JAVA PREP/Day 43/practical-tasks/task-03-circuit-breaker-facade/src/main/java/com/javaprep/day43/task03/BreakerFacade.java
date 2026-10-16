package com.javaprep.day43.task03;

import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import java.time.Duration;
import java.util.function.Supplier;

/** Protects a downstream call with a circuit breaker and answers "FALLBACK" when the call fails or is not permitted. */
public class BreakerFacade {

    private CircuitBreaker breaker;
    private Supplier<String> downstream;

    /**
     * Configuration required by the tests: COUNT_BASED window of 4 calls, minimum 4 calls, failure rate threshold 50 %,
     * open-state wait = {@code openWait}, exactly 1 permitted call in half-open state.
     */
    public BreakerFacade(Supplier<String> downstream, Duration openWait) {
        // TODO(Day43-task03): create a CircuitBreakerConfig with the settings above and the CircuitBreaker
        throw new UnsupportedOperationException("TODO(Day43-task03): implement BreakerFacade constructor");
    }

    /** Result of the downstream call, or "FALLBACK" on failure / open circuit (downstream is NOT invoked when open). */
    public String call() {
        // TODO(Day43-task03): decorate the supplier, catch failures (including CallNotPermittedException) and return the fallback
        throw new UnsupportedOperationException("TODO(Day43-task03): implement call");
    }

    public CircuitBreaker.State state() {
        // TODO(Day43-task03): expose the breaker state
        throw new UnsupportedOperationException("TODO(Day43-task03): implement state");
    }
}
