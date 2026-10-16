package com.javaprep.day09.task02;

public class Manager extends Employee {

    private final double bonus;

    public Manager(String name, double base, double bonus) {
        super(name, base);
        this.bonus = bonus;
    }

    // TODO(Day09-task02): override pay() to return base + bonus
    @Override
    public double pay() {
        throw new UnsupportedOperationException("TODO(Day09-task02): implement Manager.pay");
    }
}
