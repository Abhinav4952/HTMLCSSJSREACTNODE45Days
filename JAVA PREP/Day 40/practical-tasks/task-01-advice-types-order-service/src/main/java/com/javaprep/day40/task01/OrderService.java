package com.javaprep.day40.task01;

import org.springframework.stereotype.Service;

/** PROVIDED target bean. */
@Service
public class OrderService {

    public String place(String item) {
        return "order:" + item;
    }

    public void fail() {
        throw new IllegalStateException("boom");
    }
}
