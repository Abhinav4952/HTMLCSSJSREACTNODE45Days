package com.javaprep.day23.task01;

import java.text.Normalizer;
import java.util.Locale;
import java.util.regex.Pattern;

/** URL slug helpers. */
public final class Slugs {

    private static final Pattern COMBINING_MARKS = Pattern.compile("\\p{M}+");
    private static final Pattern NON_ALNUM = Pattern.compile("[^a-z0-9]+");
    private static final Pattern VALID = Pattern.compile("[a-z0-9]+(?:-[a-z0-9]+)*");

    private Slugs() {
    }

    public static String slugify(String text) {
        // TODO(Day23-task01): null -> IllegalArgumentException; Normalizer.normalize(NFD), remove COMBINING_MARKS, toLowerCase(Locale.ROOT), replace NON_ALNUM runs with '-', strip leading/trailing '-'
        throw new UnsupportedOperationException("TODO(Day23-task01): slugify");
    }

    public static boolean isValidSlug(String text) {
        // TODO(Day23-task01): true only for non-null text matching VALID (lowercase alphanumerics separated by single dashes)
        throw new UnsupportedOperationException("TODO(Day23-task01): isValidSlug");
    }
}
