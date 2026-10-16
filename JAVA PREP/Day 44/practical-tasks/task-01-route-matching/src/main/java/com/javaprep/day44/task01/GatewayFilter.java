package com.javaprep.day44.task01;

/** PROVIDED. A gateway filter may change the request, short-circuit, or change the response. */
@FunctionalInterface
public interface GatewayFilter {

    GatewayResponse filter(GatewayRequest request, Handler next);
}
