package com.javaprep.day31.task04;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDate;

@ValidDateRange
public record Booking(@NotBlank String guest, @NotNull LocalDate start, @NotNull LocalDate end) {
}
