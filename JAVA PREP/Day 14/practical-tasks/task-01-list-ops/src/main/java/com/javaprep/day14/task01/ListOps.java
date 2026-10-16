package com.javaprep.day14.task01;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Objects;

/** Small List utilities. None of them mutate their argument. */
public final class ListOps {

    private ListOps() {
    }

    public static <T> List<T> dedupe(List<T> input) {
        // TODO(Day14-task01): return a new list with duplicates removed, first occurrences kept in order; NullPointerException for null input
        throw new UnsupportedOperationException("TODO(Day14-task01): dedupe");
    }

    public static <T> List<T> rotate(List<T> input, int k) {
        // TODO(Day14-task01): return a new list rotated right by k; negative k rotates left; |k| may exceed size; empty list gives empty list
        throw new UnsupportedOperationException("TODO(Day14-task01): rotate");
    }

    public static <T> List<List<T>> chunk(List<T> input, int size) {
        // TODO(Day14-task01): split into consecutive copies of at most size elements; IllegalArgumentException when size <= 0
        throw new UnsupportedOperationException("TODO(Day14-task01): chunk");
    }

    public static List<Integer> removeFirstOccurrence(List<Integer> input, int value) {
        // TODO(Day14-task01): return a copy without the first element equal to value (NOT index value); unchanged copy if absent; do not mutate input
        throw new UnsupportedOperationException("TODO(Day14-task01): removeFirstOccurrence");
    }
}
