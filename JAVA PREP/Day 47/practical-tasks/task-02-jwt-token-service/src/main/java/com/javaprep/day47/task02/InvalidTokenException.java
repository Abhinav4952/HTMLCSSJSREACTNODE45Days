package com.javaprep.day47.task02;

/** PROVIDED. Any token that must not be trusted (bad format, bad signature, expired). */
public class InvalidTokenException extends RuntimeException {

    public InvalidTokenException(String message) {
        super(message);
    }

    public InvalidTokenException(String message, Throwable cause) {
        super(message, cause);
    }
}
