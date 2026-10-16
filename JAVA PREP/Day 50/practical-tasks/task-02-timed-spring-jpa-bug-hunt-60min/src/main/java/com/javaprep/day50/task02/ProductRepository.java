package com.javaprep.day50.task02;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

/** PROVIDED. */
public interface ProductRepository extends JpaRepository<Product, Long> {

    Optional<Product> findBySku(String sku);
}
