package com.javaprep.day10.task02;

public class CardPayment implements PaymentMethod {

    private final int limitCents;

    public CardPayment(int limitCents) {
        this.limitCents = limitCents;
    }

    // TODO(Day10-task02): approve (true) when amount <= limitCents (per-transaction limit, stateless); amount <= 0 -> IAE
    @Override
    public boolean pay(int amountCents) {
        throw new UnsupportedOperationException("TODO(Day10-task02): implement CardPayment.pay");
    }
}
