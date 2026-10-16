package com.javaprep.day28.task02;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@ComponentScan
public class GatewayConfig {

    // TODO(Day28-task02): mark this bean as the default choice when a PaymentGateway is injected without a qualifier
    @Bean("stripe")
    public PaymentGateway stripe() {
        return new SimpleGateway("stripe");
    }

    @Bean("paypal")
    public PaymentGateway paypal() {
        return new SimpleGateway("paypal");
    }
}
