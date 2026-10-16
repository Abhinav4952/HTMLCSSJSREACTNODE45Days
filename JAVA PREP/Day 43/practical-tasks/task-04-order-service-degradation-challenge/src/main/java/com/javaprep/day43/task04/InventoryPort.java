package com.javaprep.day43.task04;

/** PROVIDED. Port to the inventory service (may throw InventoryUnavailableException). */
public interface InventoryPort {

    int available(String sku);
}
