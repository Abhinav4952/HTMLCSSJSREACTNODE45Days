package com.javaprep.day15.task02;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class FrequencyMapTest {

    @Test
    void r1_countIsCaseInsensitiveAndIgnoresBlanks() {
        List<String> words = Arrays.asList("Go", "go", " GO ", "java", null, "  ", "Java", "rust");
        Map<String, Integer> counts = FrequencyMap.count(words);
        assertThat(counts).containsOnlyKeys("go", "java", "rust");
        assertThat(counts).containsEntry("go", 3).containsEntry("java", 2).containsEntry("rust", 1);
    }

    @Test
    void r1_countEmpty() {
        assertThat(FrequencyMap.count(List.of())).isEmpty();
    }

    @Test
    void r2_topNOrdersByCountThenAlphabet() {
        Map<String, Integer> counts = Map.of("pear", 2, "apple", 2, "fig", 5, "kiwi", 1);
        assertThat(FrequencyMap.topN(counts, 3)).containsExactly("fig", "apple", "pear");
        assertThat(FrequencyMap.topN(counts, 1)).containsExactly("fig");
    }

    @Test
    void r2_topNBoundaries() {
        Map<String, Integer> counts = Map.of("a", 1, "b", 1);
        assertThat(FrequencyMap.topN(counts, 0)).isEmpty();
        assertThat(FrequencyMap.topN(counts, -3)).isEmpty();
        assertThat(FrequencyMap.topN(counts, 10)).containsExactly("a", "b");
        assertThat(FrequencyMap.topN(Map.of(), 2)).isEmpty();
    }

    @Test
    void r3_invertGroupsAndSorts() {
        Map<String, Integer> counts = Map.of("pear", 2, "apple", 2, "fig", 5, "kiwi", 1);
        var inverted = FrequencyMap.invert(counts);
        assertThat(inverted.keySet()).containsExactly(1, 2, 5);
        assertThat(inverted.get(2)).containsExactly("apple", "pear");
        assertThat(inverted.get(5)).containsExactly("fig");
    }

    @Test
    void r4_mergeCountsSumsAndDoesNotMutate() {
        Map<String, Integer> a = new java.util.HashMap<>(Map.of("x", 1, "y", 2));
        Map<String, Integer> b = new java.util.HashMap<>(Map.of("y", 3, "z", 4));
        Map<String, Integer> merged = FrequencyMap.mergeCounts(a, b);
        assertThat(merged).containsOnlyKeys("x", "y", "z");
        assertThat(merged).containsEntry("x", 1).containsEntry("y", 5).containsEntry("z", 4);
        assertThat(a).containsOnlyKeys("x", "y").containsEntry("y", 2);
        assertThat(b).containsOnlyKeys("y", "z").containsEntry("y", 3);
    }
}
