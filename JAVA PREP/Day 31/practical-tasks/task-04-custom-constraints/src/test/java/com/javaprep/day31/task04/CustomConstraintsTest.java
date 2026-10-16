package com.javaprep.day31.task04;

import static org.assertj.core.api.Assertions.assertThat;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import java.time.LocalDate;
import java.util.Set;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class CustomConstraintsTest {

    static final Validator V = Validation.buildDefaultValidatorFactory().getValidator();

    @ParameterizedTest
    @CsvSource({"Abcdefg1,true", "abcdefg1,false", "ABCDEFG1,false", "Abcdefgh,false", "Ab1,false"})
    void strongPasswordRules(String pw, boolean ok) {
        assertThat(V.validate(new Registration(pw)).isEmpty()).isEqualTo(ok);
    }

    @Test
    void nullPasswordReportedByNotNullOnly() {
        Set<ConstraintViolation<Registration>> v = V.validate(new Registration(null));
        assertThat(v).hasSize(1);
        assertThat(v.iterator().next().getConstraintDescriptor().getAnnotation().annotationType().getSimpleName()).isEqualTo("NotNull");
    }

    @Test
    void validRange() {
        assertThat(V.validate(new Booking("Ann", LocalDate.of(2025, 1, 1), LocalDate.of(2025, 1, 2)))).isEmpty();
    }

    @Test
    void sameDayAndReversedRangesRejected() {
        assertThat(V.validate(new Booking("Ann", LocalDate.of(2025, 1, 1), LocalDate.of(2025, 1, 1)))).hasSize(1);
        Set<ConstraintViolation<Booking>> v = V.validate(new Booking("Ann", LocalDate.of(2025, 2, 1), LocalDate.of(2025, 1, 1)));
        assertThat(v).extracting(ConstraintViolation::getMessage).containsExactly("end must be after start");
    }

    @Test
    void missingDatesReportedOnlyByNotNull() {
        Set<ConstraintViolation<Booking>> v = V.validate(new Booking("Ann", null, LocalDate.of(2025, 1, 1)));
        assertThat(v).hasSize(1);
        assertThat(v.iterator().next().getPropertyPath().toString()).isEqualTo("start");
    }
}
