package com.javaprep.day12.task03;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class CounterFactoryTest {

    @Test
    @DisplayName("new counter starts at the given value")
    void start() {
        assertThat(CounterFactory.newCounter(5).value()).isEqualTo(5);
        assertThat(CounterFactory.newCounter(-3).value()).isEqualTo(-3);
    }

    @Test
    @DisplayName("increment returns the new value and updates state")
    void increment() {
        CounterFactory.Counter c = CounterFactory.newCounter(5);
        assertThat(c.increment()).isEqualTo(6);
        assertThat(c.increment()).isEqualTo(7);
        assertThat(c.value()).isEqualTo(7);
    }

    @Test
    @DisplayName("counters are independent")
    void independent() {
        CounterFactory.Counter a = CounterFactory.newCounter(0);
        CounterFactory.Counter b = CounterFactory.newCounter(100);
        a.increment();
        assertThat(a.value()).isEqualTo(1);
        assertThat(b.value()).isEqualTo(100);
    }
}
