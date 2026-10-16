package com.javaprep.day41.task03;

import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.stereotype.Component;

// TODO(Day41-task03): register as a Spring bean so Actuator picks it up as the component named "queue"
public class QueueHealthIndicator implements HealthIndicator {

    private final QueueStats stats;

    public QueueHealthIndicator(QueueStats stats) {
        this.stats = stats;
    }

    /**
     * depth < 80      -> UP
     * 80 <= depth < 100 -> OUT_OF_SERVICE (draining: no new work, HTTP 503)
     * depth >= 100    -> DOWN
     * Always include details: depth (int) and capacity (100).
     */
    @Override
    public Health health() {
        // TODO(Day41-task03): choose status by depth and add the two details
        throw new UnsupportedOperationException("TODO(Day41-task03): choose status by depth and add the two details");
    }
}
