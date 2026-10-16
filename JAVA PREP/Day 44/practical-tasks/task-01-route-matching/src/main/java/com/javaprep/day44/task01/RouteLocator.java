package com.javaprep.day44.task01;

import java.util.List;
import java.util.Optional;

/** Predicate-based route matching, like a Spring Cloud Gateway {@code Path=} predicate. */
public class RouteLocator {

    private final List<Route> routes;

    public RouteLocator(List<Route> routes) {
        this.routes = List.copyOf(routes);
    }

    /**
     * A route matches when the path (ignoring any query string) equals the prefix or starts with prefix + "/".
     * If several routes match, the one with the LONGEST prefix wins. No match -> Optional.empty().
     */
    public Optional<Route> match(String path) {
        // TODO(Day44-task01): strip the query string, filter matching routes (segment boundary!), pick the longest prefix
        throw new UnsupportedOperationException("TODO(Day44-task01): implement match");
    }
}
