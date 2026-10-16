package com.javaprep.day16.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import org.junit.jupiter.api.Test;

class OptionalChainTest {

    private static final User ANN = new User("Ann", new Address(" Pune ", "411001"));
    private static final User BOB = new User("Bob", null);
    private static final User CAL = new User("Cal", new Address("   ", null));

    @Test
    void r1_cityOf() {
        assertThat(OptionalChain.cityOf(ANN)).contains("Pune");
        assertThat(OptionalChain.cityOf(BOB)).isEmpty();
        assertThat(OptionalChain.cityOf(CAL)).isEmpty();
        assertThat(OptionalChain.cityOf(null)).isEmpty();
        assertThat(OptionalChain.cityOf(new User("D", new Address(null, "1")))).isEmpty();
    }

    @Test
    void r2_findByName() {
        List<User> users = List.of(ANN, BOB, CAL);
        assertThat(OptionalChain.findByName(users, "bob")).contains(BOB);
        assertThat(OptionalChain.findByName(users, "ANN")).contains(ANN);
        assertThat(OptionalChain.findByName(users, "zed")).isEmpty();
        assertThat(OptionalChain.findByName(users, null)).isEmpty();
        assertThat(OptionalChain.findByName(List.of(), "ann")).isEmpty();
    }

    @Test
    void r3_parsePositive() {
        assertThat(OptionalChain.parsePositive("42")).contains(42);
        assertThat(OptionalChain.parsePositive("  7 ")).contains(7);
    }

    @Test
    void r3_parsePositiveRejects() {
        assertThat(OptionalChain.parsePositive(null)).isEmpty();
        assertThat(OptionalChain.parsePositive("")).isEmpty();
        assertThat(OptionalChain.parsePositive("   ")).isEmpty();
        assertThat(OptionalChain.parsePositive("abc")).isEmpty();
        assertThat(OptionalChain.parsePositive("0")).isEmpty();
        assertThat(OptionalChain.parsePositive("-5")).isEmpty();
        assertThat(OptionalChain.parsePositive("99999999999")).isEmpty();
        assertThat(OptionalChain.parsePositive("4.5")).isEmpty();
    }

    @Test
    void r4_zipOrDefault() {
        assertThat(OptionalChain.zipOrDefault(ANN, "000000")).isEqualTo("411001");
        assertThat(OptionalChain.zipOrDefault(BOB, "000000")).isEqualTo("000000");
        assertThat(OptionalChain.zipOrDefault(CAL, "000000")).isEqualTo("000000");
        assertThat(OptionalChain.zipOrDefault(null, "000000")).isEqualTo("000000");
    }

    @Test
    void r5_requireCity() {
        assertThat(OptionalChain.requireCity(ANN)).isEqualTo("Pune");
        assertThatThrownBy(() -> OptionalChain.requireCity(BOB))
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("Bob");
        assertThatThrownBy(() -> OptionalChain.requireCity(null))
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("unknown");
    }
}
