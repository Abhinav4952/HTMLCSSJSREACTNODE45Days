package com.javaprep.day38.task03;

import java.time.Duration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** PROVIDED (do not edit). */
@Configuration
public class JwtConfig {
    @Bean
    public JwtUtil jwtUtil() {
        return new JwtUtil("0123456789-0123456789-0123456789-ab", Duration.ofMinutes(10));
    }
}
