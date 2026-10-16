package com.javaprep.day16.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.function.IntUnaryOperator;
import java.util.function.Supplier;
import org.junit.jupiter.api.Test;

class LambdaFilterTest {

    @Test
    void r1_filter() {
        assertThat(LambdaFilter.filter(List.of(1, 2, 3, 4, 5, 6), n -> n % 2 == 0)).containsExactly(2, 4, 6);
        assertThat(LambdaFilter.filter(List.of("a", "bb", "ccc"), s -> s.length() > 5)).isEmpty();
        assertThat(LambdaFilter.filter(List.of("a", "b"), s -> true)).containsExactly("a", "b");
        assertThat(LambdaFilter.filter(List.<String>of(), s -> true)).isEmpty();
    }

    @Test
    void r1_filterAcceptsSupertypePredicate() {
        java.util.function.Predicate<Object> notNullObject = o -> o != null;
        assertThat(LambdaFilter.filter(List.of("x", "y"), notNullObject)).containsExactly("x", "y");
    }

    @Test
    void r2_mapAll() {
        assertThat(LambdaFilter.mapAll(List.of("a", "bb", "ccc"), String::length)).containsExactly(1, 2, 3);
        assertThat(LambdaFilter.mapAll(List.of(1, 2), n -> "#" + n)).containsExactly("#1", "#2");
        assertThat(LambdaFilter.mapAll(List.<Integer>of(), n -> n)).isEmpty();
    }

    @Test
    void r3_applyTwice() {
        assertThat(LambdaFilter.applyTwice(x -> x * 3, 2)).isEqualTo(18);
        assertThat(LambdaFilter.applyTwice(x -> x + 10, -5)).isEqualTo(15);
        assertThat(LambdaFilter.applyTwice(IntUnaryOperator.identity(), 7)).isEqualTo(7);
    }

    @Test
    void r4_countersAreIndependent() {
        Supplier<Integer> a = LambdaFilter.counter();
        Supplier<Integer> b = LambdaFilter.counter();
        assertThat(a.get()).isEqualTo(1);
        assertThat(a.get()).isEqualTo(2);
        assertThat(b.get()).isEqualTo(1);
        assertThat(a.get()).isEqualTo(3);
    }

    @Test
    void r5_addersCaptureTheRightValue() {
        List<IntUnaryOperator> ops = LambdaFilter.adders(4);
        assertThat(ops).hasSize(4);
        for (int i = 0; i < ops.size(); i++) {
            assertThat(ops.get(i).applyAsInt(100)).isEqualTo(100 + i);
        }
    }

    @Test
    void r5_addersEdgeCases() {
        assertThat(LambdaFilter.adders(0)).isEmpty();
        assertThatThrownBy(() -> LambdaFilter.adders(-1)).isInstanceOf(IllegalArgumentException.class);
    }
}
