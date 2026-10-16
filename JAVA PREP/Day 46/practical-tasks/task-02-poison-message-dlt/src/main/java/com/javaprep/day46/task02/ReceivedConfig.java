package com.javaprep.day46.task02;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** PROVIDED. */
@Configuration
public class ReceivedConfig {

    @Bean
    public ReceivedEvents receivedEvents() {
        return new ReceivedEvents();
    }
}
