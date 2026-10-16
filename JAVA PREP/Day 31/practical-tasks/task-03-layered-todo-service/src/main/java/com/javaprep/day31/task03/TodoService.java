package com.javaprep.day31.task03;

import java.util.List;

/** Business layer. Knows nothing about HTTP. */
public class TodoService {

    private final TodoRepository repository;

    public TodoService(TodoRepository repository) {
        this.repository = repository;
    }

    /** Trims the title; blank -> IllegalArgumentException; case-insensitive duplicate -> DuplicateTodoException. New todos are open. */
    public TodoDto create(String title) {
        // TODO(Day31-task03): validate, reject duplicates (ignore case), save and map
        throw new UnsupportedOperationException("TODO(Day31-task03): validate, reject duplicates (ignore case), save and map");
    }

    /** Marks a todo as done. Unknown id -> TodoNotFoundException. Completing an already done todo -> IllegalStateException. */
    public TodoDto complete(long id) {
        // TODO(Day31-task03): load, check state, save the done copy and map
        throw new UnsupportedOperationException("TODO(Day31-task03): load, check state, save the done copy and map");
    }

    /** All todos as DTOs, optionally only the open ones. */
    public List<TodoDto> list(boolean onlyOpen) {
        // TODO(Day31-task03): map all (or only open) todos
        throw new UnsupportedOperationException("TODO(Day31-task03): map all (or only open) todos");
    }
}
