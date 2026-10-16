package com.javaprep.day17.task03;

import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.stream.Collectors;

/** Collector practice. */
public final class CollectorsWorkout {

    private CollectorsWorkout() {
    }

    public static List<String> upperNames(List<String> names) {
        // TODO(Day17-task03): map to upper case and collect with Collectors.toList()
        throw new UnsupportedOperationException("TODO(Day17-task03): upperNames");
    }

    public static Set<Integer> uniqueLengths(List<String> words) {
        // TODO(Day17-task03): map to length and collect with Collectors.toSet()
        throw new UnsupportedOperationException("TODO(Day17-task03): uniqueLengths");
    }

    public static Map<String, Integer> lengthByWord(List<String> words) {
        // TODO(Day17-task03): Collectors.toMap with a merge function keeping the first value and LinkedHashMap::new as the map supplier
        throw new UnsupportedOperationException("TODO(Day17-task03): lengthByWord");
    }

    public static String csv(List<String> items) {
        // TODO(Day17-task03): Collectors.joining(', ', '[', ']') - an empty list yields '[]'
        throw new UnsupportedOperationException("TODO(Day17-task03): csv");
    }

    public static List<String> immutableSorted(Collection<String> items) {
        // TODO(Day17-task03): sorted() then collectingAndThen(toList(), Collections::unmodifiableList)
        throw new UnsupportedOperationException("TODO(Day17-task03): immutableSorted");
    }

    public static Map<String, List<String>> toIdsByType(List<String> entries) {
        // TODO(Day17-task03): entries look like 'type:id'; groupingBy(type, TreeMap::new, mapping(id, toList()))
        throw new UnsupportedOperationException("TODO(Day17-task03): toIdsByType");
    }
}
