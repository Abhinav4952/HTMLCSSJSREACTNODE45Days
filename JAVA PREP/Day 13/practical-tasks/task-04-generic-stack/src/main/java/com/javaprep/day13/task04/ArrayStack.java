package com.javaprep.day13.task04;

import java.util.Collection;
import java.util.Iterator;
import java.util.NoSuchElementException;

/** Growable LIFO stack backed by an Object[]. */
public class ArrayStack<E> implements Iterable<E> {

    private Object[] elements;
    private int size;

    public ArrayStack() {
        this(4);
    }

    public ArrayStack(int initialCapacity) {
        // TODO(Day13-task04): reject initialCapacity <= 0 with IllegalArgumentException, else allocate the backing array
        throw new UnsupportedOperationException("TODO(Day13-task04): constructor");
    }

    public void push(E item) {
        // TODO(Day13-task04): grow the array (double) when full, then store item on top
        throw new UnsupportedOperationException("TODO(Day13-task04): push");
    }

    @SuppressWarnings("unchecked")
    public E pop() {
        // TODO(Day13-task04): remove and return the top element, null out the slot; NoSuchElementException when empty
        throw new UnsupportedOperationException("TODO(Day13-task04): pop");
    }

    @SuppressWarnings("unchecked")
    public E peek() {
        // TODO(Day13-task04): return the top element without removing it; NoSuchElementException when empty
        throw new UnsupportedOperationException("TODO(Day13-task04): peek");
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public void pushAll(Iterable<? extends E> source) {
        // TODO(Day13-task04): push every element of source in iteration order (source is a producer)
        throw new UnsupportedOperationException("TODO(Day13-task04): pushAll");
    }

    public int popAll(Collection<? super E> sink) {
        // TODO(Day13-task04): pop every element into sink (consumer) in pop order and return how many were moved
        throw new UnsupportedOperationException("TODO(Day13-task04): popAll");
    }

    @Override
    public Iterator<E> iterator() {
        // TODO(Day13-task04): return an Iterator that walks top to bottom; next() past the end throws NoSuchElementException; remove() is unsupported
        throw new UnsupportedOperationException("TODO(Day13-task04): iterator");
    }
}
