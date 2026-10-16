from common import *

# ---------------------------------------------------------------- shared sample files for the day
CI_SAMPLE = """# Sample GitHub Actions workflow: build and test a Maven project on every push and pull request.
# Copy to .github/workflows/ci.yml in your repository root (adjust working-directory for sub-projects).
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Check out the code
        uses: actions/checkout@v4

      - name: Set up JDK 21
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
          cache: maven

      - name: Build and run tests
        run: mvn -B verify
        # working-directory: backend

      - name: Upload test reports (on failure)
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: surefire-reports
          path: '**/target/surefire-reports/'
"""
CHECKSTYLE = """<?xml version="1.0"?>
<!DOCTYPE module PUBLIC "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN" "https://checkstyle.org/dtds/configuration_1_3.dtd">
<!-- Small teaching ruleset. Wire it into Maven with maven-checkstyle-plugin (see DAY-49 theory). -->
<module name="Checker">
  <property name="severity" value="error"/>
  <module name="NewlineAtEndOfFile"/>
  <module name="FileTabCharacter"/>
  <module name="RegexpSingleline">
    <property name="format" value="\\s+$"/>
    <property name="message" value="Trailing whitespace"/>
  </module>
  <module name="LineLength">
    <property name="max" value="100"/>
    <property name="ignorePattern" value="^package.*|^import.*|a href|href|http://|https://"/>
  </module>
  <module name="TreeWalker">
    <module name="AvoidStarImport"/>
    <module name="UnusedImports"/>
    <module name="RedundantImport"/>
    <module name="NeedBraces"/>
    <module name="EmptyBlock"/>
    <module name="LocalVariableName"/>
    <module name="MemberName"/>
    <module name="MethodName"/>
    <module name="TypeName"/>
    <module name="ConstantName"/>
    <module name="ModifierOrder"/>
    <module name="UpperEll"/>
    <module name="Regexp">
      <property name="format" value="System\\.(out|err)\\.print"/>
      <property name="illegalPattern" value="true"/>
      <property name="message" value="Use a logger instead of System.out/err"/>
    </module>
  </module>
</module>
"""
APP_PROD = """# application-prod.yml (committed: contains NO secrets, only placeholders resolved from the environment)
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate
    open-in-view: false
server:
  port: ${PORT:8080}
  shutdown: graceful
management:
  endpoints:
    web:
      exposure:
        include: health,info
app:
  jwt:
    secret: ${JWT_SECRET}
logging:
  level:
    root: INFO
"""
EXTRA = {
    "Day 49/samples/github-actions-ci.yml": CI_SAMPLE,
    "Day 49/samples/checkstyle.xml": CHECKSTYLE,
    "Day 49/samples/application-prod.yml": APP_PROD,
}

# ---------------------------------------------------------------- task 1
CHECK = r'''package %PKG%;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** Fail-fast validation of the environment a production deployment starts with. */
public class ProductionConfigCheck {

    /**
     * Returns problems in THIS order (empty list = OK):
     * <ol>
     *   <li>for each of DB_URL, DB_USERNAME, DB_PASSWORD, JWT_SECRET (in that order) missing or blank: "MISSING:KEY"</li>
     *   <li>DB_URL present but not starting with "jdbc:postgresql://": "BAD_DB_URL"</li>
     *   <li>DB_PASSWORD present and (case-insensitively) one of password, postgres, changeme, admin: "WEAK:DB_PASSWORD"</li>
     *   <li>JWT_SECRET present but shorter than 32 characters: "WEAK:JWT_SECRET"</li>
     *   <li>SPRING_PROFILES_ACTIVE not exactly "prod" (missing counts): "PROFILE_NOT_PROD"</li>
     * </ol>
     */
    public List<String> problems(Map<String, String> env) {
        // TODO(%TAG%): apply the rules in the stated order
        throw new UnsupportedOperationException("TODO(%TAG%): implement problems");
    }
}
'''
CHECK_TEST = r'''package %PKG%;

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
'''
p1 = task("production-config-check", "Production Configuration Validator", "Warm-up", "Java",
    "Write the fail-fast configuration check that a deployment runs before starting: required environment variables, weak secrets and the active profile.",
    "plain", {"main/ProductionConfigCheck.java": CHECK, "test/ProductionConfigCheckTest.java": CHECK_TEST},
    ["Report missing/blank required keys in a fixed order.", "Validate the JDBC URL prefix, weak database passwords and short JWT secrets.", "Require the `prod` profile.", "Do not double-report a missing key as weak."],
    ["Blank values.", "Mixed-case weak passwords.", "Absent profile."],
    ["Use a `List<String>` and add problems in the documented order.", "`String.isBlank()` handles whitespace-only values."])

