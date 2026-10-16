package com.javaprep.day10.task01;

public class Circle extends Shape {

    private final double radius;

    // TODO(Day10-task01): reject radius < 0 with IllegalArgumentException
    public Circle(double radius) {
        this.radius = radius;
    }

    // TODO(Day10-task01): return Math.PI * r * r
    @Override
    public double area() {
        throw new UnsupportedOperationException("TODO(Day10-task01): implement Circle.area");
    }
}
