package com.javaprep.day34.task04;

import jakarta.persistence.*;
import java.util.*;

@Entity
@Table(name = "authors")
public class Author {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    // TODO(Day34-task04): inverse one-to-many to Book (mappedBy author, cascade ALL, orphanRemoval, LAZY)
    private List<Book> books = new ArrayList<>();

    protected Author() {
    }

    public Author(String name) {
        this.name = name;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public List<Book> getBooks() {
        return books;
    }

    public void addBook(Book book) {
        // TODO(Day34-task04): add and set back reference
        throw new UnsupportedOperationException("TODO(Day34-task04): add and set back reference");
    }

    public void removeBook(Book book) {
        // TODO(Day34-task04): remove and clear back reference
        throw new UnsupportedOperationException("TODO(Day34-task04): remove and clear back reference");
    }
}
