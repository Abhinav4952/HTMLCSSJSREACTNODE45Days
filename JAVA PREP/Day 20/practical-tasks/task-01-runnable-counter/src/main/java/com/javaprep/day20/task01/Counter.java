package com.javaprep.day20.task01;

/** Shared counter; must be safe for concurrent increments. */
public final class Counter {

    private int value;

    public void increment() {
        // TODO(Day20-task01): make this method thread-safe: mark it synchronized (or lock a private final monitor) and increment value
        throw new UnsupportedOperationException("TODO(Day20-task01): increment");
    }

    public int get() {
        // TODO(Day20-task01): return value using the SAME lock as increment so that the latest value is visible
        throw new UnsupportedOperationException("TODO(Day20-task01): get");
    }
}
