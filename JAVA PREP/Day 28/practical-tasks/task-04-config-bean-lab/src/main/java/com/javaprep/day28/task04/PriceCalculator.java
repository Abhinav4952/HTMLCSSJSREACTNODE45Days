package com.javaprep.day28.task04;

/** PROVIDED. */
public class PriceCalculator {
    private final TaxPolicy taxPolicy;

    public PriceCalculator(TaxPolicy taxPolicy) {
        this.taxPolicy = taxPolicy;
    }

    public long priceWithTax(long cents) {
        return Math.round(cents * (1 + taxPolicy.rate()));
    }
}
