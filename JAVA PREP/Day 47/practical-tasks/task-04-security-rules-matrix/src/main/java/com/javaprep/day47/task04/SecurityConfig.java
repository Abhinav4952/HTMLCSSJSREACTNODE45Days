package com.javaprep.day47.task04;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    /**
     * Rules matrix:
     *   /public/**, /api/auth/**  -> anyone
     *   /api/admin/**             -> role ADMIN
     *   everything else           -> authenticated
     * Also: stateless sessions, CSRF disabled (token API), HTTP Basic enabled so anonymous access answers 401 (not 403).
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        // TODO(Day47-task04): http.csrf(...).sessionManagement(...).authorizeHttpRequests(...).httpBasic(...); return http.build();
        throw new UnsupportedOperationException("TODO(Day47-task04): implement filterChain");
    }
}
