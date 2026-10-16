package com.javaprep.day08.task04;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class UserIdTest {

    @Test
    @DisplayName("constructor stores the stripped value")
    void stripsInConstructor() {
        assertThat(new UserId("  u-1 ").value()).isEqualTo("u-1");
    }

    @Test
    @DisplayName("constructor rejects null and blank")
    void rejectsInvalid() {
        assertThatThrownBy(() -> new UserId(null)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new UserId("   ")).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    @DisplayName("of() validates and strips like the constructor")
    void factory() {
        assertThat(UserId.of(" abc ")).isEqualTo(new UserId("abc"));
        assertThatThrownBy(() -> UserId.of(null)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> UserId.of("")).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    @DisplayName("record equality is value based on the stripped id")
    void equality() {
        assertThat(new UserId(" x ")).isEqualTo(new UserId("x")).hasSameHashCodeAs(new UserId("x"));
        assertThat(new UserId("x")).isNotEqualTo(new UserId("y"));
    }
}
