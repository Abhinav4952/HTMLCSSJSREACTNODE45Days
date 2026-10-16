package com.javaprep.day47.task01;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class RegistrationService {

    private final UserRepository users;
    private final PasswordEncoder encoder;

    public RegistrationService(UserRepository users, PasswordEncoder encoder) {
        this.users = users;
        this.encoder = encoder;
    }

    /**
     * Rules: email is trimmed + lower-cased and must contain exactly one '@' with text on both sides, otherwise
     * IllegalArgumentException; password shorter than 8 chars -> IllegalArgumentException; blank displayName -> IAE;
     * an already registered email (any casing) -> DuplicateEmailException; the password is stored ONLY as a BCrypt hash.
     */
    @Transactional
    public UserResponse register(RegisterRequest request) {
        // TODO(Day47-task01): validate, normalise, check duplicates, encode the password, save, map to UserResponse
        throw new UnsupportedOperationException("TODO(Day47-task01): implement register");
    }
}
