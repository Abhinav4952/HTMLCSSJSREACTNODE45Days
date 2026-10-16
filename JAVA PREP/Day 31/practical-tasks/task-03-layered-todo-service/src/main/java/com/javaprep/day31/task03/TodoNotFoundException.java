package com.javaprep.day31.task03;

public class TodoNotFoundException extends RuntimeException {
    public TodoNotFoundException(long id) {
        super("Todo " + id + " not found");
    }
}
