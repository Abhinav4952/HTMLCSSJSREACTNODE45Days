package com.javaprep.day05.task03;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class JoinerTest {

    @Test
    @DisplayName("joins with the delimiter")
    void joins() {
        assertThat(Joiner.join(",", "a", "b", "c")).isEqualTo("a,b,c");
        assertThat(Joiner.join(", ", "x", "y")).isEqualTo("x, y");
        assertThat(Joiner.join("-", "solo")).isEqualTo("solo");
    }

    @Test
    @DisplayName("no parts gives an empty string; empty delimiter concatenates")
    void edges() {
        assertThat(Joiner.join(",")).isEmpty();
        assertThat(Joiner.join("", "a", "b")).isEqualTo("ab");
    }

    @Test
    @DisplayName("null part is treated as empty")
    void nullPart() {
        assertThat(Joiner.join(",", "a", null, "c")).isEqualTo("a,,c");
    }

    @Test
    @DisplayName("null delimiter or null parts array -> NullPointerException")
    void nulls() {
        assertThatThrownBy(() -> Joiner.join(null, "a")).isInstanceOf(NullPointerException.class);
        assertThatThrownBy(() -> Joiner.join(",", (String[]) null)).isInstanceOf(NullPointerException.class);
    }
}
