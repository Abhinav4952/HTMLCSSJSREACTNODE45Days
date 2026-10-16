package com.javaprep.day34.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.jdbc.core.JdbcTemplate;

@DataJpaTest
class OneToOneTest {

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

    private Account saved() {
        Account a = new Account("a@x.io");
        a.setProfile(new Profile("hi"));
        return em.persistAndFlush(a);
    }

    @Test
    void savingAccountCascadesToProfile() {
        saved();
        assertThat(count("profiles")).isEqualTo(1);
    }

    @Test
    void foreignKeyLivesOnAccounts() {
        Account a = saved();
        Long fk = jdbc.queryForObject("select profile_id from accounts where id = ?", Long.class, a.getId());
        assertThat(fk).isEqualTo(a.getProfile().getId());
    }

    @Test
    void profileIsLazy() {
        Account a = saved();
        em.clear();
        Account acc = em.find(Account.class, a.getId());
        assertThat(acc.getProfile()).isNotNull();
        assertThat(loaded(acc, "profile")).isFalse();
        assertThat(acc.getProfile().getBio()).isEqualTo("hi");
    }

    @Test
    void replacingProfileDeletesTheOrphan() {
        Account a = saved();
        a.setProfile(new Profile("new"));
        em.flush();
        assertThat(count("profiles")).isEqualTo(1);
        assertThat(jdbc.queryForObject("select bio from profiles", String.class)).isEqualTo("new");
    }

    @Test
    void removingAccountRemovesProfile() {
        Account a = saved();
        em.remove(a);
        em.flush();
        assertThat(count("accounts")).isZero();
        assertThat(count("profiles")).isZero();
    }
}
