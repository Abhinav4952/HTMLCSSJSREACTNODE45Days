package com.javaprep.day08.task03;

import java.util.List;

public class ImmutableNames {

    private List<String> names = List.of();

    // TODO(Day08-task03): defensive copy (List.copyOf); null list or null element throws NullPointerException
    public ImmutableNames(List<String> names) {
    }

    // TODO(Day08-task03): return the unmodifiable internal list
    public List<String> names() {
        throw new UnsupportedOperationException("TODO(Day08-task03): implement names");
    }
}
