package com.javaprep.day25.task04;

/** Interview-style helpers about transactions. */
public final class AcidNotes {

    private AcidNotes() {
    }

    /** 'A' -> "Atomicity", 'C' -> "Consistency", 'I' -> "Isolation", 'D' -> "Durability" (case-insensitive). */
    public static String propertyFor(char letter) {
        // TODO(Day25-task04): map the ACID letter to its property name; throw IllegalArgumentException for any other letter
        throw new UnsupportedOperationException("TODO(Day25-task04): implement propertyFor");
    }

    /**
     * Minimal SQL-standard isolation level that prevents the anomaly:
     * "dirty read" -> READ_COMMITTED, "non-repeatable read" -> REPEATABLE_READ, "phantom read" -> SERIALIZABLE.
     */
    public static String isolationFor(String anomaly) {
        // TODO(Day25-task04): implement (case-insensitive, trimmed); unknown anomaly -> IllegalArgumentException
        throw new UnsupportedOperationException("TODO(Day25-task04): implement isolationFor");
    }
}
