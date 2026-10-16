package com.javaprep.day23.task04;

import java.util.Optional;

/** Provided collaborator: persistence of customers. */
public interface CustomerRepository {

    Optional<Customer> findById(String id);

    void save(Customer customer);
}
