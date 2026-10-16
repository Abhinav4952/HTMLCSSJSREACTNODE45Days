package com.javaprep.day37.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.DisabledException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

class UserDetailsServiceTest {

    BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(4);
    StoreUserDetailsService service;
    DaoAuthenticationProvider provider;

    @BeforeEach
    void setUp() {
        UserStore store = new UserStore()
                .add(new UserRecord("alice", encoder.encode("alicepw"), List.of("ADMIN", "USER"), true))
                .add(new UserRecord("bob", encoder.encode("bobpw"), List.of("USER"), true))
                .add(new UserRecord("carl", encoder.encode("carlpw"), List.of("USER"), false));
        service = new StoreUserDetailsService(store);
        provider = new DaoAuthenticationProvider();
        provider.setUserDetailsService(service);
        provider.setPasswordEncoder(encoder);
    }

    private Authentication login(String user, String pw) {
        return provider.authenticate(UsernamePasswordAuthenticationToken.unauthenticated(user, pw));
    }

    @Test
    void mapsRolesToPrefixedAuthorities() {
        UserDetails d = service.loadUserByUsername("alice");
        assertThat(d.getUsername()).isEqualTo("alice");
        assertThat(d.getAuthorities()).extracting(Object::toString).containsExactlyInAnyOrder("ROLE_ADMIN", "ROLE_USER");
        assertThat(d.isEnabled()).isTrue();
    }

    @Test
    void lookupIsCaseInsensitive() {
        assertThat(service.loadUserByUsername("BOB").getUsername()).isEqualTo("bob");
    }

    @Test
    void unknownUserThrows() {
        assertThatThrownBy(() -> service.loadUserByUsername("nobody")).isInstanceOf(UsernameNotFoundException.class);
    }

    @Test
    void disabledAccountIsReportedDisabled() {
        assertThat(service.loadUserByUsername("carl").isEnabled()).isFalse();
    }

    @Test
    void authenticationSucceedsWithRightPassword() {
        Authentication a = login("bob", "bobpw");
        assertThat(a.isAuthenticated()).isTrue();
        assertThat(a.getAuthorities()).extracting(Object::toString).containsExactly("ROLE_USER");
    }

    @Test
    void wrongPasswordAndUnknownUserLookTheSame() {
        assertThatThrownBy(() -> login("bob", "nope")).isInstanceOf(BadCredentialsException.class);
        assertThatThrownBy(() -> login("ghost", "x")).isInstanceOf(BadCredentialsException.class);
    }

    @Test
    void disabledUserCannotLogIn() {
        assertThatThrownBy(() -> login("carl", "carlpw")).isInstanceOf(DisabledException.class);
    }
}
