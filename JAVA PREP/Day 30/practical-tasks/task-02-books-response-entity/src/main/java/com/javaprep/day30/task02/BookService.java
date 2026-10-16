package com.javaprep.day30.task02;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Service;

/** PROVIDED in-memory store (do not edit). */
@Service
public class BookService {
    private final Map<Long, Book> books = new ConcurrentHashMap<>();
    private final AtomicLong seq = new AtomicLong();

    public List<Book> findAll() {
        return new ArrayList<>(books.values().stream().sorted(java.util.Comparator.comparing(Book::id)).toList());
    }

    public Optional<Book> findById(long id) {
        return Optional.ofNullable(books.get(id));
    }

    public Book create(String title, String author) {
        Book b = new Book(seq.incrementAndGet(), title, author);
        books.put(b.id(), b);
        return b;
    }

    public boolean delete(long id) {
        return books.remove(id) != null;
    }
}
