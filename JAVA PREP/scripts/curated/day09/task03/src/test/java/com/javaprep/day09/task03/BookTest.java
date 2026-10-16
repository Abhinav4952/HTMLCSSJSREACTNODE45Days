package com.javaprep.day09.task03;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.HashSet;
import java.util.Set;

class BookTest {

    @Test
    @DisplayName("equal when ISBN matches, regardless of title")
    void equalByIsbn() {
        Book a = new Book("978-1", "Effective Java");
        Book b = new Book("978-1", "Effective Java 3rd");
        assertThat(a.equals(b)).isTrue();
        assertThat(a.equals(new Book("978-2", "Effective Java"))).isFalse();
    }

    @Test
    @DisplayName("equals contract: reflexive, symmetric, null and foreign types")
    void contract() {
        Book a = new Book("978-1", "A");
        Book b = new Book("978-1", "B");
        assertThat(a.equals(a)).isTrue();
        assertThat(a.equals(b)).isEqualTo(b.equals(a));
        assertThat(a.equals(null)).isFalse();
        assertThat(a.equals("978-1")).isFalse();
    }

    @Test
    @DisplayName("hashCode is consistent with equals")
    void hash() {
        assertThat(new Book("978-1", "A").hashCode()).isEqualTo(new Book("978-1", "B").hashCode());
    }

    @Test
    @DisplayName("works in a HashSet")
    void hashSet() {
        Set<Book> set = new HashSet<>();
        set.add(new Book("978-1", "A"));
        set.add(new Book("978-1", "B"));
        set.add(new Book("978-2", "C"));
        assertThat(set).hasSize(2);
        assertThat(set).contains(new Book("978-2", "ignored"));
    }
}
