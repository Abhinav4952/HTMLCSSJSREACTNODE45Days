package com.javaprep.day13.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.NoSuchElementException;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class BoxTest {

    @Test
    @DisplayName("of() wraps a value and rejects null")
    void r1_of() {
        Box<String> box = Box.of("hi");
        assertThat(box.get()).isEqualTo("hi");
        assertThatThrownBy(() -> Box.of(null)).isInstanceOf(NullPointerException.class);
    }

    @Test
    void r2_emptyBoxBehavior() {
        Box<String> empty = Box.empty();
        assertThat(empty.isEmpty()).isTrue();
        assertThat(Box.of(1).isEmpty()).isFalse();
        assertThatThrownBy(empty::get).isInstanceOf(NoSuchElementException.class);
    }

    @Test
    void r3_orElse() {
        assertThat(Box.of("a").orElse("z")).isEqualTo("a");
        assertThat(Box.<String>empty().orElse("z")).isEqualTo("z");
    }

    @Test
    void r4_mapTransformsValue() {
        Box<Integer> length = Box.of("hello").map(String::length);
        assertThat(length.get()).isEqualTo(5);
    }

    @Test
    void r4_mapAcceptsWiderFunction() {
        Function<Object, CharSequence> describe = o -> "<" + o + ">";
        Box<CharSequence> result = Box.of(42).map(describe);
        assertThat(result.get().toString()).isEqualTo("<42>");
    }

    @Test
    void r4_mapOnEmptyNeverCallsFunction() {
        AtomicInteger calls = new AtomicInteger();
        Box<Integer> result = Box.<String>empty().map(s -> {
            calls.incrementAndGet();
            return s.length();
        });
        assertThat(result.isEmpty()).isTrue();
        assertThat(calls).hasValue(0);
    }

    @Test
    void r4_mapReturningNullGivesEmpty() {
        Box<String> result = Box.of("x").map(s -> (String) null);
        assertThat(result.isEmpty()).isTrue();
    }

    @Test
    void r5_equalsHashCodeToString() {
        assertThat(Box.of("a")).isEqualTo(Box.of("a")).hasSameHashCodeAs(Box.of("a"));
        assertThat(Box.of("a")).isNotEqualTo(Box.of("b"));
        assertThat(Box.empty()).isEqualTo(Box.empty()).isNotEqualTo(Box.of(1));
        assertThat(Box.of(7).toString()).isEqualTo("Box[7]");
        assertThat(Box.empty().toString()).isEqualTo("Box.empty");
    }

    @Test
    @DisplayName("Erasure: Box<String> and Box<Integer> are the same runtime class")
    void r6_erasure() {
        Box<String> s = Box.of("a");
        Box<Integer> i = Box.of(1);
        assertThat(s.getClass()).isSameAs(i.getClass()).isSameAs(Box.class);
    }
}
