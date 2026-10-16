package com.javaprep.day37.task03;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

public class PasswordService {

    private final PasswordEncoder encoder;

    /** @param strength BCrypt cost factor (log rounds). */
    public PasswordService(int strength) {
        // TODO(Day37-task03): create a BCryptPasswordEncoder with the given strength
        throw new UnsupportedOperationException("TODO(Day37-task03): create a BCryptPasswordEncoder with the given strength");
    }

    /** Raw password must be non-null and at least 8 characters, else IllegalArgumentException("password too short"). */
    public String hash(String rawPassword) {
        // TODO(Day37-task03): validate then encode
        throw new UnsupportedOperationException("TODO(Day37-task03): validate then encode");
    }

    /** False for null arguments; true only when the raw password matches the stored hash. */
    public boolean matches(String rawPassword, String storedHash) {
        // TODO(Day37-task03): null-safe matches
        throw new UnsupportedOperationException("TODO(Day37-task03): null-safe matches");
    }

    /** True when the stored hash was produced with a weaker cost than this service uses and should be re-hashed on next login. */
    public boolean needsUpgrade(String storedHash) {
        // TODO(Day37-task03): ask the encoder
        throw new UnsupportedOperationException("TODO(Day37-task03): ask the encoder");
    }
}
