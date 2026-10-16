package com.javaprep.day24.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class PomReaderTest {

    private static final String POM = """
            <project>
              <modelVersion>4.0.0</modelVersion>
              <groupId>com.acme</groupId>
              <artifactId>demo</artifactId>
              <version>1.2.0</version>
              <properties>
                <junit.version>5.11.4</junit.version>
                <slf4j.version>2.0.16</slf4j.version>
              </properties>
              <dependencyManagement>
                <dependencies>
                  <dependency>
                    <groupId>org.managed</groupId>
                    <artifactId>only-managed</artifactId>
                    <version>9.9.9</version>
                  </dependency>
                </dependencies>
              </dependencyManagement>
              <dependencies>
                <dependency>
                  <groupId>org.slf4j</groupId>
                  <artifactId>slf4j-api</artifactId>
                  <version>${slf4j.version}</version>
                </dependency>
                <dependency>
                  <groupId>org.junit.jupiter</groupId>
                  <artifactId>junit-jupiter</artifactId>
                  <version>${junit.version}</version>
                  <scope>test</scope>
                </dependency>
                <dependency>
                  <groupId>jakarta.servlet</groupId>
                  <artifactId>jakarta.servlet-api</artifactId>
                  <version>6.0.0</version>
                  <scope>provided</scope>
                </dependency>
                <dependency>
                  <groupId>org.postgresql</groupId>
                  <artifactId>postgresql</artifactId>
                  <version>42.7.4</version>
                  <scope>runtime</scope>
                </dependency>
                <dependency>
                  <groupId>com.acme</groupId>
                  <artifactId>shared-model</artifactId>
                  <version>${project.version}</version>
                  <exclusions>
                    <exclusion>
                      <groupId>commons-logging</groupId>
                      <artifactId>commons-logging</artifactId>
                    </exclusion>
                  </exclusions>
                </dependency>
                <dependency>
                  <groupId>org.unresolved</groupId>
                  <artifactId>mystery</artifactId>
                  <version>${no.such.property}</version>
                </dependency>
                <dependency>
                  <groupId>org.managed</groupId>
                  <artifactId>no-version-here</artifactId>
                </dependency>
              </dependencies>
            </project>
            """;

    @Test
    void r4_readsOnlyDirectDependenciesInOrder() {
        List<PomReader.Dependency> deps = PomReader.dependencies(POM);
        assertThat(deps).extracting(PomReader.Dependency::artifactId)
                .containsExactly("slf4j-api", "junit-jupiter", "jakarta.servlet-api", "postgresql", "shared-model", "mystery", "no-version-here");
    }

    @Test
    void r4_resolvesPropertiesAndDefaultsTheScope() {
        List<PomReader.Dependency> deps = PomReader.dependencies(POM);
        assertThat(deps.get(0)).isEqualTo(new PomReader.Dependency("org.slf4j", "slf4j-api", "2.0.16", "compile"));
        assertThat(deps.get(1)).isEqualTo(new PomReader.Dependency("org.junit.jupiter", "junit-jupiter", "5.11.4", "test"));
        assertThat(deps.get(2).scope()).isEqualTo("provided");
        assertThat(deps.get(3).scope()).isEqualTo("runtime");
        assertThat(deps.get(4).version()).as("project.version").isEqualTo("1.2.0");
        assertThat(deps.get(5).version()).as("unresolvable placeholder stays").isEqualTo("${no.such.property}");
        assertThat(deps.get(6).version()).isNull();
    }

    @Test
    void r4_exclusionsAndManagedDependenciesDoNotLeak() {
        List<PomReader.Dependency> deps = PomReader.dependencies(POM);
        assertThat(deps).extracting(PomReader.Dependency::artifactId).doesNotContain("commons-logging", "only-managed");
    }

    @Test
    void r4_pomWithoutDependenciesIsEmpty() {
        assertThat(PomReader.dependencies("<project><modelVersion>4.0.0</modelVersion></project>")).isEmpty();
    }

    @Test
    void r4_malformedAndHostileXmlIsRejected() {
        assertThatThrownBy(() -> PomReader.dependencies("<project><dependencies>")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> PomReader.dependencies("")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> PomReader.dependencies(null)).isInstanceOf(IllegalArgumentException.class);
        String xxe = "<?xml version=\"1.0\"?><!DOCTYPE project [<!ENTITY x SYSTEM \"file:///etc/passwd\">]><project><groupId>&x;</groupId></project>";
        assertThatThrownBy(() -> PomReader.dependencies(xxe)).isInstanceOf(IllegalArgumentException.class);
    }

    @ParameterizedTest(name = "{0} on {1} = {2}")
    @CsvSource({
            "compile,COMPILE,true", "compile,RUNTIME,true", "compile,TEST,true",
            "provided,COMPILE,true", "provided,RUNTIME,false", "provided,TEST,true",
            "runtime,COMPILE,false", "runtime,RUNTIME,true", "runtime,TEST,true",
            "test,COMPILE,false", "test,RUNTIME,false", "test,TEST,true",
            "system,COMPILE,true", "system,RUNTIME,false", "system,TEST,true"
    })
    void r5_scopeTable(String scope, PomReader.ClasspathKind kind, boolean expected) {
        assertThat(PomReader.onClasspath(scope, kind)).isEqualTo(expected);
    }

    @Test
    void r5_unknownScopeIsRejected() {
        assertThatThrownBy(() -> PomReader.onClasspath("import", PomReader.ClasspathKind.COMPILE)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> PomReader.onClasspath(null, PomReader.ClasspathKind.COMPILE)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r5_classpathsForThePom() {
        List<PomReader.Dependency> deps = PomReader.dependencies(POM);
        assertThat(PomReader.classpath(deps, PomReader.ClasspathKind.COMPILE)).containsExactly(
                "org.slf4j:slf4j-api:2.0.16",
                "jakarta.servlet:jakarta.servlet-api:6.0.0",
                "com.acme:shared-model:1.2.0",
                "org.unresolved:mystery:${no.such.property}",
                "org.managed:no-version-here:null");
        assertThat(PomReader.classpath(deps, PomReader.ClasspathKind.RUNTIME)).containsExactly(
                "org.slf4j:slf4j-api:2.0.16",
                "org.postgresql:postgresql:42.7.4",
                "com.acme:shared-model:1.2.0",
                "org.unresolved:mystery:${no.such.property}",
                "org.managed:no-version-here:null");
        assertThat(PomReader.classpath(deps, PomReader.ClasspathKind.TEST)).hasSize(7);
        assertThat(PomReader.classpath(List.of(), PomReader.ClasspathKind.TEST)).isEmpty();
    }
}
