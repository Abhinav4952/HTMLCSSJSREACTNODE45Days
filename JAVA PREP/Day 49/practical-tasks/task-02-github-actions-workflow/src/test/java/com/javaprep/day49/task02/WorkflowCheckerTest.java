package com.javaprep.day49.task02;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;

class WorkflowCheckerTest {

    private static final String GOOD = """
            name: CI
            on:
              push:
                branches: [main]
              pull_request:
            jobs:
              build:
                runs-on: ubuntu-latest
                steps:
                  - uses: actions/checkout@v4
                  - uses: actions/setup-java@v4
                    with:
                      distribution: temurin
                      java-version: '21'
                      cache: maven
                  - run: mvn -B verify
            """;

    private final WorkflowChecker checker = new WorkflowChecker();

    @Test
    void completeWorkflowHasNothingMissing() {
        assertThat(checker.missingPieces(GOOD)).isEmpty();
    }

    @Test
    void emptyWorkflowMissesEverything() {
        assertThat(checker.missingPieces("name: CI\n")).containsExactly("trigger:push", "trigger:pull_request",
                "checkout", "setup-java", "java-21", "maven-cache", "maven-build");
    }

    @Test
    void oldJavaVersionIsDetected() {
        assertThat(checker.missingPieces(GOOD.replace("'21'", "'17'"))).containsExactly("java-21");
    }

    @Test
    void missingCacheIsDetected() {
        assertThat(checker.missingPieces(GOOD.replace("cache: maven", ""))).containsExactly("maven-cache");
    }

    @Test
    void testCommandAlsoCountsAsBuild() {
        assertThat(checker.missingPieces(GOOD.replace("mvn -B verify", "mvn test"))).isEmpty();
        assertThat(checker.missingPieces(GOOD.replace("mvn -B verify", "echo hello"))).containsExactly("maven-build");
    }

    @Test
    void yourWorkflowFileIsAcceptable() throws IOException {
        String yaml = Files.readString(Path.of("ci", "ci.yml"));
        assertThat(checker.missingPieces(yaml)).as("pieces missing from ci/ci.yml").isEmpty();
    }
}
