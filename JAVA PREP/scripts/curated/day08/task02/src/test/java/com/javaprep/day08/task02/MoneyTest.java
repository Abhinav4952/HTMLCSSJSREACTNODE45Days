package com.javaprep.day08.task02;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class MoneyTest {

    @Test
    @DisplayName("stores cents, zero allowed")
    void stores() {
        assertThat(new Money(150).cents()).isEqualTo(150L);
        assertThat(new Money(0).cents()).isZero();
    }

    @Test
    @DisplayName("negative cents -> IllegalArgumentException")
    void negative() {
        assertThatThrownBy(() -> new Money(-1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    @DisplayName("plus returns a new Money and leaves operands untouched")
    void plus() {
        Money a = new Money(100);
        Money b = new Money(250);
        Money sum = a.plus(b);
        assertThat(sum.cents()).isEqualTo(350L);
        assertThat(sum).isNotSameAs(a).isNotSameAs(b);
        assertThat(a.cents()).isEqualTo(100L);
        assertThat(b.cents()).isEqualTo(250L);
    }

    @Test
    @DisplayName("plus(null) -> NullPointerException")
    void plusNull() {
        assertThatThrownBy(() -> new Money(1).plus(null)).isInstanceOf(NullPointerException.class);
    }
}
