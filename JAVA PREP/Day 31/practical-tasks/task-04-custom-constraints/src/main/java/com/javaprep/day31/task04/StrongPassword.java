package com.javaprep.day31.task04;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/** PROVIDED constraint: at least 8 chars with an upper-case letter, a lower-case letter and a digit. */
@Target({ElementType.FIELD, ElementType.PARAMETER, ElementType.RECORD_COMPONENT})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = StrongPasswordValidator.class)
public @interface StrongPassword {
    String message() default "password is too weak";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
