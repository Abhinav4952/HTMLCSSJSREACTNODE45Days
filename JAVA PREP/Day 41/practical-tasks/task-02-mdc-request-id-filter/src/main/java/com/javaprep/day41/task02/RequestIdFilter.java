package com.javaprep.day41.task02;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.UUID;
import java.util.regex.Pattern;
import org.slf4j.MDC;
import org.springframework.web.filter.OncePerRequestFilter;

public class RequestIdFilter extends OncePerRequestFilter {

    public static final String HEADER = "X-Request-Id";
    public static final String MDC_KEY = "requestId";
    private static final Pattern SAFE = Pattern.compile("[A-Za-z0-9-]{1,64}");

    /**
     * 1. take the id from header X-Request-Id when it matches [A-Za-z0-9-]{1,64} (prevents log injection);
     *    otherwise generate UUID.randomUUID().toString()
     * 2. put it into the MDC under "requestId"
     * 3. echo it in the response header X-Request-Id
     * 4. continue the chain; ALWAYS remove the MDC key afterwards (threads are reused!)
     */
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        // TODO(Day41-task02): implement the four steps
        throw new UnsupportedOperationException("TODO(Day41-task02): implement the four steps");
    }

    /** Logback console pattern that prints the request id: time [requestId] LEVEL logger - message */
    public static String logPattern() {
        // TODO(Day41-task02): return the pattern using %X{requestId}
        throw new UnsupportedOperationException("TODO(Day41-task02): return the pattern using %X{requestId}");
    }
}
