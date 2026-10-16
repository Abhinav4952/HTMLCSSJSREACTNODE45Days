package com.javaprep.day18.task04;

import java.util.List;

/**
 * Sequential implementations plus documented guidance about parallel streams.
 * Everything here is sequential on purpose: the per-element work is trivial and the lists are small.
 */
public final class ParallelSafety {

    private ParallelSafety() {
    }

    public static long sumOfSquares(List<Integer> values) {
        // TODO(Day18-task04): sequential stream: mapToLong(v -> (long) v * v).sum(); do NOT call parallel()
        throw new UnsupportedOperationException("TODO(Day18-task04): sumOfSquares");
    }

    public static List<Integer> squaresInOrder(List<Integer> values) {
        // TODO(Day18-task04): sequential map to v * v preserving encounter order, then toList()
        throw new UnsupportedOperationException("TODO(Day18-task04): squaresInOrder");
    }

    public static boolean isSafeToParallelize(boolean stateless, boolean associative, boolean splittable,
                                              long elementCount, boolean blocking) {
        // TODO(Day18-task04): true only if stateless && associative && splittable && !blocking && elementCount >= 10_000
        throw new UnsupportedOperationException("TODO(Day18-task04): isSafeToParallelize");
    }

    public static List<String> parallelCautions() {
        // TODO(Day18-task04): return >= 5 sentences (each > 40 chars) explaining WHY: associative reductions, stateless lambdas, side effects on shared state, the common pool, blocking work, and measuring first
        throw new UnsupportedOperationException("TODO(Day18-task04): parallelCautions");
    }
}
