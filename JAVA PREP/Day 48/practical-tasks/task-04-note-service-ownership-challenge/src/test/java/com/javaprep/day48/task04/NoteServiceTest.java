package com.javaprep.day48.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.LocalDateTime;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(NoteService.class)
class NoteServiceTest {

    @Autowired
    private NoteRepository repo;
    @Autowired
    private NoteService service;

    private long noteId;

    @BeforeEach
    void seed() {
        noteId = repo.save(new Note(1L, "private plans", LocalDateTime.of(2025, 1, 1, 0, 0))).getId();
    }

    @Test
    void ownerCanReadRenameAndDelete() {
        assertThat(service.get(1L, false, noteId).getTitle()).isEqualTo("private plans");
        assertThat(service.rename(1L, false, noteId, "public plans").getTitle()).isEqualTo("public plans");
        assertThat(repo.findById(noteId).orElseThrow().getTitle()).isEqualTo("public plans");
        service.delete(1L, false, noteId);
        assertThat(repo.existsById(noteId)).isFalse();
    }

    @Test
    void strangerSeesNotFoundForEverything() {
        assertThatThrownBy(() -> service.get(2L, false, noteId)).isInstanceOf(NotFoundException.class);
        assertThatThrownBy(() -> service.rename(2L, false, noteId, "hacked")).isInstanceOf(NotFoundException.class);
        assertThatThrownBy(() -> service.delete(2L, false, noteId)).isInstanceOf(NotFoundException.class);
        assertThat(repo.findById(noteId).orElseThrow().getTitle()).isEqualTo("private plans");
    }

    @Test
    void adminCanAccessAnyNote() {
        assertThat(service.get(99L, true, noteId).getId()).isEqualTo(noteId);
        service.delete(99L, true, noteId);
        assertThat(repo.existsById(noteId)).isFalse();
    }

    @Test
    void unknownIdIsNotFound() {
        assertThatThrownBy(() -> service.get(1L, true, 123456L)).isInstanceOf(NotFoundException.class);
    }

    @Test
    void blankTitleIsRejectedBeforeAnyLookup() {
        assertThatThrownBy(() -> service.rename(2L, false, noteId, "  ")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.rename(1L, false, noteId, null)).isInstanceOf(IllegalArgumentException.class);
    }
}
