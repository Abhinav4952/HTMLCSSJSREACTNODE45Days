package com.javaprep.day35.task03;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class StockService {

    private final ProductRepository repository;

    public StockService(ProductRepository repository) {
        this.repository = repository;
    }

    @Transactional
    public Product create(String name, int stock) {
        // TODO(Day35-task03): save a new product and return it
        throw new UnsupportedOperationException("TODO(Day35-task03): save a new product and return it");
    }

    /** Changes stock by delta inside one transaction. Result below zero -> IllegalStateException("Stock cannot be negative"). */
    @Transactional
    public Product adjust(long id, int delta) {
        // TODO(Day35-task03): load, apply delta with the rule, flush and return
        throw new UnsupportedOperationException("TODO(Day35-task03): load, apply delta with the rule, flush and return");
    }

    /** Saves a possibly stale, detached copy (merge). A stale version must surface as an optimistic locking failure. */
    @Transactional
    public Product saveDetached(Product detached) {
        // TODO(Day35-task03): merge via repository.saveAndFlush
        throw new UnsupportedOperationException("TODO(Day35-task03): merge via repository.saveAndFlush");
    }

    @Transactional(readOnly = true)
    public Product get(long id) {
        // TODO(Day35-task03): load or throw
        throw new UnsupportedOperationException("TODO(Day35-task03): load or throw");
    }
}
