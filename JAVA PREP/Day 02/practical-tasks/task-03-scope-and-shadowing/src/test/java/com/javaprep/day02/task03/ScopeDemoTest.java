package com.javaprep.day02.task03;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ScopeDemoTest {

    @Test
    @DisplayName("compute(x) == x + 10")
    void addsTen() {
        assertThat(ScopeDemo.compute(5)).isEqualTo(15);
        assertThat(ScopeDemo.compute(0)).isEqualTo(10);
        assertThat(ScopeDemo.compute(-10)).isZero();
    }
}
