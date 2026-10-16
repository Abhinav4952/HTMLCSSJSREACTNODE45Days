package com.javaprep.day46.task04;

import java.sql.Connection;

/** Relays unpublished outbox rows to the broker in id order (at-least-once). */
public class OutboxPoller {

    private final Connection connection;

    public OutboxPoller(Connection connection) {
        this.connection = connection;
    }

    /**
     * Selects unpublished rows ordered by id, publishes each, and marks it published AFTER a successful publish.
     * If the publisher throws, STOP (later rows must not overtake the failed one), leave it unpublished and return
     * the number of rows published in this call.
     */
    public int pollOnce(OutboxPublisher publisher) {
        // TODO(Day46-task04): select unpublished rows order by id; publish; update published = true; stop on first failure
        throw new UnsupportedOperationException("TODO(Day46-task04): implement pollOnce");
    }
}
