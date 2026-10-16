package com.javaprep.day44.task02;

/** PROVIDED. Minimal response model. */
public record GatewayResponse(int status, String body) {

    public static GatewayResponse ok(String body) {
        return new GatewayResponse(200, body);
    }
}
