package com.javaprep.day15.task03;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.Test;

class PriorityQueueLabTest {

    @Test
    void r1_processOrderByPriorityThenId() {
        List<Job> jobs = List.of(new Job("c", 1), new Job("b", 5), new Job("a", 5), new Job("d", 3));
        assertThat(PriorityQueueLab.processOrder(jobs)).containsExactly("a", "b", "d", "c");
    }

    @Test
    void r1_processOrderEmptyAndSingle() {
        assertThat(PriorityQueueLab.processOrder(List.of())).isEmpty();
        assertThat(PriorityQueueLab.processOrder(List.of(new Job("only", 0)))).containsExactly("only");
    }

    @Test
    void r2_kSmallest() {
        List<Integer> values = List.of(9, 1, 8, 2, 7, 2);
        assertThat(PriorityQueueLab.kSmallest(values, 3)).containsExactly(1, 2, 2);
        assertThat(PriorityQueueLab.kSmallest(values, 1)).containsExactly(1);
    }

    @Test
    void r2_kSmallestBoundaries() {
        List<Integer> values = List.of(3, 1, 2);
        assertThat(PriorityQueueLab.kSmallest(values, 0)).isEmpty();
        assertThat(PriorityQueueLab.kSmallest(values, -1)).isEmpty();
        assertThat(PriorityQueueLab.kSmallest(values, 10)).containsExactly(1, 2, 3);
        assertThat(PriorityQueueLab.kSmallest(List.of(), 2)).isEmpty();
    }

    @Test
    void r3_balancedBrackets() {
        assertThat(PriorityQueueLab.isBalanced("{[()]}")).isTrue();
        assertThat(PriorityQueueLab.isBalanced("a(b)[c]{d}")).isTrue();
        assertThat(PriorityQueueLab.isBalanced("")).isTrue();
    }

    @Test
    void r3_unbalancedBrackets() {
        assertThat(PriorityQueueLab.isBalanced("(]")).isFalse();
        assertThat(PriorityQueueLab.isBalanced("]")).isFalse();
        assertThat(PriorityQueueLab.isBalanced("((")).isFalse();
        assertThat(PriorityQueueLab.isBalanced("([)]")).isFalse();
    }

    @Test
    void r4_rotateLeft() {
        assertThat(PriorityQueueLab.rotateLeft(List.of(1, 2, 3, 4, 5), 2)).containsExactly(3, 4, 5, 1, 2);
        assertThat(PriorityQueueLab.rotateLeft(List.of(1, 2, 3), 3)).containsExactly(1, 2, 3);
        assertThat(PriorityQueueLab.rotateLeft(List.of(1, 2, 3), 4)).containsExactly(2, 3, 1);
        assertThat(PriorityQueueLab.rotateLeft(List.of(1, 2, 3), -1)).containsExactly(3, 1, 2);
        assertThat(PriorityQueueLab.rotateLeft(List.<Integer>of(), 5)).isEmpty();
    }
}
