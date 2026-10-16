package com.javaprep.day13.task01;

import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.function.Function;

/** Immutable container holding zero or one non-null value. */
public final class Box<T> {

    private final T value;

    private Box(T value) {
        this.value = value;
    }

    public static <T> Box<T> of(T value) {
        // TODO(Day13-task01): return a box holding value; throw NullPointerException when value is null
        throw new UnsupportedOperationException("TODO(Day13-task01): of");
    }

    public static <T> Box<T> empty() {
        // TODO(Day13-task01): return an empty box (a box that holds no value)
        throw new UnsupportedOperationException("TODO(Day13-task01): empty");
    }

    public boolean isEmpty() {
        // TODO(Day13-task01): return true when the box holds no value
        throw new UnsupportedOperationException("TODO(Day13-task01): isEmpty");
    }

    public T get() {
        // TODO(Day13-task01): return the value; throw NoSuchElementException when the box is empty
        throw new UnsupportedOperationException("TODO(Day13-task01): get");
    }

    public T orElse(T fallback) {
        // TODO(Day13-task01): return the value, or fallback when the box is empty
        throw new UnsupportedOperationException("TODO(Day13-task01): orElse");
    }

    public <R> Box<R> map(Function<? super T, ? extends R> fn) {
        // TODO(Day13-task01): apply fn to the value and wrap the result; empty stays empty; a null result gives an empty box; never call fn on an empty box
        throw new UnsupportedOperationException("TODO(Day13-task01): map");
    }

    @Override
    public boolean equals(Object o) {
        // TODO(Day13-task01): two boxes are equal when both are empty or hold equal values; use pattern matching or getClass
        throw new UnsupportedOperationException("TODO(Day13-task01): equals");
    }

    @Override
    public int hashCode() {
        // TODO(Day13-task01): consistent with equals (Objects.hashCode(value))
        throw new UnsupportedOperationException("TODO(Day13-task01): hashCode");
    }

    @Override
    public String toString() {
        // TODO(Day13-task01): return 'Box[value]' for a full box and 'Box.empty' for an empty one
        throw new UnsupportedOperationException("TODO(Day13-task01): toString");
    }
}
