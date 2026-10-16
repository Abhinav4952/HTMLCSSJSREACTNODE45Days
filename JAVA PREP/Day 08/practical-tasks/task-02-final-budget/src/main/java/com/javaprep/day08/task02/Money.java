package com.javaprep.day08.task02;

/**
 * Non-negative amount in cents. Constructor validation is a TODO (not a throw) so instances can be created.
 */
public class Money {

    private long cents; // TODO(Day08-task02): make final and assign in the constructor

    // TODO(Day08-task02): reject negative cents with IllegalArgumentException; store cents
    public Money(long cents) {
    }

    // TODO(Day08-task02): return cents
    public long cents() {
        throw new UnsupportedOperationException("TODO(Day08-task02): implement cents");
    }

    // TODO(Day08-task02): return a NEW Money holding the sum (this stays unchanged); null throws NullPointerException
    public Money plus(Money other) {
        throw new UnsupportedOperationException("TODO(Day08-task02): implement plus");
    }
}
