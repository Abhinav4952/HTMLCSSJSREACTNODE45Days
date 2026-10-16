package com.javaprep.day39.task01;

import java.util.List;
import java.util.Optional;

public interface BookService {
    Optional<Book> find(long id);

    List<Book> findAll();

    List<Book> byAuthor(String author);
}
