package com.javaprep.day01.task02;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class MathUtilTest {

    @Test
    @DisplayName("add sums two ints, including negatives and zero")
    void add() {
        assertThat(MathUtil.add(2, 3)).isEqualTo(5);
        assertThat(MathUtil.add(-2, 3)).isEqualTo(1);
        assertThat(MathUtil.add(0, 0)).isZero();
    }

    @Test
    @DisplayName("multiply multiplies two ints")
    void multiply() {
        assertThat(MathUtil.multiply(4, 5)).isEqualTo(20);
        assertThat(MathUtil.multiply(-4, 5)).isEqualTo(-20);
        assertThat(MathUtil.multiply(7, 0)).isZero();
    }
}
