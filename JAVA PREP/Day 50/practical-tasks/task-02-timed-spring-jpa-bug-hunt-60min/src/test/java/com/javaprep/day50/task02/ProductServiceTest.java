package com.javaprep.day50.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.NoSuchElementException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(ProductService.class)
class ProductServiceTest {

    @Autowired
    private ProductRepository repo;
    @Autowired
    private ProductService service;

    @BeforeEach
    void seed() {
        repo.save(new Product("AB-1", 3, 1000));
        repo.save(new Product("AB-2", 5, 2000));
        repo.save(new Product("AB-3", 10, 3000));
    }

    @Test
    void lowStockIsStrictlyBelowThreshold() {
        assertThat(service.lowStock(5)).extracting(Product::getSku).containsExactly("AB-1");
    }

    @Test
    void discountUsesIntegerPercentMath() {
        assertThat(service.discountedPriceCents(1000, 10)).isEqualTo(900);
        assertThat(service.discountedPriceCents(999, 10)).isEqualTo(899);
        assertThat(service.discountedPriceCents(1000, 0)).isEqualTo(1000);
        assertThat(service.discountedPriceCents(1000, 100)).isZero();
    }

    @Test
    void discountRejectsOutOfRangePercent() {
        assertThatThrownBy(() -> service.discountedPriceCents(1000, 101)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.discountedPriceCents(1000, -1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void skuLookupIgnoresCaseAndWhitespace() {
        assertThat(service.skuExists(" ab-1 ")).isTrue();
        assertThat(service.skuExists("AB-1")).isTrue();
        assertThat(service.skuExists("zz-9")).isFalse();
        assertThat(service.skuExists(null)).isFalse();
    }

    @Test
    void reserveReducesStock() {
        Product p = service.reserve("ab-2", 2);
        assertThat(p.getStock()).isEqualTo(3);
        assertThat(repo.findBySku("AB-2").orElseThrow().getStock()).isEqualTo(3);
    }

    @Test
    void reserveRejectsBadRequestsWithoutChangingStock() {
        assertThatThrownBy(() -> service.reserve("AB-1", 4)).isInstanceOf(IllegalStateException.class);
        assertThat(repo.findBySku("AB-1").orElseThrow().getStock()).isEqualTo(3);
        assertThatThrownBy(() -> service.reserve("AB-1", 0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.reserve("NOPE", 1)).isInstanceOf(NoSuchElementException.class);
    }

    @Test
    void reservingExactlyTheStockIsAllowed() {
        assertThat(service.reserve("AB-1", 3).getStock()).isZero();
    }
}
