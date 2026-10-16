package com.javaprep.day09.task04;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class AccountTest {

    @Test
    @DisplayName("toString uses the documented format")
    void format() {
        assertThat(new Account("A-1", 1250).toString()).isEqualTo("Account[id=A-1, balanceCents=1250]");
        assertThat(new Account("B", 0).toString()).isEqualTo("Account[id=B, balanceCents=0]");
    }

    @Test
    @DisplayName("string concatenation and String.valueOf use toString")
    void implicitUse() {
        Account acc = new Account("A-1", -5);
        assertThat("" + acc).isEqualTo("Account[id=A-1, balanceCents=-5]");
        assertThat(String.valueOf(acc)).isEqualTo(acc.toString());
    }
}
