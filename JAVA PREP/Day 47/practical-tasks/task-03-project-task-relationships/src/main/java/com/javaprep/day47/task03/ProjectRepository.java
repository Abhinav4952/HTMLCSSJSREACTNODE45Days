package com.javaprep.day47.task03;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

/** PROVIDED. */
public interface ProjectRepository extends JpaRepository<Project, Long> {

    List<Project> findByOwnerId(Long ownerId);
}
