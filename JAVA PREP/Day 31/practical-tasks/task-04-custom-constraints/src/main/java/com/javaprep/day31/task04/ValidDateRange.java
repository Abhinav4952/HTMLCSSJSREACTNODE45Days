package com.javaprep.day31.task04;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/** PROVIDED class-level constraint: end must be strictly after start. */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = DateRangeValidator.class)
public @interface ValidDateRange {
    String message() default "end must be after start";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
