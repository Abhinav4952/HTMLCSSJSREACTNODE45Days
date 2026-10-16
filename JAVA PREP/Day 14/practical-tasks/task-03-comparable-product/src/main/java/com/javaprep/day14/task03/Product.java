package com.javaprep.day14.task03;

import java.util.Objects;

/** Catalog item. Natural order = SKU; equals/hashCode = SKU (consistent with compareTo). */
public final class Product implements Comparable<Product> {

    private final String sku;
    private final String name;
    private final long priceCents;

    public Product(String sku, String name, long priceCents) {
        // TODO(Day14-task03): validate (blank/null sku or name, negative price -> IllegalArgumentException) then store the fields
        throw new UnsupportedOperationException("TODO(Day14-task03): constructor");
    }

    public String sku() {
        return sku;
    }

    public String name() {
        return name;
    }

    public long priceCents() {
        return priceCents;
    }

    @Override
    public int compareTo(Product other) {
        // TODO(Day14-task03): compare by sku using String.compareTo (no subtraction); must be consistent with equals
        throw new UnsupportedOperationException("TODO(Day14-task03): compareTo");
    }

    @Override
    public boolean equals(Object o) {
        // TODO(Day14-task03): equal when the other object is a Product with the same sku
        throw new UnsupportedOperationException("TODO(Day14-task03): equals");
    }

    @Override
    public int hashCode() {
        // TODO(Day14-task03): derive from sku only
        throw new UnsupportedOperationException("TODO(Day14-task03): hashCode");
    }

    @Override
    public String toString() {
        return sku + ":" + name + "@" + priceCents;
    }
}
