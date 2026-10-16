package com.javaprep.day11.task03;

public class CountingResource implements AutoCloseable {

    private int closes;

    // TODO(Day11-task03): increment the close counter
    @Override
    public void close() {
        throw new UnsupportedOperationException("TODO(Day11-task03): implement close");
    }

    // TODO(Day11-task03): return how many times close() has been called
    public int getCloseCount() {
        throw new UnsupportedOperationException("TODO(Day11-task03): implement getCloseCount");
    }
}
