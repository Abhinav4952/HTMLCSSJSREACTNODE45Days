from common import *

TYPE = "Spring Boot"
S = ["spring-boot-starter"]

# ------------------------------------------------------------ task 1
PROPS = r'''package %PKG%;

import java.util.ArrayList;
import java.util.List;
import org.springframework.boot.context.properties.ConfigurationProperties;

/** Binds {@code app.*} properties (relaxed binding: app.max-users, app.maxUsers, APP_MAXUSERS all map to maxUsers). */
@ConfigurationProperties(prefix = "app")
public class AppProperties {

    private String name;
    private int maxUsers;
    private List<String> features = new ArrayList<>();
    private final Security security = new Security();

    // TODO(%TAG%): add getters and setters for name, maxUsers and features (JavaBean binding needs setters),
    //              and a getter for the nested security object

    public static class Security {
        private boolean enabled;
        private String token;

        // TODO(%TAG%): add getters and setters for enabled and token
    }

    /** "<name> (<maxUsers> users, <features.size()> features)" e.g. "demo (5 users, 2 features)". */
    public String summary() {
        // TODO(%TAG%): build the summary from the bound values
        throw new UnsupportedOperationException("TODO(%TAG%): implement summary");
    }
}
'''
PROPS_SOL = r'''package %PKG%;

import java.util.ArrayList;
import java.util.List;
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "app")
public class AppProperties {
    private String name;
    private int maxUsers;
    private List<String> features = new ArrayList<>();
    private final Security security = new Security();
    public String getName() { return name; }
    public void setName(String n) { name = n; }
    public int getMaxUsers() { return maxUsers; }
    public void setMaxUsers(int m) { maxUsers = m; }
    public List<String> getFeatures() { return features; }
    public void setFeatures(List<String> f) { features = f; }
    public Security getSecurity() { return security; }
    public static class Security {
        private boolean enabled; private String token;
        public boolean isEnabled() { return enabled; }
        public void setEnabled(boolean e) { enabled = e; }
        public String getToken() { return token; }
        public void setToken(String t) { token = t; }
    }
    public String summary() { return name + " (" + maxUsers + " users, " + features.size() + " features)"; }
}
'''
PROPS_TEST = r'''package %PKG%;

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
'''
a1 = task("property-binding", "@ConfigurationProperties Binding", "Warm-up", TYPE,
    "Make a typed properties class bindable (getters/setters, nested object, list) and prove relaxed binding with Spring Boot's Binder.",
    "boot", {"main/AppProperties.java": PROPS, "test/AppPropertiesTest.java": PROPS_TEST,
             "res/application.yml": "# Sample configuration the class is designed to bind (documentation only)\napp:\n  name: demo\n  max-users: 5\n  features: [a, b]\n  security:\n    enabled: true\n    token: change-me\n"},
    ["Add getters/setters so `Binder` can populate `AppProperties`, including the nested `Security` object and the list.", "Implement `summary()`.", "Understand relaxed binding (kebab-case vs camelCase)."],
    ["Properties that are absent keep their Java defaults (0, empty list, false).", "Both `app.max-users` and `app.maxUsers` bind."],
    ["Nested static classes need their own getters/setters.", "Boot's `@ConfigurationProperties` + `Binder` is what `@EnableConfigurationProperties` uses internally."],
    starters=S, sol={"main/AppProperties.java": PROPS_SOL})

