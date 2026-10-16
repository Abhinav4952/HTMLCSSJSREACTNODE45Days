package com.javaprep.day29.task02;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class ProfileGreetingTest {

    private static AnnotationConfigApplicationContext start(String... profiles) {
        AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext();
        ctx.getEnvironment().setActiveProfiles(profiles);
        ctx.register(ProfileConfig.class);
        ctx.refresh();
        return ctx;
    }

    @Test
    void devProfileUsesDevGreeting() {
        try (AnnotationConfigApplicationContext ctx = start("dev")) {
            assertThat(ctx.getBean(GreetingProvider.class).greeting()).isEqualTo("Hello from DEV");
        }
    }

    @Test
    void prodProfileUsesProdGreeting() {
        try (AnnotationConfigApplicationContext ctx = start("prod")) {
            assertThat(ctx.getBean(GreetingProvider.class).greeting()).isEqualTo("Hello from PROD");
        }
    }

    @Test
    void noProfileMeansNoGreetingBean() {
        try (AnnotationConfigApplicationContext ctx = start()) {
            assertThat(ctx.getBeansOfType(GreetingProvider.class)).isEmpty();
        }
    }
}
