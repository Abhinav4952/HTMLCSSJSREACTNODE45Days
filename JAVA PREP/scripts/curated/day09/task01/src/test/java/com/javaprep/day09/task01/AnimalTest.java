package com.javaprep.day09.task01;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

class AnimalTest {

    @Test
    @DisplayName("generic Animal speaks '...'")
    void animal() {
        assertThat(new Animal().speak()).isEqualTo("...");
    }

    @Test
    @DisplayName("Dog overrides speak to 'woof'")
    void dog() {
        assertThat(new Dog().speak()).isEqualTo("woof");
    }

    @Test
    @DisplayName("dynamic dispatch: Animal reference to a Dog still says 'woof'")
    void polymorphism() {
        Animal a = new Dog();
        assertThat(a.speak()).isEqualTo("woof");
        List<Animal> zoo = List.of(new Animal(), new Dog());
        assertThat(zoo).extracting(Animal::speak).containsExactly("...", "woof");
    }
}
