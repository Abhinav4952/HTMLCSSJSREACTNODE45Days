package com.javaprep.day04.task02;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class HttpStatusFamilyTest {

    @Test
    @DisplayName("each family at its lower and upper bound")
    void families() {
        assertThat(HttpStatusFamily.family(100)).isEqualTo("informational");
        assertThat(HttpStatusFamily.family(199)).isEqualTo("informational");
        assertThat(HttpStatusFamily.family(200)).isEqualTo("success");
        assertThat(HttpStatusFamily.family(204)).isEqualTo("success");
        assertThat(HttpStatusFamily.family(301)).isEqualTo("redirect");
        assertThat(HttpStatusFamily.family(404)).isEqualTo("client");
        assertThat(HttpStatusFamily.family(499)).isEqualTo("client");
        assertThat(HttpStatusFamily.family(500)).isEqualTo("server");
        assertThat(HttpStatusFamily.family(599)).isEqualTo("server");
    }

    @Test
    @DisplayName("codes outside 100..599 -> IllegalArgumentException")
    void invalid() {
        assertThatThrownBy(() -> HttpStatusFamily.family(99)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> HttpStatusFamily.family(600)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> HttpStatusFamily.family(-200)).isInstanceOf(IllegalArgumentException.class);
    }
}
