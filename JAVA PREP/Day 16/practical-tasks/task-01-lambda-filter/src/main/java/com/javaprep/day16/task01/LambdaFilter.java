package com.javaprep.day16.task01;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;
import java.util.function.IntUnaryOperator;
import java.util.function.Predicate;
import java.util.function.Supplier;

/** Higher-order functions and closures. */
public final class LambdaFilter {

    private LambdaFilter() {
    }

    public static <T> List<T> filter(List<T> items, Predicate<? super T> predicate) {
        // TODO(Day16-task01): return a new list containing only the elements for which predicate.test is true
        throw new UnsupportedOperationException("TODO(Day16-task01): filter");
    }

    public static <T, R> List<R> mapAll(List<T> items, Function<? super T, ? extends R> fn) {
        // TODO(Day16-task01): return a new list with fn applied to every element, preserving order
        throw new UnsupportedOperationException("TODO(Day16-task01): mapAll");
    }

    public static int applyTwice(IntUnaryOperator f, int x) {
        // TODO(Day16-task01): return f(f(x))
        throw new UnsupportedOperationException("TODO(Day16-task01): applyTwice");
    }

    public static Supplier<Integer> counter() {
        // TODO(Day16-task01): return a Supplier whose successive calls return 1, 2, 3, ...; every counter() call gets its own state (captured AtomicInteger)
        throw new UnsupportedOperationException("TODO(Day16-task01): counter");
    }

    public static List<IntUnaryOperator> adders(int n) {
        // TODO(Day16-task01): return n operators; operator i adds i to its input; IllegalArgumentException when n is negative (watch effectively-final capture in the loop)
        throw new UnsupportedOperationException("TODO(Day16-task01): adders");
    }
}
