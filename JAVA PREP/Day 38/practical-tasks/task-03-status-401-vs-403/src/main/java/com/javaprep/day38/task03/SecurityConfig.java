package com.javaprep.day38.task03;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    /** No/invalid credentials on a protected route -> 401, Content-Type application/json, body {"error":"unauthorized"}. */
    @Bean
    public AuthenticationEntryPoint authenticationEntryPoint() {
        // TODO(Day38-task03): return an entry point that writes status 401 and the JSON body
        throw new UnsupportedOperationException("TODO(Day38-task03): return an entry point that writes status 401 and the JSON body");
    }

    /** Authenticated but lacking the role -> 403, Content-Type application/json, body {"error":"forbidden"}. */
    @Bean
    public AccessDeniedHandler accessDeniedHandler() {
        // TODO(Day38-task03): return a handler that writes status 403 and the JSON body
        throw new UnsupportedOperationException("TODO(Day38-task03): return a handler that writes status 403 and the JSON body");
    }

    /**
     * /public/** open; /admin/** role ADMIN; everything else authenticated. CSRF off, STATELESS sessions,
     * JwtAuthFilter (new JwtAuthFilter(jwtUtil)) before UsernamePasswordAuthenticationFilter, and the two handlers above.
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http, JwtUtil jwtUtil, AuthenticationEntryPoint entryPoint, AccessDeniedHandler denied) throws Exception {
        // TODO(Day38-task03): wire csrf, sessions, exception handling, authorization rules and the JWT filter
        throw new UnsupportedOperationException("TODO(Day38-task03): wire csrf, sessions, exception handling, authorization rules and the JWT filter");
    }
}
