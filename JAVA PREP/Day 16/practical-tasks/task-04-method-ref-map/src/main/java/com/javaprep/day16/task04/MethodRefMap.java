package com.javaprep.day16.task04;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.function.Supplier;

/** One method of each method-reference kind. */
public final class MethodRefMap {

    private MethodRefMap() {
    }

    public static Function<String, Integer> parser() {
        // TODO(Day16-task04): return Integer::parseInt (static method reference)
        throw new UnsupportedOperationException("TODO(Day16-task04): parser");
    }

    public static Function<String, String> upper() {
        // TODO(Day16-task04): return String::toUpperCase (unbound instance method reference)
        throw new UnsupportedOperationException("TODO(Day16-task04): upper");
    }

    public static Function<String, String> prefixer(String prefix) {
        // TODO(Day16-task04): return prefix::concat (bound reference); a null prefix must fail immediately with NullPointerException
        throw new UnsupportedOperationException("TODO(Day16-task04): prefixer");
    }

    public static Supplier<List<String>> listFactory() {
        // TODO(Day16-task04): return ArrayList::new (constructor reference)
        throw new UnsupportedOperationException("TODO(Day16-task04): listFactory");
    }

    public static Function<String, Person> personFactory() {
        // TODO(Day16-task04): return Person::new (constructor reference)
        throw new UnsupportedOperationException("TODO(Day16-task04): personFactory");
    }

    public static <K, V> Map<K, V> indexBy(List<V> values, Function<? super V, ? extends K> keyFn) {
        // TODO(Day16-task04): build a LinkedHashMap key -> value in input order; IllegalArgumentException on a duplicate key (use putIfAbsent)
        throw new UnsupportedOperationException("TODO(Day16-task04): indexBy");
    }
}
