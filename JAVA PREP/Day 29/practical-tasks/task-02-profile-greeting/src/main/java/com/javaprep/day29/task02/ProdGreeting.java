package com.javaprep.day29.task02;

import org.springframework.stereotype.Component;

// TODO(Day29-task02): this bean must exist ONLY when the "prod" profile is active (@Profile)
@Component
public class ProdGreeting implements GreetingProvider {
    @Override
    public String greeting() {
        // TODO(Day29-task02): return "Hello from PROD"
        throw new UnsupportedOperationException("TODO(Day29-task02): implement ProdGreeting.greeting");
    }
}
