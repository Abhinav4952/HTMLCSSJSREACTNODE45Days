package com.javaprep.day47.task02;

import java.time.Instant;
import java.util.List;

/** PROVIDED. Verified token contents. */
public record TokenClaims(String subject, List<String> roles, Instant expiresAt) {
}
