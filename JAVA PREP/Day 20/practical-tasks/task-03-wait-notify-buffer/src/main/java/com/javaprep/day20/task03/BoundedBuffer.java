package com.javaprep.day20.task03;

import java.util.Objects;

/** Bounded FIFO buffer using intrinsic locks and wait/notifyAll. */
public final class BoundedBuffer<T> {

    private final Object[] items;
    private int head;
    private int tail;
    private int count;

    public BoundedBuffer(int capacity) {
        // TODO(Day20-task03): IllegalArgumentException when capacity <= 0; allocate the circular array
        throw new UnsupportedOperationException("TODO(Day20-task03): constructor");
    }

    public synchronized void put(T item) throws InterruptedException {
        // TODO(Day20-task03): NullPointerException for null; while the buffer is full wait(); then store at tail (circular), count++ and notifyAll()
        throw new UnsupportedOperationException("TODO(Day20-task03): put");
    }

    @SuppressWarnings("unchecked")
    public synchronized T take() throws InterruptedException {
        // TODO(Day20-task03): while the buffer is empty wait(); then remove from head (circular, clear the slot), count-- and notifyAll()
        throw new UnsupportedOperationException("TODO(Day20-task03): take");
    }

    public synchronized int size() {
        return count;
    }

    public int capacity() {
        return items.length;
    }
}
