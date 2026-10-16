package com.javaprep.day16.task02;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.UnaryOperator;
import org.junit.jupiter.api.Test;

class PredicateComposeTest {

    private final Predicate<Integer> positive = n -> n > 0;
    private final Predicate<Integer> even = n -> n % 2 == 0;

    @Test
    void r1_allOf() {
        Predicate<Integer> p = PredicateCompose.allOf(List.of(positive, even));
        assertThat(p.test(4)).isTrue();
        assertThat(p.test(3)).isFalse();
        assertThat(p.test(-2)).isFalse();
        assertThat(PredicateCompose.allOf(List.<Predicate<Integer>>of()).test(1)).isTrue();
    }

    @Test
    void r2_anyOf() {
        Predicate<Integer> p = PredicateCompose.anyOf(List.of(positive, even));
        assertThat(p.test(3)).isTrue();
        assertThat(p.test(-2)).isTrue();
        assertThat(p.test(-3)).isFalse();
        assertThat(PredicateCompose.anyOf(List.<Predicate<Integer>>of()).test(1)).isFalse();
    }

    @Test
    void r3_noneOf() {
        Predicate<Integer> p = PredicateCompose.noneOf(List.of(positive, even));
        assertThat(p.test(-3)).isTrue();
        assertThat(p.test(-2)).isFalse();
        assertThat(p.test(5)).isFalse();
        assertThat(PredicateCompose.noneOf(List.<Predicate<Integer>>of()).test(1)).isTrue();
    }

    @Test
    void r4_nullSafe() {
        Predicate<String> nonEmpty = s -> !s.isEmpty();
        Predicate<String> safe = PredicateCompose.nullSafe(nonEmpty);
        assertThat(safe.test(null)).isFalse();
        assertThat(safe.test("")).isFalse();
        assertThat(safe.test("x")).isTrue();
    }

    @Test
    void r5_validUsernameAccepts() {
        Predicate<String> v = PredicateCompose.validUsername();
        assertThat(v.test("abc")).isTrue();
        assertThat(v.test("Ada_99")).isTrue();
        assertThat(v.test("abcdefghijkl")).isTrue();
    }

    @Test
    void r5_validUsernameRejects() {
        Predicate<String> v = PredicateCompose.validUsername();
        assertThat(v.test(null)).isFalse();
        assertThat(v.test("ab")).isFalse();
        assertThat(v.test("abcdefghijklm")).isFalse();
        assertThat(v.test("9lives")).isFalse();
        assertThat(v.test("_hidden")).isFalse();
        assertThat(v.test("bad name")).isFalse();
        assertThat(v.test("bad-name")).isFalse();
        assertThat(v.test("")).isFalse();
    }

    @Test
    void r6_pipelineAppliesLeftToRight() {
        UnaryOperator<String> trim = String::trim;
        UnaryOperator<String> upper = String::toUpperCase;
        UnaryOperator<String> exclaim = s -> s + "!";
        Function<String, String> f = PredicateCompose.pipeline(List.of(trim, upper, exclaim));
        assertThat(f.apply("  hi ")).isEqualTo("HI!");
        UnaryOperator<Integer> plus1 = n -> n + 1;
        UnaryOperator<Integer> times2 = n -> n * 2;
        assertThat(PredicateCompose.pipeline(List.of(plus1, times2)).apply(5)).isEqualTo(12);
        assertThat(PredicateCompose.pipeline(List.of(times2, plus1)).apply(5)).isEqualTo(11);
    }

    @Test
    void r6_emptyPipelineIsIdentity() {
        assertThat(PredicateCompose.pipeline(List.<UnaryOperator<String>>of()).apply("same")).isEqualTo("same");
    }
}
