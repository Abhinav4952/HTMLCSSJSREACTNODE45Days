package com.javaprep.day41.task04;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.DistributionSummary;
import io.micrometer.core.instrument.Gauge;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Supplier;

public class OrderMetrics {

    private final MeterRegistry registry;

    public OrderMetrics(MeterRegistry registry) {
        this.registry = registry;
    }

    /** Counter "orders.placed" with ONE tag channel=<channel>; increments by 1 per call. */
    public void recordPlaced(String channel) {
        // TODO(Day41-task04): registry.counter(name, tags...).increment()
        throw new UnsupportedOperationException("TODO(Day41-task04): registry.counter(name, tags...).increment()");
    }

    /** Runs the supplier inside Timer "orders.processing" and returns its value; the timer records even when it throws. */
    public <T> T timeProcessing(Supplier<T> work) {
        // TODO(Day41-task04): Timer.builder(...).register(registry) then timer.record(supplier)
        throw new UnsupportedOperationException("TODO(Day41-task04): Timer.builder(...).register(registry) then timer.record(supplier)");
    }

    /** Gauge "orders.queue.size" that always reports the CURRENT value of the given AtomicInteger. */
    public void registerQueueGauge(AtomicInteger queue) {
        // TODO(Day41-task04): Gauge.builder(name, queue, AtomicInteger::get).register(registry)
        throw new UnsupportedOperationException("TODO(Day41-task04): Gauge.builder(name, queue, AtomicInteger::get).register(registry)");
    }

    /** DistributionSummary "orders.amount" with base unit "eur": records the amount of each order. */
    public void recordAmount(double amount) {
        // TODO(Day41-task04): DistributionSummary.builder(...).baseUnit(...).register(registry).record(amount)
        throw new UnsupportedOperationException("TODO(Day41-task04): DistributionSummary.builder(...).baseUnit(...).register(registry).record(amount)");
    }
}
