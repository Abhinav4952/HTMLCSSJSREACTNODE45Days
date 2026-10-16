package com.javaprep.day23.task02;

/** Orchestrates stock, payment, and notification. */
public final class OrderService {

    /** Result of {@link #placeOrder(String, String, int, long)}. */
    public enum Outcome { CONFIRMED, OUT_OF_STOCK, PAYMENT_FAILED }

    private final PaymentGateway payments;
    private final InventoryClient inventory;
    private final NotificationSender notifier;

    public OrderService(PaymentGateway payments, InventoryClient inventory, NotificationSender notifier) {
        this.payments = payments;
        this.inventory = inventory;
        this.notifier = notifier;
    }

    public Outcome placeOrder(String customerId, String sku, int quantity, long unitPriceCents) {
        // TODO(Day23-task02): validate qty/price (IAE, no calls); reserve; false -> OUT_OF_STOCK; charge qty*price in try/catch(RuntimeException); failure/decline -> release stock + notify 'Payment failed: <sku>' + PAYMENT_FAILED; success -> notify 'Order confirmed: <sku> x<qty>' (swallow RuntimeException from notifier) + CONFIRMED
        throw new UnsupportedOperationException("TODO(Day23-task02): placeOrder");
    }

    public void cancel(String customerId, String paymentId, String sku, int quantity) {
        // TODO(Day23-task02): payments.refund(paymentId); inventory.release(sku, quantity); notify 'Order cancelled: <sku>' (in exactly this order)
        throw new UnsupportedOperationException("TODO(Day23-task02): cancel");
    }

    private void notifySafely(String customerId, String message) {
        try {
            notifier.send(customerId, message);
        } catch (RuntimeException ignored) {
            // notification problems must never undo an order
        }
    }
}
