package com.javaprep.day44.task04;

import java.util.List;
import java.util.Map;
import java.util.Optional;

/** Edge entry point: route lookup, global filters, backend invocation. */
public class Gateway {

    private final RouteLocator locator;
    private final List<GatewayFilter> globalFilters;
    private final Map<String, Handler> backendsByRouteId;

    public Gateway(RouteLocator locator, List<GatewayFilter> globalFilters, Map<String, Handler> backendsByRouteId) {
        this.locator = locator;
        this.globalFilters = List.copyOf(globalFilters);
        this.backendsByRouteId = Map.copyOf(backendsByRouteId);
    }

    /**
     * 1) no matching route -> 404 "no route" (filters are NOT run)
     * 2) matching route without a backend registered -> 502 "no backend"
     * 3) otherwise run the global filters (in order) around the route's backend handler
     */
    public GatewayResponse handle(GatewayRequest request) {
        // TODO(Day44-task04): use locator.match, backendsByRouteId and FilterChain.build
        throw new UnsupportedOperationException("TODO(Day44-task04): implement handle");
    }
}
