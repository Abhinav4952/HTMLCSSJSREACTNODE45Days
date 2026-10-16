package com.javaprep.day28.task02;

/** PROVIDED simple implementation. */
public class SimpleGateway implements PaymentGateway {
    private final String name;

    public SimpleGateway(String name) {
        this.name = name;
    }

    @Override
    public String name() {
        return name;
    }
}