# ---------------------------------------------------------------- task 2
WF = r'''package %PKG%;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

/** A tiny structural checker for a GitHub Actions workflow file (text based, no YAML parser needed). */
public class WorkflowChecker {

    /**
     * Returns the names of MISSING pieces, in this order (empty list = workflow is acceptable):
     * <ol>
     *   <li>"trigger:push" - the text has a line starting (after indentation) with "push:"</li>
     *   <li>"trigger:pull_request" - a line starting with "pull_request:"</li>
     *   <li>"checkout" - uses "actions/checkout@"</li>
     *   <li>"setup-java" - uses "actions/setup-java@"</li>
     *   <li>"java-21" - matches regex java-version:\s*['"]?21['"]?</li>
     *   <li>"maven-cache" - matches regex cache:\s*['"]?maven['"]?</li>
     *   <li>"maven-build" - a "run:" line invoking mvn with verify or test (e.g. "mvn -B verify")</li>
     * </ol>
     */
    public List<String> missingPieces(String yaml) {
        // TODO(%TAG%): implement the seven checks above (Pattern with MULTILINE is handy)
        throw new UnsupportedOperationException("TODO(%TAG%): implement missingPieces");
    }
}
'''
WF_TEST = r'''package %PKG%;

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
'''
CI_STARTER = "# Learner workflow (this file is validated by WorkflowCheckerTest).\n# TODO(Day49-task02): write a complete GitHub Actions workflow for a Maven + Java 21 project.\n# Use ../../../samples/github-actions-ci.yml (Day 49/samples) ONLY as a reference; type it yourself to understand each key.\nname: CI\n"
p2 = task("github-actions-workflow", "GitHub Actions Workflow Checker", "Core", "Java + CI",
    "Write a real CI workflow (`ci/ci.yml`) and the small checker that verifies it contains the essential pieces: triggers, checkout, Java 21, Maven cache and a build/test command.",
    "plain", {"main/WorkflowChecker.java": WF, "ci/ci.yml": CI_STARTER, "test/WorkflowCheckerTest.java": WF_TEST},
    ["Implement `missingPieces` with the seven checks in the documented order.", "Complete `ci/ci.yml` so it passes your own checker.", "Include a `pull_request` trigger and Maven dependency caching."],
    ["Indentation variations.", "Quotes around the Java version.", "`mvn test` vs `mvn verify`."],
    ["`Pattern.compile(\"^\\\\s*push:\", Pattern.MULTILINE)`.", "The workflow file is plain text; you do not need a YAML library."])

# ---------------------------------------------------------------- task 3
LINT = r'''package %PKG%;

import java.util.ArrayList;
import java.util.List;

/** A miniature Checkstyle: finds the style problems a real Checkstyle run would flag. */
public class StyleLinter {

    public static final int MAX_LINE_LENGTH = 100;

    /**
     * Returns violations as "<line>:<RULE>" (1-based line numbers), ordered by line, at most one entry per rule per line.
     * Rules (in evaluation order within a line):
     * <ol>
     *   <li>TAB - the line contains a tab character</li>
     *   <li>TRAILING_WHITESPACE - the line ends with a space or tab (and is not empty)</li>
     *   <li>LINE_TOO_LONG - more than MAX_LINE_LENGTH characters (not counting the trailing newline)</li>
     *   <li>STAR_IMPORT - line (trimmed) starts with "import " and ends with ".*;"</li>
     *   <li>SYSTEM_OUT - line contains "System.out." or "System.err."</li>
     * </ol>
     * Additionally, when the source is non-empty and does not end with '\n', add "EOF:NO_FINAL_NEWLINE" as the last entry.
     */
    public List<String> lint(String source) {
        // TODO(%TAG%): split on '\n' (keep trailing empties out of the line count) and apply the rules
        throw new UnsupportedOperationException("TODO(%TAG%): implement lint");
    }
}
'''
LINT_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

