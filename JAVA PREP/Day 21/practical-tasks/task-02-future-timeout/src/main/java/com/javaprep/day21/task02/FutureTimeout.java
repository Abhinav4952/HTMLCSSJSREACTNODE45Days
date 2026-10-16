package com.javaprep.day21.task02;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/** Future helpers. */
public final class FutureTimeout {

    private FutureTimeout() {
    }

    public static <T> Optional<T> getWithTimeout(Future<T> future, long timeoutMillis) throws InterruptedException {
        // TODO(Day21-task02): future.get(timeout, MILLISECONDS) -> Optional.ofNullable; on TimeoutException cancel(true) and return empty; on ExecutionException throw IllegalStateException with the cause
        throw new UnsupportedOperationException("TODO(Day21-task02): getWithTimeout");
    }

    public static <T> T getOrDefault(Future<T> future, long timeoutMillis, T fallback) {
        // TODO(Day21-task02): value within the timeout, otherwise fallback on timeout (cancel the future) or task failure; if the calling thread is interrupted restore its flag and return fallback
        throw new UnsupportedOperationException("TODO(Day21-task02): getOrDefault");
    }

    public static <T> T firstSuccessful(ExecutorService pool, List<Callable<T>> tasks)
            throws InterruptedException, ExecutionException {
        // TODO(Day21-task02): return pool.invokeAny(tasks): the first successful result; ExecutionException when every task fails
        throw new UnsupportedOperationException("TODO(Day21-task02): firstSuccessful");
    }

    public static boolean cancelRunning(Future<?> future) {
        // TODO(Day21-task02): cancel(true) and report whether the future is now cancelled (false for futures that already completed)
        throw new UnsupportedOperationException("TODO(Day21-task02): cancelRunning");
    }
}
