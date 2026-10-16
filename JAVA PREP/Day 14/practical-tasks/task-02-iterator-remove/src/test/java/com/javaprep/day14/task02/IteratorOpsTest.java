package com.javaprep.day14.task02;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class IteratorOpsTest {

    @Test
    void r1_removeNegativesInPlace() {
        List<Integer> list = new ArrayList<>(List.of(5, -1, 7, -3, 0));
        int removed = IteratorOps.removeNegatives(list);
        assertThat(removed).isEqualTo(2);
        assertThat(list).containsExactly(5, 7, 0);
    }

    @Test
    void r1_removeNegativesEdgeCases() {
        List<Integer> none = new LinkedList<>(List.of(1, 2));
        assertThat(IteratorOps.removeNegatives(none)).isZero();
        List<Integer> all = new LinkedList<>(List.of(-1, -2, -3));
        assertThat(IteratorOps.removeNegatives(all)).isEqualTo(3);
        assertThat(all).isEmpty();
        assertThat(IteratorOps.removeNegatives(new ArrayList<>())).isZero();
    }

    @Test
    void r2_removeMatchingWorksOnAnyCollection() {
        Set<String> set = new TreeSet<>(List.of("apple", "avocado", "banana"));
        int removed = IteratorOps.removeMatching(set, s -> s.startsWith("a"));
        assertThat(removed).isEqualTo(2);
        assertThat(set).containsExactly("banana");

        List<Integer> nums = new ArrayList<>(List.of(1, 2, 3, 4, 5, 6));
        assertThat(IteratorOps.removeMatching(nums, n -> n % 2 == 0)).isEqualTo(3);
        assertThat(nums).containsExactly(1, 3, 5);
    }

    @Test
    void r3_duplicateEvens() {
        List<Integer> list = new ArrayList<>(List.of(1, 2, 3, 4));
        IteratorOps.duplicateEvens(list);
        assertThat(list).containsExactly(1, 2, 2, 3, 4, 4);
        List<Integer> odds = new LinkedList<>(List.of(1, 3));
        IteratorOps.duplicateEvens(odds);
        assertThat(odds).containsExactly(1, 3);
        List<Integer> zeros = new ArrayList<>(List.of(0));
        IteratorOps.duplicateEvens(zeros);
        assertThat(zeros).containsExactly(0, 0);
    }

    @Test
    @DisplayName("Removing the first element during for-each throws CME")
    void r4_removeFirstThrows() {
        assertThat(IteratorOps.forEachRemovalThrows(List.of("a", "b", "c"), "a")).isTrue();
        assertThat(IteratorOps.forEachRemovalThrows(List.of("a", "b", "c"), "c")).isTrue();
    }

    @Test
    @DisplayName("Removing the second-to-last element silently does NOT throw")
    void r4_secondToLastDoesNotThrow() {
        assertThat(IteratorOps.forEachRemovalThrows(List.of("a", "b", "c"), "b")).isFalse();
        assertThat(IteratorOps.forEachRemovalThrows(List.of("a", "b", "c"), "zzz")).isFalse();
    }

    @Test
    void r4_doesNotMutateTheInput() {
        List<String> input = new ArrayList<>(List.of("a", "b", "c"));
        IteratorOps.forEachRemovalThrows(input, "a");
        assertThat(input).containsExactly("a", "b", "c");
    }
}
