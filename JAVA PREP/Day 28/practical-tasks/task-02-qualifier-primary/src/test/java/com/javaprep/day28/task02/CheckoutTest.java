package com.javaprep.day28.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class CheckoutTest {

    @Test
    void unqualifiedInjectionPicksThePrimaryGateway() {
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(GatewayConfig.class)) {
            assertThat(ctx.getBean(PaymentGateway.class).name()).isEqualTo("stripe");
            assertThat(ctx.getBean(DefaultCheckout.class).pay(500)).isEqualTo("stripe:500");
        }
    }

    @Test
    void qualifierOverridesPrimary() {
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(GatewayConfig.class)) {
            assertThat(ctx.getBean(PaypalCheckout.class).pay(500)).isEqualTo("paypal:500");
            assertThat(ctx.getBeansOfType(PaymentGateway.class)).containsOnlyKeys("stripe", "paypal");
        }
    }

    @Test
    void rejectsNonPositiveAmounts() {
        assertThatThrownBy(() -> new DefaultCheckout(new SimpleGateway("x")).pay(0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new PaypalCheckout(new SimpleGateway("x")).pay(-5)).isInstanceOf(IllegalArgumentException.class);
    }
}
