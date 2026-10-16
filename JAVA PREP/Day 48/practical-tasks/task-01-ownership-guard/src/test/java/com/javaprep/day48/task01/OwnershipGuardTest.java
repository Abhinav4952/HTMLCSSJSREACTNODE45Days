package com.javaprep.day48.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.Optional;
import org.junit.jupiter.api.Test;

class OwnershipGuardTest {

    private final Resource doc = new Resource(1L, 10L);
    private final OwnershipGuard hide = new OwnershipGuard(OwnershipGuard.DenialPolicy.HIDE_AS_404);
    private final OwnershipGuard forbid = new OwnershipGuard(OwnershipGuard.DenialPolicy.FORBID_403);

    @Test
    void ownerGetsTheResource() {
        assertThat(hide.require(Optional.of(doc), 10L, false)).isSameAs(doc);
        assertThat(forbid.require(Optional.of(doc), 10L, false)).isSameAs(doc);
    }

    @Test
    void adminGetsTheResource() {
        assertThat(hide.require(Optional.of(doc), 99L, true)).isSameAs(doc);
        assertThat(forbid.require(Optional.of(doc), 99L, true)).isSameAs(doc);
    }

    @Test
    void missingResourceIsAlways404() {
        assertThatThrownBy(() -> hide.require(Optional.empty(), 10L, false)).isInstanceOf(NotFoundException.class);
        assertThatThrownBy(() -> forbid.require(Optional.empty(), 10L, true)).isInstanceOf(NotFoundException.class);
    }

    @Test
    void strangerIsHiddenUnderHidePolicy() {
        assertThatThrownBy(() -> hide.require(Optional.of(doc), 99L, false)).isInstanceOf(NotFoundException.class);
    }

    @Test
    void strangerIsForbiddenUnderForbidPolicy() {
        assertThatThrownBy(() -> forbid.require(Optional.of(doc), 99L, false)).isInstanceOf(ForbiddenException.class);
    }

    @Test
    void messagesDoNotLeakTheOwner() {
        assertThatThrownBy(() -> hide.require(Optional.of(doc), 99L, false)).hasMessageNotContaining("10");
        assertThatThrownBy(() -> forbid.require(Optional.of(doc), 99L, false)).hasMessageNotContaining("10");
    }
}
