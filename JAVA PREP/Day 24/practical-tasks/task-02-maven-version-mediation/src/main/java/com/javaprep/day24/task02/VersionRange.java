package com.javaprep.day24.task02;

/** A Maven version range such as [1.0,2.0). */
public final class VersionRange {

    private final MavenVersion lower;
    private final boolean lowerInclusive;
    private final MavenVersion upper;
    private final boolean upperInclusive;

    private VersionRange(MavenVersion lower, boolean lowerInclusive, MavenVersion upper, boolean upperInclusive) {
        this.lower = lower;
        this.lowerInclusive = lowerInclusive;
        this.upper = upper;
        this.upperInclusive = upperInclusive;
    }

    public static VersionRange parse(String spec) {
        // TODO(Day24-task02): null/short/no brackets -> IllegalArgumentException; strip the brackets; no comma means exact [a] (both brackets must be square); otherwise exactly two parts split on the comma, blank part = unbounded, both blank -> IAE, lower > upper -> IAE; remember inclusive ('[' / ']') vs exclusive ('(' / ')')
        throw new UnsupportedOperationException("TODO(Day24-task02): parse");
    }

    public boolean contains(MavenVersion version) {
        // TODO(Day24-task02): lower bound (when present): version >= lower if inclusive else > lower; upper bound (when present): version <= upper if inclusive else < upper
        throw new UnsupportedOperationException("TODO(Day24-task02): contains");
    }
}
