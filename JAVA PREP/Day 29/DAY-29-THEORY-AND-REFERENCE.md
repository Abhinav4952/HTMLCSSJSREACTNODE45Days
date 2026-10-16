# Day 29 — Spring Boot Starters, YAML, Profiles, and ConfigurationProperties

**Phase:** Spring Boot  
**Primary theme:** How Boot assembles an application: starters, auto-configuration, externalized configuration, profiles, and typed properties  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-property-binding`, `task-02-profile-greeting`, `task-03-actuator-info-note`, `task-04-starter-dependency-quiz`  
**Instruction alignment:** Maps to Day 29 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

How Boot assembles an application: starters, auto-configuration, externalized configuration, profiles, and typed properties. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. Starters and auto-configuration
2. application.yml, externalized configuration, and profiles
3. @ConfigurationProperties and type-safe binding
4. Actuator basics: health, info, and exposure
5. Interview corner, common mistakes, glossary

## Subtopics

### Starters and auto-configuration

#### What it is

A **starter** is a curated dependency descriptor (`spring-boot-starter-web`, `-data-jpa`, ...) that pulls in a compatible set of libraries. **Auto-configuration** inspects the classpath and properties and registers beans conditionally (`@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty`). `@SpringBootApplication` = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`.

#### Why it exists / why it matters

Before Boot you hand-picked library versions and wrote infrastructure XML/Java config. Boot's BOM (parent POM) aligns versions and auto-configuration provides sensible defaults you can override.

#### Pros and cons

**Pros**

- Compatible dependency versions via the parent BOM
- Convention over configuration: a working app in minutes
- Back-off: your own bean replaces the default
- Uniform operations (Actuator, metrics, logging)

**Cons / trade-offs**

- Magic can hide what is happening (use `--debug` conditions report)
- Large transitive dependency trees
- Upgrading Boot can change defaults (read migration guides)

#### What happens without it / when misused

Missing starter -> `ClassNotFoundException`/missing beans (e.g. no `DataSource` without JDBC starter). Two starters pulling conflicting servers (Tomcat + Jetty) cause surprises. Overriding managed versions casually breaks compatibility.

#### Syntax and rules

```xml
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>3.4.1</version>
</parent>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>   <!-- no version: managed -->
</dependency>
```
Debug: run with `--debug` or set `debug=true` for the conditions evaluation report.

#### Examples

**Example 1 — Choosing starters**

```text
REST API -> spring-boot-starter-web
Database with JPA -> spring-boot-starter-data-jpa (+ driver)
Security -> spring-boot-starter-security
Bean Validation -> spring-boot-starter-validation
Tests -> spring-boot-starter-test
```

**Example 2 — Backing off auto-config**

```java
@Bean
ObjectMapper objectMapper() { return new ObjectMapper(); } // replaces Boot's default (ConditionalOnMissingBean)
```

**Example 3 — Excluding auto-config**

```java
@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)
class App {}
```

#### Quick checks

1. What does @SpringBootApplication combine?
2. Why do starters have no versions in your pom?
3. How can you see why an auto-configuration was or wasn't applied?

### application.yml, externalized configuration, and profiles

#### What it is

Boot loads configuration from many sources in a defined precedence (command-line args > env vars > profile files > `application.yml`/`.properties` > defaults). **Profiles** group beans and properties per environment: `application-dev.yml`, `@Profile("dev")`, `spring.profiles.active`.

#### Why it exists / why it matters

The same artifact must run on a laptop, CI and production with different databases and secrets. Twelve-factor apps keep config out of the code.

#### Pros and cons

**Pros**

- One build, many environments
- Secrets can come from env vars/secret stores
- YAML supports hierarchy and lists
- Profile-specific beans for dev tools, stubs, mocks

**Cons / trade-offs**

- Precedence rules surprise newcomers
- YAML indentation errors
- Too many profiles become unmanageable; prefer a few well-named ones

#### What happens without it / when misused

Committing production passwords in `application.yml` leaks secrets. Forgetting to activate a profile makes beans missing (`NoSuchBeanDefinitionException`). A typo in a key silently uses defaults.

#### Syntax and rules

```yaml
spring:
  application:
    name: demo
server:
  port: 8080
---
spring:
  config:
    activate:
      on-profile: dev
logging:
  level:
    root: DEBUG
```
Activate: `--spring.profiles.active=dev`, `SPRING_PROFILES_ACTIVE=dev`. `@Profile("!prod")` negation; `@ActiveProfiles("test")` in tests.

#### Examples

**Example 1 — Profile bean**

```java
@Component @Profile("dev")
class DevGreeting implements GreetingProvider { ... }
```

**Example 2 — Env var override**

```text
SERVER_PORT=9090 java -jar app.jar   # overrides server.port
```

**Example 3 — Multi-document YAML**

```yaml
app:
  mode: default
---
spring.config.activate.on-profile: prod
app:
  mode: prod
```

#### Quick checks

1. Which wins: env var or application.yml?
2. How do you activate a profile in tests?
3. Where should production secrets live?

### @ConfigurationProperties and type-safe binding

#### What it is

`@ConfigurationProperties(prefix = "app")` binds a group of properties to a typed Java class with **relaxed binding** (kebab-case, camelCase, env-style all map). Supports nested objects, lists, maps, `Duration`, `DataSize`, and validation with `@Validated` + Bean Validation.

#### Why it exists / why it matters

