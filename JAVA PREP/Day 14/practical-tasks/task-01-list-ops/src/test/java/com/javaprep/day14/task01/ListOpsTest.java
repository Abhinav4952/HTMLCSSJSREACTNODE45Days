package com.javaprep.day14.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ListOpsTest {

    @Test
    void r1_dedupeKeepsFirstOccurrenceOrder() {
        assertThat(ListOps.dedupe(List.of("b", "a", "b", "c", "a"))).containsExactly("b", "a", "c");
        assertThat(ListOps.dedupe(new LinkedList<>(List.of(3, 3, 3)))).containsExactly(3);
        assertThat(ListOps.dedupe(List.<String>of())).isEmpty();
    }

    @Test
    void r1_dedupeReturnsNewMutableListAndRejectsNull() {
        List<String> in = new ArrayList<>(List.of("a", "a"));
        List<String> out = ListOps.dedupe(in);
        out.add("z");
        assertThat(in).containsExactly("a", "a");
        assertThatThrownBy(() -> ListOps.dedupe(null)).isInstanceOf(NullPointerException.class);
    }

    @Test
    void r2_rotateRight() {
        assertThat(ListOps.rotate(List.of(1, 2, 3, 4, 5), 2)).containsExactly(4, 5, 1, 2, 3);
        assertThat(ListOps.rotate(List.of(1, 2, 3), 0)).containsExactly(1, 2, 3);
        assertThat(ListOps.rotate(List.of(1, 2, 3), 3)).containsExactly(1, 2, 3);
        assertThat(ListOps.rotate(List.of(1, 2, 3), 4)).containsExactly(3, 1, 2);
    }

    @Test
    void r2_rotateLeftAndEmpty() {
        assertThat(ListOps.rotate(List.of(1, 2, 3, 4), -1)).containsExactly(2, 3, 4, 1);
        assertThat(ListOps.rotate(List.of(1, 2, 3), -7)).containsExactly(2, 3, 1);
        assertThat(ListOps.rotate(List.<Integer>of(), 5)).isEmpty();
    }

    @Test
    void r3_chunk() {
        List<List<Integer>> chunks = ListOps.chunk(List.of(1, 2, 3, 4, 5), 2);
        assertThat(chunks).containsExactly(List.of(1, 2), List.of(3, 4), List.of(5));
        assertThat(ListOps.chunk(List.of(1, 2), 10)).containsExactly(List.of(1, 2));
        assertThat(ListOps.chunk(List.<Integer>of(), 3)).isEmpty();
    }

    @Test
    void r3_chunksAreIndependentCopiesAndSizeIsValidated() {
        List<Integer> source = new ArrayList<>(List.of(1, 2, 3, 4));
        List<List<Integer>> chunks = ListOps.chunk(source, 2);
        source.set(0, 99);
        assertThat(chunks.get(0)).containsExactly(1, 2);
        assertThatThrownBy(() -> ListOps.chunk(source, 0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> ListOps.chunk(source, -2)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    @DisplayName("Trap: remove the VALUE 1, not the element at index 1")
    void r4_removeFirstOccurrenceByValue() {
        List<Integer> in = new ArrayList<>(List.of(10, 20, 30, 1, 2));
        assertThat(ListOps.removeFirstOccurrence(in, 1)).containsExactly(10, 20, 30, 2);
        assertThat(in).containsExactly(10, 20, 30, 1, 2);
    }

    @Test
    void r4_removeOnlyFirstAndMissingValue() {
        assertThat(ListOps.removeFirstOccurrence(List.of(5, 7, 5, 7), 7)).containsExactly(5, 5, 7);
        assertThat(ListOps.removeFirstOccurrence(new LinkedList<>(List.of(1, 2)), 9)).containsExactly(1, 2);
    }
}
