package com.javaprep.day44.task04;

import java.util.Set;

/** Rejects requests without a valid X-API-Key header. */
public class ApiKeyFilter implements GatewayFilter {

    private final Set<String> validKeys;

    public ApiKeyFilter(Set<String> validKeys) {
        this.validKeys = Set.copyOf(validKeys);
    }

    /** Missing or unknown key -> new GatewayResponse(401, "missing or invalid api key") and do NOT call next. */
    @Override
    public GatewayResponse filter(GatewayRequest request, Handler next) {
        // TODO(Day44-task04): check the X-API-Key header against validKeys
        throw new UnsupportedOperationException("TODO(Day44-task04): implement ApiKeyFilter");
    }
}
