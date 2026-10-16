package com.javaprep.day38.task02;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.filter.OncePerRequestFilter;

/** Reads "Authorization: Bearer <jwt>" and, when valid, authenticates the request. Never rejects requests itself. */
public class JwtAuthFilter extends OncePerRequestFilter {

    private final JwtUtil jwt;

    public JwtAuthFilter(JwtUtil jwt) {
        this.jwt = jwt;
    }

    /**
     * Valid bearer token -> put a UsernamePasswordAuthenticationToken (principal = username, no credentials,
     * authorities = "ROLE_" + each role) into the SecurityContext. In ALL cases continue the filter chain.
     * Missing header, other schemes (Basic ...) and invalid tokens leave the context untouched.
     */
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        // TODO(Day38-task02): parse the header, validate the token, populate SecurityContextHolder, always call chain.doFilter
        throw new UnsupportedOperationException("TODO(Day38-task02): parse the header, validate the token, populate SecurityContextHolder, always call chain.doFilter");
    }
}
