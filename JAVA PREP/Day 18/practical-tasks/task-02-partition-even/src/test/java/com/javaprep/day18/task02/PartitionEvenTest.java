package com.javaprep.day18.task02;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class PartitionEvenTest {

    @Test
    void r1_partitionEven() {
        var parts = PartitionEven.partitionEven(List.of(1, 2, 3, 4, 5, -3, -4));
        assertThat(parts.get(true)).containsExactly(2, 4, -4);
        assertThat(parts.get(false)).containsExactly(1, 3, 5, -3);
    }

    @Test
    @DisplayName("Both keys exist even when one bucket (or the input) is empty")
    void r5_bothKeysAlwaysPresent() {
        var allOdd = PartitionEven.partitionEven(List.of(1, 3));
        assertThat(allOdd).containsOnlyKeys(true, false);
        assertThat(allOdd.get(true)).isEmpty();
        var none = PartitionEven.partitionEven(List.of());
        assertThat(none).containsOnlyKeys(true, false);
        assertThat(none.get(false)).isEmpty();
    }

    @Test
    void r2_genericPartition() {
        var parts = PartitionEven.partition(List.of("a", "bb", "ccc", "dd"), s -> s.length() >= 2);
        assertThat(parts.get(true)).containsExactly("bb", "ccc", "dd");
        assertThat(parts.get(false)).containsExactly("a");
        Object marker = new Object();
        java.util.function.Predicate<Object> anything = o -> o == marker;
        assertThat(PartitionEven.partition(List.of("x"), anything).get(false)).containsExactly("x");
    }

    @Test
    void r3_countPassFail() {
        var result = PartitionEven.countPassFail(List.of(40, 50, 75, 49, 100), 50);
        assertThat(result.get(true)).isEqualTo(3L);
        assertThat(result.get(false)).isEqualTo(2L);
    }

    @Test
    void r3_countPassFailEmptyHasZeroes() {
        var result = PartitionEven.countPassFail(List.of(), 50);
        assertThat(result).containsOnlyKeys(true, false);
        assertThat(result.get(true)).isZero();
        assertThat(result.get(false)).isZero();
    }

    @Test
    void r4_sumEvenOdd() {
        var sums = PartitionEven.sumEvenOdd(List.of(1, 2, 3, 4, 5));
        assertThat(sums.get(true)).isEqualTo(6);
        assertThat(sums.get(false)).isEqualTo(9);
        var empty = PartitionEven.sumEvenOdd(List.of());
        assertThat(empty.get(true)).isZero();
        assertThat(empty.get(false)).isZero();
    }
}
