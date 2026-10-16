package com.javaprep.day23.task02;

/** Provided collaborator: stock reservation. */
public interface InventoryClient {

    boolean reserve(String sku, int quantity);

    void release(String sku, int quantity);
}
