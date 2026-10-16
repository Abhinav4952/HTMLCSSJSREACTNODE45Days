package com.javaprep.day03.task04;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class CompoundAssignTest {

    @Test
    @DisplayName("in-range results are unchanged")
    void inRange() {
        assertThat(CompoundAssign.addToByte((byte) 10, 5)).isEqualTo((byte) 15);
        assertThat(CompoundAssign.addToByte((byte) -10, -5)).isEqualTo((byte) -15);
    }

    @Test
    @DisplayName("results wrap around like a narrowing cast")
    void wraps() {
        assertThat(CompoundAssign.addToByte((byte) 127, 1)).isEqualTo((byte) -128);
        assertThat(CompoundAssign.addToByte((byte) -128, -1)).isEqualTo((byte) 127);
        assertThat(CompoundAssign.addToByte((byte) 0, 300)).isEqualTo((byte) 44);
    }
}
