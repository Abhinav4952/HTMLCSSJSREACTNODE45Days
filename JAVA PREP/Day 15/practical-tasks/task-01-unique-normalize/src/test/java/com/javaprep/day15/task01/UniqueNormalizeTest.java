package com.javaprep.day15.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class UniqueNormalizeTest {

    @Test
    void r1_normalizeTrimsLowercasesAndKeepsOrder() {
        List<String> raw = Arrays.asList("  Apple ", "banana", "APPLE", null, "   ", "Cherry", "BANANA ");
        Set<String> out = UniqueNormalize.normalize(raw);
        assertThat(out).isInstanceOf(LinkedHashSet.class).containsExactly("apple", "banana", "cherry");
    }

    @Test
    void r1_normalizeEdgeCases() {
        assertThat(UniqueNormalize.normalize(List.of())).isEmpty();
        assertThatThrownBy(() -> UniqueNormalize.normalize(null)).isInstanceOf(NullPointerException.class);
    }

    @Test
    void r2_duplicates() {
        assertThat(UniqueNormalize.duplicates(List.of(1, 2, 1, 3, 2, 1, 4))).containsExactly(1, 2);
        assertThat(UniqueNormalize.duplicates(List.of("a", "b"))).isEmpty();
        assertThat(UniqueNormalize.duplicates(List.<String>of())).isEmpty();
    }

    @Test
    void r3_setAlgebra() {
        Set<Integer> a = new LinkedHashSet<>(List.of(1, 2, 3));
        Set<Integer> b = new LinkedHashSet<>(List.of(3, 4));
        assertThat(UniqueNormalize.union(a, b)).containsExactlyInAnyOrder(1, 2, 3, 4);
        assertThat(UniqueNormalize.intersection(a, b)).containsExactly(3);
        assertThat(UniqueNormalize.difference(a, b)).containsExactlyInAnyOrder(1, 2);
        assertThat(UniqueNormalize.difference(b, a)).containsExactly(4);
    }

    @Test
    void r3_argumentsAreNeverMutated() {
        Set<String> a = new LinkedHashSet<>(List.of("x", "y"));
        Set<String> b = new LinkedHashSet<>(List.of("y", "z"));
        UniqueNormalize.union(a, b);
        UniqueNormalize.intersection(a, b);
        UniqueNormalize.difference(a, b);
        assertThat(a).containsExactly("x", "y");
        assertThat(b).containsExactly("y", "z");
    }

    @Test
    void r3_disjointAndEmpty() {
        Set<Integer> empty = Set.of();
        assertThat(UniqueNormalize.intersection(Set.of(1), Set.of(2))).isEmpty();
        assertThat(UniqueNormalize.union(empty, empty)).isEmpty();
        assertThat(UniqueNormalize.difference(Set.of(1, 2), empty)).containsExactlyInAnyOrder(1, 2);
    }

    @Test
    void r4_caseInsensitiveSortedSet() {
        List<String> words = new ArrayList<>(List.of("pear", "Apple", "apple", "Banana", "APPLE"));
        var set = UniqueNormalize.sortedCaseInsensitive(words);
        assertThat(set).containsExactly("Apple", "Banana", "pear");
        assertThat(set.contains("BANANA")).isTrue();
    }
}
