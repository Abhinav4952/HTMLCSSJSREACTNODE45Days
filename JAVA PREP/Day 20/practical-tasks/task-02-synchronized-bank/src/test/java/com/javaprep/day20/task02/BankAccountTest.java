package com.javaprep.day20.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(30)
class BankAccountTest {

    @Test
    void r1_constructorValidation() {
        assertThatThrownBy(() -> new BankAccount(1, -1)).isInstanceOf(IllegalArgumentException.class);
        assertThat(new BankAccount(1, 0).balance()).isZero();
        assertThat(new BankAccount(7, 50).id()).isEqualTo(7);
    }

    @Test
    void r2_depositAndWithdraw() {
        BankAccount a = new BankAccount(1, 100);
        a.deposit(50);
        a.withdraw(30);
        assertThat(a.balance()).isEqualTo(120);
    }

    @Test
    void r2_invalidAmountsAndInsufficientFunds() {
        BankAccount a = new BankAccount(1, 100);
        assertThatThrownBy(() -> a.deposit(0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> a.withdraw(-5)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> a.withdraw(101)).isInstanceOf(IllegalStateException.class);
        assertThat(a.balance()).isEqualTo(100);
        a.withdraw(100);
        assertThat(a.balance()).isZero();
    }

    @Test
    void r3_concurrentDepositsAreNotLost() throws Exception {
        BankAccount a = new BankAccount(1, 0);
        runInParallel(8, () -> {
            for (int i = 0; i < 20_000; i++) {
                a.deposit(1);
            }
        });
        assertThat(a.balance()).isEqualTo(160_000);
    }

    @Test
    void r4_transferMovesMoneyAtomically() {
        BankAccount a = new BankAccount(1, 100);
        BankAccount b = new BankAccount(2, 10);
        BankAccount.transfer(a, b, 40);
        assertThat(a.balance()).isEqualTo(60);
        assertThat(b.balance()).isEqualTo(50);
    }

    @Test
    void r4_failedTransferChangesNothing() {
        BankAccount a = new BankAccount(1, 10);
        BankAccount b = new BankAccount(2, 10);
        assertThatThrownBy(() -> BankAccount.transfer(a, b, 11)).isInstanceOf(IllegalStateException.class);
        assertThat(a.balance()).isEqualTo(10);
        assertThat(b.balance()).isEqualTo(10);
    }

    @Test
    void r5_opposingTransfersDoNotDeadlockAndKeepTheTotal() throws Exception {
        BankAccount a = new BankAccount(1, 1_000_000);
        BankAccount b = new BankAccount(2, 1_000_000);
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 20_000; i++) {
                BankAccount.transfer(a, b, 1);
            }
        });
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 20_000; i++) {
                BankAccount.transfer(b, a, 1);
            }
        });
        t1.start();
        t2.start();
        t1.join(20_000);
        t2.join(20_000);
        assertThat(t1.isAlive()).as("thread 1 finished (no deadlock)").isFalse();
        assertThat(t2.isAlive()).as("thread 2 finished (no deadlock)").isFalse();
        assertThat(a.balance() + b.balance()).isEqualTo(2_000_000);
        assertThat(a.balance()).isEqualTo(1_000_000);
    }

    @Test
    void r6_invalidTransfers() {
        BankAccount a = new BankAccount(1, 10);
        assertThatThrownBy(() -> BankAccount.transfer(a, a, 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> BankAccount.transfer(a, new BankAccount(2, 0), 0)).isInstanceOf(IllegalArgumentException.class);
        assertThat(a.balance()).isEqualTo(10);
    }

    private static void runInParallel(int threads, Runnable task) throws InterruptedException {
        List<Thread> all = new ArrayList<>();
        for (int i = 0; i < threads; i++) {
            Thread t = new Thread(task);
            all.add(t);
            t.start();
        }
        for (Thread t : all) {
            t.join();
        }
    }
}
