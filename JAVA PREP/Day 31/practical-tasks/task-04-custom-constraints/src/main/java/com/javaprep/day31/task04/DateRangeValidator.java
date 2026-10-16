package com.javaprep.day31.task04;

import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class DateRangeValidator implements ConstraintValidator<ValidDateRange, Booking> {

    /** Valid when either date is null (let @NotNull report that) or end is strictly after start. */
    @Override
    public boolean isValid(Booking value, ConstraintValidatorContext context) {
        // TODO(Day31-task04): null-tolerant strict end-after-start check
        throw new UnsupportedOperationException("TODO(Day31-task04): null-tolerant strict end-after-start check");
    }
}
