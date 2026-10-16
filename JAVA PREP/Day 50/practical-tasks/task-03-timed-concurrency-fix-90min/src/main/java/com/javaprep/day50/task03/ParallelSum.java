package com.javaprep.day50.task03;

/** Parallel array sum with an explicit thread pool (no parallel streams). */
public final class ParallelSum {

    private ParallelSum() {
    }

    /**
     * Splits the array into {@code threads} contiguous chunks, sums each in an ExecutorService task, combines the partial
     * sums. threads &lt; 1 -> IllegalArgumentException; empty array -> 0. The pool must be shut down before returning.
     * Interrupted / failed tasks -> IllegalStateException.
     */
    public static long sum(int[] data, int threads) {
        // TODO(Day50-task03): ExecutorService + Callable<Long> per chunk, collect Futures, shut down in finally
        throw new UnsupportedOperationException("TODO(Day50-task03): implement sum");
    }
}
