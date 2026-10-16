package com.javaprep.day11.task04;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ValidationExceptionTest {

    @Test
    @DisplayName("carries field and message")
    void carries() {
        ValidationException ex = new ValidationException("email", "bad email");
        assertThat(ex.getField()).isEqualTo("email");
        assertThat(ex.getMessage()).isEqualTo("bad email");
        assertThat(ex).isInstanceOf(RuntimeException.class);
    }

    @Test
    @DisplayName("requireEmail accepts a plausible address")
    void accepts() {
        assertThatCode(() -> ValidationException.requireEmail("ada@example.com")).doesNotThrowAnyException();
    }

    @Test
    @DisplayName("requireEmail rejects null, blank and missing '@' with field=email")
    void rejects() {
        for (String bad : new String[] {null, "", "   ", "no-at-sign"}) {
            assertThatThrownBy(() -> ValidationException.requireEmail(bad))
                    .isInstanceOf(ValidationException.class)
                    .isInstanceOfSatisfying(ValidationException.class, ex -> assertThat(ex.getField()).isEqualTo("email"));
        }
    }
}
