package com.javaprep.day19.task02;

import java.time.DayOfWeek;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

/** Cross-zone scheduling helpers. */
public final class ZonedMeeting {

    private static final DateTimeFormatter FORMAT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");

    private ZonedMeeting() {
    }

    public static ZonedDateTime convert(LocalDateTime local, ZoneId from, ZoneId to) {
        // TODO(Day19-task02): interpret local in zone from, then return the same instant expressed in zone to (withZoneSameInstant)
        throw new UnsupportedOperationException("TODO(Day19-task02): convert");
    }

    public static List<String> localTimes(Instant instant, List<String> zoneIds) {
        // TODO(Day19-task02): for each zone id (in order) format instant.atZone(ZoneId.of(id)) as yyyy-MM-dd HH:mm; unknown id propagates DateTimeException
        throw new UnsupportedOperationException("TODO(Day19-task02): localTimes");
    }

    public static boolean isDuringWorkHours(ZonedDateTime t) {
        // TODO(Day19-task02): Monday-Friday and 09:00 <= local time < 17:00 in t's own zone
        throw new UnsupportedOperationException("TODO(Day19-task02): isDuringWorkHours");
    }

    public static long minutesBetween(ZonedDateTime a, ZonedDateTime b) {
        // TODO(Day19-task02): elapsed minutes from a to b using Duration.between (so DST changes are respected)
        throw new UnsupportedOperationException("TODO(Day19-task02): minutesBetween");
    }

    public static ZonedDateTime plusWeeksWallClock(ZonedDateTime start, int weeks) {
        // TODO(Day19-task02): add weeks keeping the local wall-clock time (ZonedDateTime.plusWeeks, not Duration)
        throw new UnsupportedOperationException("TODO(Day19-task02): plusWeeksWallClock");
    }

    public static String formatUtc(ZonedDateTime t) {
        // TODO(Day19-task02): the instant of t as an ISO-8601 UTC string (Instant#toString)
        throw new UnsupportedOperationException("TODO(Day19-task02): formatUtc");
    }
}
