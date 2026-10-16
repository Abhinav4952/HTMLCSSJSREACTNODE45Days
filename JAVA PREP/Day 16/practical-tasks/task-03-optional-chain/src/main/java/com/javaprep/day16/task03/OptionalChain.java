package com.javaprep.day16.task03;

import java.util.List;
import java.util.Optional;

/** Optional-based lookups. */
public final class OptionalChain {

    private OptionalChain() {
    }

    public static Optional<String> cityOf(User user) {
        // TODO(Day16-task03): Optional.ofNullable(user) -> map address -> map city -> map trim -> filter non-empty
        throw new UnsupportedOperationException("TODO(Day16-task03): cityOf");
    }

    public static Optional<User> findByName(List<User> users, String name) {
        // TODO(Day16-task03): first user whose name equalsIgnoreCase name; empty if name is null or none matches (loop or later-day streams are both fine)
        throw new UnsupportedOperationException("TODO(Day16-task03): findByName");
    }

    public static Optional<Integer> parsePositive(String text) {
        // TODO(Day16-task03): parse a trimmed int; empty for null/blank/non-numeric/overflow/zero/negative (catch NumberFormatException)
        throw new UnsupportedOperationException("TODO(Day16-task03): parsePositive");
    }

    public static String zipOrDefault(User user, String defaultZip) {
        // TODO(Day16-task03): return the address zip, or defaultZip when the user, address, or zip is missing
        throw new UnsupportedOperationException("TODO(Day16-task03): zipOrDefault");
    }

    public static String requireCity(User user) {
        // TODO(Day16-task03): return cityOf(user) or throw IllegalStateException with a message containing the user's name ('unknown' for a null user) via orElseThrow
        throw new UnsupportedOperationException("TODO(Day16-task03): requireCity");
    }
}
