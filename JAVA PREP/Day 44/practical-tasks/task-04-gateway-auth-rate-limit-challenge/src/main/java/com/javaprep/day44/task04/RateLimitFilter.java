package com.javaprep.day44.task04;

import java.time.Clock;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

/** Fixed-window rate limiter per X-API-Key (header absent -> client "anonymous"). */
public class RateLimitFilter implements GatewayFilter {

    private final int maxRequests;
    private final Duration window;
    private final Clock clock;
    private final Map<String, long[]> windows = new HashMap<>(); // client -> {windowStartMillis, count}

    public RateLimitFilter(int maxRequests, Duration window, Clock clock) {
        this.maxRequests = maxRequests;
        this.window = window;
        this.clock = clock;
    }

    /**
     * Allow at most maxRequests per client per window. The window starts at the client's first request; once
     * {@code window} has elapsed the counter resets. Over the limit -> new GatewayResponse(429, "rate limit exceeded").
     */
    @Override
    public synchronized GatewayResponse filter(GatewayRequest request, Handler next) {
        // TODO(Day44-task04): look up/create the client's window, reset if expired, count, and allow or answer 429
        throw new UnsupportedOperationException("TODO(Day44-task04): implement RateLimitFilter");
    }
}
