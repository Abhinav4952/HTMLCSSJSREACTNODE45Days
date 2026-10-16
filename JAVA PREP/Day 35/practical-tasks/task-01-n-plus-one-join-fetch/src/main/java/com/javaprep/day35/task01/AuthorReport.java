package com.javaprep.day35.task01;

import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import org.springframework.stereotype.Component;

@Component
public class AuthorReport {

    private final AuthorRepository repository;

    public AuthorReport(AuthorRepository repository) {
        this.repository = repository;
    }

    /** PROVIDED: the classic N+1 trap (1 query for authors + 1 per author for books). */
    public Map<String, Integer> bookCountsNaive() {
        Map<String, Integer> out = new TreeMap<>();
        for (Author a : repository.findAll()) {
            out.put(a.getName(), a.getBooks().size());
        }
        return out;
    }

    /** author name -> number of books, using ONE SQL statement (join fetch). */
    public Map<String, Integer> bookCountsJoinFetch() {
        // TODO(Day35-task01): use repository.findAllWithBooks()
        throw new UnsupportedOperationException("TODO(Day35-task01): use repository.findAllWithBooks()");
    }

    /** author name -> number of books, using ONE SQL statement (entity graph). */
    public Map<String, Integer> bookCountsEntityGraph() {
        // TODO(Day35-task01): use repository.findAllWithGraph()
        throw new UnsupportedOperationException("TODO(Day35-task01): use repository.findAllWithGraph()");
    }

    private static Map<String, Integer> toCounts(List<Author> authors) {
        Map<String, Integer> out = new TreeMap<>();
        for (Author a : authors) {
            out.put(a.getName(), a.getBooks().size());
        }
        return out;
    }
}
