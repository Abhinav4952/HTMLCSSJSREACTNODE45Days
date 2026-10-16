package com.javaprep.day47.task01;

/** PROVIDED. */
public class DuplicateEmailException extends RuntimeException {

    public DuplicateEmailException(String email) {
        super("email already registered: " + email);
    }
}
