package com.javaprep.day35.task02;

/** CHECKED exception: Spring does NOT roll back for it by default. */
public class AuditUnavailableException extends Exception {
    public AuditUnavailableException(String message) {
        super(message);
    }
}
