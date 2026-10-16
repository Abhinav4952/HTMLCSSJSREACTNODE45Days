package com.javaprep.day19.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Clock;
import java.time.DayOfWeek;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import org.junit.jupiter.api.Test;

class LocalDateSpanTest {

    @Test
    void r1_ageOnBirthday() {
        LocalDate birth = LocalDate.of(1990, 5, 15);
        assertThat(LocalDateSpan.ageOn(birth, LocalDate.of(2024, 5, 14))).isEqualTo(33);
        assertThat(LocalDateSpan.ageOn(birth, LocalDate.of(2024, 5, 15))).isEqualTo(34);
        assertThat(LocalDateSpan.ageOn(birth, birth)).isZero();
    }

    @Test
    void r1_ageForLeapDayBirthAndInvalidOrder() {
        LocalDate leap = LocalDate.of(2000, 2, 29);
        assertThat(LocalDateSpan.ageOn(leap, LocalDate.of(2023, 2, 28))).isEqualTo(22);
        assertThat(LocalDateSpan.ageOn(leap, LocalDate.of(2023, 3, 1))).isEqualTo(23);
        assertThatThrownBy(() -> LocalDateSpan.ageOn(LocalDate.of(2025, 1, 1), LocalDate.of(2024, 1, 1)))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r2_addBusinessDaysSkipsWeekends() {
        LocalDate friday = LocalDate.of(2024, 5, 17);
        assertThat(LocalDateSpan.addBusinessDays(friday, 1)).isEqualTo(LocalDate.of(2024, 5, 20));
        assertThat(LocalDateSpan.addBusinessDays(friday, 5)).isEqualTo(LocalDate.of(2024, 5, 24));
        assertThat(LocalDateSpan.addBusinessDays(friday, 0)).isEqualTo(friday);
        LocalDate saturday = LocalDate.of(2024, 5, 18);
        assertThat(LocalDateSpan.addBusinessDays(saturday, 1)).isEqualTo(LocalDate.of(2024, 5, 20));
        assertThat(LocalDateSpan.addBusinessDays(LocalDate.of(2024, 5, 20), 10)).isEqualTo(LocalDate.of(2024, 6, 3));
    }

    @Test
    void r2_negativeBusinessDaysRejected() {
        assertThatThrownBy(() -> LocalDateSpan.addBusinessDays(LocalDate.of(2024, 5, 17), -1))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r3_datesBetween() {
        assertThat(LocalDateSpan.datesBetween(LocalDate.of(2024, 2, 27), LocalDate.of(2024, 3, 2)))
                .containsExactly(LocalDate.of(2024, 2, 27), LocalDate.of(2024, 2, 28), LocalDate.of(2024, 2, 29), LocalDate.of(2024, 3, 1));
        LocalDate same = LocalDate.of(2024, 1, 1);
        assertThat(LocalDateSpan.datesBetween(same, same)).isEmpty();
        assertThatThrownBy(() -> LocalDateSpan.datesBetween(LocalDate.of(2024, 1, 2), LocalDate.of(2024, 1, 1)))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r4_humanSpan() {
        assertThat(LocalDateSpan.humanSpan(LocalDate.of(2020, 1, 31), LocalDate.of(2021, 3, 2))).isEqualTo("1y 1m 2d");
        assertThat(LocalDateSpan.humanSpan(LocalDate.of(2024, 5, 1), LocalDate.of(2024, 5, 1))).isEqualTo("0y 0m 0d");
        assertThat(LocalDateSpan.humanSpan(LocalDate.of(2024, 1, 1), LocalDate.of(2024, 12, 31))).isEqualTo("0y 11m 30d");
        assertThatThrownBy(() -> LocalDateSpan.humanSpan(LocalDate.of(2024, 5, 2), LocalDate.of(2024, 5, 1)))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r5_nextWeekdayIsStrictlyAfter() {
        LocalDate friday = LocalDate.of(2024, 5, 17);
        assertThat(LocalDateSpan.nextWeekday(friday, DayOfWeek.MONDAY)).isEqualTo(LocalDate.of(2024, 5, 20));
        assertThat(LocalDateSpan.nextWeekday(friday, DayOfWeek.FRIDAY)).isEqualTo(LocalDate.of(2024, 5, 24));
        assertThat(LocalDateSpan.nextWeekday(friday, DayOfWeek.SATURDAY)).isEqualTo(LocalDate.of(2024, 5, 18));
    }

    @Test
    void r6_isOverdueUsesTheInjectedClock() {
        Clock may20 = Clock.fixed(Instant.parse("2024-05-20T10:00:00Z"), ZoneOffset.UTC);
        assertThat(LocalDateSpan.isOverdue(LocalDate.of(2024, 5, 19), may20)).isTrue();
        assertThat(LocalDateSpan.isOverdue(LocalDate.of(2024, 5, 20), may20)).isFalse();
        assertThat(LocalDateSpan.isOverdue(LocalDate.of(2024, 5, 21), may20)).isFalse();
    }
}
