package com.javaprep.day10.task01;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

class ShapeTest {

    @Test
    @DisplayName("circle area = pi r^2")
    void circle() {
        assertThat(new Circle(1).area()).isCloseTo(Math.PI, within(1e-9));
        assertThat(new Circle(2).area()).isCloseTo(4 * Math.PI, within(1e-9));
        assertThat(new Circle(0).area()).isZero();
    }

    @Test
    @DisplayName("rectangle area = w * h")
    void rectangle() {
        assertThat(new Rectangle(3, 4).area()).isEqualTo(12.0);
        assertThat(new Rectangle(0, 4).area()).isZero();
    }

    @Test
    @DisplayName("negative dimensions -> IllegalArgumentException")
    void invalid() {
        assertThatThrownBy(() -> new Circle(-1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new Rectangle(-1, 2)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new Rectangle(2, -1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    @DisplayName("polymorphic total area through Shape")
    void polymorphic() {
        List<Shape> shapes = List.of(new Rectangle(2, 3), new Circle(1));
        double total = shapes.stream().mapToDouble(Shape::area).sum();
        assertThat(total).isCloseTo(6 + Math.PI, within(1e-9));
    }
}
