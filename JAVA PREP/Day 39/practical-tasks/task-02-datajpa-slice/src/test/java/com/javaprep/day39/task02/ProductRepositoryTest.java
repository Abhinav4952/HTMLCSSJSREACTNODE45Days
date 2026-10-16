package com.javaprep.day39.task02;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;

/** JPA slice: entities, repositories and an embedded database; each test rolls back automatically. */
@DataJpaTest
class ProductRepositoryTest {

    @Autowired TestEntityManager em;
    @Autowired ProductRepository repo;

    @BeforeEach
    void seed() {
        em.persist(new Product("P-1", "tools", "30.00"));
        em.persist(new Product("P-2", "tools", "10.00"));
        em.persist(new Product("P-3", "toys", "20.00"));
        em.flush();
        em.clear();
    }

    @Test
    void ordersByPriceWithinCategory() {
        assertThat(repo.findByCategoryOrderByPriceAsc("tools")).extracting(Product::getSku).containsExactly("P-2", "P-1");
    }

    @Test
    void existsBySku() {
        assertThat(repo.existsBySku("P-3")).isTrue();
        assertThat(repo.existsBySku("nope")).isFalse();
    }

    @Test
    void priceRangeIsInclusiveAndSorted() {
        assertThat(repo.findInPriceRange(new BigDecimal("10.00"), new BigDecimal("20.00"))).extracting(Product::getSku)
                .containsExactly("P-2", "P-3");
    }

    @Test
    void countsByCategory() {
        assertThat(repo.countByCategory("tools")).isEqualTo(2);
        assertThat(repo.countByCategory("none")).isZero();
    }

    @Test
    void sliceRollsBackBetweenTests() {
        assertThat(repo.count()).isEqualTo(3);
    }
}
