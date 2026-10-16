package com.javaprep.day34.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.jdbc.core.JdbcTemplate;

@DataJpaTest
class OneToManyTest {

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

    private Customer saved() {
        Customer c = new Customer("Ann");
        c.addOrder(new PurchaseOrder("A-1"));
        c.addOrder(new PurchaseOrder("A-2"));
        return em.persistAndFlush(c);
    }

    @Test
    void helpersKeepBothSidesInSync() {
        Customer c = new Customer("Ann");
        PurchaseOrder o = new PurchaseOrder("X");
        c.addOrder(o);
        assertThat(c.getOrders()).containsExactly(o);
        assertThat(o.getCustomer()).isSameAs(c);
        c.removeOrder(o);
        assertThat(c.getOrders()).isEmpty();
        assertThat(o.getCustomer()).isNull();
    }

    @Test
    void persistCascadesToOrders() {
        saved();
        assertThat(count("purchase_orders")).isEqualTo(2);
    }

    @Test
    void foreignKeyIsOnTheManySide() {
        Customer c = saved();
        Integer n = jdbc.queryForObject("select count(*) from purchase_orders where customer_id = ?", Integer.class, c.getId());
        assertThat(n).isEqualTo(2);
    }

    @Test
    void noJoinTableBecauseOfMappedBy() {
        saved();
        Integer n = jdbc.queryForObject("select count(*) from information_schema.tables where table_name like 'customers_%'", Integer.class);
        assertThat(n).isZero();
    }

    @Test
    void orphanRemovalDeletesRemovedOrder() {
        Customer c = saved();
        c.removeOrder(c.getOrders().get(0));
        em.flush();
        assertThat(count("purchase_orders")).isEqualTo(1);
    }

    @Test
    void removingCustomerRemovesOrders() {
        Customer c = saved();
        em.remove(c);
        em.flush();
        assertThat(count("purchase_orders")).isZero();
    }

    @Test
    void manyToOneIsLazy() {
        saved();
        em.clear();
        PurchaseOrder o = em.getEntityManager().createQuery("select o from PurchaseOrder o where o.reference = 'A-1'", PurchaseOrder.class).getSingleResult();
        assertThat(loaded(o, "customer")).isFalse();
    }
}
