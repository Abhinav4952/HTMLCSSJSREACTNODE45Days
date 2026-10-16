package com.javaprep.day08.task01;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class PointTest {

    @Test
    @DisplayName("no-arg constructor creates the origin")
    void origin() {
        Point p = new Point();
        assertThat(p.x()).isZero();
        assertThat(p.y()).isZero();
    }

    @Test
    @DisplayName("two-arg constructor stores x and y (including negatives)")
    void storesCoordinates() {
        Point p = new Point(3, -4);
        assertThat(p.x()).isEqualTo(3);
        assertThat(p.y()).isEqualTo(-4);
    }

    @Test
    @DisplayName("distanceSquaredTo")
    void distanceSquared() {
        assertThat(new Point().distanceSquaredTo(new Point(3, 4))).isEqualTo(25);
        assertThat(new Point(1, 1).distanceSquaredTo(new Point(1, 1))).isZero();
        assertThat(new Point(-1, -1).distanceSquaredTo(new Point(2, 3))).isEqualTo(25);
    }

    @Test
    @DisplayName("distanceSquaredTo(null) -> NullPointerException")
    void nullOther() {
        assertThatThrownBy(() -> new Point().distanceSquaredTo(null)).isInstanceOf(NullPointerException.class);
    }
}
