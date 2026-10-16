package com.javaprep.day39.task01;

import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/books")
public class BookController {

    private final BookService service;

    public BookController(BookService service) {
        this.service = service;
    }

    /** 200 + book JSON or 404. */
    @GetMapping("/{id}")
    public ResponseEntity<Book> get(@PathVariable long id) {
        // TODO(Day39-task01): return the book as 200 or answer 404
        throw new UnsupportedOperationException("TODO(Day39-task01): return the book as 200 or answer 404");
    }

    /** Without `author` -> service.findAll(); with `author` -> service.byAuthor(author) and NEVER findAll(). */
    @GetMapping
    public List<Book> list(@RequestParam(required = false) String author) {
        // TODO(Day39-task01): delegate to findAll or byAuthor depending on the parameter
        throw new UnsupportedOperationException("TODO(Day39-task01): delegate to findAll or byAuthor depending on the parameter");
    }
}
