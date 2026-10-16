package com.javaprep.day07.task04;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Modifier;

class PasswordMaskerTest {

    @Test
    @DisplayName("masks every character")
    void masks() {
        assertThat(PasswordMasker.mask("secret")).isEqualTo("******");
        assertThat(PasswordMasker.mask("a")).isEqualTo("*");
        assertThat(PasswordMasker.mask("p@ss w0rd")).isEqualTo("*********");
    }

    @Test
    @DisplayName("null or blank -> IllegalArgumentException")
    void invalid() {
        assertThatThrownBy(() -> PasswordMasker.mask(null)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> PasswordMasker.mask("")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> PasswordMasker.mask("   ")).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    @DisplayName("validation lives in a private helper (access boundary)")
    void hasPrivateHelper() {
        long privateMethods = java.util.Arrays.stream(PasswordMasker.class.getDeclaredMethods())
                .filter(m -> Modifier.isPrivate(m.getModifiers()))
                .count();
        assertThat(privateMethods).isGreaterThanOrEqualTo(1);
    }
}
