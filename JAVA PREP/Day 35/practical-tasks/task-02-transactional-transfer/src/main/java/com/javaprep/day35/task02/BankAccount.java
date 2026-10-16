package com.javaprep.day35.task02;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.util.*;

@Entity
@Table(name = "bank_accounts")
public class BankAccount {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String owner;

    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal balance;

    protected BankAccount() {
    }

    public BankAccount(String owner, String balance) {
        this.owner = owner;
        this.balance = new BigDecimal(balance);
    }

    public Long getId() {
        return id;
    }

    public String getOwner() {
        return owner;
    }

    public BigDecimal getBalance() {
        return balance;
    }

    public void setBalance(BigDecimal balance) {
        this.balance = balance;
    }
}
