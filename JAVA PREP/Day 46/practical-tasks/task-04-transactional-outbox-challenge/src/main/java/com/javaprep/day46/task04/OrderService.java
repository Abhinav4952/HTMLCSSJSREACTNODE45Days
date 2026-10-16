package com.javaprep.day46.task04;

import java.sql.Connection;

public class OrderService {

    private final Connection connection;

    public OrderService(Connection connection) {
        this.connection = connection;
    }

    /**
     * Atomically (ONE transaction) inserts the order row AND an outbox row (event_type "OrderPlaced", aggregate_id =
     * orderId, same payload). Any failure rolls BOTH back and is rethrown as IllegalStateException.
     * Auto-commit is restored afterwards.
     */
    public void placeOrder(String orderId, String payload) {
        // TODO(Day46-task04): setAutoCommit(false); insert into orders; insert into outbox; commit; rollback on any exception
        throw new UnsupportedOperationException("TODO(Day46-task04): implement placeOrder");
    }
}
