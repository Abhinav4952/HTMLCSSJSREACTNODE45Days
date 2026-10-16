package com.javaprep.day12.task01;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

class SafeSumTest {

    @Test
    @DisplayName("sums boxed integers")
    void sums() {
        assertThat(SafeSum.sum(List.of(1, 2, 3))).isEqualTo(6);
        assertThat(SafeSum.sum(List.of())).isZero();
        assertThat(SafeSum.sum(List.of(-5, 5))).isZero();
    }

    @Test
    @DisplayName("null elements count as 0 instead of throwing on unboxing")
    void nullElements() {
        assertThat(SafeSum.sum(Arrays.asList(1, null, 3))).isEqualTo(4);
        assertThat(SafeSum.sum(Arrays.asList(null, null))).isZero();
    }

    @Test
    @DisplayName("null list -> NullPointerException")
    void nullList() {
        assertThatThrownBy(() -> SafeSum.sum(null)).isInstanceOf(NullPointerException.class);
    }
}
