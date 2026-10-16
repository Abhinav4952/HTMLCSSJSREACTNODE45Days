package com.javaprep.day41.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class MicrometerMetricsTest {

    SimpleMeterRegistry registry;
    OrderMetrics metrics;

    @BeforeEach
    void setUp() {
        registry = new SimpleMeterRegistry();
        metrics = new OrderMetrics(registry);
    }

    @Test
    void counterIsTaggedPerChannel() {
        metrics.recordPlaced("web");
        metrics.recordPlaced("web");
        metrics.recordPlaced("mobile");
        assertThat(registry.get("orders.placed").tag("channel", "web").counter().count()).isEqualTo(2.0);
        assertThat(registry.get("orders.placed").tag("channel", "mobile").counter().count()).isEqualTo(1.0);
    }

    @Test
    void timerRecordsDurationAndReturnsResult() {
        String result = metrics.timeProcessing(() -> {
            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "done";
        });
        assertThat(result).isEqualTo("done");
        var timer = registry.get("orders.processing").timer();
        assertThat(timer.count()).isEqualTo(1);
        assertThat(timer.totalTime(TimeUnit.MILLISECONDS)).isGreaterThanOrEqualTo(9.0);
    }

    @Test
    void timerAlsoCountsFailures() {
        assertThatThrownBy(() -> metrics.timeProcessing(() -> {
            throw new IllegalStateException("x");
        })).isInstanceOf(IllegalStateException.class);
        assertThat(registry.get("orders.processing").timer().count()).isEqualTo(1);
    }

    @Test
    void gaugeFollowsTheLiveValue() {
        AtomicInteger queue = new AtomicInteger(3);
        metrics.registerQueueGauge(queue);
        assertThat(registry.get("orders.queue.size").gauge().value()).isEqualTo(3.0);
        queue.set(11);
        assertThat(registry.get("orders.queue.size").gauge().value()).isEqualTo(11.0);
    }

    @Test
    void distributionSummaryTracksAmounts() {
        metrics.recordAmount(10);
        metrics.recordAmount(30);
        var summary = registry.get("orders.amount").summary();
        assertThat(summary.count()).isEqualTo(2);
        assertThat(summary.totalAmount()).isEqualTo(40.0);
        assertThat(summary.getId().getBaseUnit()).isEqualTo("eur");
        assertThat(summary.max()).isEqualTo(30.0);
    }
}
