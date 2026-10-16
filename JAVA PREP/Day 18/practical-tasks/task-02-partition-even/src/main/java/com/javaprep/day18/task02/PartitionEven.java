package com.javaprep.day18.task02;

import java.util.List;
import java.util.Map;
import java.util.function.Predicate;
import java.util.stream.Collectors;

/** partitioningBy practice. */
public final class PartitionEven {

    private PartitionEven() {
    }

    public static Map<Boolean, List<Integer>> partitionEven(List<Integer> numbers) {
        // TODO(Day18-task02): partitioningBy(n -> n % 2 == 0): evens under true, odds under false
        throw new UnsupportedOperationException("TODO(Day18-task02): partitionEven");
    }

    public static <T> Map<Boolean, List<T>> partition(List<T> items, Predicate<? super T> predicate) {
        // TODO(Day18-task02): generic partitioningBy(predicate)
        throw new UnsupportedOperationException("TODO(Day18-task02): partition");
    }

    public static Map<Boolean, Long> countPassFail(List<Integer> scores, int passMark) {
        // TODO(Day18-task02): partitioningBy(score >= passMark, counting())
        throw new UnsupportedOperationException("TODO(Day18-task02): countPassFail");
    }

    public static Map<Boolean, Integer> sumEvenOdd(List<Integer> numbers) {
        // TODO(Day18-task02): partitioningBy(even, summingInt(Integer::intValue))
        throw new UnsupportedOperationException("TODO(Day18-task02): sumEvenOdd");
    }
}
