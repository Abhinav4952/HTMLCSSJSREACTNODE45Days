package com.javaprep.day38.task01;

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
        // TODO(Day38-task01): validate the secret length and build the HMAC key with Keys.hmacShaKeyFor
        throw new UnsupportedOperationException("TODO(Day38-task01): validate the secret length and build the HMAC key with Keys.hmacShaKeyFor");
    }

    /** Token with subject = username, claim "roles" = list of role names (no ROLE_ prefix), issuedAt = now, expiration = now + ttl. */
    public String generate(String username, Collection<String> roles) {
        // TODO(Day38-task01): build and sign the token
        throw new UnsupportedOperationException("TODO(Day38-task01): build and sign the token");
    }

    private Claims claims(String token) {
        return Jwts.parser().verifyWith(key).clock(() -> Date.from(clock.instant())).build().parseSignedClaims(token).getPayload();
    }

    /** True only for a well-formed, correctly signed, unexpired token. Never throws (null/blank -> false). */
    public boolean isValid(String token) {
        // TODO(Day38-task01): parse and catch JwtException / IllegalArgumentException
        throw new UnsupportedOperationException("TODO(Day38-task01): parse and catch JwtException / IllegalArgumentException");
    }

    /** Subject of a VALID token; invalid tokens throw JwtException. */
    public String username(String token) {
        // TODO(Day38-task01): return the subject
        throw new UnsupportedOperationException("TODO(Day38-task01): return the subject");
    }

    /** Roles claim of a VALID token (empty list when absent); invalid tokens throw JwtException. */
    public List<String> roles(String token) {
        // TODO(Day38-task01): read the "roles" claim defensively
        throw new UnsupportedOperationException("TODO(Day38-task01): read the 'roles' claim defensively");
    }
}
