package com.javaprep.day43.task04;

public class OrderService {

    private final InventoryPort inventory;
    private final int maxAttempts;

    public OrderService(InventoryPort inventory, int maxAttempts) {
        this.inventory = inventory;
        this.maxAttempts = maxAttempts;
    }

    /**
     * Rules:
     * <ol>
     *   <li>qty &lt;= 0 -> IllegalArgumentException</li>
     *   <li>Ask inventory for the stock; retry ONLY on {@link InventoryUnavailableException}, up to maxAttempts calls in total</li>
     *   <li>stock &gt;= qty -> CONFIRMED; stock &lt; qty -> REJECTED_OUT_OF_STOCK (inventory called once)</li>
     *   <li>still unavailable after all attempts -> PENDING_INVENTORY_UNAVAILABLE (graceful degradation, no exception)</li>
     *   <li>any other exception propagates immediately</li>
     * </ol>
     */
    public OrderResult placeOrder(String sku, int qty) {
        // TODO(Day43-task04): implement the rules above (hand-written loop or Resilience4j Retry)
        throw new UnsupportedOperationException("TODO(Day43-task04): implement placeOrder");
    }
}
