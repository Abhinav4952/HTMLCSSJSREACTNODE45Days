package com.javaprep.day24.task02;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Nearest-wins dependency mediation. */
public final class DependencyMediation {

    /** One occurrence of an artifact in the dependency tree. */
    public record Declaration(String artifact, String version, int depth) {
    }

    private DependencyMediation() {
    }

    public static Map<String, String> resolve(List<Declaration> declarations) {
        // TODO(Day24-task02): for every artifact keep the declaration with the smallest depth (the first one wins ties); the result is a LinkedHashMap artifact -> version ordered by first appearance
        throw new UnsupportedOperationException("TODO(Day24-task02): resolve");
    }

    public static String highest(List<String> versions) {
        // TODO(Day24-task02): empty list -> IllegalArgumentException; return the original string of the greatest MavenVersion
        throw new UnsupportedOperationException("TODO(Day24-task02): highest");
    }

    public static List<String> satisfying(VersionRange range, List<String> versions) {
        // TODO(Day24-task02): keep versions for which range.contains(MavenVersion.parse(v)) and return them sorted ascending by MavenVersion
        throw new UnsupportedOperationException("TODO(Day24-task02): satisfying");
    }
}
