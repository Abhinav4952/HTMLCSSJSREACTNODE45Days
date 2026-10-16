package com.javaprep.day44.task02;

import java.util.LinkedHashMap;
import java.util.Map;

/** PROVIDED. Immutable request model used by the simulated gateway. */
public record GatewayRequest(String method, String path, Map<String, String> headers) {

    public GatewayRequest {
        headers = Map.copyOf(headers == null ? Map.of() : headers);
    }

    public static GatewayRequest get(String path) {
        return new GatewayRequest("GET", path, Map.of());
    }

    public GatewayRequest withPath(String newPath) {
        return new GatewayRequest(method, newPath, headers);
    }

    public GatewayRequest withHeader(String name, String value) {
        Map<String, String> copy = new LinkedHashMap<>(headers);
        copy.put(name, value);
        return new GatewayRequest(method, path, copy);
    }

    public String header(String name) {
        return headers.get(name);
    }
}
