package com.javaprep.day13.task03;

import java.util.Collection;
import java.util.List;

/** Utilities demonstrating Producer-Extends / Consumer-Super. */
public final class Pecs {

    private Pecs() {
    }

    public static <T> void copy(List<? super T> dst, List<? extends T> src) {
        // TODO(Day13-task03): append every element of src to dst; src is a producer (extends), dst a consumer (super)
        throw new UnsupportedOperationException("TODO(Day13-task03): copy");
    }

    public static <T> void moveAll(Collection<? extends T> src, Collection<? super T> dst) {
        // TODO(Day13-task03): add every element of src to dst, then clear src
        throw new UnsupportedOperationException("TODO(Day13-task03): moveAll");
    }

    public static <T> void fill(List<? super T> dst, T value, int n) {
        // TODO(Day13-task03): add n copies of value to dst; IllegalArgumentException when n is negative
        throw new UnsupportedOperationException("TODO(Day13-task03): fill");
    }

    public static <T> T firstOrDefault(List<? extends T> src, T def) {
        // TODO(Day13-task03): return src.get(0), or def when src is empty
        throw new UnsupportedOperationException("TODO(Day13-task03): firstOrDefault");
    }

    public static void swap(List<?> list, int i, int j) {
        // TODO(Day13-task03): delegate to the private generic helper swapHelper(list, i, j) (wildcard capture)
        throw new UnsupportedOperationException("TODO(Day13-task03): swap");
    }

    private static <E> void swapHelper(List<E> list, int i, int j) {
        E tmp = list.get(i);
        list.set(i, list.get(j));
        list.set(j, tmp);
    }
}
