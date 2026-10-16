package com.javaprep.day29.task01;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.bind.Binder;
import org.springframework.boot.context.properties.source.MapConfigurationPropertySource;

class AppPropertiesTest {

    private static AppProperties bind(Map<String, String> map) {
        return new Binder(new MapConfigurationPropertySource(map)).bind("app", AppProperties.class).get();
    }

    @Test
    void bindsScalarsListsAndNestedObjects() {
        AppProperties p = bind(Map.of(
                "app.name", "demo", "app.max-users", "5",
                "app.features[0]", "a", "app.features[1]", "b",
                "app.security.enabled", "true", "app.security.token", "t0k"));
        assertThat(p.getName()).isEqualTo("demo");
        assertThat(p.getMaxUsers()).isEqualTo(5);
        assertThat(p.getFeatures()).containsExactly("a", "b");
        assertThat(p.getSecurity().isEnabled()).isTrue();
        assertThat(p.getSecurity().getToken()).isEqualTo("t0k");
    }

    @Test
    void missingValuesKeepDefaults() {
        AppProperties p = bind(Map.of("app.name", "solo"));
        assertThat(p.getMaxUsers()).isZero();
        assertThat(p.getFeatures()).isEmpty();
        assertThat(p.getSecurity().isEnabled()).isFalse();
    }

    @Test
    void camelCaseKeysAlsoBind() {
        assertThat(bind(Map.of("app.maxUsers", "9", "app.name", "x")).getMaxUsers()).isEqualTo(9);
    }

    @Test
    void summaryDescribesTheBoundValues() {
        AppProperties p = bind(Map.of("app.name", "demo", "app.max-users", "5", "app.features[0]", "a", "app.features[1]", "b"));
        assertThat(p.summary()).isEqualTo("demo (5 users, 2 features)");
    }

    @Test
    void prefixIsDeclaredOnTheClass() {
        assertThat(AppProperties.class.getAnnotation(ConfigurationProperties.class).prefix()).isEqualTo("app");
    }
}
