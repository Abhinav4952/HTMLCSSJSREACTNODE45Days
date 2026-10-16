package com.javaprep.day50.task03;

import java.util.function.Supplier;

/** Thread-safe counter. 8 threads x 10 000 increments must give exactly 80 000. */
public class SafeCounter {

    private long value;

    public void increment() {
        // TODO(Day50-task03): make this thread-safe (AtomicLong, LongAdder, synchronized or a lock)
        throw new UnsupportedOperationException("TODO(Day50-task03): implement increment");
    }

    public long get() {
        // TODO(Day50-task03): return the current value consistently with increment()
        throw new UnsupportedOperationException("TODO(Day50-task03): implement get");
    }
}
