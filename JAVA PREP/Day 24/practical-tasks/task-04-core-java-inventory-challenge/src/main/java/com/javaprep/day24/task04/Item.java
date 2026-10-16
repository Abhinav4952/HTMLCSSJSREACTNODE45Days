package com.javaprep.day24.task04;

/** An inventory line. */
public record Item(String sku, String category, int qty, long priceCents) {

    public Item {
        // TODO(Day24-task04): sku and category must be non-null and non-blank (IllegalArgumentException with a message naming the field); qty >= 0; priceCents >= 0; store the trimmed sku and category
        throw new UnsupportedOperationException("TODO(Day24-task04): validation");
    }

    public long valueCents() {
        return (long) qty * priceCents;
    }
}
