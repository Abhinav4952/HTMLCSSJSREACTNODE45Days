package com.javaprep.day31.task04;

import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class StrongPasswordValidator implements ConstraintValidator<StrongPassword, String> {

    /** null is VALID here (combine with @NotNull when required). */
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        // TODO(Day31-task04): null valid; otherwise length >= 8 with upper, lower and digit
        throw new UnsupportedOperationException("TODO(Day31-task04): null valid; otherwise length >= 8 with upper, lower and digit");
    }
}
