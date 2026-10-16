package com.javaprep.day29.task02;

import org.springframework.stereotype.Component;

// TODO(Day29-task02): this bean must exist ONLY when the "dev" profile is active (@Profile)
@Component
public class DevGreeting implements GreetingProvider {
    @Override
    public String greeting() {
        // TODO(Day29-task02): return "Hello from DEV"
        throw new UnsupportedOperationException("TODO(Day29-task02): implement DevGreeting.greeting");
    }
}
