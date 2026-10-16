package com.javaprep.day12.task02;

public enum OrderStatus {
    NEW,
    PAID,
    SHIPPED,
    DELIVERED,
    CANCELLED;

    // TODO(Day12-task02): NEW->PAID/CANCELLED; PAID->SHIPPED/CANCELLED; SHIPPED->DELIVERED; everything else false; null -> NPE
    public boolean canTransitionTo(OrderStatus next) {
        throw new UnsupportedOperationException("TODO(Day12-task02): implement canTransitionTo");
    }
}
