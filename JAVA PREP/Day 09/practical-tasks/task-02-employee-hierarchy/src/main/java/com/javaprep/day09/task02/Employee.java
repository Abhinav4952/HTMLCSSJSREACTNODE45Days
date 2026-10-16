package com.javaprep.day09.task02;

public class Employee {

    private final String name;
    private final double base;

    public Employee(String name, double base) {
        this.name = name;
        this.base = base;
    }

    public String name() {
        return name;
    }

    /** Base pay available to subclasses. */
    protected double base() {
        return base;
    }

    // TODO(Day09-task02): return the base pay
    public double pay() {
        throw new UnsupportedOperationException("TODO(Day09-task02): implement pay");
    }
}
