package com.javaprep.day11.task03;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class CountingResourceTest {

    @Test
    @DisplayName("starts at zero")
    void startsAtZero() {
        assertThat(new CountingResource().getCloseCount()).isZero();
    }

    @Test
    @DisplayName("try-with-resources closes exactly once")
    void closedOnce() {
        CountingResource r = new CountingResource();
        try (r) {
            assertThat(r.getCloseCount()).isZero();
        }
        assertThat(r.getCloseCount()).isEqualTo(1);
    }

    @Test
    @DisplayName("closes even when the body throws")
    void closedOnException() {
        CountingResource r = new CountingResource();
        assertThatThrownBy(() -> {
            try (r) {
                throw new IllegalStateException("boom");
            }
        }).isInstanceOf(IllegalStateException.class);
        assertThat(r.getCloseCount()).isEqualTo(1);
    }

    @Test
    @DisplayName("explicit repeated close() calls are counted")
    void repeatedClose() {
        CountingResource r = new CountingResource();
        r.close();
        r.close();
        assertThat(r.getCloseCount()).isEqualTo(2);
    }

    @Test
    @DisplayName("multiple resources close in reverse order, each once")
    void multiple() {
        CountingResource a = new CountingResource();
        CountingResource b = new CountingResource();
        try (a; b) {
            // use
        }
        assertThat(a.getCloseCount()).isEqualTo(1);
        assertThat(b.getCloseCount()).isEqualTo(1);
    }
}
