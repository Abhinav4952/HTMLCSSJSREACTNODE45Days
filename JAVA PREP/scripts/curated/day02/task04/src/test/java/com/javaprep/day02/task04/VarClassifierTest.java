package com.javaprep.day02.task04;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class VarClassifierTest {

    @Test
    @DisplayName("var with an inferable initializer is VALID")
    void valid() {
        assertThat(VarClassifier.classify("var x = 5;")).isEqualTo("VALID");
        assertThat(VarClassifier.classify("var name = \"Ada\";")).isEqualTo("VALID");
        assertThat(VarClassifier.classify("var list = new java.util.ArrayList<String>();")).isEqualTo("VALID");
    }

    @Test
    @DisplayName("var without a usable initializer NEEDS_EXPLICIT")
    void needsExplicit() {
        assertThat(VarClassifier.classify("var x;")).isEqualTo("NEEDS_EXPLICIT");
        assertThat(VarClassifier.classify("var x = null;")).isEqualTo("NEEDS_EXPLICIT");
        assertThat(VarClassifier.classify("var a = {1, 2};")).isEqualTo("NEEDS_EXPLICIT");
        assertThat(VarClassifier.classify("var f = () -> 1;")).isEqualTo("NEEDS_EXPLICIT");
        assertThat(VarClassifier.classify("var m = String::length;")).isEqualTo("NEEDS_EXPLICIT");
    }

    @Test
    @DisplayName("malformed or non-var declarations are INVALID")
    void invalid() {
        assertThat(VarClassifier.classify(null)).isEqualTo("INVALID");
        assertThat(VarClassifier.classify("  ")).isEqualTo("INVALID");
        assertThat(VarClassifier.classify("int x = 5;")).isEqualTo("INVALID");
        assertThat(VarClassifier.classify("var = 5;")).isEqualTo("INVALID");
    }
}
