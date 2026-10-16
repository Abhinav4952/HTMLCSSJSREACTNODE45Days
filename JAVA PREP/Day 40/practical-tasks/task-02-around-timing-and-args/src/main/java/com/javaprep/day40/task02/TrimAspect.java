package com.javaprep.day40.task02;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

// TODO(Day40-task02): make this an aspect bean
public class TrimAspect {

    /**
     * Around every TextService method whose only parameter is a String: replace String arguments by their trimmed
     * version before proceeding (pjp.proceed(newArgs)). Pointcut: execution(* com.javaprep.day40.task02.TextService.*(String)).
     */
    // TODO(Day40-task02): @Around with execution(* com.javaprep.day40.task02.TextService.*(String))
    public Object trim(ProceedingJoinPoint pjp) throws Throwable {
        // TODO(Day40-task02): copy args, trim strings, proceed with the new arguments
        throw new UnsupportedOperationException("TODO(Day40-task02): copy args, trim strings, proceed with the new arguments");
    }
}
