package com.javaprep.day20.task04;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.Test;

class LockOrderAnalyzerTest {

    @Test
    void r1_oppositeOrdersAreConflicting() {
        var pairs = LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "B"), List.of("B", "A")));
        assertThat(pairs).containsExactly("A<->B");
    }

    @Test
    void r1_sameOrderIsSafe() {
        assertThat(LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "B"), List.of("A", "B"), List.of("A", "B")))).isEmpty();
        assertThat(LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "B", "C"), List.of("A", "C")))).isEmpty();
    }

    @Test
    void r1_singleThreadIsNeverAConflict() {
        assertThat(LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "B", "A")))).isEmpty();
        assertThat(LockOrderAnalyzer.conflictingPairs(List.of())).isEmpty();
    }

    @Test
    void r1_nonAdjacentAndMultiplePairs() {
        var pairs = LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "C", "B"), List.of("B", "A"), List.of("C", "X")));
        assertThat(pairs).containsExactly("A<->B");
        var more = LockOrderAnalyzer.conflictingPairs(List.of(List.of("L1", "L2", "L3"), List.of("L3", "L2"), List.of("L2", "L1")));
        assertThat(more).containsExactly("L1<->L2", "L2<->L3");
    }

    @Test
    void r1_reentrantDuplicatesUseFirstPosition() {
        assertThat(LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "A", "B"), List.of("A", "B")))).isEmpty();
        assertThat(LockOrderAnalyzer.conflictingPairs(List.of(List.of("A", "A", "B"), List.of("B", "A")))).containsExactly("A<->B");
    }

    @Test
    void r2_hasOrderingRisk() {
        assertThat(LockOrderAnalyzer.hasOrderingRisk(List.of(List.of("lockX", "lockY"), List.of("lockY", "lockX")))).isTrue();
        assertThat(LockOrderAnalyzer.hasOrderingRisk(List.of(List.of("lockX", "lockY"), List.of("lockX")))).isFalse();
    }

    @Test
    void r3_coffmanConditions() {
        assertThat(LockOrderAnalyzer.coffmanConditions())
                .containsExactly("Mutual exclusion", "Hold and wait", "No preemption", "Circular wait");
    }

    @Test
    void r4_adviceWhenSafe() {
        assertThat(LockOrderAnalyzer.advice(List.of(List.of("A", "B"), List.of("A", "B"))))
                .isEqualTo("No lock-ordering conflicts found.");
    }

    @Test
    void r4_adviceWhenRisky() {
        String text = LockOrderAnalyzer.advice(List.of(List.of("accounts", "audit"), List.of("audit", "accounts"), List.of("zeta")));
        assertThat(text).contains("accounts<->audit").contains("global order");
        assertThat(text).contains("accounts, audit, zeta");
    }
}
