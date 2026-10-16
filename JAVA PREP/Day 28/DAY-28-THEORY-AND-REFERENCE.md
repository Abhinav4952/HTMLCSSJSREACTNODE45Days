# Day 28 — Spring Core: IoC and Dependency Injection

**Phase:** Spring Boot  
**Primary theme:** How the Spring container creates and wires objects: constructor injection, bean selection, lifecycle, scopes, and Java configuration  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-constructor-injection`, `task-02-qualifier-primary`, `task-03-bean-lifecycle`, `task-04-config-bean-lab`  
**Instruction alignment:** Maps to Day 28 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

How the Spring container creates and wires objects: constructor injection, bean selection, lifecycle, scopes, and Java configuration. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. Inversion of Control, dependency injection, and the container
2. Choosing between beans: @Primary, @Qualifier, and component scanning
3. Bean lifecycle and scopes
4. Java-based configuration, @Bean, and @Value
5. Interview corner, common mistakes, glossary

## Subtopics

### Inversion of Control, dependency injection, and the container

#### What it is

**IoC** means objects do not create their collaborators; a container does. **Dependency injection (DI)** is the technique: the container reads configuration (annotations/Java config), creates **beans**, resolves their dependencies and hands them in — preferably through the **constructor**. The `ApplicationContext` is that container.

#### Why it exists / why it matters

Hard-coded `new` calls weld classes together, making tests hard and swaps painful. DI gives loose coupling (depend on interfaces), easy mocking, and central lifecycle management — the basis of everything in Spring Boot.

#### Pros and cons

**Pros**

- Loose coupling and testability (pass a fake via the constructor)
- Constructor injection makes dependencies explicit, final and non-null
- Container manages lifecycle and scope
- Cross-cutting features (AOP, transactions) hook in via proxies

**Cons / trade-offs**

- Wiring errors appear at startup (or runtime) instead of compile time
- Debugging proxies and bean graphs has a learning curve
- Overuse leads to 'everything is a bean' and hidden coupling

#### What happens without it / when misused

Field injection (`@Autowired private X x`) hides dependencies and makes plain unit tests impossible without reflection. Circular constructor dependencies fail with `BeanCurrentlyInCreationException`. Missing beans give `NoSuchBeanDefinitionException` / `UnsatisfiedDependencyException`.

#### Syntax and rules

```java
@Service
public class GreetingServiceImpl implements GreetingService {
    private final MessageRepository repo;
    public GreetingServiceImpl(MessageRepository repo) { this.repo = repo; } // no @Autowired needed (single ctor)
}

@Configuration @ComponentScan class AppConfig {}
var ctx = new AnnotationConfigApplicationContext(AppConfig.class);
GreetingService s = ctx.getBean(GreetingService.class);
```
Stereotypes: `@Component`, `@Service`, `@Repository` (adds exception translation), `@Controller`/`@RestController`.

#### Examples

**Example 1 — Constructor injection vs `new`**

```java
// tightly coupled
class Bad { private final Repo r = new JdbcRepo(); }
// injected
class Good { private final Repo r; Good(Repo r) { this.r = r; } }
```

**Example 2 — Unit test without Spring**

```java
GreetingService s = new GreetingServiceImpl(() -> "Hi");
assertThat(s.greet("Ada")).isEqualTo("Hi, Ada!");
```

**Example 3 — Starting a container**

```java
try (var ctx = new AnnotationConfigApplicationContext(AppConfig.class)) {
    System.out.println(ctx.getBeanDefinitionNames().length);
}
```

#### Quick checks

1. Why prefer constructor injection?
2. Is `@Autowired` required on a single-constructor bean?
3. What do stereotypes add beyond @Component?

### Choosing between beans: @Primary, @Qualifier, and component scanning

#### What it is

When several beans share a type, Spring needs a rule. **`@Primary`** marks the default candidate; **`@Qualifier("name")`** selects explicitly (by bean name or custom qualifier). **Component scanning** (`@ComponentScan`) discovers annotated classes under a base package; `@Bean` methods register beans explicitly.

#### Why it exists / why it matters

Real systems have multiple implementations (payment gateways, serializers, data sources). Explicit selection prevents ambiguous wiring and silent wrong choices.

#### Pros and cons

**Pros**

- Clear, declarative selection
- `@Primary` gives sane defaults with explicit overrides
- Collections injection (`List<PaymentGateway>`) enables strategy patterns
- Scanning removes XML/boilerplate

**Cons / trade-offs**

- String qualifiers are not refactor-safe
- Scanning can pick up unintended classes if packages are broad
- Too many primaries become confusing

#### What happens without it / when misused

Two candidates and no rule -> `NoUniqueBeanDefinitionException: expected single matching bean but found 2`. A mistyped qualifier gives `NoSuchBeanDefinitionException`. Scanning from the wrong package silently registers nothing.

#### Syntax and rules

```java
@Bean @Primary PaymentGateway stripe() { ... }
@Bean PaymentGateway paypal() { ... }

