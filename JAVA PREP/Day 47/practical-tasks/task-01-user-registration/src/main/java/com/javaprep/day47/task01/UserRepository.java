package com.javaprep.day47.task01;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

/** PROVIDED. */
public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);

    boolean existsByEmail(String email);
}
