package com.javaprep.day10.task02;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class PaymentMethodTest {

    @Test
    @DisplayName("card: approves up to the per-transaction limit, statelessly")
    void card() {
        PaymentMethod card = new CardPayment(500);
        assertThat(card.pay(500)).isTrue();
        assertThat(card.pay(500)).isTrue();
        assertThat(card.pay(501)).isFalse();
    }

    @Test
    @DisplayName("wallet: deducts balance and declines when insufficient")
    void wallet() {
        PaymentMethod wallet = new WalletPayment(100);
        assertThat(wallet.pay(60)).isTrue();
        assertThat(wallet.pay(60)).isFalse(); // only 40 left, and a failed payment changes nothing
        assertThat(wallet.pay(40)).isTrue();
        assertThat(wallet.pay(1)).isFalse();
    }

    @Test
    @DisplayName("non-positive amounts -> IllegalArgumentException")
    void invalidAmounts() {
        PaymentMethod card = new CardPayment(100);
        PaymentMethod wallet = new WalletPayment(100);
        assertThatThrownBy(() -> card.pay(0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> wallet.pay(-5)).isInstanceOf(IllegalArgumentException.class);
    }
}
