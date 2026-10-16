package com.javaprep.day44.task04;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;

/** PROVIDED (reference implementation from task 1). */
public class RouteLocator {

    private final List<Route> routes;

    public RouteLocator(List<Route> routes) {
        this.routes = List.copyOf(routes);
    }

    public Optional<Route> match(String path) {
        String p = path.contains("?") ? path.substring(0, path.indexOf('?')) : path;
        return routes.stream()
                .filter(r -> p.equals(r.pathPrefix()) || p.startsWith(r.pathPrefix() + "/"))
                .max(Comparator.comparingInt(r -> r.pathPrefix().length()));
    }
}
