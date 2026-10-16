package com.javaprep.day11.task01;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ParseIntSafeTest {

    @Test
    @DisplayName("valid integers are parsed")
    void valid() {
        assertThat(ParseIntSafe.parseOrDefault("42", -1)).isEqualTo(42);
        assertThat(ParseIntSafe.parseOrDefault("-7", 0)).isEqualTo(-7);
    }

    @Test
    @DisplayName("unparsable input yields the default")
    void invalid() {
        assertThat(ParseIntSafe.parseOrDefault("abc", 9)).isEqualTo(9);
        assertThat(ParseIntSafe.parseOrDefault("", 9)).isEqualTo(9);
        assertThat(ParseIntSafe.parseOrDefault(" 7", 9)).isEqualTo(9);
        assertThat(ParseIntSafe.parseOrDefault("99999999999", 9)).isEqualTo(9);
    }

    @Test
    @DisplayName("null -> NullPointerException (not the default)")
    void nullInput() {
        assertThatThrownBy(() -> ParseIntSafe.parseOrDefault(null, 1)).isInstanceOf(NullPointerException.class);
    }
}
