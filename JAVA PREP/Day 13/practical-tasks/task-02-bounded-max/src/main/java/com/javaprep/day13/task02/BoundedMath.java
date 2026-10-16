package com.javaprep.day13.task02;

import java.util.Collection;
import java.util.List;

/** Generic helpers that rely on bounded type parameters. */
public final class BoundedMath {

    private BoundedMath() {
    }

    public static <T extends Comparable<? super T>> T max(List<? extends T> items) {
        // TODO(Day13-task02): return the greatest element (compareTo); IllegalArgumentException when items is null or empty
        throw new UnsupportedOperationException("TODO(Day13-task02): max");
    }

    public static <T extends Comparable<? super T>> T min(List<? extends T> items) {
        // TODO(Day13-task02): return the smallest element (compareTo); IllegalArgumentException when items is null or empty
        throw new UnsupportedOperationException("TODO(Day13-task02): min");
    }

    public static <T extends Number & Comparable<T>> T clamp(T value, T lo, T hi) {
        // TODO(Day13-task02): return lo if value < lo, hi if value > hi, else value; IllegalArgumentException when lo > hi
        throw new UnsupportedOperationException("TODO(Day13-task02): clamp");
    }

    public static double sum(Collection<? extends Number> numbers) {
        // TODO(Day13-task02): add doubleValue() of every element; empty collection gives 0.0
        throw new UnsupportedOperationException("TODO(Day13-task02): sum");
    }
}
