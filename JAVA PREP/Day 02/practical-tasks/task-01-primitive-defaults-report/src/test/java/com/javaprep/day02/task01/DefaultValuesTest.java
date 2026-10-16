package com.javaprep.day02.task01;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class DefaultValuesTest {

    @Test
    @DisplayName("int field defaults to 0")
    void intDefault() {
        assertThat(new DefaultValues().getIntDefault()).isZero();
    }

    @Test
    @DisplayName("boolean field defaults to false")
    void booleanDefault() {
        assertThat(new DefaultValues().getBooleanDefault()).isFalse();
    }

    @Test
    @DisplayName("reference field defaults to null")
    void referenceDefault() {
        assertThat(new DefaultValues().getReferenceDefault()).isNull();
    }
}
