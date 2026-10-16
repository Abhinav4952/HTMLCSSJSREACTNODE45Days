package com.javaprep.day01.task03;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.Map;

class ClassLookupTest {

    private final Map<String, String> index =
            Map.of("List", "java.util.List", "String", "java.lang.String");

    @Test
    @DisplayName("returns the FQCN when present")
    void found() {
        assertThat(ClassLookup.resolve("List", index)).isEqualTo("java.util.List");
        assertThat(ClassLookup.resolve("String", index)).isEqualTo("java.lang.String");
    }

    @Test
    @DisplayName("unknown simple name -> IllegalArgumentException mentioning the name")
    void missing() {
        assertThatThrownBy(() -> ClassLookup.resolve("Nope", index))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("Nope");
    }

    @Test
    @DisplayName("null or blank simple name -> IllegalArgumentException")
    void badName() {
        assertThatThrownBy(() -> ClassLookup.resolve(null, index)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> ClassLookup.resolve("  ", index)).isInstanceOf(IllegalArgumentException.class);
    }
}
