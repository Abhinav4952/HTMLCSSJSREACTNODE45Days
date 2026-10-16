package com.javaprep.day34.task02;

import jakarta.persistence.*;
import java.util.*;

@Entity
@Table(name = "purchase_orders")
public class PurchaseOrder {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String reference;

    // TODO(Day34-task02): owning side: many-to-one, LAZY, join column customer_id, not nullable
    private Customer customer;

    protected PurchaseOrder() {
    }

    public PurchaseOrder(String reference) {
        this.reference = reference;
    }

    public Long getId() {
        return id;
    }

    public String getReference() {
        return reference;
    }

    public Customer getCustomer() {
        return customer;
    }

    void setCustomer(Customer customer) {
        this.customer = customer;
    }
}
