package com.javaprep.day38.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import io.jsonwebtoken.JwtException;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.List;
import org.junit.jupiter.api.Test;

class JwtUtilTest {

    static final String SECRET = "0123456789-0123456789-0123456789-ab";
    static final Clock T0 = Clock.fixed(Instant.parse("2025-01-01T00:00:00Z"), ZoneOffset.UTC);

    private JwtUtil util(Clock clock) {
        return new JwtUtil(SECRET, Duration.ofMinutes(30), clock);
    }

    @Test
    void roundTrip() {
        JwtUtil u = util(T0);
        String token = u.generate("ann", List.of("USER", "ADMIN"));
        assertThat(token.split("\\.")).hasSize(3);
        assertThat(u.isValid(token)).isTrue();
        assertThat(u.username(token)).isEqualTo("ann");
        assertThat(u.roles(token)).containsExactly("USER", "ADMIN");
    }

    @Test
    void expiresAfterTtl() {
        String token = util(T0).generate("ann", List.of("USER"));
        assertThat(util(Clock.offset(T0, Duration.ofMinutes(29))).isValid(token)).isTrue();
        assertThat(util(Clock.offset(T0, Duration.ofMinutes(31))).isValid(token)).isFalse();
    }

    @Test
    void tamperedPayloadIsRejected() {
        JwtUtil u = util(T0);
        String[] parts = u.generate("ann", List.of("USER")).split("\\.");
        String forged = java.util.Base64.getUrlEncoder().withoutPadding().encodeToString("{\"sub\":\"root\",\"roles\":[\"ADMIN\"]}".getBytes());
        assertThat(u.isValid(parts[0] + "." + forged + "." + parts[2])).isFalse();
    }

    @Test
    void differentSecretIsRejected() {
        String token = util(T0).generate("ann", List.of("USER"));
        JwtUtil other = new JwtUtil("zzzzzzzzzz-zzzzzzzzzz-zzzzzzzzzz-zz", Duration.ofMinutes(30), T0);
        assertThat(other.isValid(token)).isFalse();
    }

    @Test
    void garbageIsInvalidNotAnException() {
        JwtUtil u = util(T0);
        assertThat(u.isValid(null)).isFalse();
        assertThat(u.isValid("")).isFalse();
        assertThat(u.isValid("not.a.jwt")).isFalse();
        assertThatThrownBy(() -> u.username("not.a.jwt")).isInstanceOf(JwtException.class);
    }

    @Test
    void shortSecretIsRejected() {
        assertThatThrownBy(() -> new JwtUtil("too-short", Duration.ofMinutes(1))).isInstanceOf(IllegalArgumentException.class);
    }
}
