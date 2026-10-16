package com.javaprep.day43.task04;

/** PROVIDED. */
public record OrderResult(Status status, String sku, int quantity) {

    public enum Status { CONFIRMED, REJECTED_OUT_OF_STOCK, PENDING_INVENTORY_UNAVAILABLE }
}