`@Value` strings scatter configuration and lack validation/IDE support. A properties class is one documented, testable, validated unit of configuration.

#### Pros and cons

**Pros**

- Type-safe and structured
- Relaxed binding across sources
- Validation at startup (fail fast)
- IDE metadata via spring-boot-configuration-processor

**Cons / trade-offs**

- Requires getters/setters or constructor binding
- Boilerplate for many small settings
- Binding errors surface only at startup/bind time

#### What happens without it / when misused

Missing setters leave fields at defaults silently. Without `@EnableConfigurationProperties` or `@ConfigurationPropertiesScan` the class is never registered. A wrong prefix binds nothing.

#### Syntax and rules

```java
@ConfigurationProperties(prefix = "app")
@Validated
public class AppProperties {
    @NotBlank private String name;
    private int maxUsers = 10;
    private List<String> features = new ArrayList<>();
    // getters/setters
}
@SpringBootApplication @ConfigurationPropertiesScan class App {}
```

#### Examples

**Example 1 — Binder in a unit test**

```java
var binder = new Binder(new MapConfigurationPropertySource(Map.of("app.max-users", "5")));
AppProperties p = binder.bind("app", AppProperties.class).get();
```

**Example 2 — Constructor binding with a record**

```java
@ConfigurationProperties(prefix = "mail")
record MailProperties(String host, int port) {}
```

**Example 3 — Duration binding**

```yaml
app:
  timeout: 5s     # Duration
```

#### Quick checks

1. What is relaxed binding?
2. Why prefer it over @Value for groups?
3. What happens if there is no setter?

### Actuator basics: health, info, and exposure

#### What it is

**Spring Boot Actuator** adds production endpoints: `/actuator/health`, `/info`, `/metrics`, `/env`, `/loggers`... By default only `health` is exposed over HTTP; others are enabled but must be exposed (`management.endpoints.web.exposure.include`). `InfoContributor` beans add data to `/info`.

#### Why it exists / why it matters

Operations need liveness/readiness checks, version info and metrics; Kubernetes and load balancers poll health endpoints.

#### Pros and cons

**Pros**

- Free operational endpoints
- Extensible via contributors and indicators
- Integrates with Micrometer metrics
- Separate management port possible

**Cons / trade-offs**

- Exposing sensitive endpoints is a security risk
- Extra attack surface and overhead
- Health details can leak internals

#### What happens without it / when misused

`include: '*'` in production exposes `env`, `heapdump` and more. A health endpoint calling slow downstream systems can bring the app down under probes.

#### Syntax and rules

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info
  endpoint:
    health:
      show-details: when-authorized
```
```java
@Component class AppInfo implements InfoContributor {
  public void contribute(Info.Builder b) { b.withDetail("app", Map.of("name", "demo")); }
}
```

#### Examples

**Example 1 — Info contributor**

```java
builder.withDetail("app", Map.of("name", name, "version", version));
```

**Example 2 — Exposure**

```yaml
management.endpoints.web.exposure.include: health,info,metrics
```

**Example 3 — Check**

```text
GET /actuator/info -> {"app":{"name":"demo","version":"1.0"}}
```

#### Quick checks

1. Which endpoint is exposed over HTTP by default?
2. How do you add data to /info?
3. Why not expose `*` in production?

## Interview corner

**Q1. How does auto-configuration work?**

Conditional @Configuration classes listed in `AutoConfiguration.imports` activate based on classpath, beans and properties.

**Q2. What is the property precedence order?**

Command-line args, system props, env vars, profile files, application files, defaults.

**Q3. @Value vs @ConfigurationProperties?**

@Value for single values; @ConfigurationProperties for typed groups with validation.

**Q4. How do you override an auto-configured bean?**

Define your own bean of the same type; `@ConditionalOnMissingBean` backs off.

**Q5. What does Actuator expose by default?**

Only health over HTTP; everything else must be exposed explicitly.

## Common mistakes & debugging

- Wrong YAML indentation.
- Forgetting `@ConfigurationPropertiesScan`/`@EnableConfigurationProperties`.
- Using the wrong profile file name (`application-dev.yml`).
- Exposing all Actuator endpoints.

## Further reading

- Spring Boot Reference: Externalized Configuration, Auto-configuration, Actuator
- Spring Boot Reference: Profiles

## Glossary

| Term | Meaning |
|------|---------|
| Starter | Dependency bundle for a feature |
| BOM | Bill of materials managing versions |
| Relaxed binding | Flexible property name matching |
| Profile | Named environment configuration group |
| Actuator | Production-ready endpoints |

## Answers

### Starters and auto-configuration

1. @Configuration, @EnableAutoConfiguration and @ComponentScan.
2. The Boot parent/BOM manages them.
3. The conditions evaluation report (`--debug`).

### application.yml, externalized configuration, and profiles

1. The environment variable.
2. `@ActiveProfiles("test")`.
3. Environment variables or a secret manager — not in the repo.

### @ConfigurationProperties and type-safe binding

1. Different spellings (`max-users`, `maxUsers`, `MAX_USERS`) map to the same property.
2. Type safety, structure, validation and IDE support.
3. JavaBean binding cannot set the value (unless constructor binding is used).

### Actuator basics: health, info, and exposure

1. `health` (and `info` in some versions when enabled); sensitive ones are not.
2. Provide an `InfoContributor` bean or `info.*` properties.
3. It exposes sensitive endpoints such as env and heapdump.
