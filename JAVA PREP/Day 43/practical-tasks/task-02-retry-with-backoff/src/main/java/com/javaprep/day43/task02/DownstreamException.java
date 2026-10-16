package com.javaprep.day43.task02;

/** PROVIDED. Retryable failure of a downstream dependency. */
public class DownstreamException extends RuntimeException {

    public DownstreamException(String message) {
        super(message);
    }
}
