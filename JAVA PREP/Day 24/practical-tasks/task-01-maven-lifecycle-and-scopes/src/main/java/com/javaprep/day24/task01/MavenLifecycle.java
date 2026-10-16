package com.javaprep.day24.task01;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;

/** Models Maven's built-in lifecycles. */
public final class MavenLifecycle {

    public static final List<String> CLEAN = List.of("pre-clean", "clean", "post-clean");

    public static final List<String> DEFAULT = List.of(
            "validate", "initialize", "generate-sources", "process-sources", "generate-resources", "process-resources",
            "compile", "process-classes", "generate-test-sources", "process-test-sources", "generate-test-resources",
            "process-test-resources", "test-compile", "process-test-classes", "test", "prepare-package", "package",
            "pre-integration-test", "integration-test", "post-integration-test", "verify", "install", "deploy");

    public static final List<String> SITE = List.of("pre-site", "site", "post-site", "site-deploy");

    private MavenLifecycle() {
    }

    public static List<String> phasesUpTo(String phase) {
        // TODO(Day24-task01): null/blank/unknown -> IllegalArgumentException; find the lifecycle (CLEAN, DEFAULT, SITE) containing the phase and return a copy of its phases from the start up to and including it
        throw new UnsupportedOperationException("TODO(Day24-task01): phasesUpTo");
    }

    public static List<String> plan(String... phases) {
        // TODO(Day24-task01): no arguments -> IllegalArgumentException; for each requested phase add phasesUpTo(phase) to a LinkedHashSet (keeps order, drops duplicates); return it as a List
        throw new UnsupportedOperationException("TODO(Day24-task01): plan");
    }

    public static Optional<String> boundGoal(String packaging, String phase) {
        // TODO(Day24-task01): packaging must be jar, war or pom and phase must be in DEFAULT (else IllegalArgumentException); pom binds only install:install and deploy:deploy; jar/war bind process-resources=resources:resources, compile=compiler:compile, process-test-resources=resources:testResources, test-compile=compiler:testCompile, test=surefire:test, package=jar:jar (war:war for war), install=install:install, deploy=deploy:deploy; everything else Optional.empty()
        throw new UnsupportedOperationException("TODO(Day24-task01): boundGoal");
    }
}
