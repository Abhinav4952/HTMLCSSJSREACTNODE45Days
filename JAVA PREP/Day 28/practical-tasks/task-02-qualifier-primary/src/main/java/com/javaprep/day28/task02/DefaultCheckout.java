package com.javaprep.day28.task02;

import org.springframework.stereotype.Service;

/** Uses whichever gateway is @Primary. */
@Service
public class DefaultCheckout {

    private final PaymentGateway gateway;

    public DefaultCheckout(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    /** "<gateway name>:<cents>"; cents &lt;= 0 -> IllegalArgumentException. */
    public String pay(int cents) {
        // TODO(Day28-task02): delegate to the injected gateway
        throw new UnsupportedOperationException("TODO(Day28-task02): implement pay");
    }
}
