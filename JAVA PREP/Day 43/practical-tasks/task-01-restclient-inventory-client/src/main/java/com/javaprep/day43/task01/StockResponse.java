package com.javaprep.day43.task01;

/** PROVIDED. JSON body returned by the Inventory service. */
public record StockResponse(String sku, int available) {
}