class StyleLinterTest {

    private final StyleLinter linter = new StyleLinter();

    @Test
    void cleanSourceHasNoViolations() {
        assertThat(linter.lint("package a;\n\nclass A {\n}\n")).isEmpty();
    }

    @Test
    void emptySourceHasNoViolations() {
        assertThat(linter.lint("")).isEmpty();
    }

    @Test
    void tabsAndTrailingWhitespaceAreFound() {
        String src = "class A {\n\tint x;\n    int y; \n}\n";
        assertThat(linter.lint(src)).containsExactly("2:TAB", "3:TRAILING_WHITESPACE");
    }

    @Test
    void longLinesAreFound() {
        String src = "// " + "x".repeat(98) + "\n// " + "x".repeat(97) + "\n";
        assertThat(linter.lint(src)).containsExactly("1:LINE_TOO_LONG");
    }

    @Test
    void starImportsAndConsolePrintsAreFound() {
        String src = "import java.util.*;\nimport java.io.File;\nclass A { void m() { System.out.println(1); } }\n";
        assertThat(linter.lint(src)).containsExactly("1:STAR_IMPORT", "3:SYSTEM_OUT");
    }

    @Test
    void oneLineCanHaveSeveralRulesInOrder() {
        String src = "\tSystem.out.println(\"x\"); \n";
        assertThat(linter.lint(src)).containsExactly("1:TAB", "1:TRAILING_WHITESPACE", "1:SYSTEM_OUT");
    }

    @Test
    void missingFinalNewlineIsReportedLast() {
        assertThat(linter.lint("class A {\n\tint x;\n}")).containsExactly("2:TAB", "EOF:NO_FINAL_NEWLINE");
    }
}
'''
p3 = task("style-linter", "Style Linter (Checkstyle in Miniature)", "Core", "Java",
    "Build a small linter for the style rules in the team Checkstyle configuration (tabs, trailing whitespace, line length, star imports, console prints, final newline).",
    "plain", {"main/StyleLinter.java": LINT, "test/StyleLinterTest.java": LINT_TEST},
    ["Return `line:RULE` entries ordered by line and rule order.", "Detect the five line-level rules.", "Report a missing final newline as `EOF:NO_FINAL_NEWLINE`.", "Empty input has no violations."],
    ["File without trailing newline.", "A line that violates several rules.", "Exactly 100 characters is allowed."],
    ["`source.split(\"\\n\", -1)` keeps trailing empty strings; drop the last one if the source ends with a newline.", "Compare lengths with `>`, not `>=`."])

# ---------------------------------------------------------------- task 4
GIT = r'''package %PKG%;

import java.util.regex.Pattern;

/** Team Git conventions as executable rules (branch names, commit messages, release versions). */
public final class GitConventions {

    private GitConventions() {
    }

    /**
     * Valid branch names:
     * <ul>
     *   <li>"main" or "develop"</li>
     *   <li>"feature/", "bugfix/", "hotfix/" or "chore/" + ticket (UPPERCASE letters, dash, digits) + dash + kebab-case slug,
     *       e.g. feature/PAY-123-add-idempotency-key (slug: lower-case letters/digits separated by single dashes)</li>
     *   <li>"release/" + major.minor.patch, e.g. release/1.4.0</li>
     * </ul>
     */
    public static boolean isValidBranchName(String name) {
        // TODO(%TAG%): implement with one or more regular expressions
        throw new UnsupportedOperationException("TODO(%TAG%): implement isValidBranchName");
    }

    /**
     * Conventional Commits: first line "type(scope)!: subject" where type is one of feat, fix, docs, refactor, test,
     * chore, build, ci; (scope) optional lower-case kebab; "!" optional; subject 1..72 chars, not blank.
     * Only the FIRST line is validated. null/blank -> false.
     */
    public static boolean isValidCommitMessage(String message) {
        // TODO(%TAG%): validate the first line
        throw new UnsupportedOperationException("TODO(%TAG%): implement isValidCommitMessage");
    }

