package com.javaprep.day34.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.jdbc.core.JdbcTemplate;

@DataJpaTest
class LibraryModelTest {

    @Autowired
    TestEntityManager em;
    @Autowired
    JdbcTemplate jdbc;

    private int count(String table) {
        Integer n = jdbc.queryForObject("select count(*) from " + table, Integer.class);
        return n == null ? 0 : n;
    }

    private boolean loaded(Object entity, String attribute) {
        return em.getEntityManager().getEntityManagerFactory().getPersistenceUnitUtil().isLoaded(entity, attribute);
    }

    private Author saved() {
        Tag java = em.persist(new Tag("java"));
        Tag spring = em.persist(new Tag("spring"));
        Author a = new Author("Ann");
        Book b1 = new Book("JPA", 300);
        Book b2 = new Book("Boot", 200);
        b1.tag(java);
        b1.tag(spring);
        b2.tag(spring);
        a.addBook(b1);
        a.addBook(b2);
        return em.persistAndFlush(a);
    }

    @Test
    void cascadesFromAuthorThroughBooksToDetails() {
        saved();
        assertThat(count("books")).isEqualTo(2);
        assertThat(count("book_details")).isEqualTo(2);
        assertThat(count("book_tags")).isEqualTo(3);
        assertThat(count("tags")).isEqualTo(2);
    }

    @Test
    void associationsAreLazy() {
        Author a = saved();
        em.clear();
        Author found = em.find(Author.class, a.getId());
        assertThat(loaded(found, "books")).isFalse();
        Long bookId = found.getBooks().get(0).getId();
        em.clear();
        Book fresh = em.find(Book.class, bookId);
        assertThat(loaded(fresh, "author")).isFalse();
        assertThat(loaded(fresh, "detail")).isFalse();
        assertThat(loaded(fresh, "tags")).isFalse();
    }

    @Test
    void removingBookRemovesItsDetailButNotTags() {
        Author a = saved();
        a.removeBook(a.getBooks().get(0));
        em.flush();
        assertThat(count("books")).isEqualTo(1);
        assertThat(count("book_details")).isEqualTo(1);
        assertThat(count("tags")).isEqualTo(2);
        assertThat(count("book_tags")).isEqualTo(1);
    }

    @Test
    void removingAuthorRemovesBooksAndDetailsButKeepsTags() {
        Author a = saved();
        em.remove(a);
        em.flush();
        assertThat(count("books")).isZero();
        assertThat(count("book_details")).isZero();
        assertThat(count("book_tags")).isZero();
        assertThat(count("tags")).isEqualTo(2);
    }

    @Test
    void tagKnowsItsBooks() {
        Author a = saved();
        Tag spring = a.getBooks().get(0).getTags().stream().filter(t -> t.getName().equals("spring")).findFirst().orElseThrow();
        assertThat(spring.getBooks()).hasSize(2);
    }
}
