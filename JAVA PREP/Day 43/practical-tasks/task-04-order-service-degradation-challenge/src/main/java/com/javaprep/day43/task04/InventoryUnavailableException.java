package com.javaprep.day43.task04;

/** PROVIDED. Retryable failure of the inventory service. */
public class InventoryUnavailableException extends RuntimeException {

    public InventoryUnavailableException(String message) {
        super(message);
    }
}
