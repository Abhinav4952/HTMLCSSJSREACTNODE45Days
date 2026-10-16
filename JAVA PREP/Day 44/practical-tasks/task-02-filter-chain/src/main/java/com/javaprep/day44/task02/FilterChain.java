package com.javaprep.day44.task02;

import java.util.List;

/** Builds a chain of {@link GatewayFilter}s ending in a terminal {@link Handler} (like Spring's filter chains). */
public final class FilterChain {

    private FilterChain() {
    }

    /**
     * Filters run in list order on the way in and in reverse order on the way out. A filter may skip
     * {@code next.handle(...)} to short-circuit (the terminal is then never called). The list is copied at build time.
     */
    public static Handler build(List<GatewayFilter> filters, Handler terminal) {
        // TODO(Day44-task02): compose the filters around the terminal handler (hint: iterate backwards)
        throw new UnsupportedOperationException("TODO(Day44-task02): implement build");
    }
}
