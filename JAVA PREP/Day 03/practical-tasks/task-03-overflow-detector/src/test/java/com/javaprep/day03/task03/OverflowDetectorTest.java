package com.javaprep.day03.task03;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class OverflowDetectorTest {

    @Test
    @DisplayName("normal sums are returned")
    void normal() {
        assertThat(OverflowDetector.addExact(2, 3)).isEqualTo(5);
        assertThat(OverflowDetector.addExact(Integer.MAX_VALUE, 0)).isEqualTo(Integer.MAX_VALUE);
        assertThat(OverflowDetector.addExact(Integer.MAX_VALUE, Integer.MIN_VALUE)).isEqualTo(-1);
    }

    @Test
    @DisplayName("positive and negative overflow -> ArithmeticException")
    void overflow() {
        assertThatThrownBy(() -> OverflowDetector.addExact(Integer.MAX_VALUE, 1))
                .isInstanceOf(ArithmeticException.class);
        assertThatThrownBy(() -> OverflowDetector.addExact(Integer.MIN_VALUE, -1))
                .isInstanceOf(ArithmeticException.class);
    }
}
