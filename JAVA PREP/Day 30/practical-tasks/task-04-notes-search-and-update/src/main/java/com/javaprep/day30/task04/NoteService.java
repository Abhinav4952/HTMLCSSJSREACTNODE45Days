package com.javaprep.day30.task04;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Service;

/** PROVIDED in-memory store (do not edit). */
@Service
public class NoteService {
    private final Map<Long, Note> notes = new ConcurrentHashMap<>();
    private final AtomicLong seq = new AtomicLong();

    public Note add(String text) {
        Note n = new Note(seq.incrementAndGet(), text);
        notes.put(n.id(), n);
        return n;
    }

    public List<Note> all() {
        return new ArrayList<>(notes.values().stream().sorted(java.util.Comparator.comparing(Note::id)).toList());
    }

    public Optional<Note> update(long id, String text) {
        return notes.computeIfPresent(id, (k, old) -> new Note(k, text)) == null ? Optional.empty() : Optional.of(notes.get(id));
    }
}
