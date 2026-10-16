package com.javaprep.day38.task03;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import java.nio.charset.StandardCharsets;
import java.time.Clock;
import java.time.Duration;
import java.util.Collection;
import java.util.Date;
import java.util.List;
import javax.crypto.SecretKey;

/** Issues and verifies HS256 JWTs. */
public class JwtUtil {

    private final SecretKey key;
    private final Duration ttl;
    private final Clock clock;

    public JwtUtil(String secret, Duration ttl) {
        this(secret, ttl, Clock.systemUTC());
    }

    /** secret must be at least 32 bytes (UTF-8) for HS256, otherwise IllegalArgumentException. */
    public JwtUtil(String secret, Duration ttl, Clock clock) {
        if (secret == null || secret.getBytes(StandardCharsets.UTF_8).length < 32) {
            throw new IllegalArgumentException("secret must be at least 32 bytes");
        }
        this.key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        this.ttl = ttl;
        this.clock = clock;
    }

    /** Token with subject = username, claim "roles" = list of role names (no ROLE_ prefix), issuedAt = now, expiration = now + ttl. */
    public String generate(String username, Collection<String> roles) {
        Date now = Date.from(clock.instant());
        return Jwts.builder().subject(username).claim("roles", List.copyOf(roles)).issuedAt(now)
                .expiration(Date.from(clock.instant().plus(ttl))).signWith(key).compact();
    }

    private Claims claims(String token) {
        return Jwts.parser().verifyWith(key).clock(() -> Date.from(clock.instant())).build().parseSignedClaims(token).getPayload();
    }

    /** True only for a well-formed, correctly signed, unexpired token. Never throws (null/blank -> false). */
    public boolean isValid(String token) {
        if (token == null || token.isBlank()) {
            return false;
        }
        try {
            claims(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }

    /** Subject of a VALID token; invalid tokens throw JwtException. */
    public String username(String token) {
        return claims(token).getSubject();
    }

    /** Roles claim of a VALID token (empty list when absent); invalid tokens throw JwtException. */
    public List<String> roles(String token) {
        Object raw = claims(token).get("roles");
        if (!(raw instanceof List<?> l)) {
            return List.of();
        }
        return l.stream().map(String::valueOf).toList();
    }
}
