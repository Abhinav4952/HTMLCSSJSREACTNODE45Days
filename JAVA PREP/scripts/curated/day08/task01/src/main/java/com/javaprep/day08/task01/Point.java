package com.javaprep.day08.task01;

/**
 * Immutable-style 2D integer point.
 *
 * <p>Constructors are intentionally left as TODOs without {@code throw}, so the class can be instantiated; the
 * accessors and {@link #distanceSquaredTo(Point)} are the stubbed API that tests exercise.
 */
public class Point {

    private int x;
    private int y;

    // TODO(Day08-task01): no-arg constructor -- origin (0,0); delegate with this(0, 0)
    public Point() {
    }

    // TODO(Day08-task01): store x and y (make the fields final once done)
    public Point(int x, int y) {
    }

    // TODO(Day08-task01): return x
    public int x() {
        throw new UnsupportedOperationException("TODO(Day08-task01): implement x");
    }

    // TODO(Day08-task01): return y
    public int y() {
        throw new UnsupportedOperationException("TODO(Day08-task01): implement y");
    }

    // TODO(Day08-task01): return (dx*dx + dy*dy) between this and other; null throws NullPointerException
    public int distanceSquaredTo(Point other) {
        throw new UnsupportedOperationException("TODO(Day08-task01): implement distanceSquaredTo");
    }
}
