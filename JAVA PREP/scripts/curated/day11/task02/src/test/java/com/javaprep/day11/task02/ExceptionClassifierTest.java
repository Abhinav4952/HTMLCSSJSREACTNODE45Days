package com.javaprep.day11.task02;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ExceptionClassifierTest {

    @Test
    @DisplayName("NullPointerException -> NPE")
    void npe() {
        assertThat(ExceptionClassifier.classify(new NullPointerException())).isEqualTo("NPE");
    }

    @Test
    @DisplayName("IllegalArgumentException and subclasses -> IAE")
    void iae() {
        assertThat(ExceptionClassifier.classify(new IllegalArgumentException("x"))).isEqualTo("IAE");
        assertThat(ExceptionClassifier.classify(new NumberFormatException("x"))).isEqualTo("IAE");
    }

    @Test
    @DisplayName("other runtime exceptions -> RUNTIME")
    void runtime() {
        assertThat(ExceptionClassifier.classify(new IllegalStateException())).isEqualTo("RUNTIME");
        assertThat(ExceptionClassifier.classify(new ArithmeticException())).isEqualTo("RUNTIME");
    }

    @Test
    @DisplayName("checked exceptions -> CHECKED")
    void checked() {
        assertThat(ExceptionClassifier.classify(new java.io.IOException("io"))).isEqualTo("CHECKED");
        assertThat(ExceptionClassifier.classify(new Exception("plain"))).isEqualTo("CHECKED");
    }

    @Test
    @DisplayName("null -> NullPointerException")
    void nullInput() {
        assertThatThrownBy(() -> ExceptionClassifier.classify(null)).isInstanceOf(NullPointerException.class);
    }
}
