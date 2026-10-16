package com.javaprep.day10.task03;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class DescribeTest {

    @Test
    @DisplayName("String and Integer")
    void stringAndInteger() {
        assertThat(Describe.describe("hi")).isEqualTo("String:hi");
        assertThat(Describe.describe(42)).isEqualTo("Integer:42");
        assertThat(Describe.describe("")).isEqualTo("String:");
    }

    @Test
    @DisplayName("null")
    void nullValue() {
        assertThat(Describe.describe(null)).isEqualTo("null");
    }

    @Test
    @DisplayName("other types use the simple class name")
    void other() {
        assertThat(Describe.describe(3.5)).isEqualTo("Other:Double");
        assertThat(Describe.describe(new java.util.ArrayList<String>())).isEqualTo("Other:ArrayList");
    }
}
