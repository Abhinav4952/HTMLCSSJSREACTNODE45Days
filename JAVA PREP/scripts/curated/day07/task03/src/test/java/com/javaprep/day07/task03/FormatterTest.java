package com.javaprep.day07.task03;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class FormatterTest {

    @Test
    @DisplayName("int overload")
    void intOverload() {
        assertThat(Formatter.format(5)).isEqualTo("INT:5");
        assertThat(Formatter.format('a')).isEqualTo("INT:97"); // char widens to int
    }

    @Test
    @DisplayName("double overload (also chosen for long/float via widening)")
    void doubleOverload() {
        assertThat(Formatter.format(2.5)).isEqualTo("DBL:2.5");
        assertThat(Formatter.format(5L)).isEqualTo("DBL:5.0");
        assertThat(Formatter.format(1.5f)).isEqualTo("DBL:1.5");
    }

    @Test
    @DisplayName("String overload; null -> NullPointerException")
    void stringOverload() {
        assertThat(Formatter.format("hi")).isEqualTo("STR:hi");
        assertThatThrownBy(() -> Formatter.format((String) null)).isInstanceOf(NullPointerException.class);
    }
}
