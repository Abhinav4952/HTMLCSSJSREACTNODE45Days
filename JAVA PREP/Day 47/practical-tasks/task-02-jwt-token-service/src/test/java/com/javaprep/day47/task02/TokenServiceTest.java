package com.javaprep.day47.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.nio.charset.StandardCharsets;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.Base64;
import java.util.List;
import org.junit.jupiter.api.Test;

class TokenServiceTest {

    private static final String SECRET = "0123456789abcdef0123456789abcdef-secret";
    private static final Instant T0 = Instant.parse("2025-01-01T00:00:00Z");

    private TokenService at(Instant now) {
        return new TokenService(SECRET, Clock.fixed(now, ZoneOffset.UTC));
    }

    private static String b64(String s) {
        return Base64.getUrlEncoder().withoutPadding().encodeToString(s.getBytes(StandardCharsets.UTF_8));
    }

    @Test
    void issuedTokenVerifiesAndCarriesClaims() {
        String token = at(T0).issue("ana@example.com", List.of("USER", "ADMIN"), Duration.ofMinutes(15));
        TokenClaims claims = at(T0.plusSeconds(60)).verify(token);
        assertThat(claims.subject()).isEqualTo("ana@example.com");
        assertThat(claims.roles()).containsExactly("USER", "ADMIN");
        assertThat(claims.expiresAt()).isEqualTo(T0.plusSeconds(900));
    }

    @Test
    void tokenHasThreeBase64UrlPartsAndHs256Header() {
        String token = at(T0).issue("a", List.of(), Duration.ofMinutes(1));
        String[] parts = token.split("\\.");
        assertThat(parts).hasSize(3);
        assertThat(token).doesNotContain("=").doesNotContain("+").doesNotContain("/");
        assertThat(new String(Base64.getUrlDecoder().decode(parts[0]), StandardCharsets.UTF_8)).contains("HS256");
    }

    @Test
    void expiredTokenIsRejected() {
        String token = at(T0).issue("a", List.of(), Duration.ofMinutes(1));
        assertThatThrownBy(() -> at(T0.plusSeconds(61)).verify(token)).isInstanceOf(InvalidTokenException.class);
    }

    @Test
    void tamperedPayloadIsRejected() {
        String[] parts = at(T0).issue("a", List.of("USER"), Duration.ofMinutes(5)).split("\\.");
        String forged = b64("{\"sub\":\"a\",\"roles\":[\"ADMIN\"],\"iat\":1735689600,\"exp\":1735690000}");
        assertThatThrownBy(() -> at(T0).verify(parts[0] + "." + forged + "." + parts[2])).isInstanceOf(InvalidTokenException.class);
    }

    @Test
    void wrongSecretIsRejected() {
        String token = new TokenService("another-secret-another-secret-another", Clock.fixed(T0, ZoneOffset.UTC))
                .issue("a", List.of(), Duration.ofMinutes(5));
        assertThatThrownBy(() -> at(T0).verify(token)).isInstanceOf(InvalidTokenException.class);
    }

    @Test
    void algNoneTokenIsRejected() {
        String token = b64("{\"alg\":\"none\",\"typ\":\"JWT\"}") + "." + b64("{\"sub\":\"a\",\"roles\":[],\"exp\":9999999999}") + ".";
        assertThatThrownBy(() -> at(T0).verify(token)).isInstanceOf(InvalidTokenException.class);
    }

    @Test
    void garbageIsRejected() {
        assertThatThrownBy(() -> at(T0).verify("not-a-jwt")).isInstanceOf(InvalidTokenException.class);
        assertThatThrownBy(() -> at(T0).verify("a.b.c")).isInstanceOf(InvalidTokenException.class);
    }

    @Test
    void invalidArgumentsAreRejected() {
        assertThatThrownBy(() -> new TokenService("short", Clock.systemUTC())).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> at(T0).issue("a", List.of(), Duration.ZERO)).isInstanceOf(IllegalArgumentException.class);
    }
}
