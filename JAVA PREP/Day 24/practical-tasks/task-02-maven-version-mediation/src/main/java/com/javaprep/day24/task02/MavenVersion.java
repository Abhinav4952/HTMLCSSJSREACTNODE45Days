package com.javaprep.day24.task02;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** A simplified Maven version with Maven's ordering rules. */
public final class MavenVersion implements Comparable<MavenVersion> {

    private static final Pattern FORMAT = Pattern.compile("(\\d+(?:\\.\\d+)*)(?:-(alpha|beta|milestone|rc|cr|snapshot|ga|final)(?:[.-]?(\\d+))?)?",
            Pattern.CASE_INSENSITIVE);

    private final String text;
    private final List<Integer> numbers;
    private final int rank;
    private final int qualifierNumber;

    private MavenVersion(String text, List<Integer> numbers, int rank, int qualifierNumber) {
        this.text = text;
        this.numbers = numbers;
        this.rank = rank;
        this.qualifierNumber = qualifierNumber;
    }

    public static MavenVersion parse(String text) {
        // TODO(Day24-task02): null/blank/non-matching -> IllegalArgumentException; split numeric parts (strip trailing zero components), qualifier rank (alpha 0, beta 1, milestone 2, rc/cr 3, snapshot 4, none/ga/final 5) and qualifier number (default 0)
        throw new UnsupportedOperationException("TODO(Day24-task02): parse");
    }

    @Override
    public int compareTo(MavenVersion other) {
        // TODO(Day24-task02): compare numeric components pairwise (missing = 0), then rank, then qualifierNumber
        throw new UnsupportedOperationException("TODO(Day24-task02): compareTo");
    }

    @Override
    public boolean equals(Object o) {
        return o instanceof MavenVersion other && compareTo(other) == 0;
    }

    @Override
    public int hashCode() {
        return Objects.hash(numbers, rank, qualifierNumber);
    }

    @Override
    public String toString() {
        return text;
    }
}
