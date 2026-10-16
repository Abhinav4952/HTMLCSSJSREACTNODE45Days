package com.javaprep.day13.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class PecsTest {

    @Test
    void r1_copyIntegersIntoNumberList() {
        List<Number> dst = new ArrayList<>(List.of(0.5));
        List<Integer> src = List.of(1, 2, 3);
        Pecs.copy(dst, src);
        assertThat(dst).containsExactly(0.5, 1, 2, 3);
    }

    @Test
    void r1_copyIntoObjectListAndEmptySource() {
        List<Object> dst = new ArrayList<>(List.of("x"));
        Pecs.copy(dst, List.of("a", "b"));
        Pecs.copy(dst, List.<Integer>of());
        assertThat(dst).containsExactly("x", "a", "b");
    }

    @Test
    void r2_moveAllEmptiesSource() {
        List<Integer> src = new ArrayList<>(List.of(4, 5));
        Collection<Number> dst = new ArrayList<>(List.of(1.5));
        Pecs.moveAll(src, dst);
        assertThat(src).isEmpty();
        assertThat(dst).containsExactly(1.5, 4, 5);
    }

    @Test
    void r2_moveAllIntoSet() {
        Set<String> src = new HashSet<>(Set.of("a", "b"));
        Set<Object> dst = new HashSet<>();
        Pecs.moveAll(src, dst);
        assertThat(src).isEmpty();
        assertThat(dst).containsExactlyInAnyOrder("a", "b");
    }

    @Test
    void r3_fill() {
        List<Number> dst = new ArrayList<>();
        Pecs.fill(dst, 7, 3);
        assertThat(dst).containsExactly(7, 7, 7);
        List<Object> objs = new ArrayList<>();
        Pecs.fill(objs, "z", 0);
        assertThat(objs).isEmpty();
    }

    @Test
    void r3_fillRejectsNegative() {
        List<Object> dst = new ArrayList<>();
        assertThatThrownBy(() -> Pecs.fill(dst, "x", -1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r4_firstOrDefault() {
        Number n = Pecs.firstOrDefault(List.of(10, 20), 0.5);
        assertThat(n).isEqualTo(10);
        Number fallback = Pecs.firstOrDefault(List.<Integer>of(), 0.5);
        assertThat(fallback).isEqualTo(0.5);
    }

    @Test
    void r5_swapWorksOnAnyListType() {
        List<String> strings = new ArrayList<>(List.of("a", "b", "c"));
        Pecs.swap(strings, 0, 2);
        assertThat(strings).containsExactly("c", "b", "a");

        List<Integer> ints = new ArrayList<>(List.of(1, 2));
        Pecs.swap(ints, 1, 1);
        assertThat(ints).containsExactly(1, 2);
    }

    @Test
    void r5_swapOutOfRange() {
        List<String> strings = new ArrayList<>(List.of("a"));
        assertThatThrownBy(() -> Pecs.swap(strings, 0, 3)).isInstanceOf(IndexOutOfBoundsException.class);
    }
}
