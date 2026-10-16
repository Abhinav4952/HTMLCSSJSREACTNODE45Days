package com.javaprep.day04.task03;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class LoopAggregatorsTest {

    @Test
    @DisplayName("sum adds values, empty is 0, and it does not overflow int")
    void sum() {
        assertThat(LoopAggregators.sum(new int[] {1, 2, 3, 4})).isEqualTo(10L);
        assertThat(LoopAggregators.sum(new int[0])).isZero();
        assertThat(LoopAggregators.sum(new int[] {Integer.MAX_VALUE, Integer.MAX_VALUE}))
                .isEqualTo(4_294_967_294L);
    }

    @Test
    @DisplayName("countPositives counts only values > 0")
    void countPositives() {
        assertThat(LoopAggregators.countPositives(new int[] {-1, 0, 1, 2, 3})).isEqualTo(3);
        assertThat(LoopAggregators.countPositives(new int[0])).isZero();
        assertThat(LoopAggregators.countPositives(new int[] {0, -5})).isZero();
    }

    @Test
    @DisplayName("null input -> NullPointerException")
    void nulls() {
        assertThatThrownBy(() -> LoopAggregators.sum(null)).isInstanceOf(NullPointerException.class);
        assertThatThrownBy(() -> LoopAggregators.countPositives(null)).isInstanceOf(NullPointerException.class);
    }
}
