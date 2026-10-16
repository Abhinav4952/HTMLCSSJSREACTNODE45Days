package com.javaprep.day15.task01;

import java.util.Collection;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Objects;
import java.util.Set;
import java.util.TreeSet;

/** Set-based helpers. */
public final class UniqueNormalize {

    private UniqueNormalize() {
    }

    public static Set<String> normalize(List<String> raw) {
        // TODO(Day15-task01): trim + lower-case each element, skip null and blank, keep first-seen order in a LinkedHashSet; NullPointerException for null list
        throw new UnsupportedOperationException("TODO(Day15-task01): normalize");
    }

    public static <T> Set<T> duplicates(List<T> items) {
        // TODO(Day15-task01): return the elements seen more than once, ordered by when the repeat was detected (use the boolean result of Set.add)
        throw new UnsupportedOperationException("TODO(Day15-task01): duplicates");
    }

    public static <T> Set<T> union(Set<? extends T> a, Set<? extends T> b) {
        // TODO(Day15-task01): new set containing every element of a and b; do not mutate a or b
        throw new UnsupportedOperationException("TODO(Day15-task01): union");
    }

    public static <T> Set<T> intersection(Set<? extends T> a, Set<? extends T> b) {
        // TODO(Day15-task01): new set of the elements present in both; do not mutate a or b
        throw new UnsupportedOperationException("TODO(Day15-task01): intersection");
    }

    public static <T> Set<T> difference(Set<? extends T> a, Set<? extends T> b) {
        // TODO(Day15-task01): new set of the elements in a that are not in b; do not mutate a or b
        throw new UnsupportedOperationException("TODO(Day15-task01): difference");
    }

    public static TreeSet<String> sortedCaseInsensitive(Collection<String> words) {
        // TODO(Day15-task01): TreeSet with String.CASE_INSENSITIVE_ORDER containing words; the first inserted spelling wins
        throw new UnsupportedOperationException("TODO(Day15-task01): sortedCaseInsensitive");
    }
}
