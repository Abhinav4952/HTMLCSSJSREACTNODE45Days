package com.javaprep.day34.task02;

import jakarta.persistence.*;
import java.util.*;

@Entity
@Table(name = "customers")
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    // TODO(Day34-task02): inverse side: mappedBy "customer", cascade ALL, orphanRemoval
    private List<PurchaseOrder> orders = new ArrayList<>();

    protected Customer() {
    }

    public Customer(String name) {
        this.name = name;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public List<PurchaseOrder> getOrders() {
        return orders;
    }

    /** Keep BOTH sides of the association in sync. */
    public void addOrder(PurchaseOrder order) {
        // TODO(Day34-task02): add to the list and set the back reference
        throw new UnsupportedOperationException("TODO(Day34-task02): add to the list and set the back reference");
    }

    /** Keep BOTH sides in sync; orphanRemoval then deletes the row. */
    public void removeOrder(PurchaseOrder order) {
        // TODO(Day34-task02): remove from the list and clear the back reference
        throw new UnsupportedOperationException("TODO(Day34-task02): remove from the list and clear the back reference");
    }
}
