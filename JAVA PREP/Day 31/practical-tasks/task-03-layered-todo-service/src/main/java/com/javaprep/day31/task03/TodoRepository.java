package com.javaprep.day31.task03;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;

/** PROVIDED in-memory repository (data layer). */
public class TodoRepository {
    private final Map<Long, Todo> data = new TreeMap<>();
    private long seq;

    public Todo save(Todo todo) {
        long id = todo.id() == 0 ? ++seq : todo.id();
        Todo saved = new Todo(id, todo.title(), todo.done());
        data.put(id, saved);
        return saved;
    }

    public Optional<Todo> findById(long id) {
        return Optional.ofNullable(data.get(id));
    }

    public List<Todo> findAll() {
        return new ArrayList<>(data.values());
    }
}
