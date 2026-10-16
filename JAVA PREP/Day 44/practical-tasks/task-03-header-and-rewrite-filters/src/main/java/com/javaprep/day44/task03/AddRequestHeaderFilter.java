package com.javaprep.day44.task03;

/** Like Gateway's AddRequestHeader: sets (overwrites) a header before calling the downstream. */
public class AddRequestHeaderFilter implements GatewayFilter {

    private final String name;
    private final String value;

    public AddRequestHeaderFilter(String name, String value) {
        this.name = name;
        this.value = value;
    }

    @Override
    public GatewayResponse filter(GatewayRequest request, Handler next) {
        // TODO(Day44-task03): add the header (overwrite an existing one) and continue the chain
        throw new UnsupportedOperationException("TODO(Day44-task03): implement AddRequestHeaderFilter");
    }
}
