package com.javaprep.day43.task01;

/** PROVIDED. Signals that the downstream inventory service could not give an answer. */
public class InventoryUnavailableException extends RuntimeException {

    public InventoryUnavailableException(String message, Throwable cause) {
        super(message, cause);
    }
}
