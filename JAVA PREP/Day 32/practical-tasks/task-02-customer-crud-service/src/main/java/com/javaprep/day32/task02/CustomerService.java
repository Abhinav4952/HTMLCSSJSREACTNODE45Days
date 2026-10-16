package com.javaprep.day32.task02;

import java.util.List;
import java.util.NoSuchElementException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class CustomerService {

    private final CustomerRepository repository;

    public CustomerService(CustomerRepository repository) {
        this.repository = repository;
    }

    /** Persists and returns a new customer (id assigned). */
    public Customer create(String name, String email) {
        // TODO(Day32-task02): save a new Customer
        throw new UnsupportedOperationException("TODO(Day32-task02): save a new Customer");
    }

    /** Unknown id -> NoSuchElementException("Customer <id> not found"). */
    @Transactional(readOnly = true)
    public Customer get(long id) {
        // TODO(Day32-task02): findById or throw NoSuchElementException
        throw new UnsupportedOperationException("TODO(Day32-task02): findById or throw NoSuchElementException");
    }

    /** Changes the name using dirty checking: load, mutate, do NOT call save(). Unknown id -> NoSuchElementException. */
    public Customer rename(long id, String newName) {
        // TODO(Day32-task02): load the managed entity and mutate it (dirty checking flushes the UPDATE)
        throw new UnsupportedOperationException("TODO(Day32-task02): load the managed entity and mutate it (dirty checking flushes the UPDATE)");
    }

    /** Unknown id -> NoSuchElementException. */
    public void delete(long id) {
        // TODO(Day32-task02): check existence, then deleteById
        throw new UnsupportedOperationException("TODO(Day32-task02): check existence, then deleteById");
    }

    @Transactional(readOnly = true)
    public List<Customer> all() {
        // TODO(Day32-task02): return every customer
        throw new UnsupportedOperationException("TODO(Day32-task02): return every customer");
    }

    @Transactional(readOnly = true)
    public long count() {
        // TODO(Day32-task02): number of rows
        throw new UnsupportedOperationException("TODO(Day32-task02): number of rows");
    }
}
