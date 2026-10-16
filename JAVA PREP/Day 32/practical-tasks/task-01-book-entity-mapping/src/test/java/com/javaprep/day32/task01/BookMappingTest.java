package com.javaprep.day32.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.jdbc.core.JdbcTemplate;

@DataJpaTest
class BookMappingTest {

    @Autowired
    TestEntityManager em;
    @Autowired
    JdbcTemplate jdbc;

    @Test
    void persistGeneratesId() {
        Book b = em.persistFlushFind(new Book("Dune", "978-0441", Genre.SCIFI));
        assertThat(b.getId()).isNotNull().isPositive();
        assertThat(b.getTitle()).isEqualTo("Dune");
    }

    @Test
    void usesTableBooksAndStoresEnumAsText() {
        Book b = em.persistAndFlush(new Book("Dune", "978-0441", Genre.SCIFI));
        String stored = jdbc.queryForObject("select genre from books where id = ?", String.class, b.getId());
        assertThat(stored).isEqualTo("SCIFI");
    }

    @Test
    void titleIsRequired() {
        assertThatThrownBy(() -> em.persistAndFlush(new Book(null, "1", Genre.TECH))).isInstanceOf(RuntimeException.class);
    }

    @Test
    void isbnMustBeUnique() {
        em.persistAndFlush(new Book("A", "same", Genre.TECH));
        assertThatThrownBy(() -> em.persistAndFlush(new Book("B", "same", Genre.TECH))).isInstanceOf(RuntimeException.class);
    }

    @Test
    void titleLongerThan120IsRejected() {
        assertThatThrownBy(() -> em.persistAndFlush(new Book("x".repeat(121), "long", Genre.TECH))).isInstanceOf(RuntimeException.class);
    }

    @Test
    void titleOf120IsAccepted() {
        assertThat(em.persistAndFlush(new Book("x".repeat(120), "ok", Genre.TECH)).getId()).isNotNull();
    }
}
