package com.javaprep.day21.task01;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

/** ExecutorService practice. */
public final class ExecutorSum {

    private ExecutorSum() {
    }

    public static long parallelSum(List<Integer> numbers, int chunks, ExecutorService pool)
            throws InterruptedException, ExecutionException {
        // TODO(Day21-task01): IllegalArgumentException if chunks <= 0; empty list -> 0; split into <= chunks consecutive slices, submit one Callable<Long> per slice, then add up future.get() results
        throw new UnsupportedOperationException("TODO(Day21-task01): parallelSum");
    }

    public static <T> List<T> runAll(ExecutorService pool, List<Callable<T>> tasks)
            throws InterruptedException, ExecutionException {
        // TODO(Day21-task01): pool.invokeAll(tasks) then collect future.get() values in input order; a failed task propagates ExecutionException
        throw new UnsupportedOperationException("TODO(Day21-task01): runAll");
    }

    public static boolean shutdownGracefully(ExecutorService pool, long timeoutMillis) {
        // TODO(Day21-task01): shutdown(); awaitTermination(timeoutMillis); if not terminated call shutdownNow() (and wait briefly) and return false; restore the interrupt flag if interrupted; return true when it terminated by itself
        throw new UnsupportedOperationException("TODO(Day21-task01): shutdownGracefully");
    }
}