@Service class PaypalCheckout {
    PaypalCheckout(@Qualifier("paypal") PaymentGateway g) { ... }
}
```
Resolution order: type -> `@Primary` -> `@Priority` -> parameter name = bean name.

#### Examples

**Example 1 — Two gateways**

```java
@Configuration class GatewayConfig {
  @Bean @Primary PaymentGateway stripe() { return new Stripe(); }
  @Bean PaymentGateway paypal() { return new Paypal(); }
}
```

**Example 2 — Inject all implementations**

```java
@Service class Router {
  Router(Map<String, PaymentGateway> byName) { ... } // keys are bean names
}
```

**Example 3 — Custom base package**

```java
@Configuration @ComponentScan(basePackages = "com.javaprep.shop") class ShopConfig {}
```

#### Quick checks

1. What happens with two candidates and no @Primary?
2. Qualifier vs Primary?
3. How can you inject every implementation?

### Bean lifecycle and scopes

#### What it is

The container instantiates a bean, injects dependencies, applies post-processors, calls init callbacks (`@PostConstruct`, `InitializingBean`, `initMethod`), the bean is used, and on shutdown destroy callbacks (`@PreDestroy`, `DisposableBean`) run. **Scopes**: `singleton` (default, one per container), `prototype` (new per request), plus web scopes (`request`, `session`).

#### Why it exists / why it matters

Resources (pools, caches, schedulers) must be started after injection and released on shutdown. Scope decides whether state is shared — a major source of concurrency bugs.

#### Pros and cons

**Pros**

- Deterministic startup/shutdown hooks
- Singleton default saves memory
- Prototype gives per-use state
- Hooks keep resource handling out of business code

**Cons / trade-offs**

- Singletons must be thread-safe
- Prototype beans injected into singletons are created once (need `ObjectProvider`)
- Destroy callbacks are not called for prototypes

#### What happens without it / when misused

Mutable state in a singleton (`private List<X> cache`) causes race conditions. Using fields in the constructor that depend on injection before it finished causes `NullPointerException` — do it in `@PostConstruct`. A prototype injected into a singleton behaves like a singleton.

#### Syntax and rules

```java
@Component class Cache {
  @PostConstruct void warm() { ... }
  @PreDestroy void flush() { ... }
}
@Component @Scope("prototype") class ReportBuilder { }
```
Order: constructor -> injection -> `@PostConstruct` -> ready -> `@PreDestroy` on `ctx.close()`.

#### Examples

**Example 1 — Events order**

```text
ctor -> init (after injection) -> ... -> destroy (context close)
```

**Example 2 — Prototype from singleton**

```java
@Component class Service {
  private final ObjectProvider<ReportBuilder> builders;
  void run() { ReportBuilder b = builders.getObject(); }
}
```

**Example 3 — Initialization with @Bean**

```java
@Bean(initMethod = "start", destroyMethod = "stop") Server server() { return new Server(); }
```

#### Quick checks

1. When is @PostConstruct called?
2. Is a singleton bean thread-safe by default?
3. Does Spring call @PreDestroy for prototypes?

### Java-based configuration, @Bean, and @Value

#### What it is

`@Configuration` classes declare beans with `@Bean` methods, giving full control (third-party classes, conditional creation). Method parameters are injected from the container, so beans wire into each other. `@Value("${key:default}")` injects externalized properties with defaults; Boot's `Environment` merges sources (env vars, `application.yml`, CLI).

#### Why it exists / why it matters

Third-party classes cannot be annotated; configuration classes centralize wiring and make construction explicit and testable.

#### Pros and cons

**Pros**

- Explicit and type-safe wiring
- Works for classes you do not own
- Properties externalized per environment
- Proxy-based `@Configuration` ensures singleton semantics between `@Bean` methods

**Cons / trade-offs**

- Boilerplate versus scanning
- `@Value` strings are untyped (prefer `@ConfigurationProperties`, Day 29)
- Misconfigured placeholders fail at startup

#### What happens without it / when misused

Missing property without default -> `IllegalArgumentException: Could not resolve placeholder 'x'`. Calling a `@Bean` method directly from a `@Component` (not `@Configuration`) creates a second instance.

#### Syntax and rules

```java
@Configuration
class PricingConfig {
  @Bean TaxPolicy taxPolicy(@Value("${tax.rate:0.2}") double rate) { return new TaxPolicy(rate); }
  @Bean PriceCalculator calc(TaxPolicy p) { return new PriceCalculator(p); }
}
```

#### Examples

**Example 1 — Property with default**

```java
@Value("${app.name:demo}") String appName;
```

**Example 2 — Programmatic property override in tests**

```java
ctx.getEnvironment().getPropertySources().addFirst(new MapPropertySource("t", Map.of("tax.rate", "0.1")));
```

**Example 3 — Fail-fast validation**

```java
if (rate < 0 || rate > 1) throw new IllegalArgumentException("rate");
```

#### Quick checks

1. How are @Bean method parameters resolved?
2. What does `${x:y}` mean?
3. Why not use @Value everywhere?

## Interview corner

**Q1. What is IoC?**

A design principle where the framework controls object creation and wiring instead of your code.

**Q2. Constructor vs setter vs field injection?**

Constructor for required deps (immutable, testable); setter for optional; field injection discouraged.

**Q3. How does Spring resolve circular dependencies?**

Constructor cycles fail; singleton setter/field cycles can be resolved via early references but indicate bad design (and Boot disables by default).

**Q4. Singleton scope vs the Singleton pattern?**

Spring's singleton is one instance per container, not per JVM/classloader.

**Q5. What is a BeanPostProcessor?**

A hook invoked around bean initialization; AOP proxies and @Autowired processing use them.

## Common mistakes & debugging

- Using field injection and then being unable to unit test.
- Putting stateful fields in singleton beans.
- Scanning a package the config class does not cover.
- Typos in `@Qualifier` names.

## Further reading

- Spring Framework Reference: The IoC Container
- Spring Boot reference: Externalized Configuration

## Glossary

| Term | Meaning |
|------|---------|
| Bean | Object managed by the Spring container |
| ApplicationContext | The container interface |
| Stereotype | @Component/@Service/@Repository meta-annotations |
| Scope | Lifetime/visibility rules of a bean |
| Primary | Default candidate when several beans match |

## Answers

### Inversion of Control, dependency injection, and the container

1. Immutable, mandatory dependencies, easy unit tests, and cycles are detected early.
2. No, since Spring 4.3.
3. Semantics, and for @Repository exception translation.

### Choosing between beans: @Primary, @Qualifier, and component scanning

1. `NoUniqueBeanDefinitionException` at injection time.
2. Primary is the default for the type; Qualifier is a per-injection-point override.
3. Inject `List<T>` or `Map<String, T>`.

### Bean lifecycle and scopes

1. After the bean is constructed and its dependencies are injected.
2. No — keep it stateless or synchronize/immutable.
3. No; the container does not manage their destruction.

### Java-based configuration, @Bean, and @Value

1. They are injected by type (and qualifier) from the container.
2. Use property `x`, falling back to `y`.
3. Strings are not type-safe or grouped; `@ConfigurationProperties` is better for structured settings.