    /**
     * Semantic version bump. bump is "major", "minor" or "patch" (case-insensitive).
     * major: X+1.0.0, minor: X.Y+1.0, patch: X.Y.Z+1. Invalid version/bump -> IllegalArgumentException.
     */
    public static String nextVersion(String current, String bump) {
        // TODO(%TAG%): parse MAJOR.MINOR.PATCH and apply the bump
        throw new UnsupportedOperationException("TODO(%TAG%): implement nextVersion");
    }
}
'''
GIT_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;

class GitConventionsTest {

    @Test
    void validBranchNames() {
        assertThat(GitConventions.isValidBranchName("main")).isTrue();
        assertThat(GitConventions.isValidBranchName("develop")).isTrue();
        assertThat(GitConventions.isValidBranchName("feature/PAY-123-add-idempotency-key")).isTrue();
        assertThat(GitConventions.isValidBranchName("hotfix/OPS-9-fix")).isTrue();
        assertThat(GitConventions.isValidBranchName("release/1.4.0")).isTrue();
    }

    @Test
    void invalidBranchNames() {
        assertThat(GitConventions.isValidBranchName(null)).isFalse();
        assertThat(GitConventions.isValidBranchName("feature/add-stuff")).isFalse();
        assertThat(GitConventions.isValidBranchName("feature/pay-1-x")).isFalse();
        assertThat(GitConventions.isValidBranchName("feature/PAY-1-Bad_Slug")).isFalse();
        assertThat(GitConventions.isValidBranchName("feature/PAY-1-double--dash")).isFalse();
        assertThat(GitConventions.isValidBranchName("release/1.4")).isFalse();
        assertThat(GitConventions.isValidBranchName("my-branch")).isFalse();
    }

    @Test
    void validCommitMessages() {
        assertThat(GitConventions.isValidCommitMessage("feat: add login")).isTrue();
        assertThat(GitConventions.isValidCommitMessage("fix(auth): reject expired tokens")).isTrue();
        assertThat(GitConventions.isValidCommitMessage("refactor(user-service)!: drop v1 api\n\nBody text here")).isTrue();
    }

    @Test
    void invalidCommitMessages() {
        assertThat(GitConventions.isValidCommitMessage(null)).isFalse();
        assertThat(GitConventions.isValidCommitMessage("  ")).isFalse();
        assertThat(GitConventions.isValidCommitMessage("added stuff")).isFalse();
        assertThat(GitConventions.isValidCommitMessage("feat:no space")).isFalse();
        assertThat(GitConventions.isValidCommitMessage("wip: something")).isFalse();
        assertThat(GitConventions.isValidCommitMessage("feat: " + "x".repeat(73))).isFalse();
        assertThat(GitConventions.isValidCommitMessage("feat(Auth): upper scope")).isFalse();
    }

    @Test
    void versionBumps() {
        assertThat(GitConventions.nextVersion("1.4.9", "patch")).isEqualTo("1.4.10");
        assertThat(GitConventions.nextVersion("1.4.9", "MINOR")).isEqualTo("1.5.0");
        assertThat(GitConventions.nextVersion("1.4.9", "major")).isEqualTo("2.0.0");
    }

    @Test
    void invalidVersionInputs() {
        assertThatThrownBy(() -> GitConventions.nextVersion("1.4", "patch")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GitConventions.nextVersion("a.b.c", "patch")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GitConventions.nextVersion("1.0.0", "huge")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GitConventions.nextVersion(null, "patch")).isInstanceOf(IllegalArgumentException.class);
    }
}
'''
p4 = task("git-conventions-release-checklist", "Git Conventions and Release Versions", "Challenge", "Java + Git",
    "Turn the team's branching, commit-message and release-version rules into code, the same checks a PR bot or commit hook would run.",
    "plain", {"main/GitConventions.java": GIT, "test/GitConventionsTest.java": GIT_TEST},
    ["Validate branch names (main/develop, ticketed work branches, release branches).", "Validate Conventional Commit first lines.", "Bump semantic versions and reject invalid input."],
    ["Null inputs.", "Subject length boundary (72).", "Double dashes in slugs.", "Versions with missing parts."],
    ["Anchor patterns with `^...$` and use `Pattern.matches`/`matcher().matches()`.", "Slug: `[a-z0-9]+(-[a-z0-9]+)*`."])

