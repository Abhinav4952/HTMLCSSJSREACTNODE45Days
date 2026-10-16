package com.javaprep.day08.task04;

/**
 * Validated user identifier. The compact constructor TODO (validate + strip) does not throw so the record can
 * be created; {@link #of(String)} is the stubbed factory.
 */
public record UserId(String value) {

    // TODO(Day08-task04): compact constructor -- reject null/blank with IllegalArgumentException; store stripped value
    public UserId {
    }

    // TODO(Day08-task04): return new UserId(raw) (same validation); null/blank throws IllegalArgumentException
    public static UserId of(String raw) {
        throw new UnsupportedOperationException("TODO(Day08-task04): implement of");
    }
}
