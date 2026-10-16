package com.javaprep.day32.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.jdbc.core.JdbcTemplate;

@DataJpaTest
class SchemaValidationTest {

    @Autowired
    ProductRepository repository;
    @Autowired
    JdbcTemplate jdbc;

    @Test
    void contextStartsWithValidateAgainstYourSchema() {
        assertThat(repository.count()).isZero();
    }

    @Test
    void roundTripsAProduct() {
        Product p = repository.saveAndFlush(new Product("Pen", "PEN-1", new BigDecimal("1.50")));
        assertThat(repository.findById(p.getId()).orElseThrow().getPrice()).isEqualByComparingTo("1.50");
        assertThat(p.isActive()).isTrue();
    }

    @Test
    void skuMustBeUnique() {
        repository.saveAndFlush(new Product("Pen", "DUP", BigDecimal.ONE));
        assertThatThrownBy(() -> repository.saveAndFlush(new Product("Pencil", "DUP", BigDecimal.TEN)))
                .isInstanceOf(DataIntegrityViolationException.class);
    }

    @Test
    void databaseRejectsNullName() {
        assertThatThrownBy(() -> jdbc.update("insert into products(name, sku, price, active, created_at) values (null, 'S', 1, true, now())"))
                .isInstanceOf(DataIntegrityViolationException.class);
    }

    @Test
    void tableWasCreatedBySchemaSqlNotHibernate() {
        Integer n = jdbc.queryForObject("select count(*) from information_schema.tables where table_name = 'products'", Integer.class);
        assertThat(n).isEqualTo(1);
    }
}
