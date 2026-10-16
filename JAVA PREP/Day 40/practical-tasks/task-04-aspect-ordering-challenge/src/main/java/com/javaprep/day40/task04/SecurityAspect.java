package com.javaprep.day40.task04;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

// TODO(Day40-task04): aspect bean with the HIGHEST precedence of the two (@Order(1))
public class SecurityAspect {

    private final CallRecorder recorder;

    public SecurityAspect(CallRecorder recorder) {
        this.recorder = recorder;
    }

    /** records "security:in" before proceeding and "security:out" afterwards, even when the call fails. */
    // TODO(Day40-task04): @Around using the named pointcut Pointcuts.payment()
    public Object guard(ProceedingJoinPoint pjp) throws Throwable {
        // TODO(Day40-task04): record in, proceed, record out in finally
        throw new UnsupportedOperationException("TODO(Day40-task04): record in, proceed, record out in finally");
    }
}
