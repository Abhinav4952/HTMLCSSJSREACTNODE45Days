package com.javaprep.day06.task03;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class SortSearchTest {

    @Test
    @DisplayName("returns the index within the sorted copy")
    void found() {
        int[] data = {5, 3, 9, 1};
        assertThat(SortSearch.indexOfSortedCopy(data, 1)).isZero();
        assertThat(SortSearch.indexOfSortedCopy(data, 5)).isEqualTo(2);
        assertThat(SortSearch.indexOfSortedCopy(data, 9)).isEqualTo(3);
    }

    @Test
    @DisplayName("missing key -> -1 (also for empty array)")
    void missing() {
        assertThat(SortSearch.indexOfSortedCopy(new int[] {5, 3, 9}, 4)).isEqualTo(-1);
        assertThat(SortSearch.indexOfSortedCopy(new int[0], 1)).isEqualTo(-1);
    }

    @Test
    @DisplayName("the original array is not reordered")
    void originalUntouched() {
        int[] data = {5, 3, 9, 1};
        SortSearch.indexOfSortedCopy(data, 9);
        assertThat(data).containsExactly(5, 3, 9, 1);
    }

    @Test
    @DisplayName("null -> NullPointerException")
    void nullInput() {
        assertThatThrownBy(() -> SortSearch.indexOfSortedCopy(null, 1)).isInstanceOf(NullPointerException.class);
    }
}
