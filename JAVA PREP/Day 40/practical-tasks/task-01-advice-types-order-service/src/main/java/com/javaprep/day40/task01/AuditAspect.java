package com.javaprep.day40.task01;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

// TODO(Day40-task01): declare this class as an aspect and a Spring bean (@Aspect + @Component)
public class AuditAspect {

    private final CallRecorder recorder;

    public AuditAspect(CallRecorder recorder) {
        this.recorder = recorder;
    }

    /** All methods of OrderService. */
    @Pointcut("execution(* com.javaprep.day40.task01.OrderService.*(..))")
    public void orderOps() {
    }

    /** records "before:<method name>" */
    // TODO(Day40-task01): run before orderOps()
    public void before(JoinPoint jp) {
        // TODO(Day40-task01): record before:<method>
        throw new UnsupportedOperationException("TODO(Day40-task01): record before:<method>");
    }

    /** records "returned:<method>=<result>" (only when the method completes normally) */
    // TODO(Day40-task01): run after normal return, binding the result to the parameter named result
    public void returned(JoinPoint jp, Object result) {
        // TODO(Day40-task01): record returned:<method>=<result>
        throw new UnsupportedOperationException("TODO(Day40-task01): record returned:<method>=<result>");
    }

    /** records "threw:<method>:<exception simple name>" (only when an exception escapes) */
    // TODO(Day40-task01): run after an exception, binding it to the parameter named ex
    public void threw(JoinPoint jp, Throwable ex) {
        // TODO(Day40-task01): record threw:<method>:<exception simple class name>
        throw new UnsupportedOperationException("TODO(Day40-task01): record threw:<method>:<exception simple class name>");
    }

    /** records "finally:<method>" (always) */
    // TODO(Day40-task01): run after the method no matter how it ended
    public void atEnd(JoinPoint jp) {
        // TODO(Day40-task01): record finally:<method>
        throw new UnsupportedOperationException("TODO(Day40-task01): record finally:<method>");
    }
}
