package com.javaprep.day43.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class OrderServiceTest {

    private final AtomicInteger calls = new AtomicInteger();

    private InventoryPort failingFirst(int failures, int stock) {
        return sku -> {
            if (calls.incrementAndGet() <= failures) {
                throw new InventoryUnavailableException("down");
            }
            return stock;
        };
    }

    @Test
    void confirmsWhenStockIsSufficient() {
        OrderService service = new OrderService(failingFirst(0, 10), 3);
        OrderResult r = service.placeOrder("A", 4);
        assertThat(r.status()).isEqualTo(OrderResult.Status.CONFIRMED);
        assertThat(r.sku()).isEqualTo("A");
        assertThat(r.quantity()).isEqualTo(4);
    }

    @Test
    void rejectsWithoutRetryWhenStockIsTooLow() {
        OrderService service = new OrderService(failingFirst(0, 1), 3);
        assertThat(service.placeOrder("A", 4).status()).isEqualTo(OrderResult.Status.REJECTED_OUT_OF_STOCK);
        assertThat(calls.get()).isEqualTo(1);
    }

    @Test
    void retriesTransientFailures() {
        OrderService service = new OrderService(failingFirst(2, 10), 3);
        assertThat(service.placeOrder("A", 1).status()).isEqualTo(OrderResult.Status.CONFIRMED);
        assertThat(calls.get()).isEqualTo(3);
    }

    @Test
    void degradesToPendingWhenInventoryStaysDown() {
        OrderService service = new OrderService(failingFirst(99, 10), 3);
        assertThat(service.placeOrder("A", 1).status()).isEqualTo(OrderResult.Status.PENDING_INVENTORY_UNAVAILABLE);
        assertThat(calls.get()).isEqualTo(3);
    }

    @Test
    void otherExceptionsPropagateImmediately() {
        OrderService service = new OrderService(sku -> {
            calls.incrementAndGet();
            throw new IllegalStateException("bug");
        }, 3);
        assertThatThrownBy(() -> service.placeOrder("A", 1)).isInstanceOf(IllegalStateException.class);
        assertThat(calls.get()).isEqualTo(1);
    }

    @Test
    void rejectsNonPositiveQuantity() {
        OrderService service = new OrderService(failingFirst(0, 10), 3);
        assertThatThrownBy(() -> service.placeOrder("A", 0)).isInstanceOf(IllegalArgumentException.class);
    }
}
