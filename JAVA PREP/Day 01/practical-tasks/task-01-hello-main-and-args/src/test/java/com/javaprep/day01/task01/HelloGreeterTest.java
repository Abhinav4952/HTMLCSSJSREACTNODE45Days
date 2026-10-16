package com.javaprep.day01.task01;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class HelloGreeterTest {

    @Test
    @DisplayName("uses first argument as the name")
    void usesFirstArg() {
        assertThat(HelloGreeter.greet(new String[] {"Ada"})).isEqualTo("Hello, Ada!");
        assertThat(HelloGreeter.greet(new String[] {"Ada", "Bob"})).isEqualTo("Hello, Ada!");
    }

    @Test
    @DisplayName("strips surrounding whitespace from the name")
    void stripsName() {
        assertThat(HelloGreeter.greet(new String[] {"  Grace  "})).isEqualTo("Hello, Grace!");
    }

    @Test
    @DisplayName("falls back to World for empty, null, or blank input")
    void defaults() {
        assertThat(HelloGreeter.greet(new String[0])).isEqualTo("Hello, World!");
        assertThat(HelloGreeter.greet(null)).isEqualTo("Hello, World!");
        assertThat(HelloGreeter.greet(new String[] {"   "})).isEqualTo("Hello, World!");
        assertThat(HelloGreeter.greet(new String[] {null})).isEqualTo("Hello, World!");
    }
}
