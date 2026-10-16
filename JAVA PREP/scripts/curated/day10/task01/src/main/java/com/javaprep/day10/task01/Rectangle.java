package com.javaprep.day10.task01;

public class Rectangle extends Shape {

    private final double width;
    private final double height;

    // TODO(Day10-task01): reject negative width or height with IllegalArgumentException
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    // TODO(Day10-task01): return width * height
    @Override
    public double area() {
        throw new UnsupportedOperationException("TODO(Day10-task01): implement Rectangle.area");
    }
}
