package com.javaprep.day06.task02;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class MatrixSumTest {

    @Test
    @DisplayName("sums a rectangular matrix")
    void rectangular() {
        assertThat(MatrixSum.sum(new int[][] {{1, 2, 3}, {4, 5, 6}})).isEqualTo(21L);
    }

    @Test
    @DisplayName("handles jagged and empty rows / empty matrix")
    void jaggedAndEmpty() {
        assertThat(MatrixSum.sum(new int[][] {{1}, {}, {2, 3}})).isEqualTo(6L);
        assertThat(MatrixSum.sum(new int[0][0])).isZero();
    }

    @Test
    @DisplayName("sums into a long")
    void noOverflow() {
        assertThat(MatrixSum.sum(new int[][] {{Integer.MAX_VALUE}, {Integer.MAX_VALUE}})).isEqualTo(4_294_967_294L);
    }

    @Test
    @DisplayName("null matrix or null row -> NullPointerException")
    void nulls() {
        assertThatThrownBy(() -> MatrixSum.sum(null)).isInstanceOf(NullPointerException.class);
        assertThatThrownBy(() -> MatrixSum.sum(new int[][] {{1}, null})).isInstanceOf(NullPointerException.class);
    }
}
