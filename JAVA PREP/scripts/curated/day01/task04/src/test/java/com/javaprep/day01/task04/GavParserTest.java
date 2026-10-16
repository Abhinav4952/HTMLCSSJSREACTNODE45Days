package com.javaprep.day01.task04;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class GavParserTest {

    @Test
    @DisplayName("parses a well-formed GAV")
    void parses() {
        assertThat(GavParser.parse("org.junit.jupiter:junit-jupiter:5.11.4"))
                .containsExactly("org.junit.jupiter", "junit-jupiter", "5.11.4");
    }

    @Test
    @DisplayName("wrong number of parts is rejected")
    void wrongPartCount() {
        assertThatThrownBy(() -> GavParser.parse("a:b")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GavParser.parse("a:b:c:d")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GavParser.parse("a:b:c:")).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    @DisplayName("blank parts and null input are rejected")
    void blankOrNull() {
        assertThatThrownBy(() -> GavParser.parse("a::c")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GavParser.parse(" :b:c")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GavParser.parse(null)).isInstanceOf(IllegalArgumentException.class);
    }
}
