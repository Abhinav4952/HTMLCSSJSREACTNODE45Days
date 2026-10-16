package com.javaprep.day31.task03;

public class DuplicateTodoException extends RuntimeException {
    public DuplicateTodoException(String title) {
        super("Duplicate todo: " + title);
    }
}
