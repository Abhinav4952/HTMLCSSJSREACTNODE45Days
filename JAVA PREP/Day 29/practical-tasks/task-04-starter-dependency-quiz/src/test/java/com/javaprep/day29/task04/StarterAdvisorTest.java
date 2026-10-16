package com.javaprep.day29.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class StarterAdvisorTest {

    @ParameterizedTest
    @CsvSource({"rest api,spring-boot-starter-web", "JPA,spring-boot-starter-data-jpa", "  security ,spring-boot-starter-security",
            "validation,spring-boot-starter-validation", "metrics,spring-boot-starter-actuator", "testing,spring-boot-starter-test",
            "aop,spring-boot-starter-aop", "cache,spring-boot-starter-cache", "jdbc,spring-boot-starter-jdbc"})
    void mapsUseCases(String useCase, String starter) {
        assertThat(StarterAdvisor.starterFor(useCase)).isEqualTo(starter);
    }

    @Test
    void unknownUseCaseIsRejected() {
        assertThatThrownBy(() -> StarterAdvisor.starterFor("quantum")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> StarterAdvisor.starterFor(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void recognizesStarterNames() {
        assertThat(StarterAdvisor.isStarterName("spring-boot-starter")).isTrue();
        assertThat(StarterAdvisor.isStarterName("spring-boot-starter-web")).isTrue();
        assertThat(StarterAdvisor.isStarterName("spring-boot-starter-data-jpa")).isTrue();
        assertThat(StarterAdvisor.isStarterName("spring-boot-web")).isFalse();
        assertThat(StarterAdvisor.isStarterName("spring-boot-starter-")).isFalse();
        assertThat(StarterAdvisor.isStarterName("Spring-Boot-Starter-Web")).isFalse();
        assertThat(StarterAdvisor.isStarterName(null)).isFalse();
    }

    @Test
    void transitives() {
        assertThat(StarterAdvisor.typicalTransitives("spring-boot-starter-web"))
                .containsExactly("spring-boot-starter-tomcat", "spring-boot-starter-json", "spring-webmvc");
        assertThat(StarterAdvisor.typicalTransitives("spring-boot-starter-data-jpa")).contains("hibernate-core");
        assertThat(StarterAdvisor.typicalTransitives("spring-boot-starter-cache")).isEmpty();
        assertThatThrownBy(() -> StarterAdvisor.typicalTransitives("guava")).isInstanceOf(IllegalArgumentException.class);
    }
}