TOPICS = [
    T("Profiles, externalized configuration, and secrets",
      "Production behavior comes from configuration, not code. Spring Boot layers sources: defaults < `application.yml` < `application-{profile}.yml` < OS environment variables < command-line args. Secrets (DB password, JWT key) must come from the environment or a secret manager, never from the repository.",
      "The same JAR runs in dev, test and prod. Committed secrets are leaked secrets (Git history is forever); misconfigured prod (dev profile, weak secrets, `ddl-auto=create`) causes incidents.",
      ["One artifact for all environments", "Secrets rotate without rebuilds", "Fail-fast validation at startup"],
      ["More moving parts to document", "Environment drift between machines"],
      "A committed `application.yml` with real credentials is a breach; `ddl-auto=update` in prod silently mutates schemas; `management.endpoints.web.exposure.include=*` exposes internals.",
      "```yaml\nspring:\n  datasource:\n    url: ${DB_URL}\n    username: ${DB_USERNAME}\n    password: ${DB_PASSWORD}\n  jpa.hibernate.ddl-auto: validate\n```\nRun: `SPRING_PROFILES_ACTIVE=prod DB_URL=... java -jar app.jar`. Local only: `application-local.yml` (git-ignored). See `samples/application-prod.yml`.",
      [("Fail fast", "java", "if (!problems.isEmpty()) throw new IllegalStateException(\"Bad configuration: \" + problems);"),
       ("Env var mapping", "text", "app.jwt.secret  <-  APP_JWT_SECRET (relaxed binding)")],
      [("Where do production secrets live?", "Environment variables injected by the platform or a secret manager (Vault, cloud secrets)."),
       ("Why `ddl-auto=validate` in prod?", "Schema changes must be explicit migrations; Hibernate should only verify.")]),
    T("Packaging and running an executable JAR",
      "`spring-boot-maven-plugin` repackages the app into a **fat (executable) JAR** containing dependencies and an embedded server: `mvn -DskipTests package` then `java -jar target/app-1.0.0.jar`. Useful flags: `-Xmx`, `-Dspring.profiles.active=prod`, `--server.port=9090`; graceful shutdown with `server.shutdown=graceful`.",
      "A single self-contained artifact is simple to deploy, version and roll back. Operations need health endpoints, logs on stdout, and predictable shutdown.",
      ["No external app server", "Reproducible builds", "Easy containerless deployment (systemd, VM)"],
      ["Big artifacts", "Dependencies are updated only by rebuilding"],
      "Running with the IDE classpath instead of the JAR hides packaging bugs (missing resources); logging to a local file on ephemeral hosts loses logs.",
      "```bash\nmvn -B clean verify\njava -jar target/payflow-1.0.0.jar --spring.profiles.active=prod\ncurl -s localhost:8080/actuator/health\n```\nStop with SIGTERM (graceful shutdown completes in-flight requests).",
      [("Memory and profile", "bash", "JAVA_OPTS=\"-Xms256m -Xmx512m\"\njava $JAVA_OPTS -jar app.jar --spring.profiles.active=prod")],
      [("What does repackage do?", "Creates a nested-JAR executable archive with a launcher and the app's dependencies."),
       ("How do you stop it cleanly?", "Send SIGTERM; with graceful shutdown in-flight requests complete.")]),
    T("CI with GitHub Actions and code quality with Checkstyle",
      "A **workflow** (`.github/workflows/*.yml`) runs jobs on events (`push`, `pull_request`). A Java job: checkout -> setup-java (Temurin 21, Maven cache) -> `mvn -B verify`. **Checkstyle** enforces style rules via `maven-checkstyle-plugin` bound to `validate`/`verify`.",
      "Automation makes quality non-negotiable: every pull request builds, tests and lints before review, so humans review design not whitespace.",
      ["Fast feedback on every PR", "Consistent style", "Reproducible clean-room build"],
      ["CI minutes cost; flaky tests erode trust", "Strict rules need team agreement"],
      "Without CI, 'works on my machine' merges break main. Without a style gate, reviews become style debates.",
      "See `samples/github-actions-ci.yml` and `samples/checkstyle.xml`.\n```xml\n<plugin>\n  <artifactId>maven-checkstyle-plugin</artifactId>\n  <configuration><configLocation>checkstyle.xml</configLocation><failOnViolation>true</failOnViolation></configuration>\n  <executions><execution><phase>validate</phase><goals><goal>check</goal></goals></execution></executions>\n</plugin>\n```",
      [("Minimal workflow", "yaml", "on: [push, pull_request]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-java@v4\n        with: { distribution: temurin, java-version: '21', cache: maven }\n      - run: mvn -B verify")],
      [("Why cache Maven dependencies?", "To avoid re-downloading them on every run."),
       ("Where do CI secrets go?", "GitHub repository/environment secrets, referenced as `${{ secrets.NAME }}`.")]),
    T("Git branching, pull requests, and release hygiene",
      "Common models: **trunk-based** (short-lived branches off `main`, small PRs, feature flags) and **GitFlow** (`develop`, `release/*`, `hotfix/*`). Good PRs are small, linked to a ticket, have a clear description and pass CI. Use **Conventional Commits** and **semantic versioning** for readable history and releases.",
      "Predictable branching and history make code review, bisecting and releases safe.",
      ["Easier reviews and reverts", "Automatable release notes", "Clear versioning contract"],
      ["Process overhead", "Long-lived branches cause painful merges"],
      "Giant PRs get rubber-stamped; force-pushing shared branches destroys teammates' work; committing secrets requires a history rewrite and key rotation.",
      "Branch: `feature/PAY-123-add-idempotency-key`. Commit: `feat(payments): add idempotency key`. Release: tag `v1.4.0` from `release/1.4.0`. Release checklist: tests green, migration reviewed, config documented, changelog, tag, rollback plan.",
      [("Semver", "text", "MAJOR (breaking) . MINOR (feature) . PATCH (fix)  e.g. 1.4.9 -> 1.5.0 for a new feature")],
      [("Rebase or merge?", "Rebase keeps history linear on private branches; merge/squash for shared integration per team policy; never rebase shared history."),
       ("What do you do after committing a secret?", "Rotate it immediately; removing it from Git history alone is not enough.")]),
]