# ------------------------------------------------------------ task 2
a2files = {
    "main/GreetingProvider.java": "package %PKG%;\n\npublic interface GreetingProvider {\n    String greeting();\n}\n",
    "main/DevGreeting.java": r'''package %PKG%;

import org.springframework.stereotype.Component;

// TODO(%TAG%): this bean must exist ONLY when the "dev" profile is active (@Profile)
@Component
public class DevGreeting implements GreetingProvider {
    @Override
    public String greeting() {
        // TODO(%TAG%): return "Hello from DEV"
        throw new UnsupportedOperationException("TODO(%TAG%): implement DevGreeting.greeting");
    }
}
''',
    "main/ProdGreeting.java": r'''package %PKG%;

import org.springframework.stereotype.Component;

// TODO(%TAG%): this bean must exist ONLY when the "prod" profile is active (@Profile)
@Component
public class ProdGreeting implements GreetingProvider {
    @Override
    public String greeting() {
        // TODO(%TAG%): return "Hello from PROD"
        throw new UnsupportedOperationException("TODO(%TAG%): implement ProdGreeting.greeting");
    }
}
''',
    "main/ProfileConfig.java": "package %PKG%;\n\nimport org.springframework.context.annotation.ComponentScan;\nimport org.springframework.context.annotation.Configuration;\n\n@Configuration\n@ComponentScan\npublic class ProfileConfig {\n}\n",
    "res/application.yml": "# Shared defaults. Profile files application-dev.yml / application-prod.yml override them.\ngreeting:\n  suffix: \"!\"\n",
    "res/application-dev.yml": "greeting:\n  suffix: \" (dev)\"\n",
    "res/application-prod.yml": "greeting:\n  suffix: \".\"\n",
    "test/ProfileGreetingTest.java": r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class ProfileGreetingTest {

    private static AnnotationConfigApplicationContext start(String... profiles) {
        AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext();
        ctx.getEnvironment().setActiveProfiles(profiles);
        ctx.register(ProfileConfig.class);
        ctx.refresh();
        return ctx;
    }

    @Test
    void devProfileUsesDevGreeting() {
        try (AnnotationConfigApplicationContext ctx = start("dev")) {
            assertThat(ctx.getBean(GreetingProvider.class).greeting()).isEqualTo("Hello from DEV");
        }
    }

    @Test
    void prodProfileUsesProdGreeting() {
        try (AnnotationConfigApplicationContext ctx = start("prod")) {
            assertThat(ctx.getBean(GreetingProvider.class).greeting()).isEqualTo("Hello from PROD");
        }
    }

    @Test
    void noProfileMeansNoGreetingBean() {
        try (AnnotationConfigApplicationContext ctx = start()) {
            assertThat(ctx.getBeansOfType(GreetingProvider.class)).isEmpty();
        }
    }
}
''',
}
a2sol = {
    "main/DevGreeting.java": a2files["main/DevGreeting.java"].replace("@Component\n", '@Component\n@org.springframework.context.annotation.Profile("dev")\n').replace('throw new UnsupportedOperationException("TODO(%TAG%): implement DevGreeting.greeting");', 'return "Hello from DEV";'),
    "main/ProdGreeting.java": a2files["main/ProdGreeting.java"].replace("@Component\n", '@Component\n@org.springframework.context.annotation.Profile("prod")\n').replace('throw new UnsupportedOperationException("TODO(%TAG%): implement ProdGreeting.greeting");', 'return "Hello from PROD";'),
}
a2 = task("profile-greeting", "Profiles and Per-Environment Beans", "Core", TYPE,
    "Activate different beans per Spring profile and understand how application-{profile}.yml overlays shared defaults.",
    "boot", a2files,
    ["Restrict `DevGreeting` and `ProdGreeting` with `@Profile`.", "Implement both `greeting()` methods.", "Read the three YAML files and explain which value wins when `dev` is active."],
    ["No active profile -> neither bean exists.", "Profile names are case-sensitive."],
    ["`@Profile(\"!prod\")` negates a profile.", "In Boot apps use `spring.profiles.active=dev` or `SPRING_PROFILES_ACTIVE=dev`."],
    starters=S, sol=a2sol)

# ------------------------------------------------------------ task 3
INFO = r'''package %PKG%;

import java.util.Map;
import org.springframework.boot.actuate.info.Info;
import org.springframework.boot.actuate.info.InfoContributor;

/** Adds an "app" section (name + version) to the /actuator/info response. */
public class AppInfoContributor implements InfoContributor {

    private final String name;
    private final String version;

    public AppInfoContributor(String name, String version) {
        this.name = name;
        this.version = version;
    }

    @Override
    public void contribute(Info.Builder builder) {
        // TODO(%TAG%): add a detail "app" whose value is a Map with keys "name" and "version"
        throw new UnsupportedOperationException("TODO(%TAG%): implement contribute");
    }

    /** The URL path where the info endpoint is exposed by default. */
    public static String infoEndpointPath() {
        // TODO(%TAG%): return "/actuator/info"
        throw new UnsupportedOperationException("TODO(%TAG%): implement infoEndpointPath");
    }

    /** The property line that exposes health and info over HTTP, exactly: management.endpoints.web.exposure.include=health,info */
    public static String exposureProperty() {
        // TODO(%TAG%): return the property line
        throw new UnsupportedOperationException("TODO(%TAG%): implement exposureProperty");
    }
}
'''
INFO_SOL = r'''package %PKG%;

import java.util.Map;
import org.springframework.boot.actuate.info.Info;
import org.springframework.boot.actuate.info.InfoContributor;

public class AppInfoContributor implements InfoContributor {
    private final String name, version;
    public AppInfoContributor(String n, String v) { name = n; version = v; }
    @Override public void contribute(Info.Builder b) { b.withDetail("app", Map.of("name", name, "version", version)); }
    public static String infoEndpointPath() { return "/actuator/info"; }
    public static String exposureProperty() { return "management.endpoints.web.exposure.include=health,info"; }
}
'''
INFO_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.boot.actuate.info.Info;

class AppInfoContributorTest {

    @Test
    void contributesAppSection() {
        Info.Builder builder = new Info.Builder();
        new AppInfoContributor("demo", "1.2.3").contribute(builder);
        Info info = builder.build();
        assertThat(info.get("app")).isEqualTo(Map.of("name", "demo", "version", "1.2.3"));
    }

    @Test
    void keepsExistingDetails() {
        Info.Builder builder = new Info.Builder().withDetail("git", "abc");
        new AppInfoContributor("demo", "1").contribute(builder);
        assertThat(builder.build().getDetails()).containsKeys("git", "app");
    }

    @Test
    void endpointAndExposureProperties() {
        assertThat(AppInfoContributor.infoEndpointPath()).isEqualTo("/actuator/info");
        assertThat(AppInfoContributor.exposureProperty()).isEqualTo("management.endpoints.web.exposure.include=health,info");
    }
}
'''
a3 = task("actuator-info-note", "Actuator Info Contributor", "Core", TYPE,
    "Implement an InfoContributor that adds app name/version to /actuator/info and record the properties that expose the endpoint.",
    "boot", {"main/AppInfoContributor.java": INFO, "test/AppInfoContributorTest.java": INFO_TEST,
             "res/application.yml": "management:\n  endpoints:\n    web:\n      exposure:\n        include: health,info\n  info:\n    env:\n      enabled: true\ninfo:\n  team: backend\n"},
    ["Implement `contribute` using `Info.Builder#withDetail`.", "Implement the two static helper methods.", "Describe in a sentence why Actuator endpoints are not all exposed over HTTP by default."],
    ["Existing details contributed by other InfoContributors must be preserved.", "The value of `app` must be a Map with exactly `name` and `version`."],
    ["`builder.withDetail(String, Object)` returns the builder.", "In a real app, register the contributor as a `@Bean`."],
    starters=S + ["spring-boot-starter-actuator"], sol={"main/AppInfoContributor.java": INFO_SOL})

# ------------------------------------------------------------ task 4
ADV = r'''package %PKG%;

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
        // TODO(%TAG%): implement the mapping (a Map<String,String> constant is fine)
        throw new UnsupportedOperationException("TODO(%TAG%): implement starterFor");
    }

    /** True for "spring-boot-starter" and "spring-boot-starter-<lowercase-words-with-dashes>"; false for null/anything else. */
    public static boolean isStarterName(String artifactId) {
        // TODO(%TAG%): validate with a regex
        throw new UnsupportedOperationException("TODO(%TAG%): implement isStarterName");
    }

    /**
     * Notable transitive libraries (artifactIds):
     * spring-boot-starter-web -> [spring-boot-starter-tomcat, spring-boot-starter-json, spring-webmvc]
     * spring-boot-starter-data-jpa -> [hibernate-core, spring-boot-starter-jdbc, spring-data-jpa]
     * spring-boot-starter-test -> [junit-jupiter, mockito-core, assertj-core]
     * any other valid starter -> empty list; a non-starter name -> IllegalArgumentException.
     */
    public static List<String> typicalTransitives(String starter) {
        // TODO(%TAG%): implement
        throw new UnsupportedOperationException("TODO(%TAG%): implement typicalTransitives");
    }
}
'''
ADV_SOL = r'''package %PKG%;

import java.util.List;
import java.util.Map;

public final class StarterAdvisor {
    private static final Map<String, String> M = Map.of("rest api", "spring-boot-starter-web", "jpa", "spring-boot-starter-data-jpa",
        "security", "spring-boot-starter-security", "validation", "spring-boot-starter-validation", "metrics", "spring-boot-starter-actuator",
        "testing", "spring-boot-starter-test", "aop", "spring-boot-starter-aop", "cache", "spring-boot-starter-cache", "jdbc", "spring-boot-starter-jdbc");
    public static String starterFor(String u) {
        String r = u == null ? null : M.get(u.trim().toLowerCase());
        if (r == null) throw new IllegalArgumentException("unknown use case: " + u);
        return r;
    }
    public static boolean isStarterName(String a) { return a != null && a.matches("spring-boot-starter(-[a-z0-9]+)*"); }
    public static List<String> typicalTransitives(String s) {
        if (!isStarterName(s)) throw new IllegalArgumentException(s);
        return switch (s) {
            case "spring-boot-starter-web" -> List.of("spring-boot-starter-tomcat", "spring-boot-starter-json", "spring-webmvc");
            case "spring-boot-starter-data-jpa" -> List.of("hibernate-core", "spring-boot-starter-jdbc", "spring-data-jpa");
            case "spring-boot-starter-test" -> List.of("junit-jupiter", "mockito-core", "assertj-core");
            default -> List.of();
        };
    }
}
'''
ADV_TEST = r'''package %PKG%;

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
'''
a4 = task("starter-dependency-quiz", "Starter Dependency Quiz", "Challenge", TYPE,
    "Encode Spring Boot starter knowledge in code: map use cases to starters, validate starter names, and list notable transitive dependencies.",
    "boot", {"main/StarterAdvisor.java": ADV, "test/StarterAdvisorTest.java": ADV_TEST},
    ["Implement `starterFor` with the documented mapping.", "Implement `isStarterName` using a regular expression.", "Implement `typicalTransitives`."],
    ["Input is trimmed and case-insensitive for use cases.", "Starter names are case-sensitive lowercase.", "Non-starter artifact -> `IllegalArgumentException`."],
    ["A `Map.of(...)` constant keeps the mapping readable.", "`typicalTransitives` can reuse `isStarterName` for validation."],
    starters=S, sol={"main/StarterAdvisor.java": ADV_SOL})

topics = [
    T("Starters and auto-configuration",
      "A **starter** is a curated dependency descriptor (`spring-boot-starter-web`, `-data-jpa`, ...) that pulls in a compatible set of libraries. **Auto-configuration** inspects the classpath and properties and registers beans conditionally (`@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty`). `@SpringBootApplication` = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`.",
      "Before Boot you hand-picked library versions and wrote infrastructure XML/Java config. Boot's BOM (parent POM) aligns versions and auto-configuration provides sensible defaults you can override.",
      ["Compatible dependency versions via the parent BOM", "Convention over configuration: a working app in minutes", "Back-off: your own bean replaces the default", "Uniform operations (Actuator, metrics, logging)"],
      ["Magic can hide what is happening (use `--debug` conditions report)", "Large transitive dependency trees", "Upgrading Boot can change defaults (read migration guides)"],
      "Missing starter -> `ClassNotFoundException`/missing beans (e.g. no `DataSource` without JDBC starter). Two starters pulling conflicting servers (Tomcat + Jetty) cause surprises. Overriding managed versions casually breaks compatibility.",
      "```xml\n<parent>\n  <groupId>org.springframework.boot</groupId>\n  <artifactId>spring-boot-starter-parent</artifactId>\n  <version>3.4.1</version>\n</parent>\n<dependency>\n  <groupId>org.springframework.boot</groupId>\n  <artifactId>spring-boot-starter-web</artifactId>   <!-- no version: managed -->\n</dependency>\n```\nDebug: run with `--debug` or set `debug=true` for the conditions evaluation report.",
      [("Choosing starters", "text", "REST API -> spring-boot-starter-web\nDatabase with JPA -> spring-boot-starter-data-jpa (+ driver)\nSecurity -> spring-boot-starter-security\nBean Validation -> spring-boot-starter-validation\nTests -> spring-boot-starter-test"),
       ("Backing off auto-config", "java", "@Bean\nObjectMapper objectMapper() { return new ObjectMapper(); } // replaces Boot's default (ConditionalOnMissingBean)"),
       ("Excluding auto-config", "java", "@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)\nclass App {}")],
      [("What does @SpringBootApplication combine?", "@Configuration, @EnableAutoConfiguration and @ComponentScan."),
       ("Why do starters have no versions in your pom?", "The Boot parent/BOM manages them."),
       ("How can you see why an auto-configuration was or wasn't applied?", "The conditions evaluation report (`--debug`).")]),
    T("application.yml, externalized configuration, and profiles",
      "Boot loads configuration from many sources in a defined precedence (command-line args > env vars > profile files > `application.yml`/`.properties` > defaults). **Profiles** group beans and properties per environment: `application-dev.yml`, `@Profile(\"dev\")`, `spring.profiles.active`.",
      "The same artifact must run on a laptop, CI and production with different databases and secrets. Twelve-factor apps keep config out of the code.",
      ["One build, many environments", "Secrets can come from env vars/secret stores", "YAML supports hierarchy and lists", "Profile-specific beans for dev tools, stubs, mocks"],
      ["Precedence rules surprise newcomers", "YAML indentation errors", "Too many profiles become unmanageable; prefer a few well-named ones"],
      "Committing production passwords in `application.yml` leaks secrets. Forgetting to activate a profile makes beans missing (`NoSuchBeanDefinitionException`). A typo in a key silently uses defaults.",
      "```yaml\nspring:\n  application:\n    name: demo\nserver:\n  port: 8080\n---\nspring:\n  config:\n    activate:\n      on-profile: dev\nlogging:\n  level:\n    root: DEBUG\n```\nActivate: `--spring.profiles.active=dev`, `SPRING_PROFILES_ACTIVE=dev`. `@Profile(\"!prod\")` negation; `@ActiveProfiles(\"test\")` in tests.",
      [("Profile bean", "java", "@Component @Profile(\"dev\")\nclass DevGreeting implements GreetingProvider { ... }"),
       ("Env var override", "text", "SERVER_PORT=9090 java -jar app.jar   # overrides server.port"),
       ("Multi-document YAML", "yaml", "app:\n  mode: default\n---\nspring.config.activate.on-profile: prod\napp:\n  mode: prod")],
      [("Which wins: env var or application.yml?", "The environment variable."),
       ("How do you activate a profile in tests?", "`@ActiveProfiles(\"test\")`."),
       ("Where should production secrets live?", "Environment variables or a secret manager — not in the repo.")]),
    T("@ConfigurationProperties and type-safe binding",
      "`@ConfigurationProperties(prefix = \"app\")` binds a group of properties to a typed Java class with **relaxed binding** (kebab-case, camelCase, env-style all map). Supports nested objects, lists, maps, `Duration`, `DataSize`, and validation with `@Validated` + Bean Validation.",
      "`@Value` strings scatter configuration and lack validation/IDE support. A properties class is one documented, testable, validated unit of configuration.",
      ["Type-safe and structured", "Relaxed binding across sources", "Validation at startup (fail fast)", "IDE metadata via spring-boot-configuration-processor"],
      ["Requires getters/setters or constructor binding", "Boilerplate for many small settings", "Binding errors surface only at startup/bind time"],
      "Missing setters leave fields at defaults silently. Without `@EnableConfigurationProperties` or `@ConfigurationPropertiesScan` the class is never registered. A wrong prefix binds nothing.",
      "```java\n@ConfigurationProperties(prefix = \"app\")\n@Validated\npublic class AppProperties {\n    @NotBlank private String name;\n    private int maxUsers = 10;\n    private List<String> features = new ArrayList<>();\n    // getters/setters\n}\n@SpringBootApplication @ConfigurationPropertiesScan class App {}\n```",
      [("Binder in a unit test", "java", "var binder = new Binder(new MapConfigurationPropertySource(Map.of(\"app.max-users\", \"5\")));\nAppProperties p = binder.bind(\"app\", AppProperties.class).get();"),
       ("Constructor binding with a record", "java", "@ConfigurationProperties(prefix = \"mail\")\nrecord MailProperties(String host, int port) {}"),
       ("Duration binding", "yaml", "app:\n  timeout: 5s     # Duration")],
      [("What is relaxed binding?", "Different spellings (`max-users`, `maxUsers`, `MAX_USERS`) map to the same property."),
       ("Why prefer it over @Value for groups?", "Type safety, structure, validation and IDE support."),
       ("What happens if there is no setter?", "JavaBean binding cannot set the value (unless constructor binding is used).")]),
    T("Actuator basics: health, info, and exposure",
      "**Spring Boot Actuator** adds production endpoints: `/actuator/health`, `/info`, `/metrics`, `/env`, `/loggers`... By default only `health` is exposed over HTTP; others are enabled but must be exposed (`management.endpoints.web.exposure.include`). `InfoContributor` beans add data to `/info`.",
      "Operations need liveness/readiness checks, version info and metrics; Kubernetes and load balancers poll health endpoints.",
      ["Free operational endpoints", "Extensible via contributors and indicators", "Integrates with Micrometer metrics", "Separate management port possible"],
      ["Exposing sensitive endpoints is a security risk", "Extra attack surface and overhead", "Health details can leak internals"],
      "`include: '*'` in production exposes `env`, `heapdump` and more. A health endpoint calling slow downstream systems can bring the app down under probes.",
      "```yaml\nmanagement:\n  endpoints:\n    web:\n      exposure:\n        include: health,info\n  endpoint:\n    health:\n      show-details: when-authorized\n```\n```java\n@Component class AppInfo implements InfoContributor {\n  public void contribute(Info.Builder b) { b.withDetail(\"app\", Map.of(\"name\", \"demo\")); }\n}\n```",
      [("Info contributor", "java", "builder.withDetail(\"app\", Map.of(\"name\", name, \"version\", version));"),
       ("Exposure", "yaml", "management.endpoints.web.exposure.include: health,info,metrics"),
       ("Check", "text", "GET /actuator/info -> {\"app\":{\"name\":\"demo\",\"version\":\"1.0\"}}")],
      [("Which endpoint is exposed over HTTP by default?", "`health` (and `info` in some versions when enabled); sensitive ones are not."),
       ("How do you add data to /info?", "Provide an `InfoContributor` bean or `info.*` properties."),
       ("Why not expose `*` in production?", "It exposes sensitive endpoints such as env and heapdump.")]),
]

day(29, "Spring Boot Starters, YAML, Profiles, and ConfigurationProperties", "Spring Boot",
    "How Boot assembles an application: starters, auto-configuration, externalized configuration, profiles, and typed properties",
    ["Explain starters, the BOM and auto-configuration back-off", "Configure apps with YAML and profiles", "Bind structured settings with @ConfigurationProperties", "Expose and extend Actuator health/info safely", "Choose the right starter for a use case"],
    ["Day 28 Spring Core (beans, scanning, @Value)"],
    topics, [a1, a2, a3, a4],
    [("How does auto-configuration work?", "Conditional @Configuration classes listed in `AutoConfiguration.imports` activate based on classpath, beans and properties."),
     ("What is the property precedence order?", "Command-line args, system props, env vars, profile files, application files, defaults."),
     ("@Value vs @ConfigurationProperties?", "@Value for single values; @ConfigurationProperties for typed groups with validation."),
     ("How do you override an auto-configured bean?", "Define your own bean of the same type; `@ConditionalOnMissingBean` backs off."),
     ("What does Actuator expose by default?", "Only health over HTTP; everything else must be exposed explicitly.")],
    ["Wrong YAML indentation.", "Forgetting `@ConfigurationPropertiesScan`/`@EnableConfigurationProperties`.", "Using the wrong profile file name (`application-dev.yml`).", "Exposing all Actuator endpoints."],
    ["Spring Boot Reference: Externalized Configuration, Auto-configuration, Actuator", "Spring Boot Reference: Profiles"],
    [("Starter", "Dependency bundle for a feature"), ("BOM", "Bill of materials managing versions"), ("Relaxed binding", "Flexible property name matching"),
     ("Profile", "Named environment configuration group"), ("Actuator", "Production-ready endpoints")],
    "2–3 h theory + 3–5 h tasks", spring=True)
