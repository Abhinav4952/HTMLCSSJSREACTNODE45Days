package com.javaprep.day50.task03;

import java.util.function.Supplier;

/** Lazily computes a value exactly ONCE, even when many threads call {@link #get()} simultaneously. */
public class LazyHolder<T> {

    private final Supplier<T> supplier;

    public LazyHolder(Supplier<T> supplier) {
        this.supplier = supplier;
    }

    /** All callers receive the same instance; the supplier runs at most once (supplier never returns null). */
    public T get() {
        // TODO(Day50-task03): thread-safe lazy initialisation (double-checked locking with volatile, holder, or synchronized)
        throw new UnsupportedOperationException("TODO(Day50-task03): implement get");
    }
}
