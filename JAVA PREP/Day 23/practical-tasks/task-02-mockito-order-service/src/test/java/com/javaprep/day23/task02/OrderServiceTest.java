package com.javaprep.day23.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.inOrder;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.verifyNoMoreInteractions;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InOrder;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    PaymentGateway gateway;
    @Mock
    InventoryClient inventory;
    @Mock
    NotificationSender notifier;

    OrderService service;

    @BeforeEach
    void setUp() {
        service = new OrderService(gateway, inventory, notifier);
    }

    @Test
    void r1_invalidInputTouchesNoCollaborator() {
        assertThatThrownBy(() -> service.placeOrder("c1", "sku", 0, 100)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.placeOrder("c1", "sku", -3, 100)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.placeOrder("c1", "sku", 1, 0)).isInstanceOf(IllegalArgumentException.class);
        verifyNoInteractions(gateway, inventory, notifier);
    }

    @Test
    void r2_outOfStockDoesNotChargeOrNotify() {
        when(inventory.reserve("sku-1", 2)).thenReturn(false);

        assertThat(service.placeOrder("c1", "sku-1", 2, 1_000)).isEqualTo(OrderService.Outcome.OUT_OF_STOCK);

        verify(inventory).reserve("sku-1", 2);
        verifyNoMoreInteractions(inventory);
        verifyNoInteractions(gateway, notifier);
    }

    @Test
    void r3_chargesQuantityTimesPriceAndConfirms() {
        when(inventory.reserve("sku-1", 3)).thenReturn(true);
        when(gateway.charge("c1", 3_000_000_000L)).thenReturn(new PaymentGateway.PaymentResult(true, "p-1"));

        assertThat(service.placeOrder("c1", "sku-1", 3, 1_000_000_000L)).isEqualTo(OrderService.Outcome.CONFIRMED);

        ArgumentCaptor<String> message = ArgumentCaptor.forClass(String.class);
        verify(notifier).send(eq("c1"), message.capture());
        assertThat(message.getValue()).isEqualTo("Order confirmed: sku-1 x3");
        verify(inventory, never()).release(anyString(), anyInt());
    }

    @Test
    void r3_declinedPaymentReleasesStockAndNotifies() {
        when(inventory.reserve("sku-1", 2)).thenReturn(true);
        when(gateway.charge("c1", 2_000L)).thenReturn(new PaymentGateway.PaymentResult(false, null));

        assertThat(service.placeOrder("c1", "sku-1", 2, 1_000)).isEqualTo(OrderService.Outcome.PAYMENT_FAILED);

        verify(inventory).release("sku-1", 2);
        verify(notifier).send("c1", "Payment failed: sku-1");
    }

    @Test
    void r3_gatewayOutageIsTreatedAsPaymentFailure() {
        when(inventory.reserve("sku-1", 1)).thenReturn(true);
        when(gateway.charge(anyString(), anyLong())).thenThrow(new IllegalStateException("gateway down"));

        assertThat(service.placeOrder("c1", "sku-1", 1, 500)).isEqualTo(OrderService.Outcome.PAYMENT_FAILED);

        verify(inventory).release("sku-1", 1);
        verify(notifier).send("c1", "Payment failed: sku-1");
        verify(gateway, never()).refund(any());
    }

    @Test
    void r4_notificationFailureDoesNotUndoTheOrder() {
        when(inventory.reserve("sku-1", 1)).thenReturn(true);
        when(gateway.charge("c1", 500L)).thenReturn(new PaymentGateway.PaymentResult(true, "p-9"));
        doThrow(new IllegalStateException("smtp down")).when(notifier).send(anyString(), anyString());

        assertThat(service.placeOrder("c1", "sku-1", 1, 500)).isEqualTo(OrderService.Outcome.CONFIRMED);

        verify(inventory, never()).release(anyString(), anyInt());
        verify(gateway, never()).refund(any());
    }

    @Test
    void r4_stockIsReservedBeforeThePaymentIsTaken() {
        when(inventory.reserve("sku-1", 1)).thenReturn(true);
        when(gateway.charge("c1", 500L)).thenReturn(new PaymentGateway.PaymentResult(true, "p-9"));

        service.placeOrder("c1", "sku-1", 1, 500);

        InOrder order = inOrder(inventory, gateway, notifier);
        order.verify(inventory).reserve("sku-1", 1);
        order.verify(gateway).charge("c1", 500L);
        order.verify(notifier).send(eq("c1"), anyString());
    }

    @Test
    void r5_cancelRefundsThenReleasesThenNotifies() {
        service.cancel("c1", "p-77", "sku-9", 2);

        InOrder order = inOrder(gateway, inventory, notifier);
        order.verify(gateway).refund("p-77");
        order.verify(inventory).release("sku-9", 2);
        order.verify(notifier).send("c1", "Order cancelled: sku-9");
        verifyNoMoreInteractions(gateway, inventory, notifier);
    }
}
