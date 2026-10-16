package com.javaprep.day23.task03;

import java.util.NoSuchElementException;

/** Fixed-capacity LIFO stack. */
public final class BoundedStack<T> {

    private final Object[] items;
    private int size;

    public BoundedStack(int capacity) {
        // TODO(Day23-task03): capacity <= 0 -> IllegalArgumentException; allocate the backing array
        throw new UnsupportedOperationException("TODO(Day23-task03): constructor");
    }

    public void push(T item) {
        // TODO(Day23-task03): when size == capacity throw IllegalStateException('stack full'); otherwise store at items[size++]
        throw new UnsupportedOperationException("TODO(Day23-task03): push");
    }

    @SuppressWarnings("unchecked")
    public T pop() {
        // TODO(Day23-task03): empty -> NoSuchElementException; otherwise return the top element and clear its slot (avoid keeping a reference)
        throw new UnsupportedOperationException("TODO(Day23-task03): pop");
    }

    @SuppressWarnings("unchecked")
    public T peek() {
        // TODO(Day23-task03): empty -> NoSuchElementException; otherwise return the top element without removing it
        throw new UnsupportedOperationException("TODO(Day23-task03): peek");
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public int capacity() {
        return items.length;
    }
}
