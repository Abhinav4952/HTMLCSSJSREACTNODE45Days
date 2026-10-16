package com.javaprep.day05.task02;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class StringCompareTest {

    @Test
    @DisplayName("sameReference distinguishes identity from equality")
    void identity() {
        String literal = "java";
        String copy = new String("java");
        assertThat(StringCompare.sameReference(literal, "java")).isTrue();
        assertThat(StringCompare.sameReference(literal, copy)).isFalse();
        assertThat(StringCompare.sameReference(null, null)).isTrue();
    }

    @Test
    @DisplayName("sameContent compares characters and is null-safe")
    void content() {
        assertThat(StringCompare.sameContent("java", new String("java"))).isTrue();
        assertThat(StringCompare.sameContent("java", "Java")).isFalse();
        assertThat(StringCompare.sameContent(null, null)).isTrue();
        assertThat(StringCompare.sameContent("java", null)).isFalse();
        assertThat(StringCompare.sameContent(null, "java")).isFalse();
    }
}
