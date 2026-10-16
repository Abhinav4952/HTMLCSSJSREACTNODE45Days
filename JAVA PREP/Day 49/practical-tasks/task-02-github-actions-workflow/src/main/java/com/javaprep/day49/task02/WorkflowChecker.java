package com.javaprep.day49.task02;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

/** A tiny structural checker for a GitHub Actions workflow file (text based, no YAML parser needed). */
public class WorkflowChecker {

    /**
     * Returns the names of MISSING pieces, in this order (empty list = workflow is acceptable):
     * <ol>
     *   <li>"trigger:push" - the text has a line starting (after indentation) with "push:"</li>
     *   <li>"trigger:pull_request" - a line starting with "pull_request:"</li>
     *   <li>"checkout" - uses "actions/checkout@"</li>
     *   <li>"setup-java" - uses "actions/setup-java@"</li>
     *   <li>"java-21" - matches regex java-version:\s*['"]?21['"]?</li>
     *   <li>"maven-cache" - matches regex cache:\s*['"]?maven['"]?</li>
     *   <li>"maven-build" - a "run:" line invoking mvn with verify or test (e.g. "mvn -B verify")</li>
     * </ol>
     */
    public List<String> missingPieces(String yaml) {
        // TODO(Day49-task02): implement the seven checks above (Pattern with MULTILINE is handy)
        throw new UnsupportedOperationException("TODO(Day49-task02): implement missingPieces");
    }
}
