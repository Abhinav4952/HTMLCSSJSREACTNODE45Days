package com.javaprep.day44.task03;

/** Like Gateway's StripPrefix: removes the first N path segments before calling the downstream. */
public class StripPrefixFilter implements GatewayFilter {

    private final int parts;

    public StripPrefixFilter(int parts) {
        this.parts = parts;
    }

    /** "/api/users/1" with parts=1 -> "/users/1"; parts=2 -> "/1"; more parts than segments -> "/". */
    @Override
    public GatewayResponse filter(GatewayRequest request, Handler next) {
        // TODO(Day44-task03): split the path into segments, drop the first `parts`, rebuild the path (keep query string)
        throw new UnsupportedOperationException("TODO(Day44-task03): implement StripPrefixFilter");
    }
}
