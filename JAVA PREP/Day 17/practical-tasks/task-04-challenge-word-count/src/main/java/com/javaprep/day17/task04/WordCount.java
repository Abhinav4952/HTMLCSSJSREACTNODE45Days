package com.javaprep.day17.task04;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.SortedMap;
import java.util.SortedSet;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** Text analytics with streams. */
public final class WordCount {

    private WordCount() {
    }

    /** Lower-cased runs of letters/digits; blank or null text yields an empty stream. */
    private static Stream<String> words(String text) {
        if (text == null || text.isBlank()) {
            return Stream.empty();
        }
        return Arrays.stream(text.toLowerCase(Locale.ROOT).split("[^\\p{L}\\p{N}]+"))
                .filter(w -> !w.isEmpty());
    }

    public static Map<String, Long> countWords(String text, Set<String> stopWords) {
        // TODO(Day17-task04): words(text) minus stop words, grouped by identity with Collectors.counting()
        throw new UnsupportedOperationException("TODO(Day17-task04): countWords");
    }

    public static List<String> topN(String text, int n, Set<String> stopWords) {
        // TODO(Day17-task04): sort the entries by count desc then word asc, limit n (n <= 0 -> empty), map to 'word=count'
        throw new UnsupportedOperationException("TODO(Day17-task04): topN");
    }

    public static SortedMap<Integer, Long> lengthHistogram(String text) {
        // TODO(Day17-task04): group word occurrences by length into a TreeMap with counting()
        throw new UnsupportedOperationException("TODO(Day17-task04): lengthHistogram");
    }

    public static SortedSet<String> hapax(String text) {
        // TODO(Day17-task04): words with count exactly 1, collected into a TreeSet
        throw new UnsupportedOperationException("TODO(Day17-task04): hapax");
    }
}
