package com.javaprep.day48.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.LocalDateTime;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(NoteSearchService.class)
class NoteSearchServiceTest {

    @Autowired
    private NoteRepository repo;
    @Autowired
    private NoteSearchService service;

    @BeforeEach
    void seed() {
        LocalDateTime base = LocalDateTime.of(2025, 1, 1, 0, 0);
        for (int i = 1; i <= 12; i++) {
            repo.save(new Note(1L, String.format("Note %02d", i), base.plusMinutes(i)));
        }
        for (int i = 1; i <= 3; i++) {
            repo.save(new Note(2L, "Other " + i, base.plusMinutes(i)));
        }
    }

    @Test
    void pagesAndTotalsAreReported() {
        PageResponse<Note> p = service.search(1L, "note", 0, 5, "title", "asc");
        assertThat(p.content()).hasSize(5);
        assertThat(p.totalElements()).isEqualTo(12);
        assertThat(p.totalPages()).isEqualTo(3);
        assertThat(p.content().get(0).getTitle()).isEqualTo("Note 01");
        assertThat(service.search(1L, "note", 2, 5, "title", "asc").content()).hasSize(2);
    }

    @Test
    void sortsByCreatedAtDescending() {
        PageResponse<Note> p = service.search(1L, "", 0, 3, "createdAt", "DESC");
        assertThat(p.content()).extracting(Note::getTitle).containsExactly("Note 12", "Note 11", "Note 10");
    }

    @Test
    void searchIsScopedToTheOwner() {
        assertThat(service.search(2L, null, 0, 10, "title", "asc").totalElements()).isEqualTo(3);
        assertThat(service.search(2L, "note", 0, 10, "title", "asc").totalElements()).isZero();
    }

    @Test
    void sizeIsClamped() {
        assertThat(service.search(1L, "", 0, 1000, "title", "asc").size()).isEqualTo(NoteSearchService.MAX_SIZE);
    }

    @Test
    void invalidArgumentsAreRejected() {
        assertThatThrownBy(() -> service.search(1L, "", -1, 5, "title", "asc")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.search(1L, "", 0, 0, "title", "asc")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.search(1L, "", 0, 5, "ownerId", "asc")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.search(1L, "", 0, 5, "title", "sideways")).isInstanceOf(IllegalArgumentException.class);
    }
}
