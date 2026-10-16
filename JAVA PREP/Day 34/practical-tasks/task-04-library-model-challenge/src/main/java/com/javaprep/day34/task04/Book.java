package com.javaprep.day34.task04;

import jakarta.persistence.*;
import java.util.*;

@Entity
@Table(name = "books")
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;

    // TODO(Day34-task04): many-to-one to Author: LAZY, join column author_id, not nullable
    private Author author;

    // TODO(Day34-task04): one-to-one to BookDetail owned by Book: LAZY, cascade ALL, orphanRemoval, join column detail_id
    private BookDetail detail;

    // TODO(Day34-task04): many-to-many to Tag through join table book_tags(book_id, tag_id); no cascade
    private Set<Tag> tags = new HashSet<>();

    protected Book() {
    }

    public Book(String title, int pages) {
        this.title = title;
        this.detail = new BookDetail(pages);
    }

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public Author getAuthor() {
        return author;
    }

    void setAuthor(Author author) {
        this.author = author;
    }

    public BookDetail getDetail() {
        return detail;
    }

    public Set<Tag> getTags() {
        return tags;
    }

    public void tag(Tag tag) {
        // TODO(Day34-task04): add to both sides
        throw new UnsupportedOperationException("TODO(Day34-task04): add to both sides");
    }
}
