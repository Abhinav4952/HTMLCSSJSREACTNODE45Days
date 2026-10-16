package com.javaprep.day40.task02;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

// TODO(Day40-task02): make this an aspect bean
public class TimingAspect {

    private final MetricsRegistry registry;

    public TimingAspect(MetricsRegistry registry) {
        this.registry = registry;
    }

    /**
     * Around every method annotated with @Timed: measure with System.nanoTime(), ALWAYS record the duration under the
     * method name (also when the method throws), and let the original result/exception pass through unchanged.
     */
    // TODO(Day40-task02): @Around on methods annotated with Timed (pointcut: @annotation(com.javaprep.day40.task02.Timed))
    public Object time(ProceedingJoinPoint pjp) throws Throwable {
        // TODO(Day40-task02): time pjp.proceed() in try/finally and record under pjp.getSignature().getName()
        throw new UnsupportedOperationException("TODO(Day40-task02): time pjp.proceed() in try/finally and record under pjp.getSignature().getName()");
    }
}
