package com.javaprep.day47.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;

@SpringBootTest
class RegistrationServiceTest {

    @Autowired
    private RegistrationService service;
    @Autowired
    private UserRepository users;
    @Autowired
    private PasswordEncoder encoder;

    @BeforeEach
    void clean() {
        users.deleteAll();
    }

    @Test
    void registersAndNormalisesEmail() {
        UserResponse r = service.register(new RegisterRequest("  Ana@Example.COM ", "s3cretpass", "Ana"));
        assertThat(r.id()).isNotNull();
        assertThat(r.email()).isEqualTo("ana@example.com");
        assertThat(r.displayName()).isEqualTo("Ana");
    }

    @Test
    void passwordIsStoredAsBcryptHash() {
        service.register(new RegisterRequest("ana@example.com", "s3cretpass", "Ana"));
        User stored = users.findByEmail("ana@example.com").orElseThrow();
        assertThat(stored.getPasswordHash()).isNotEqualTo("s3cretpass").startsWith("$2");
        assertThat(encoder.matches("s3cretpass", stored.getPasswordHash())).isTrue();
    }

    @Test
    void duplicateEmailIsRejectedCaseInsensitively() {
        service.register(new RegisterRequest("ana@example.com", "s3cretpass", "Ana"));
        assertThatThrownBy(() -> service.register(new RegisterRequest("ANA@example.com", "other-pass1", "Other")))
                .isInstanceOf(DuplicateEmailException.class);
        assertThat(users.count()).isEqualTo(1);
    }

    @Test
    void invalidInputIsRejected() {
        assertThatThrownBy(() -> service.register(new RegisterRequest("no-at-sign", "s3cretpass", "A")))
                .isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.register(new RegisterRequest("@x.io", "s3cretpass", "A")))
                .isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.register(new RegisterRequest("a@x.io", "short", "A")))
                .isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.register(new RegisterRequest("a@x.io", "s3cretpass", "  ")))
                .isInstanceOf(IllegalArgumentException.class);
        assertThat(users.count()).isZero();
    }
}
