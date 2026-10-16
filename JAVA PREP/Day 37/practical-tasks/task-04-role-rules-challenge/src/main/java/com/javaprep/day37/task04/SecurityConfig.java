package com.javaprep.day37.task04;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    /** BCrypt with low strength 4 (fast tests). */
    @Bean
    public PasswordEncoder passwordEncoder() {
        // TODO(Day37-task04): return a BCryptPasswordEncoder(4)
        throw new UnsupportedOperationException("TODO(Day37-task04): return a BCryptPasswordEncoder(4)");
    }

    /** Users: alice / alicepw with role ADMIN, bob / bobpw with role USER. Store only ENCODED passwords. */
    @Bean
    public UserDetailsService userDetailsService(PasswordEncoder encoder) {
        // TODO(Day37-task04): InMemoryUserDetailsManager with the two users
        throw new UnsupportedOperationException("TODO(Day37-task04): InMemoryUserDetailsManager with the two users");
    }

    /**
     * Rules:
     *  /public/**                 everyone
     *  GET    /api/reports/** and /api/reports   USER or ADMIN
     *  DELETE /api/reports/**                    ADMIN only
     *  everything else (e.g. /api/whoami)        authenticated
     * Stateless, CSRF disabled, HTTP Basic.
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        // TODO(Day37-task04): authorizeHttpRequests with HttpMethod-specific matchers; stateless; basic
        throw new UnsupportedOperationException("TODO(Day37-task04): authorizeHttpRequests with HttpMethod-specific matchers; stateless; basic");
    }
}
