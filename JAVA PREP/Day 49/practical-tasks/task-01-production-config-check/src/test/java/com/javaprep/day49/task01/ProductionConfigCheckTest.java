package com.javaprep.day49.task01;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.Test;

class ProductionConfigCheckTest {

    private final ProductionConfigCheck check = new ProductionConfigCheck();

    private Map<String, String> valid() {
        Map<String, String> env = new HashMap<>();
        env.put("DB_URL", "jdbc:postgresql://db.internal:5432/app");
        env.put("DB_USERNAME", "app_user");
        env.put("DB_PASSWORD", "9f3b-Long-Random-Value");
        env.put("JWT_SECRET", "x".repeat(40));
        env.put("SPRING_PROFILES_ACTIVE", "prod");
        return env;
    }

    @Test
    void validEnvironmentHasNoProblems() {
        assertThat(check.problems(valid())).isEmpty();
    }

    @Test
    void missingAndBlankKeysAreReportedInOrder() {
        Map<String, String> env = valid();
        env.remove("DB_URL");
        env.put("JWT_SECRET", "   ");
        assertThat(check.problems(env)).containsExactly("MISSING:DB_URL", "MISSING:JWT_SECRET");
    }

    @Test
    void badUrlAndWeakSecretsAreReported() {
        Map<String, String> env = valid();
        env.put("DB_URL", "jdbc:h2:mem:test");
        env.put("DB_PASSWORD", "ChangeMe");
        env.put("JWT_SECRET", "short");
        assertThat(check.problems(env)).containsExactly("BAD_DB_URL", "WEAK:DB_PASSWORD", "WEAK:JWT_SECRET");
    }

    @Test
    void wrongOrMissingProfileIsReported() {
        Map<String, String> env = valid();
        env.put("SPRING_PROFILES_ACTIVE", "dev");
        assertThat(check.problems(env)).containsExactly("PROFILE_NOT_PROD");
        env.remove("SPRING_PROFILES_ACTIVE");
        assertThat(check.problems(env)).containsExactly("PROFILE_NOT_PROD");
    }

    @Test
    void missingPasswordIsOnlyReportedAsMissing() {
        Map<String, String> env = valid();
        env.remove("DB_PASSWORD");
        assertThat(check.problems(env)).containsExactly("MISSING:DB_PASSWORD");
    }
}
