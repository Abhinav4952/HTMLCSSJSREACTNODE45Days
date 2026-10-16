package com.javaprep.day48.task02;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

/** PROVIDED. */
public interface NoteRepository extends JpaRepository<Note, Long> {

    Page<Note> findByOwnerIdAndTitleContainingIgnoreCase(Long ownerId, String titlePart, Pageable pageable);
}
