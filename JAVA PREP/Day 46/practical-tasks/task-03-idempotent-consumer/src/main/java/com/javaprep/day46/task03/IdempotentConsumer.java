package com.javaprep.day46.task03;

import java.sql.Connection;

/** Makes at-least-once delivery behave like exactly-once for side effects, using a processed-events table. */
public class IdempotentConsumer {

    private final Connection connection;

    public IdempotentConsumer(Connection connection) {
        this.connection = connection;
    }

    /**
     * In ONE transaction: insert eventId into processed_events, then run {@code sideEffect}, then commit.
     * <ul>
     *   <li>eventId already stored (primary-key violation) -> return false, sideEffect NOT run</li>
     *   <li>sideEffect throws -> roll back (event is NOT marked processed), rethrow the exception</li>
     *   <li>otherwise return true</li>
     *   <li>auto-commit must be restored to its previous value afterwards; SQLExceptions -> IllegalStateException</li>
     * </ul>
     */
    public boolean processOnce(String eventId, Runnable sideEffect) {
        // TODO(Day46-task03): setAutoCommit(false), insert, detect SQLIntegrityConstraintViolationException, run, commit / rollback
        throw new UnsupportedOperationException("TODO(Day46-task03): implement processOnce");
    }
}
