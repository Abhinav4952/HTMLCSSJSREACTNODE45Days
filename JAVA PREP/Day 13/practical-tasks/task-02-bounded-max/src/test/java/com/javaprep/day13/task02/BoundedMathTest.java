package com.javaprep.day13.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class BoundedMathTest {

    static class Animal implements Comparable<Animal> {
        final int weight;

        Animal(int weight) {
            this.weight = weight;
        }

        @Override
        public int compareTo(Animal o) {
            return Integer.compare(weight, o.weight);
        }
    }

    static class Dog extends Animal {
        Dog(int weight) {
            super(weight);
        }
    }

    @Test
    void r1_maxOfStringsAndIntegers() {
        assertThat(BoundedMath.max(List.of("pear", "apple", "zoo", "kiwi"))).isEqualTo("zoo");
        assertThat(BoundedMath.max(List.of(3, 9, -2))).isEqualTo(9);
        assertThat(BoundedMath.max(List.of(5))).isEqualTo(5);
    }

    @Test
    void r1_maxRejectsNullAndEmpty() {
        assertThatThrownBy(() -> BoundedMath.max(List.<Integer>of())).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> BoundedMath.max((List<Integer>) null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r2_minOfStringsAndDoubles() {
        assertThat(BoundedMath.min(List.of("pear", "apple", "zoo"))).isEqualTo("apple");
        assertThat(BoundedMath.min(List.of(2.5, -1.0, 7.0))).isEqualTo(-1.0);
        assertThatThrownBy(() -> BoundedMath.min(new ArrayList<Integer>())).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r3_worksForSubclassOfComparableParent() {
        Dog light = new Dog(10);
        Dog heavy = new Dog(30);
        Dog result = BoundedMath.max(List.of(light, heavy));
        assertThat(result).isSameAs(heavy);
        assertThat(BoundedMath.min(List.of(light, heavy))).isSameAs(light);
    }

    @Test
    void r4_clamp() {
        assertThat(BoundedMath.clamp(5, 1, 10)).isEqualTo(5);
        assertThat(BoundedMath.clamp(-4, 0, 10)).isEqualTo(0);
        assertThat(BoundedMath.clamp(99, 0, 10)).isEqualTo(10);
        assertThat(BoundedMath.clamp(2.5, 2.5, 2.5)).isEqualTo(2.5);
    }

    @Test
    void r4_clampRejectsInvertedRange() {
        assertThatThrownBy(() -> BoundedMath.clamp(5, 10, 1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r5_sumAcceptsAnyNumberCollection() {
        assertThat(BoundedMath.sum(List.of(1, 2, 3))).isEqualTo(6.0);
        assertThat(BoundedMath.sum(List.of(1.5, 2.5))).isEqualTo(4.0);
        assertThat(BoundedMath.sum(Set.of(10L))).isEqualTo(10.0);
        assertThat(BoundedMath.sum(List.<Number>of())).isEqualTo(0.0);
    }
}
