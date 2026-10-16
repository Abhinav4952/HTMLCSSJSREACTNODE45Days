package com.javaprep.day44.task04;

/** PROVIDED. Minimal response model. */
public record GatewayResponse(int status, String body) {

    public static GatewayResponse ok(String body) {
        return new GatewayResponse(200, body);
    }
}
