package com.javaprep.day30.task02;

import java.net.URI;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/books")
public class BookController {

    private final BookService service;

    public BookController(BookService service) {
        this.service = service;
    }

    /** GET /api/books -> 200 + JSON array. */
    @GetMapping
    public List<Book> list() {
        // TODO(Day30-task02): return all books
        throw new UnsupportedOperationException("TODO(Day30-task02): return all books");
    }

    /** GET /api/books/{id} -> 200 + book, or 404 with empty body. */
    @GetMapping("/{id}")
    public ResponseEntity<Book> get(@PathVariable long id) {
        // TODO(Day30-task02): 200 with the book or 404 (ResponseEntity.notFound)
        throw new UnsupportedOperationException("TODO(Day30-task02): 200 with the book or 404 (ResponseEntity.notFound)");
    }

    /** POST /api/books -> 201, Location: /api/books/{newId}, body = created book. */
    @PostMapping
    public ResponseEntity<Book> create(@RequestBody CreateBookRequest request) {
        // TODO(Day30-task02): create the book and answer 201 Created with a Location header and the book as body
        throw new UnsupportedOperationException("TODO(Day30-task02): create the book and answer 201 Created with a Location header and the book as body");
    }

    /** DELETE /api/books/{id} -> 204 when deleted, 404 when unknown. */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable long id) {
        // TODO(Day30-task02): 204 No Content when removed, otherwise 404
        throw new UnsupportedOperationException("TODO(Day30-task02): 204 No Content when removed, otherwise 404");
    }
}
