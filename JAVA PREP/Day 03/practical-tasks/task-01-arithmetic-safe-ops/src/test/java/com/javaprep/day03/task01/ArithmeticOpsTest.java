package com.javaprep.day03.task01;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ArithmeticOpsTest {

    @Test
    @DisplayName("divide truncates toward zero")
    void divide() {
        assertThat(ArithmeticOps.divide(7, 2)).isEqualTo(3);
        assertThat(ArithmeticOps.divide(-7, 2)).isEqualTo(-3);
        assertThat(ArithmeticOps.divide(0, 5)).isZero();
    }

    @Test
    @DisplayName("remainder takes the sign of the dividend")
    void remainder() {
        assertThat(ArithmeticOps.remainder(7, 2)).isEqualTo(1);
        assertThat(ArithmeticOps.remainder(-7, 2)).isEqualTo(-1);
        assertThat(ArithmeticOps.remainder(7, -2)).isEqualTo(1);
    }

    @Test
    @DisplayName("division by zero -> ArithmeticException")
    void byZero() {
        assertThatThrownBy(() -> ArithmeticOps.divide(1, 0)).isInstanceOf(ArithmeticException.class);
        assertThatThrownBy(() -> ArithmeticOps.remainder(1, 0)).isInstanceOf(ArithmeticException.class);
    }
}
