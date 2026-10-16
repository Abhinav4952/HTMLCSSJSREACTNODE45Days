package com.javaprep.day49.task03;

import java.util.ArrayList;
import java.util.List;

/** A miniature Checkstyle: finds the style problems a real Checkstyle run would flag. */
public class StyleLinter {

    public static final int MAX_LINE_LENGTH = 100;

    /**
     * Returns violations as "<line>:<RULE>" (1-based line numbers), ordered by line, at most one entry per rule per line.
     * Rules (in evaluation order within a line):
     * <ol>
     *   <li>TAB - the line contains a tab character</li>
     *   <li>TRAILING_WHITESPACE - the line ends with a space or tab (and is not empty)</li>
     *   <li>LINE_TOO_LONG - more than MAX_LINE_LENGTH characters (not counting the trailing newline)</li>
     *   <li>STAR_IMPORT - line (trimmed) starts with "import " and ends with ".*;"</li>
     *   <li>SYSTEM_OUT - line contains "System.out." or "System.err."</li>
     * </ol>
     * Additionally, when the source is non-empty and does not end with '\n', add "EOF:NO_FINAL_NEWLINE" as the last entry.
     */
    public List<String> lint(String source) {
        // TODO(Day49-task03): split on '\n' (keep trailing empties out of the line count) and apply the rules
        throw new UnsupportedOperationException("TODO(Day49-task03): implement lint");
    }
}