day(49, "Production Readiness: Profiles, Secrets, JAR, CI, Checkstyle, Git", "Capstone",
    "What it takes to ship: externalized configuration, executable JARs, CI pipelines, style gates and disciplined Git workflow",
    ["Configure profiles and externalize secrets safely", "Build and run an executable Spring Boot JAR", "Write a GitHub Actions workflow for Maven", "Explain and apply Checkstyle rules", "Apply branching, commit and versioning conventions"],
    ["Days 29-30 profiles and configuration", "Day 47-48 capstone slices"],
    TOPICS, [p1, p2, p3, p4],
    [("What is a twelve-factor config?", "Config in environment variables, strictly separated from code."),
     ("How do you roll back a bad release?", "Redeploy the previous immutable artifact (and compatible schema)."),
     ("Why avoid long-lived branches?", "They diverge and cause integration pain; prefer short-lived branches and small PRs."),
     ("What does `mvn -B verify` do?", "Runs compile, test and package checks in batch (non-interactive) mode."),
     ("What belongs in CI?", "Build, tests, static analysis, dependency checks; deploy on tagged releases.")],
    ["Committing secrets or `application-local.yml`.", "Using `ddl-auto=update` in prod.", "Running prod with the dev profile.", "Not caching dependencies in CI.", "Force-pushing shared branches."],
    ["Spring Boot Reference: Externalized Configuration, Packaging", "GitHub Actions documentation: Building and testing Java with Maven", "Checkstyle documentation", "Conventional Commits 1.0", "Semantic Versioning 2.0"],
    [("Profile", "Named configuration group"), ("Fat JAR", "Executable JAR with dependencies"), ("Workflow", "GitHub Actions automation file"), ("Checkstyle", "Style checking tool"),
     ("Trunk-based", "Integrate small changes to main frequently"), ("Semver", "Major.Minor.Patch versioning")],
    "2-3 h theory + 4-6 h tasks", spring=True)
