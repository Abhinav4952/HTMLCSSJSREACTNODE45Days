package com.javaprep.day37.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.factory.PasswordEncoderFactories;

class PasswordServiceTest {

    PasswordService service = new PasswordService(6);

    @Test
    void hashLooksLikeBcryptAndIsNotThePassword() {
        String h = service.hash("correct horse");
        assertThat(h).startsWith("$2a$06$").hasSize(60).doesNotContain("correct");
    }

    @Test
    void sameInputGivesDifferentHashesBecauseOfSalt() {
        assertThat(service.hash("correct horse")).isNotEqualTo(service.hash("correct horse"));
    }

    @Test
    void matchesAcceptsOnlyTheRightPassword() {
        String h = service.hash("correct horse");
        assertThat(service.matches("correct horse", h)).isTrue();
        assertThat(service.matches("Correct horse", h)).isFalse();
        assertThat(service.matches(null, h)).isFalse();
        assertThat(service.matches("correct horse", null)).isFalse();
    }

    @Test
    void shortOrMissingPasswordsAreRejected() {
        assertThatThrownBy(() -> service.hash("short")).isInstanceOf(IllegalArgumentException.class).hasMessage("password too short");
        assertThatThrownBy(() -> service.hash(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void weakerHashesNeedAnUpgrade() {
        String weak = new BCryptPasswordEncoder(4).encode("correct horse");
        assertThat(service.needsUpgrade(weak)).isTrue();
        assertThat(service.needsUpgrade(service.hash("correct horse"))).isFalse();
        assertThat(new PasswordService(4).needsUpgrade(weak)).isFalse();
    }

    @Test
    void delegatingEncoderUnderstandsIdPrefixes() {
        var delegating = PasswordEncoderFactories.createDelegatingPasswordEncoder();
        String stored = "{bcrypt}" + service.hash("correct horse").substring(0);
        assertThat(delegating.matches("correct horse", stored)).isTrue();
    }
}
