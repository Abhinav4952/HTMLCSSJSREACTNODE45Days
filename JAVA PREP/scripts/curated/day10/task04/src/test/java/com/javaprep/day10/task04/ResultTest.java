package com.javaprep.day10.task04;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ResultTest {

    @Test
    @DisplayName("ok() builds a Success carrying the value")
    void ok() {
        Result r = Result.ok("done");
        assertThat(r).isInstanceOf(Result.Success.class);
        assertThat(((Result.Success) r).value()).isEqualTo("done");
    }

    @Test
    @DisplayName("fail() builds a Failure carrying the error")
    void fail() {
        Result r = Result.fail("boom");
        assertThat(r).isInstanceOf(Result.Failure.class);
        assertThat(((Result.Failure) r).error()).isEqualTo("boom");
    }

    @Test
    @DisplayName("exhaustive switch over the sealed hierarchy")
    void exhaustiveSwitch() {
        assertThat(render(Result.ok("x"))).isEqualTo("ok:x");
        assertThat(render(Result.fail("e"))).isEqualTo("fail:e");
    }

    @Test
    @DisplayName("invalid arguments -> IllegalArgumentException")
    void invalid() {
        assertThatThrownBy(() -> Result.ok(null)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> Result.fail(null)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> Result.fail("  ")).isInstanceOf(IllegalArgumentException.class);
    }

    private static String render(Result r) {
        return switch (r) {
            case Result.Success s -> "ok:" + s.value();
            case Result.Failure f -> "fail:" + f.error();
        };
    }
}
