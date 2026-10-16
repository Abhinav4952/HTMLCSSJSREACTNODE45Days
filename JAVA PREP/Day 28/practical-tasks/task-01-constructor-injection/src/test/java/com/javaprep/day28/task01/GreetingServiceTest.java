package com.javaprep.day28.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class GreetingServiceTest {

    @Test
    void greetsUsingTheInjectedRepository() {
        GreetingService service = new GreetingServiceImpl(() -> "Hi");
        assertThat(service.greet("Ada")).isEqualTo("Hi, Ada!");
    }

    @Test
    void rejectsBlankNames() {
        GreetingService service = new GreetingServiceImpl(() -> "Hi");
        assertThatThrownBy(() -> service.greet(" ")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.greet(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void containerWiresTheServiceWithConstructorInjection() {
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class)) {
            assertThat(ctx.getBeansOfType(GreetingService.class)).hasSize(1);
            assertThat(ctx.getBean(GreetingService.class).greet("Ada")).isEqualTo("Hello, Ada!");
        }
    }
}
