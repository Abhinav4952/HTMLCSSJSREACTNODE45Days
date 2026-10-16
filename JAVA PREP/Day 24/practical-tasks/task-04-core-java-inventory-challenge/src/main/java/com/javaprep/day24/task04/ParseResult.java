package com.javaprep.day24.task04;

/** Provided: outcome of parsing one CSV line. */
public sealed interface ParseResult {

    /** A valid item. */
    record Ok(Item item) implements ParseResult {
    }

    /** A rejected line with the reason. */
    record Failed(int lineNumber, String reason) implements ParseResult {
    }
}
