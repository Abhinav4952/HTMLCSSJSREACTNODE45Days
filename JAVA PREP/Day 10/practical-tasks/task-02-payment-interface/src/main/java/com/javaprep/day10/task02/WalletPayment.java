package com.javaprep.day10.task02;

public class WalletPayment implements PaymentMethod {

    private int balanceCents;

    public WalletPayment(int balanceCents) {
        this.balanceCents = balanceCents;
    }

    // TODO(Day10-task02): if amount <= balance, deduct it and return true; otherwise return false (balance unchanged);
    // amount <= 0 -> IAE
    @Override
    public boolean pay(int amountCents) {
        throw new UnsupportedOperationException("TODO(Day10-task02): implement WalletPayment.pay");
    }
}
