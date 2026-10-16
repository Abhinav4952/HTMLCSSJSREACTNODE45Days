package com.javaprep.day39.task02;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import java.math.BigDecimal;

@Entity
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String sku;
    private String category;
    private BigDecimal price;

    protected Product() {
    }

    public Product(String sku, String category, String price) {
        this.sku = sku;
        this.category = category;
        this.price = new BigDecimal(price);
    }

    public Long getId() { return id; }
    public String getSku() { return sku; }
    public String getCategory() { return category; }
    public BigDecimal getPrice() { return price; }
}
