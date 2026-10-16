package com.javaprep.day40.task02;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Component;

/** PROVIDED registry of call counts and total nanoseconds by method name. */
@Component
public class MetricsRegistry {
    private final Map<String, AtomicLong> counts = new ConcurrentHashMap<>();
    private final Map<String, AtomicLong> totals = new ConcurrentHashMap<>();

    public void record(String name, long nanos) {
        counts.computeIfAbsent(name, k -> new AtomicLong()).incrementAndGet();
        totals.computeIfAbsent(name, k -> new AtomicLong()).addAndGet(nanos);
    }

    public long count(String name) {
        AtomicLong c = counts.get(name);
        return c == null ? 0 : c.get();
    }

    public long totalNanos(String name) {
        AtomicLong t = totals.get(name);
        return t == null ? 0 : t.get();
    }
}
