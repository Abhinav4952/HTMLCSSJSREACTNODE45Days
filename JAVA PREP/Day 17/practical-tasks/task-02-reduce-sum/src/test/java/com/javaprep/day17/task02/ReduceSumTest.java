package com.javaprep.day17.task02;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Arrays;
import java.util.IntSummaryStatistics;
import java.util.List;
import org.junit.jupiter.api.Test;

class ReduceSumTest {

    @Test
    void r1_sum() {
        assertThat(ReduceSum.sum(List.of(3, 1, 4, 1, 5))).isEqualTo(14);
        assertThat(ReduceSum.sum(List.of(-5, 5))).isZero();
        assertThat(ReduceSum.sum(List.of())).isZero();
    }

    @Test
    void r2_product() {
        assertThat(ReduceSum.product(List.of(3, 1, 4, 1, 5))).isEqualTo(60L);
        assertThat(ReduceSum.product(List.of())).isEqualTo(1L);
        assertThat(ReduceSum.product(List.of(100_000, 100_000))).isEqualTo(10_000_000_000L);
        assertThat(ReduceSum.product(List.of(7, 0, 9))).isZero();
    }

    @Test
    void r3_max() {
        assertThat(ReduceSum.max(List.of(3, 9, -1))).contains(9);
        assertThat(ReduceSum.max(List.of(-8, -3))).contains(-3);
        assertThat(ReduceSum.max(List.of())).isEmpty();
    }

    @Test
    void r4_average() {
        assertThat(ReduceSum.average(List.of(1, 2, 3, 4)).getAsDouble()).isEqualTo(2.5);
        assertThat(ReduceSum.average(List.of())).isEmpty();
    }

    @Test
    void r5_longestKeepsFirstOnTies() {
        assertThat(ReduceSum.longest(List.of("kiwi", "pear", "banana", "melon", "cherry"))).contains("banana");
        assertThat(ReduceSum.longest(Arrays.asList(null, "a", null, "b"))).contains("a");
        assertThat(ReduceSum.longest(List.of())).isEmpty();
        assertThat(ReduceSum.longest(Arrays.asList((String) null))).isEmpty();
    }

    @Test
    void r6_stats() {
        IntSummaryStatistics s = ReduceSum.stats(List.of(3, 1, 4, 1, 5));
        assertThat(s.getCount()).isEqualTo(5);
        assertThat(s.getSum()).isEqualTo(14);
        assertThat(s.getMin()).isEqualTo(1);
        assertThat(s.getMax()).isEqualTo(5);
        assertThat(ReduceSum.stats(List.of()).getCount()).isZero();
    }

    @Test
    void r7_sumLongDoesNotOverflow() {
        assertThat(ReduceSum.sumLong(List.of(Integer.MAX_VALUE, Integer.MAX_VALUE))).isEqualTo(4_294_967_294L);
        assertThat(ReduceSum.sumLong(List.of())).isZero();
    }
}
