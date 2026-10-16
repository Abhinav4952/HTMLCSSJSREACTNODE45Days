package com.javaprep.day36.task03;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * CORS policy for /api/**: origin https://app.example.com only; methods GET, POST, PUT, DELETE;
 * any request headers; credentials allowed; preflight cached for 3600 seconds.
 */
@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        // TODO(Day36-task03): registry.addMapping on /api/** with origins, methods, headers, credentials and maxAge
        throw new UnsupportedOperationException("TODO(Day36-task03): registry.addMapping on /api/** with origins, methods, headers, credentials and maxAge");
    }
}
