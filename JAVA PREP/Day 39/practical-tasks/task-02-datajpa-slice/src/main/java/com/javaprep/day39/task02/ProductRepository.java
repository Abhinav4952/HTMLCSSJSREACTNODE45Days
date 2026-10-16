package com.javaprep.day39.task02;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * TODO(Day39-task02): replace every `default` method below with an abstract Spring Data method:
 *  - findByCategoryOrderByPriceAsc(String)   derived query
 *  - existsBySku(String)                     derived existence query
 *  - findInPriceRange(BigDecimal min, BigDecimal max) with @Query ("... where p.price between :min and :max order by p.price") and @Param
 *  - countByCategory(String)                 derived count query
 */
public interface ProductRepository extends JpaRepository<Product, Long> {

    default List<Product> findByCategoryOrderByPriceAsc(String category) {
        throw new UnsupportedOperationException("TODO(Day39-task02): derived query");
    }

    default boolean existsBySku(String sku) {
        throw new UnsupportedOperationException("TODO(Day39-task02): derived exists query");
    }

    default List<Product> findInPriceRange(BigDecimal min, BigDecimal max) {
        throw new UnsupportedOperationException("TODO(Day39-task02): @Query between");
    }

    default long countByCategory(String category) {
        throw new UnsupportedOperationException("TODO(Day39-task02): derived count query");
    }
}
