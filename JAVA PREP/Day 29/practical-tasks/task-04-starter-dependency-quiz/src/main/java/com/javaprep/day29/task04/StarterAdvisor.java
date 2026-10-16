package com.javaprep.day29.task04;

import java.util.List;

/** A tiny "which starter do I need?" advisor. */
public final class StarterAdvisor {

    private StarterAdvisor() {
    }

    /**
     * Maps a use case (case-insensitive, trimmed) to a starter artifactId:
     * "rest api" -> spring-boot-starter-web, "jpa" -> spring-boot-starter-data-jpa, "security" -> spring-boot-starter-security,
     * "validation" -> spring-boot-starter-validation, "metrics" -> spring-boot-starter-actuator, "testing" -> spring-boot-starter-test,
     * "aop" -> spring-boot-starter-aop, "cache" -> spring-boot-starter-cache, "jdbc" -> spring-boot-starter-jdbc.
     * Unknown or null use case -> IllegalArgumentException.
     */
    public static String starterFor(String useCase) {
        // TODO(Day29-task04): implement the mapping (a Map<String,String> constant is fine)
        throw new UnsupportedOperationException("TODO(Day29-task04): implement starterFor");
    }

    /** True for "spring-boot-starter" and "spring-boot-starter-<lowercase-words-with-dashes>"; false for null/anything else. */
    public static boolean isStarterName(String artifactId) {
        // TODO(Day29-task04): validate with a regex
        throw new UnsupportedOperationException("TODO(Day29-task04): implement isStarterName");
    }

    /**
     * Notable transitive libraries (artifactIds):
     * spring-boot-starter-web -> [spring-boot-starter-tomcat, spring-boot-starter-json, spring-webmvc]
     * spring-boot-starter-data-jpa -> [hibernate-core, spring-boot-starter-jdbc, spring-data-jpa]
     * spring-boot-starter-test -> [junit-jupiter, mockito-core, assertj-core]
     * any other valid starter -> empty list; a non-starter name -> IllegalArgumentException.
     */
    public static List<String> typicalTransitives(String starter) {
        // TODO(Day29-task04): implement
        throw new UnsupportedOperationException("TODO(Day29-task04): implement typicalTransitives");
    }
}
