package com.javaprep.day47.task01;

/** PROVIDED. Never contains the password or its hash. */
public record UserResponse(Long id, String email, String displayName) {
}
