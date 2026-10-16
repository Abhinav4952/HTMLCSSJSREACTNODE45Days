package com.javaprep.day12.task04;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

class LengthThenAlphaTest {

    @Test
    @DisplayName("sorts by length then alphabetically")
    void sorts() {
        List<String> words = new ArrayList<>(List.of("bb", "a", "ccc", "aa", "b"));
        words.sort(LengthThenAlpha.comparator());
        assertThat(words).containsExactly("a", "b", "aa", "bb", "ccc");
    }

    @Test
    @DisplayName("compare sign semantics")
    void compare() {
        Comparator<String> c = LengthThenAlpha.comparator();
        assertThat(c.compare("b", "aa")).isNegative();
        assertThat(c.compare("aa", "b")).isPositive();
        assertThat(c.compare("a", "b")).isNegative();
        assertThat(c.compare("same", "same")).isZero();
    }

    @Test
    @DisplayName("is implemented as an anonymous class (Day 12 lesson)")
    void anonymousClass() {
        assertThat(LengthThenAlpha.comparator().getClass().isAnonymousClass()).isTrue();
    }
}
