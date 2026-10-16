package com.javaprep.day44.task04;

/** PROVIDED. Terminal handler (a downstream service) or the rest of a filter chain. */
@FunctionalInterface
public interface Handler {

    GatewayResponse handle(GatewayRequest request);
}
