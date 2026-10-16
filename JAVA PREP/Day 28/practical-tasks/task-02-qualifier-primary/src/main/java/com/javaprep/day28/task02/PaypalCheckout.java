package com.javaprep.day28.task02;

import org.springframework.stereotype.Service;

/** Must always use the "paypal" gateway, regardless of @Primary. */
@Service
public class PaypalCheckout {

    private final PaymentGateway gateway;

    // TODO(Day28-task02): select the bean named "paypal" for this parameter (@Qualifier)
    public PaypalCheckout(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    /** "<gateway name>:<cents>"; cents &lt;= 0 -> IllegalArgumentException. */
    public String pay(int cents) {
        // TODO(Day28-task02): delegate to the injected gateway
        throw new UnsupportedOperationException("TODO(Day28-task02): implement pay");
    }
}
