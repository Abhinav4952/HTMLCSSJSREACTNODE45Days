package com.javaprep.day45.task02;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** PROVIDED. Exposes the shared collector bean. */
@Configuration
public class ReceivedConfig {

    @Bean
    public ReceivedEvents receivedEvents() {
        return new ReceivedEvents();
    }
}
