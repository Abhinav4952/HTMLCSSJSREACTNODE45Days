package com.javaprep.day10.task02;

public interface PaymentMethod {

    /**
     * Attempts to pay {@code amountCents}. Returns true if the payment is approved, false if funds/limit do
     * not allow it. Throws {@link IllegalArgumentException} when {@code amountCents <= 0}.
     */
    boolean pay(int amountCents);
}
