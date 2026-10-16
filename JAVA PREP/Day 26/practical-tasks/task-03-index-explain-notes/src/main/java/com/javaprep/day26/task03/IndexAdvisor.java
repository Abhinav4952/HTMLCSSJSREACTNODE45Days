package com.javaprep.day26.task03;

import java.util.List;

/** Produces index DDL and reads query plans. Pure string logic — no database needed. */
public final class IndexAdvisor {

    private IndexAdvisor() {
    }

    /**
     * Composite index recommendation: equality columns first (in the given order), then the optional range column.
     * Format: {@code CREATE INDEX idx_<table>_<col1>_<col2> ON <table> (<col1>, <col2>)}.
     * Example: ("orders", [customer_id, status], "created_at") ->
     * {@code CREATE INDEX idx_orders_customer_id_status_created_at ON orders (customer_id, status, created_at)}.
     * rangeColumn may be null. No columns at all -> IllegalArgumentException.
     */
    public static String recommendIndex(String table, List<String> equalityColumns, String rangeColumn) {
        // TODO(Day26-task03): build the DDL string as documented above
        throw new UnsupportedOperationException("TODO(Day26-task03): implement recommendIndex");
    }

    /** {@code CREATE UNIQUE INDEX uq_<table>_<column> ON <table> (<column>)} */
    public static String recommendUniqueIndex(String table, String column) {
        // TODO(Day26-task03): build the unique-index DDL string
        throw new UnsupportedOperationException("TODO(Day26-task03): implement recommendUniqueIndex");
    }

    /**
     * Can a B-tree index on the column serve this predicate? False for a leading-wildcard LIKE
     * ({@code email like '%gmail.com'}) and for a function wrapped around the column ({@code lower(email) = 'a'}).
     * True otherwise ({@code status = 'NEW'}, {@code email like 'ana%'}, {@code created_at > '2024-01-01'}).
     */
    public static boolean isIndexUsable(String predicate) {
        // TODO(Day26-task03): lower-case + trim the predicate and apply the two rules
        throw new UnsupportedOperationException("TODO(Day26-task03): implement isIndexUsable");
    }

    /**
     * Classifies an H2 EXPLAIN plan text: contains "tablescan" (any case) -> "FULL_SCAN";
     * contains "idx_" (any case) -> "INDEX_SCAN"; otherwise "UNKNOWN".
     */
    public static String classifyPlan(String planText) {
        // TODO(Day26-task03): classify the plan
        throw new UnsupportedOperationException("TODO(Day26-task03): implement classifyPlan");
    }
}
