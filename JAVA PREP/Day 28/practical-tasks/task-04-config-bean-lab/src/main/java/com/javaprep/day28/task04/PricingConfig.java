package com.javaprep.day28.task04;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class PricingConfig {

    /** Rate from property {@code tax.rate}, default 0.2. A rate outside [0, 1] -> IllegalArgumentException. */
    @Bean
    // TODO(Day28-task04): inject the property: add @Value("${tax.rate:0.2}") to the parameter
    public TaxPolicy taxPolicy(double rate) {
        // TODO(Day28-task04): validate the rate and return the policy
        throw new UnsupportedOperationException("TODO(Day28-task04): implement taxPolicy");
    }

    @Bean
    public PriceCalculator priceCalculator(TaxPolicy taxPolicy) {
        // TODO(Day28-task04): wire the calculator with the policy bean
        throw new UnsupportedOperationException("TODO(Day28-task04): implement priceCalculator");
    }
}
