package com.javaprep.day07.task02;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class PassByValueLabTest {

    @Test
    @DisplayName("reassigning the parameter does not change the caller's variable or arrays")
    void reassignDoesNotAffectCaller() {
        int[] holder = {1, 2};
        int[] other = {9};
        int[] holderBefore = holder;
        PassByValueLab.reassign(holder, other);
        assertThat(holder).isSameAs(holderBefore).containsExactly(1, 2);
        assertThat(other).containsExactly(9);
    }

    @Test
    @DisplayName("mutating through the reference is visible to the caller")
    void mutateFirstVisible() {
        int[] arr = {1, 2, 3};
        PassByValueLab.mutateFirst(arr, 42);
        assertThat(arr).containsExactly(42, 2, 3);
    }

    @Test
    @DisplayName("empty array is a no-op; null -> NullPointerException")
    void edges() {
        int[] empty = {};
        PassByValueLab.mutateFirst(empty, 1);
        assertThat(empty).isEmpty();
        assertThatThrownBy(() -> PassByValueLab.mutateFirst(null, 1)).isInstanceOf(NullPointerException.class);
    }
}
