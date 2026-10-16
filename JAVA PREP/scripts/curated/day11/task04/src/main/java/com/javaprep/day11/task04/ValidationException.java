package com.javaprep.day11.task04;

public class ValidationException extends RuntimeException {

    private final String field;

    public ValidationException(String field, String message) {
        super(message);
        this.field = field;
    }

    // TODO(Day11-task04): return the field name that failed validation
    public String getField() {
        throw new UnsupportedOperationException("TODO(Day11-task04): implement getField");
    }

    // TODO(Day11-task04): throw ValidationException(field "email") if email is null/blank or has no '@'; otherwise return normally
    public static void requireEmail(String email) {
        throw new UnsupportedOperationException("TODO(Day11-task04): implement requireEmail");
    }
}
