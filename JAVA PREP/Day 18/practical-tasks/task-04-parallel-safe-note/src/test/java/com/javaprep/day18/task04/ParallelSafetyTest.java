package com.javaprep.day18.task04;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Locale;
import org.junit.jupiter.api.Test;

class ParallelSafetyTest {

    @Test
    void r1_sumOfSquaresDoesNotOverflow() {
        assertThat(ParallelSafety.sumOfSquares(List.of(1, 2, 3))).isEqualTo(14L);
        assertThat(ParallelSafety.sumOfSquares(List.of(46_341))).isEqualTo(2_147_488_281L);
        assertThat(ParallelSafety.sumOfSquares(List.of())).isZero();
        assertThat(ParallelSafety.sumOfSquares(List.of(-3, 3))).isEqualTo(18L);
    }

    @Test
    void r2_squaresInOrder() {
        assertThat(ParallelSafety.squaresInOrder(List.of(3, -1, 2))).containsExactly(9, 1, 4);
        assertThat(ParallelSafety.squaresInOrder(List.of())).isEmpty();
    }

    @Test
    void r3_decisionHelper() {
        assertThat(ParallelSafety.isSafeToParallelize(true, true, true, 10_000, false)).isTrue();
        assertThat(ParallelSafety.isSafeToParallelize(true, true, true, 9_999, false)).isFalse();
        assertThat(ParallelSafety.isSafeToParallelize(false, true, true, 1_000_000, false)).isFalse();
        assertThat(ParallelSafety.isSafeToParallelize(true, false, true, 1_000_000, false)).isFalse();
        assertThat(ParallelSafety.isSafeToParallelize(true, true, false, 1_000_000, false)).isFalse();
        assertThat(ParallelSafety.isSafeToParallelize(true, true, true, 1_000_000, true)).isFalse();
    }

    @Test
    void r4_cautionsAreSubstantive() {
        List<String> cautions = ParallelSafety.parallelCautions();
        assertThat(cautions).hasSizeGreaterThanOrEqualTo(5);
        assertThat(cautions).allSatisfy(c -> assertThat(c.length()).isGreaterThan(40));
        assertThat(cautions).doesNotHaveDuplicates();
    }

    @Test
    void r4_cautionsCoverTheKeyIdeas() {
        String all = String.join(" ", ParallelSafety.parallelCautions()).toLowerCase(Locale.ROOT);
        assertThat(all).contains("associative", "stateless", "side effect", "common pool", "blocking", "measure");
    }
}
