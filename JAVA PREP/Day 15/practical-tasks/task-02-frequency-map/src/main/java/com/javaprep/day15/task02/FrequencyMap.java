package com.javaprep.day15.task02;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.SortedMap;
import java.util.TreeMap;

/** Word-frequency helpers built on the Map API. */
public final class FrequencyMap {

    private FrequencyMap() {
    }

    public static Map<String, Integer> count(List<String> words) {
        // TODO(Day15-task02): count occurrences of trimmed lower-case words (skip null/blank) using Map.merge
        throw new UnsupportedOperationException("TODO(Day15-task02): count");
    }

    public static List<String> topN(Map<String, Integer> counts, int n) {
        // TODO(Day15-task02): return up to n words ordered by count descending, then word ascending; n <= 0 gives an empty list
        throw new UnsupportedOperationException("TODO(Day15-task02): topN");
    }

    public static SortedMap<Integer, List<String>> invert(Map<String, Integer> counts) {
        // TODO(Day15-task02): group words by count into a TreeMap (counts ascending); each word list sorted alphabetically; use computeIfAbsent
        throw new UnsupportedOperationException("TODO(Day15-task02): invert");
    }

    public static Map<String, Integer> mergeCounts(Map<String, Integer> a, Map<String, Integer> b) {
        // TODO(Day15-task02): return a new map with the sum of counts per key; do not mutate a or b
        throw new UnsupportedOperationException("TODO(Day15-task02): mergeCounts");
    }
}
