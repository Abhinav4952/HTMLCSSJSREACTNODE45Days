package com.javaprep.day06.task01;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ArrayStatsTest {

    private final int[] data = {4, -2, 9, 1};

    @Test
    @DisplayName("min / max / average")
    void stats() {
        assertThat(ArrayStats.min(data)).isEqualTo(-2);
        assertThat(ArrayStats.max(data)).isEqualTo(9);
        assertThat(ArrayStats.average(data)).isEqualTo(3.0);
        assertThat(ArrayStats.average(new int[] {1, 2})).isEqualTo(1.5);
    }

    @Test
    @DisplayName("single element")
    void single() {
        assertThat(ArrayStats.min(new int[] {7})).isEqualTo(7);
        assertThat(ArrayStats.max(new int[] {7})).isEqualTo(7);
        assertThat(ArrayStats.average(new int[] {7})).isEqualTo(7.0);
    }

    @Test
    @DisplayName("empty -> IllegalArgumentException")
    void empty() {
        assertThatThrownBy(() -> ArrayStats.min(new int[0])).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> ArrayStats.max(new int[0])).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> ArrayStats.average(new int[0])).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    @DisplayName("null -> NullPointerException")
    void nulls() {
        assertThatThrownBy(() -> ArrayStats.min(null)).isInstanceOf(NullPointerException.class);
        assertThatThrownBy(() -> ArrayStats.max(null)).isInstanceOf(NullPointerException.class);
        assertThatThrownBy(() -> ArrayStats.average(null)).isInstanceOf(NullPointerException.class);
    }
}
