package com.javaprep.day17.task02;

import java.util.IntSummaryStatistics;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.OptionalDouble;

/** Reductions. */
public final class ReduceSum {

    private ReduceSum() {
    }

    public static int sum(List<Integer> numbers) {
        // TODO(Day17-task02): reduce with identity 0 and Integer::sum
        throw new UnsupportedOperationException("TODO(Day17-task02): sum");
    }

    public static long product(List<Integer> numbers) {
        // TODO(Day17-task02): multiply as long; identity 1 so an empty list gives 1
        throw new UnsupportedOperationException("TODO(Day17-task02): product");
    }

    public static Optional<Integer> max(List<Integer> numbers) {
        // TODO(Day17-task02): reduce(Integer::max) without identity so empty input gives Optional.empty()
        throw new UnsupportedOperationException("TODO(Day17-task02): max");
    }

    public static OptionalDouble average(List<Integer> numbers) {
        // TODO(Day17-task02): mapToInt then average(); empty gives OptionalDouble.empty()
        throw new UnsupportedOperationException("TODO(Day17-task02): average");
    }

    public static Optional<String> longest(List<String> words) {
        // TODO(Day17-task02): ignore nulls; reduce keeping the first word on length ties
        throw new UnsupportedOperationException("TODO(Day17-task02): longest");
    }

    public static IntSummaryStatistics stats(List<Integer> numbers) {
        // TODO(Day17-task02): mapToInt(Integer::intValue).summaryStatistics()
        throw new UnsupportedOperationException("TODO(Day17-task02): stats");
    }

    public static long sumLong(List<Integer> numbers) {
        // TODO(Day17-task02): mapToLong then sum() so that large inputs do not overflow int
        throw new UnsupportedOperationException("TODO(Day17-task02): sumLong");
    }
}
