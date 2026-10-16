package com.javaprep.day19.task01;

import java.time.Clock;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.Period;
import java.time.temporal.TemporalAdjusters;
import java.util.ArrayList;
import java.util.List;

/** Calendar math with java.time. */
public final class LocalDateSpan {

    private LocalDateSpan() {
    }

    public static int ageOn(LocalDate birth, LocalDate on) {
        // TODO(Day19-task01): completed years between birth and on (Period.between(...).getYears()); IllegalArgumentException if birth is after on
        throw new UnsupportedOperationException("TODO(Day19-task01): ageOn");
    }

    public static LocalDate addBusinessDays(LocalDate start, int n) {
        // TODO(Day19-task01): move forward n weekdays skipping Saturday/Sunday; n == 0 returns start; negative n -> IllegalArgumentException
        throw new UnsupportedOperationException("TODO(Day19-task01): addBusinessDays");
    }

    public static List<LocalDate> datesBetween(LocalDate startInclusive, LocalDate endExclusive) {
        // TODO(Day19-task01): every date from startInclusive up to (not including) endExclusive; equal -> empty; end before start -> IllegalArgumentException
        throw new UnsupportedOperationException("TODO(Day19-task01): datesBetween");
    }

    public static String humanSpan(LocalDate from, LocalDate to) {
        // TODO(Day19-task01): format Period.between(from, to) as '<years>y <months>m <days>d'; IllegalArgumentException if to is before from
        throw new UnsupportedOperationException("TODO(Day19-task01): humanSpan");
    }

    public static LocalDate nextWeekday(LocalDate from, DayOfWeek dayOfWeek) {
        // TODO(Day19-task01): the next date strictly after from that falls on dayOfWeek (TemporalAdjusters.next)
        throw new UnsupportedOperationException("TODO(Day19-task01): nextWeekday");
    }

    public static boolean isOverdue(LocalDate due, Clock clock) {
        // TODO(Day19-task01): true when LocalDate.now(clock) is after due (never call LocalDate.now() without the clock)
        throw new UnsupportedOperationException("TODO(Day19-task01): isOverdue");
    }
}
