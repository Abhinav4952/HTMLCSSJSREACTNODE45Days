package com.javaprep.day41.task01;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class OrderProcessor {

    private static final Logger log = LoggerFactory.getLogger(OrderProcessor.class);

    /**
     * Logging contract (use PARAMETERIZED messages, never string concatenation):
     *  1. INFO  "Processing order {} (amount={})"      args: orderId, amount
     *  2. amount <= 0  -> ERROR "Invalid amount for order {}" with args (orderId, exception) where exception is a
     *                     new IllegalArgumentException("amount must be positive"); return false
     *  3. amount > 1000 -> WARN "Large order {}"        arg: orderId
     *  4. DEBUG "Order {} validated"                    arg: orderId   (emitted only when DEBUG is enabled)
     *  5. return true
     */
    public boolean process(String orderId, double amount) {
        // TODO(Day41-task01): implement the logging contract
        throw new UnsupportedOperationException("TODO(Day41-task01): implement the logging contract");
    }
}
