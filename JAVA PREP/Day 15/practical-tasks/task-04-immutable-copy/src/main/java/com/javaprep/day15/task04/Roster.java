package com.javaprep.day15.task04;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/** Immutable roster: names plus a score per name. */
public final class Roster {

    private final List<String> names;
    private final Map<String, Integer> scores;

    public Roster(List<String> names, Map<String, Integer> scores) {
        // TODO(Day15-task04): store List.copyOf(names) and Map.copyOf(scores) (null arguments or elements -> NullPointerException)
        throw new UnsupportedOperationException("TODO(Day15-task04): constructor");
    }

    public List<String> names() {
        return names;
    }

    public Map<String, Integer> scores() {
        return scores;
    }

    public Roster withName(String name) {
        // TODO(Day15-task04): return a NEW Roster whose names are this.names plus name appended; scores unchanged; this stays unchanged
        throw new UnsupportedOperationException("TODO(Day15-task04): withName");
    }

    public static <T> List<T> safeCopy(Collection<? extends T> source) {
        // TODO(Day15-task04): return an immutable snapshot list of source (List.copyOf)
        throw new UnsupportedOperationException("TODO(Day15-task04): safeCopy");
    }

    public static boolean viewReflectsChanges(List<String> base) {
        // TODO(Day15-task04): on a mutable COPY of base: wrap it in Collections.unmodifiableList, add an element to the copy, return whether the view's size grew (true); never mutate base
        throw new UnsupportedOperationException("TODO(Day15-task04): viewReflectsChanges");
    }

    public static boolean copyIgnoresChanges(List<String> base) {
        // TODO(Day15-task04): on a mutable COPY of base: take List.copyOf, add an element to the copy, return whether the snapshot's size stayed the same (true); never mutate base
        throw new UnsupportedOperationException("TODO(Day15-task04): copyIgnoresChanges");
    }
}
