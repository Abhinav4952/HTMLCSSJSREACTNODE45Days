package com.javaprep.day28.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.core.env.MapPropertySource;

class PricingConfigTest {

    private static AnnotationConfigApplicationContext context(Map<String, Object> props) {
        AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext();
        ctx.getEnvironment().getPropertySources().addFirst(new MapPropertySource("test", props));
        ctx.register(PricingConfig.class);
        ctx.refresh();
        return ctx;
    }

    @Test
    void defaultRateIsTwentyPercent() {
        try (AnnotationConfigApplicationContext ctx = context(Map.of())) {
            assertThat(ctx.getBean(TaxPolicy.class).rate()).isEqualTo(0.2);
            assertThat(ctx.getBean(PriceCalculator.class).priceWithTax(1000)).isEqualTo(1200);
        }
    }

    @Test
    void rateComesFromTheEnvironment() {
        try (AnnotationConfigApplicationContext ctx = context(Map.of("tax.rate", "0.1"))) {
            assertThat(ctx.getBean(PriceCalculator.class).priceWithTax(1000)).isEqualTo(1100);
        }
    }

    @Test
    void invalidRateFailsContextStartup() {
        assertThatThrownBy(() -> context(Map.of("tax.rate", "1.5")))
                .hasRootCauseInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void calculatorUsesTheSameTaxPolicyBean() {
        try (AnnotationConfigApplicationContext ctx = context(Map.of("tax.rate", "0.5"))) {
            assertThat(ctx.getBean(PriceCalculator.class).priceWithTax(200)).isEqualTo(300);
        }
    }
}
