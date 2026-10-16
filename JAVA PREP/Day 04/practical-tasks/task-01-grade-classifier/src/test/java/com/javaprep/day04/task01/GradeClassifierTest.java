package com.javaprep.day04.task01;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class GradeClassifierTest {

    @Test
    @DisplayName("band boundaries")
    void boundaries() {
        assertThat(GradeClassifier.grade(100)).isEqualTo('A');
        assertThat(GradeClassifier.grade(90)).isEqualTo('A');
        assertThat(GradeClassifier.grade(89)).isEqualTo('B');
        assertThat(GradeClassifier.grade(80)).isEqualTo('B');
        assertThat(GradeClassifier.grade(79)).isEqualTo('C');
        assertThat(GradeClassifier.grade(70)).isEqualTo('C');
        assertThat(GradeClassifier.grade(69)).isEqualTo('D');
        assertThat(GradeClassifier.grade(60)).isEqualTo('D');
        assertThat(GradeClassifier.grade(59)).isEqualTo('F');
        assertThat(GradeClassifier.grade(0)).isEqualTo('F');
    }

    @Test
    @DisplayName("scores outside 0..100 -> IllegalArgumentException")
    void outOfRange() {
        assertThatThrownBy(() -> GradeClassifier.grade(-1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GradeClassifier.grade(101)).isInstanceOf(IllegalArgumentException.class);
    }
}
