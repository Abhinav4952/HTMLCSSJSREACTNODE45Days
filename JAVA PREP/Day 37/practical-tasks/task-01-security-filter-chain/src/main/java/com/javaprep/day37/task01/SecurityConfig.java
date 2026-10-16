package com.javaprep.day37.task01;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    /**
     * Rules (first match wins, most specific first):
     *  - /public/**  -> everyone
     *  - /admin/**   -> role ADMIN
     *  - anything else -> authenticated
     * Stateless REST API: CSRF disabled, no HTTP session, HTTP Basic for authentication (gives 401 + WWW-Authenticate).
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        // TODO(Day37-task01): configure csrf, sessionManagement (STATELESS), authorizeHttpRequests and httpBasic, then return http.build()
        throw new UnsupportedOperationException("TODO(Day37-task01): configure csrf, sessionManagement (STATELESS), authorizeHttpRequests and httpBasic, then return http.build()");
    }
}
