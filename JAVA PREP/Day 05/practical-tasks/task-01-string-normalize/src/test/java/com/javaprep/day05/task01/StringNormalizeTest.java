package com.javaprep.day05.task01;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class StringNormalizeTest {

    @Test
    @DisplayName("strips, collapses whitespace runs and lower-cases")
    void normalizes() {
        assertThat(StringNormalize.normalize("  Hello   World \t")).isEqualTo("hello world");
        assertThat(StringNormalize.normalize("A\n\nB")).isEqualTo("a b");
        assertThat(StringNormalize.normalize("ALREADY")).isEqualTo("already");
    }

    @Test
    @DisplayName("empty and whitespace-only input become empty")
    void empties() {
        assertThat(StringNormalize.normalize("")).isEmpty();
        assertThat(StringNormalize.normalize("   \t ")).isEmpty();
    }

    @Test
    @DisplayName("null -> NullPointerException")
    void nullInput() {
        assertThatThrownBy(() -> StringNormalize.normalize(null)).isInstanceOf(NullPointerException.class);
    }
}
