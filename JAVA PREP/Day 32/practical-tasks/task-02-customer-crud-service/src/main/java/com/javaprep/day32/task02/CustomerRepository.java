package com.javaprep.day32.task02;

import org.springframework.data.jpa.repository.JpaRepository;

/** PROVIDED: Spring Data generates the implementation at startup. */
public interface CustomerRepository extends JpaRepository<Customer, Long> {
}
