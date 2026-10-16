package com.javaprep.day34.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.jdbc.core.JdbcTemplate;

@DataJpaTest
class ManyToManyTest {

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

    private Course course(String code) {
        return em.persist(new Course(code, "T-" + code));
    }

    @Test
    void enrollWritesJoinTableRows() {
        Course java = course("JAVA");
        Course sql = course("SQL");
        Student ann = new Student("Ann");
        ann.enroll(java);
        ann.enroll(sql);
        em.persistAndFlush(ann);
        assertThat(count("enrollments")).isEqualTo(2);
        assertThat(java.getStudents()).containsExactly(ann);
    }

    @Test
    void dropRemovesOnlyTheLink() {
        Course java = course("JAVA");
        Student ann = new Student("Ann");
        ann.enroll(java);
        em.persistAndFlush(ann);
        ann.drop(java);
        em.flush();
        assertThat(count("enrollments")).isZero();
        assertThat(count("courses")).isEqualTo(1);
        assertThat(java.getStudents()).isEmpty();
    }

    @Test
    void deletingStudentKeepsCoursesButClearsLinks() {
        Course java = course("JAVA");
        Student ann = new Student("Ann");
        ann.enroll(java);
        em.persistAndFlush(ann);
        em.remove(ann);
        em.flush();
        assertThat(count("enrollments")).isZero();
        assertThat(count("courses")).isEqualTo(1);
    }

    @Test
    void noCascadeFromStudentToCourse() {
        Student ann = new Student("Ann");
        ann.enroll(new Course("NEW", "not persisted"));
        assertThatThrownBy(() -> em.persistAndFlush(ann)).isInstanceOf(RuntimeException.class);
    }

    @Test
    void courseEqualityUsesBusinessKey() {
        Course a = new Course("J1", "x");
        Course b = new Course("J1", "y");
        assertThat(a).isEqualTo(b).hasSameHashCodeAs(b);
        assertThat(a).isNotEqualTo(new Course("J2", "x")).isNotEqualTo(null).isNotEqualTo("J1");
        assertThat(new java.util.HashSet<>(java.util.List.of(a, b))).hasSize(1);
        assertThat(new Course(null, "x")).isNotEqualTo(new Course(null, "x"));
    }
}
