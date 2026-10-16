package com.javaprep.day47.task02;

import java.time.Clock;
import java.time.Duration;
import java.util.List;

/**
 * Minimal HS256 JWT implementation for learning purposes (production code should use a vetted library such as
 * Nimbus JOSE or jjwt). Format: base64url(header) . base64url(payload) . base64url(HMAC-SHA256(header.payload)).
 * Header JSON: {"alg":"HS256","typ":"JWT"}. Payload JSON: {"sub":..., "roles":[...], "iat":epochSec, "exp":epochSec}.
 */
public class TokenService {

    private final String secret;
    private final Clock clock;

    /** Secret shorter than 32 characters -> IllegalArgumentException. */
    public TokenService(String secret, Clock clock) {
        // TODO(Day47-task02): validate the secret length and keep the fields
        this.secret = secret;
        this.clock = clock;
    }

    /** ttl must be positive (else IllegalArgumentException). exp = now + ttl. */
    public String issue(String subject, List<String> roles, Duration ttl) {
        // TODO(Day47-task02): build header + payload JSON (Jackson ObjectMapper), base64url without padding, sign with HmacSHA256
        throw new UnsupportedOperationException("TODO(Day47-task02): implement issue");
    }

    /**
     * Returns the claims of a valid token. Throws InvalidTokenException for: wrong number of parts, signature mismatch
     * (compare in constant time), header alg other than HS256 (reject "none"!), unreadable JSON, or exp <= now.
     */
    public TokenClaims verify(String token) {
        // TODO(Day47-task02): split, check header, recompute and compare the signature, then parse payload and check expiry
        throw new UnsupportedOperationException("TODO(Day47-task02): implement verify");
    }
}
