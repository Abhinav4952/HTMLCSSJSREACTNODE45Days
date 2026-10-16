package com.javaprep.day48.task02;

import java.util.Set;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class NoteSearchService {

    public static final int MAX_SIZE = 50;
    private static final Set<String> SORTABLE = Set.of("createdAt", "title");

    private final NoteRepository notes;

    public NoteSearchService(NoteRepository notes) {
        this.notes = notes;
    }

    /**
     * Owner-scoped, paged, sorted title search.
     * <ul>
     *   <li>page &lt; 0 or size &lt; 1 -> IllegalArgumentException; size is clamped to MAX_SIZE</li>
     *   <li>sortBy must be in {createdAt, title} (whitelist!) else IllegalArgumentException; direction "asc"/"desc" (any case), else IAE</li>
     *   <li>null query is treated as ""; returned PageResponse reports the EFFECTIVE (clamped) size</li>
     * </ul>
     */
    @Transactional(readOnly = true)
    public PageResponse<Note> search(Long ownerId, String query, int page, int size, String sortBy, String direction) {
        // TODO(Day48-task02): validate, build PageRequest.of(page, size, Sort.by(dir, sortBy)), query the repository, map the Page
        throw new UnsupportedOperationException("TODO(Day48-task02): implement search");
    }
}
