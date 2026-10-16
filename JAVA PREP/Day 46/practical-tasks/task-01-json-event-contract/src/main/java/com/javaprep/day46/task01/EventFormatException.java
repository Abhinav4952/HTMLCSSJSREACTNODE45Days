package com.javaprep.day46.task01;

/** PROVIDED. Thrown for malformed or invalid events. */
public class EventFormatException extends RuntimeException {

    public EventFormatException(String message, Throwable cause) {
        super(message, cause);
    }

    public EventFormatException(String message) {
        super(message);
    }
}
