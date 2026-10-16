package com.javaprep.day06.task04;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class VarargsMaxTest {

    @Test
    @DisplayName("max of first and rest")
    void max() {
        assertThat(VarargsMax.max(1, 5, 3)).isEqualTo(5);
        assertThat(VarargsMax.max(9, 2, 4)).isEqualTo(9);
        assertThat(VarargsMax.max(-3, -1, -2)).isEqualTo(-1);
    }

    @Test
    @DisplayName("rest may be empty")
    void onlyFirst() {
        assertThat(VarargsMax.max(42)).isEqualTo(42);
        assertThat(VarargsMax.max(7, new int[0])).isEqualTo(7);
    }

    @Test
    @DisplayName("null rest array -> NullPointerException")
    void nullRest() {
        assertThatThrownBy(() -> VarargsMax.max(1, (int[]) null)).isInstanceOf(NullPointerException.class);
    }
}
