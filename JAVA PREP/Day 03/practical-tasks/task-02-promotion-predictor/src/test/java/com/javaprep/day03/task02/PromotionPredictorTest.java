package com.javaprep.day03.task02;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class PromotionPredictorTest {

    @Test
    @DisplayName("small integral types promote to int")
    void smallTypes() {
        assertThat(PromotionPredictor.resultType("byte", "byte")).isEqualTo("int");
        assertThat(PromotionPredictor.resultType("short", "char")).isEqualTo("int");
        assertThat(PromotionPredictor.resultType("int", "byte")).isEqualTo("int");
    }

    @Test
    @DisplayName("wider operand wins: long, float, double")
    void widerWins() {
        assertThat(PromotionPredictor.resultType("int", "long")).isEqualTo("long");
        assertThat(PromotionPredictor.resultType("long", "float")).isEqualTo("float");
        assertThat(PromotionPredictor.resultType("float", "double")).isEqualTo("double");
        assertThat(PromotionPredictor.resultType("double", "byte")).isEqualTo("double");
        assertThat(PromotionPredictor.resultType("long", "long")).isEqualTo("long");
    }

    @Test
    @DisplayName("unknown or null type names -> IllegalArgumentException")
    void invalid() {
        assertThatThrownBy(() -> PromotionPredictor.resultType("String", "int"))
                .isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> PromotionPredictor.resultType(null, "int"))
                .isInstanceOf(IllegalArgumentException.class);
    }
}
