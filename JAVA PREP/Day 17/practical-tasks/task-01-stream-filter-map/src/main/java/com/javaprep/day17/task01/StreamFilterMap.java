package com.javaprep.day17.task01;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Stream;

/** Core intermediate operations. */
public final class StreamFilterMap {

    private StreamFilterMap() {
    }

    public static List<String> upperLongNames(List<String> names, int minLen) {
        // TODO(Day17-task01): stream: drop nulls, trim, keep length >= minLen, upper-case, toList (input order)
        throw new UnsupportedOperationException("TODO(Day17-task01): upperLongNames");
    }

    public static List<Integer> squaresOfOdds(List<Integer> numbers) {
        // TODO(Day17-task01): keep odd numbers (negative ones too) and map each to its square
        throw new UnsupportedOperationException("TODO(Day17-task01): squaresOfOdds");
    }

    public static List<String> distinctSortedLower(List<String> words) {
        // TODO(Day17-task01): drop nulls, trim, lower-case, drop blank, distinct, sorted alphabetically
        throw new UnsupportedOperationException("TODO(Day17-task01): distinctSortedLower");
    }

    public static <T> List<T> page(List<T> items, int pageIndex, int size) {
        // TODO(Day17-task01): validate (pageIndex >= 0, size > 0 else IllegalArgumentException), then skip(pageIndex * size) and limit(size); use long arithmetic
        throw new UnsupportedOperationException("TODO(Day17-task01): page");
    }

    public static Optional<String> firstStartingWith(List<String> names, String prefix) {
        // TODO(Day17-task01): findFirst among non-null names that start with prefix
        throw new UnsupportedOperationException("TODO(Day17-task01): firstStartingWith");
    }

    public static List<String> traceLaziness() {
        // TODO(Day17-task01): pipeline over 'a','bb','cc': filter(length>1) logging 'filter:<s>', map(upper) logging 'map:<s>', then findFirst(); return the log (it shows per-element, short-circuited processing)
        throw new UnsupportedOperationException("TODO(Day17-task01): traceLaziness");
    }
}
