package com.javaprep.day08.task03;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class ImmutableNamesTest {

    @Test
    @DisplayName("exposes the given names in order")
    void exposesNames() {
        assertThat(new ImmutableNames(List.of("a", "b")).names()).containsExactly("a", "b");
    }

    @Test
    @DisplayName("defensively copies the input list")
    void defensiveCopy() {
        List<String> source = new ArrayList<>(List.of("a", "b"));
        ImmutableNames holder = new ImmutableNames(source);
        source.add("c");
        source.set(0, "z");
        assertThat(holder.names()).containsExactly("a", "b");
    }

    @Test
    @DisplayName("returned list is unmodifiable")
    void unmodifiable() {
        List<String> view = new ImmutableNames(List.of("a")).names();
        assertThatThrownBy(() -> view.add("x")).isInstanceOf(UnsupportedOperationException.class);
        assertThatThrownBy(() -> view.remove(0)).isInstanceOf(UnsupportedOperationException.class);
    }

    @Test
    @DisplayName("null list or null element -> NullPointerException")
    void nulls() {
        assertThatThrownBy(() -> new ImmutableNames(null)).isInstanceOf(NullPointerException.class);
        assertThatThrownBy(() -> new ImmutableNames(Arrays.asList("a", null))).isInstanceOf(NullPointerException.class);
    }
}
