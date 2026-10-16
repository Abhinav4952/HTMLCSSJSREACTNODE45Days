package com.javaprep.day04.task04;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class PairSearchTest {

    @Test
    @DisplayName("finds the first pair in scan order")
    void firstPair() {
        assertThat(PairSearch.findPair(new int[] {2, 7, 11, 15}, 9)).containsExactly(0, 1);
        assertThat(PairSearch.findPair(new int[] {1, 2, 3, 4}, 5)).containsExactly(0, 3);
        assertThat(PairSearch.findPair(new int[] {3, 2, 4}, 6)).containsExactly(1, 2);
    }

    @Test
    @DisplayName("no pair -> empty array")
    void none() {
        assertThat(PairSearch.findPair(new int[] {1, 2, 3}, 100)).isEmpty();
        assertThat(PairSearch.findPair(new int[] {5}, 5)).isEmpty();
        assertThat(PairSearch.findPair(new int[0], 0)).isEmpty();
    }

    @Test
    @DisplayName("an element is not paired with itself")
    void noSelfPair() {
        assertThat(PairSearch.findPair(new int[] {3, 1}, 6)).isEmpty();
    }

    @Test
    @DisplayName("null array -> NullPointerException")
    void nullInput() {
        assertThatThrownBy(() -> PairSearch.findPair(null, 1)).isInstanceOf(NullPointerException.class);
    }
}
