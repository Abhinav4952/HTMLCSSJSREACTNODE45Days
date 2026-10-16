package com.javaprep.day19.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.DateTimeException;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.List;
import org.junit.jupiter.api.Test;

class ZonedMeetingTest {

    private static final ZoneId NY = ZoneId.of("America/New_York");
    private static final ZoneId KOLKATA = ZoneId.of("Asia/Kolkata");

    @Test
    void r1_convertKeepsTheInstant() {
        ZonedDateTime utc = ZonedMeeting.convert(LocalDateTime.of(2024, 5, 20, 9, 0), KOLKATA, ZoneOffset.UTC);
        assertThat(utc.toLocalDateTime()).isEqualTo(LocalDateTime.of(2024, 5, 20, 3, 30));
        assertThat(utc.getZone()).isEqualTo(ZoneOffset.UTC);
        ZonedDateTime ny = ZonedMeeting.convert(LocalDateTime.of(2024, 12, 1, 12, 0), ZoneOffset.UTC, NY);
        assertThat(ny.toLocalDateTime()).isEqualTo(LocalDateTime.of(2024, 12, 1, 7, 0));
    }

    @Test
    void r2_localTimesInRequestedOrder() {
        Instant meeting = Instant.parse("2024-05-20T12:00:00Z");
        assertThat(ZonedMeeting.localTimes(meeting, List.of("Asia/Kolkata", "America/New_York", "Europe/London")))
                .containsExactly("2024-05-20 17:30", "2024-05-20 08:00", "2024-05-20 13:00");
        assertThat(ZonedMeeting.localTimes(meeting, List.of())).isEmpty();
    }

    @Test
    void r2_unknownZoneFails() {
        Instant meeting = Instant.parse("2024-05-20T12:00:00Z");
        assertThatThrownBy(() -> ZonedMeeting.localTimes(meeting, List.of("Mars/Base")))
                .isInstanceOf(DateTimeException.class);
    }

    @Test
    void r3_workHoursInTheMeetingsOwnZone() {
        assertThat(ZonedMeeting.isDuringWorkHours(ZonedDateTime.of(2024, 5, 20, 9, 0, 0, 0, KOLKATA))).isTrue();
        assertThat(ZonedMeeting.isDuringWorkHours(ZonedDateTime.of(2024, 5, 20, 16, 59, 0, 0, KOLKATA))).isTrue();
        assertThat(ZonedMeeting.isDuringWorkHours(ZonedDateTime.of(2024, 5, 20, 17, 0, 0, 0, KOLKATA))).isFalse();
        assertThat(ZonedMeeting.isDuringWorkHours(ZonedDateTime.of(2024, 5, 20, 8, 59, 0, 0, NY))).isFalse();
        assertThat(ZonedMeeting.isDuringWorkHours(ZonedDateTime.of(2024, 5, 18, 10, 0, 0, 0, NY))).isFalse();
        assertThat(ZonedMeeting.isDuringWorkHours(ZonedDateTime.of(2024, 5, 19, 10, 0, 0, 0, NY))).isFalse();
    }

    @Test
    void r4_minutesBetweenIsElapsedTime() {
        ZonedDateTime before = ZonedDateTime.of(2024, 3, 10, 1, 30, 0, 0, NY);
        ZonedDateTime after = ZonedDateTime.of(2024, 3, 10, 3, 30, 0, 0, NY);
        assertThat(ZonedMeeting.minutesBetween(before, after)).isEqualTo(60);
        ZonedDateTime a = ZonedDateTime.of(2024, 5, 20, 9, 0, 0, 0, KOLKATA);
        ZonedDateTime b = ZonedDateTime.of(2024, 5, 20, 10, 30, 0, 0, KOLKATA);
        assertThat(ZonedMeeting.minutesBetween(a, b)).isEqualTo(90);
        assertThat(ZonedMeeting.minutesBetween(b, a)).isEqualTo(-90);
    }

    @Test
    void r5_weeklyRecurrenceKeepsLocalTimeAcrossDst() {
        ZonedDateTime start = ZonedDateTime.of(2024, 3, 4, 10, 0, 0, 0, NY);
        ZonedDateTime next = ZonedMeeting.plusWeeksWallClock(start, 1);
        assertThat(next.toLocalTime()).isEqualTo(LocalTime.of(10, 0));
        assertThat(next.getOffset()).isEqualTo(ZoneOffset.ofHours(-4));
        assertThat(next.toLocalDate()).hasToString("2024-03-11");
        assertThat(ZonedMeeting.plusWeeksWallClock(start, 0)).isEqualTo(start);
    }

    @Test
    void r6_formatUtc() {
        assertThat(ZonedMeeting.formatUtc(ZonedDateTime.of(2024, 5, 20, 9, 0, 0, 0, ZoneOffset.UTC))).isEqualTo("2024-05-20T09:00:00Z");
        assertThat(ZonedMeeting.formatUtc(ZonedDateTime.of(2024, 5, 20, 9, 0, 0, 0, KOLKATA))).isEqualTo("2024-05-20T03:30:00Z");
    }
}
