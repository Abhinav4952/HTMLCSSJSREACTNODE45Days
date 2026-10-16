package com.javaprep.day27.task03;

import javax.sql.DataSource;

/** Table: accounts(id BIGINT PK, balance_cents BIGINT NOT NULL CHECK (balance_cents >= 0)). */
public class TransferService {

    private final DataSource dataSource;

    public TransferService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public long balanceOf(long accountId) {
        // TODO(Day27-task03): SELECT balance_cents; unknown account -> IllegalArgumentException
        throw new UnsupportedOperationException("TODO(Day27-task03): implement balanceOf");
    }

    /**
     * Moves money atomically: setAutoCommit(false), debit, credit, commit. On ANY failure rollback and rethrow.
     * - amount &lt;= 0 or from == to  -> IllegalArgumentException (before touching the database)
     * - source balance &lt; amount     -> IllegalStateException("insufficient funds") and nothing changes
     * - unknown source/destination   -> IllegalArgumentException and nothing changes (no half transfer!)
     * Restore autoCommit(true) before the connection returns to the pool.
     */
    public void transfer(long fromId, long toId, long amountCents) {
        // TODO(Day27-task03): implement the transactional transfer described above
        throw new UnsupportedOperationException("TODO(Day27-task03): implement transfer");
    }
}
