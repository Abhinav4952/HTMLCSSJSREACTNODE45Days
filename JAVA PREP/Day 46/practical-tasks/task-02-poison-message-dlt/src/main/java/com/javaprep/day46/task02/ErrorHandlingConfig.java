package com.javaprep.day46.task02;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.listener.DefaultErrorHandler;

@Configuration
public class ErrorHandlingConfig {

    /**
     * Retry a failing record 2 more times (3 deliveries in total) with a 10 ms pause, then publish it to the
     * dead-letter topic "<original>.DLT" and move on. Boot wires a CommonErrorHandler bean into the listener factory.
     */
    @Bean
    public DefaultErrorHandler errorHandler(KafkaTemplate<Object, Object> template) {
        // TODO(Day46-task02): DeadLetterPublishingRecoverer(template) + FixedBackOff(10L, 2L) -> new DefaultErrorHandler(recoverer, backOff)
        throw new UnsupportedOperationException("TODO(Day46-task02): implement errorHandler");
    }
}
