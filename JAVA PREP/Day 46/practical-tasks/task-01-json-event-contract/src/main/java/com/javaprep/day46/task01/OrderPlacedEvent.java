package com.javaprep.day46.task01;

/** PROVIDED. v1 contract of the OrderPlaced event. */
public record OrderPlacedEvent(int version, String orderId, String customerId, long amountCents) {
}
