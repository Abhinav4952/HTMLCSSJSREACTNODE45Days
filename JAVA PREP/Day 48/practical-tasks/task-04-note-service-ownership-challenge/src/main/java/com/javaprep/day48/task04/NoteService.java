package com.javaprep.day48.task04;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class NoteService {

    private final NoteRepository notes;

    public NoteService(NoteRepository notes) {
        this.notes = notes;
    }

    /** Owner or admin may read; everyone else (and missing ids) get NotFoundException (policy: hide existence). */
    @Transactional(readOnly = true)
    public Note get(long callerId, boolean admin, long noteId) {
        // TODO(Day48-task04): load the note and apply the ownership rule
        throw new UnsupportedOperationException("TODO(Day48-task04): implement get");
    }

    /** Same access rule as get; blank title -> IllegalArgumentException (checked BEFORE touching the database). Persists the change. */
    @Transactional
    public Note rename(long callerId, boolean admin, long noteId, String newTitle) {
        // TODO(Day48-task04): validate, authorize, change the title, save
        throw new UnsupportedOperationException("TODO(Day48-task04): implement rename");
    }

    /** Owner or admin may delete; others get NotFoundException and the row survives. */
    @Transactional
    public void delete(long callerId, boolean admin, long noteId) {
        // TODO(Day48-task04): authorize and delete
        throw new UnsupportedOperationException("TODO(Day48-task04): implement delete");
    }
}
