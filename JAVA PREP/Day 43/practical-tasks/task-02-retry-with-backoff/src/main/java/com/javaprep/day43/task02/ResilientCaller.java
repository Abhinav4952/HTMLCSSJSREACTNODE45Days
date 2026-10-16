package com.javaprep.day43.task02;

import java.time.Duration;
import java.util.function.Supplier;

public class ResilientCaller {

    /**
     * Calls {@code call}; if it throws {@code retryOn} (or a subclass) retries until {@code maxAttempts} total attempts
     * were made, waiting {@code wait} between attempts. The LAST exception is rethrown when attempts run out.
     * Other exception types are NOT retried. maxAttempts &lt; 1 -> IllegalArgumentException.
     */
    public <T> T callWithRetry(Supplier<T> call, int maxAttempts, Duration wait, Class<? extends Throwable> retryOn) {
        // TODO(Day43-task02): build a RetryConfig (maxAttempts, waitDuration, retryExceptions) and decorate the supplier
        throw new UnsupportedOperationException("TODO(Day43-task02): implement callWithRetry");
    }
}
