package com.javaprep.day24.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

class MavenLifecycleTest {

    @Test
    void r1_defaultLifecycleHasTwentyThreePhasesInOrder() {
        assertThat(MavenLifecycle.DEFAULT).hasSize(23).startsWith("validate", "initialize").endsWith("verify", "install", "deploy");
        assertThat(MavenLifecycle.DEFAULT.indexOf("compile")).isLessThan(MavenLifecycle.DEFAULT.indexOf("test-compile"));
        assertThat(MavenLifecycle.DEFAULT.indexOf("test")).isLessThan(MavenLifecycle.DEFAULT.indexOf("package"));
    }

    @Test
    void r1_phasesUpToCompile() {
        assertThat(MavenLifecycle.phasesUpTo("compile")).containsExactly(
                "validate", "initialize", "generate-sources", "process-sources", "generate-resources", "process-resources", "compile");
    }

    @Test
    void r1_phasesUpToTestIncludesTestCompileButNotPackage() {
        List<String> phases = MavenLifecycle.phasesUpTo("test");
        assertThat(phases).hasSize(15).endsWith("test-compile", "process-test-classes", "test");
        assertThat(phases).doesNotContain("package", "prepare-package");
    }

    @Test
    void r1_otherLifecycles() {
        assertThat(MavenLifecycle.phasesUpTo("pre-clean")).containsExactly("pre-clean");
        assertThat(MavenLifecycle.phasesUpTo("clean")).containsExactly("pre-clean", "clean");
        assertThat(MavenLifecycle.phasesUpTo("post-clean")).containsExactly("pre-clean", "clean", "post-clean");
        assertThat(MavenLifecycle.phasesUpTo("site")).containsExactly("pre-site", "site");
        assertThat(MavenLifecycle.phasesUpTo("deploy")).hasSize(23);
    }

    @Test
    void r1_returnedListsAreIndependentCopies() {
        List<String> phases = MavenLifecycle.phasesUpTo("compile");
        phases.add("hack");
        assertThat(MavenLifecycle.phasesUpTo("compile")).doesNotContain("hack");
        assertThat(MavenLifecycle.DEFAULT).doesNotContain("hack");
    }

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "build", "Compile", "run"})
    void r1_unknownPhasesAreRejected(String phase) {
        assertThatThrownBy(() -> MavenLifecycle.phasesUpTo(phase)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r1_nullPhaseIsRejected() {
        assertThatThrownBy(() -> MavenLifecycle.phasesUpTo(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r2_cleanPackagePlan() {
        List<String> plan = MavenLifecycle.plan("clean", "package");
        assertThat(plan).hasSize(2 + 17).startsWith("pre-clean", "clean", "validate").endsWith("prepare-package", "package");
        assertThat(plan).doesNotHaveDuplicates();
    }

    @Test
    void r2_overlappingPhasesAreNotRepeated() {
        List<String> plan = MavenLifecycle.plan("package", "test", "compile");
        assertThat(plan).hasSize(17).endsWith("package");
        assertThat(plan).doesNotHaveDuplicates();
        assertThat(MavenLifecycle.plan("test", "package")).isEqualTo(MavenLifecycle.phasesUpTo("package"));
    }

    @Test
    void r2_orderFollowsTheCommandLine() {
        assertThat(MavenLifecycle.plan("site", "clean")).containsExactly("pre-site", "site", "pre-clean", "clean");
    }

    @Test
    void r2_planNeedsAtLeastOnePhase() {
        assertThatThrownBy(() -> MavenLifecycle.plan()).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> MavenLifecycle.plan("compile", "bogus")).isInstanceOf(IllegalArgumentException.class);
    }

    @ParameterizedTest(name = "jar: {0} -> {1}")
    @CsvSource({
            "process-resources,resources:resources",
            "compile,compiler:compile",
            "process-test-resources,resources:testResources",
            "test-compile,compiler:testCompile",
            "test,surefire:test",
            "package,jar:jar",
            "install,install:install",
            "deploy,deploy:deploy"
    })
    void r3_jarBindings(String phase, String goal) {
        assertThat(MavenLifecycle.boundGoal("jar", phase)).contains(goal);
    }

    @ParameterizedTest
    @ValueSource(strings = {"validate", "initialize", "generate-sources", "process-classes", "prepare-package", "integration-test", "verify"})
    void r3_phasesWithoutBindingsAreEmpty(String phase) {
        assertThat(MavenLifecycle.boundGoal("jar", phase)).isEqualTo(Optional.empty());
    }

    @Test
    void r3_warAndPomPackaging() {
        assertThat(MavenLifecycle.boundGoal("war", "package")).contains("war:war");
        assertThat(MavenLifecycle.boundGoal("war", "compile")).contains("compiler:compile");
        assertThat(MavenLifecycle.boundGoal("pom", "compile")).isEmpty();
        assertThat(MavenLifecycle.boundGoal("pom", "test")).isEmpty();
        assertThat(MavenLifecycle.boundGoal("pom", "package")).isEmpty();
        assertThat(MavenLifecycle.boundGoal("pom", "install")).contains("install:install");
        assertThat(MavenLifecycle.boundGoal("pom", "deploy")).contains("deploy:deploy");
    }

    @Test
    void r3_invalidArguments() {
        assertThatThrownBy(() -> MavenLifecycle.boundGoal("ear", "compile")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> MavenLifecycle.boundGoal(null, "compile")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> MavenLifecycle.boundGoal("jar", "clean")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> MavenLifecycle.boundGoal("jar", "nope")).isInstanceOf(IllegalArgumentException.class);
    }
}
