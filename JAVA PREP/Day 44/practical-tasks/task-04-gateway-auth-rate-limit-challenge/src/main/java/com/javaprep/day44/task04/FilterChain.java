package com.javaprep.day44.task04;

import java.util.List;

/** PROVIDED (reference implementation from task 2). */
public final class FilterChain {

    private FilterChain() {
    }

    public static Handler build(List<GatewayFilter> filters, Handler terminal) {
        Handler next = terminal;
        List<GatewayFilter> copy = List.copyOf(filters);
        for (int i = copy.size() - 1; i >= 0; i--) {
            GatewayFilter f = copy.get(i);
            Handler downstream = next;
            next = request -> f.filter(request, downstream);
        }
        return next;
    }
}
