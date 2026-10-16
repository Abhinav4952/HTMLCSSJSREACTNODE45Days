package com.javaprep.day20.task02;

/** Thread-safe account; money is in whole cents. */
public final class BankAccount {

    private final long id;
    private long balance;

    public BankAccount(long id, long initialBalance) {
        // TODO(Day20-task02): store id and initialBalance; IllegalArgumentException when initialBalance is negative
        throw new UnsupportedOperationException("TODO(Day20-task02): constructor");
    }

    public long id() {
        return id;
    }

    public void deposit(long amount) {
        // TODO(Day20-task02): IllegalArgumentException when amount <= 0; add to balance under this account's lock
        throw new UnsupportedOperationException("TODO(Day20-task02): deposit");
    }

    public void withdraw(long amount) {
        // TODO(Day20-task02): IllegalArgumentException when amount <= 0; IllegalStateException (balance unchanged) when amount > balance; subtract under the lock
        throw new UnsupportedOperationException("TODO(Day20-task02): withdraw");
    }

    public long balance() {
        // TODO(Day20-task02): read balance under the same lock used by writers
        throw new UnsupportedOperationException("TODO(Day20-task02): balance");
    }

    public static void transfer(BankAccount from, BankAccount to, long amount) {
        // TODO(Day20-task02): validate (amount > 0, from != to by id) then lock the account with the smaller id first, then the other; withdraw from 'from' and deposit into 'to' while holding both locks
        throw new UnsupportedOperationException("TODO(Day20-task02): transfer");
    }
}
