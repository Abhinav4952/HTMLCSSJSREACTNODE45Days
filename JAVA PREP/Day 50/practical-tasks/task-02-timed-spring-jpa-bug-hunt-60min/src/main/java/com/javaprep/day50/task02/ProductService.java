package com.javaprep.day50.task02;

import java.util.List;
import java.util.NoSuchElementException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * TIME BOX: 60 minutes. This service was handed over with several defects (BUG-1..BUG-3) plus one unfinished method.
 * Read the Javadoc SPEC of each method, run the tests, find the root cause, fix it.
 */
@Service
public class ProductService {

    private final ProductRepository repository;

    public ProductService(ProductRepository repository) {
        this.repository = repository;
    }

    /** SPEC: products whose stock is STRICTLY below the threshold. */
    @Transactional(readOnly = true)
    public List<Product> lowStock(int threshold) {
        // TODO(Day50-task02): BUG-1 - something about this comparison does not match the spec
        return repository.findAll().stream().filter(p -> p.getStock() <= threshold).toList();
    }

    /**
     * SPEC: price after a percentage discount using integer math rounded down: priceCents * (100 - percentOff) / 100.
     * percentOff outside 0..100 -> IllegalArgumentException.
     */
    public long discountedPriceCents(long priceCents, int percentOff) {
        // TODO(Day50-task02): BUG-2 - integer division strikes again; also validate the range
        return priceCents * (1 - percentOff / 100);
    }

    /** SPEC: SKUs are stored upper-case; lookups ignore case and surrounding whitespace; null -> false. */
    @Transactional(readOnly = true)
    public boolean skuExists(String sku) {
        // TODO(Day50-task02): BUG-3 - lookup does not normalise the input
        return repository.findBySku(sku).isPresent();
    }

    /**
     * SPEC: reduce the stock of the (normalised, see skuExists) SKU by qty and return the saved product.
     * qty &lt;= 0 -> IllegalArgumentException; unknown SKU -> NoSuchElementException; qty greater than stock ->
     * IllegalStateException and the stock stays unchanged. Must be transactional.
     */
    @Transactional
    public Product reserve(String sku, int qty) {
        // TODO(Day50-task02): implement reserve according to the SPEC
        throw new UnsupportedOperationException("TODO(Day50-task02): implement reserve");
    }
}
