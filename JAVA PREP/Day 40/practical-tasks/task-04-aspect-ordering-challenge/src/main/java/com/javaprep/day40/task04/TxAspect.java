package com.javaprep.day40.task04;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

// TODO(Day40-task04): aspect bean with LOWER precedence than SecurityAspect (@Order(2))
public class TxAspect {

    private final CallRecorder recorder;

    public TxAspect(CallRecorder recorder) {
        this.recorder = recorder;
    }

    /** records "tx:begin"; after success "tx:commit"; on any Throwable "tx:rollback" and rethrows it. */
    // TODO(Day40-task04): @Around using the named pointcut Pointcuts.payment()
    public Object transaction(ProceedingJoinPoint pjp) throws Throwable {
        // TODO(Day40-task04): begin, proceed, commit or rollback
        throw new UnsupportedOperationException("TODO(Day40-task04): begin, proceed, commit or rollback");
    }
}
