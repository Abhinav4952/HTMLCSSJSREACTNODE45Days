package com.javaprep.day09.task03;

public class Book {

    private final String isbn;
    private final String title;

    public Book(String isbn, String title) {
        this.isbn = isbn;
        this.title = title;
    }

    public String isbn() {
        return isbn;
    }

    public String title() {
        return title;
    }

    // TODO(Day09-task03): equal when the other object is a Book with the same ISBN (title is ignored); null-safe
    @Override
    public boolean equals(Object o) {
        throw new UnsupportedOperationException("TODO(Day09-task03): implement equals");
    }

    // TODO(Day09-task03): hash of the ISBN only, consistent with equals
    @Override
    public int hashCode() {
        throw new UnsupportedOperationException("TODO(Day09-task03): implement hashCode");
    }
}
