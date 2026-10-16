package com.javaprep.day40.task04;

import org.aspectj.lang.annotation.Pointcut;

/** PROVIDED: a shared, named pointcut that aspects can reference. */
public class Pointcuts {

    @Pointcut("execution(* com.javaprep.day40.task04.PaymentService.pay(..))")
    public void payment() {
    }
}
