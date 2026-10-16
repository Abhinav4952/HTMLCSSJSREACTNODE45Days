package com.javaprep.day05.task04;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class TextBlockTemplateTest {

    @Test
    @DisplayName("renders both lines with a trailing newline")
    void renders() {
        assertThat(TextBlockTemplate.welcome("Ada", 5))
                .isEqualTo("Welcome, Ada!\nYou are on Day 5 of Java Prep.\n");
    }

    @Test
    @DisplayName("is multi-line and reflects different inputs")
    void multiLine() {
        String out = TextBlockTemplate.welcome("Bob", 12);
        assertThat(out.lines().toList()).containsExactly("Welcome, Bob!", "You are on Day 12 of Java Prep.");
    }

    @Test
    @DisplayName("null name -> NullPointerException")
    void nullName() {
        assertThatThrownBy(() -> TextBlockTemplate.welcome(null, 1)).isInstanceOf(NullPointerException.class);
    }
}
