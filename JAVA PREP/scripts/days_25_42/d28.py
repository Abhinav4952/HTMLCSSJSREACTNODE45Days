from common import *

STARTERS = ["spring-boot-starter"]
TYPE = "Spring Boot"

# ------------------------------------------------------------ task 1
c1 = {
    "main/MessageRepository.java": r'''package %PKG%;

/** PROVIDED collaborator. */
public interface MessageRepository {
    String greetingPrefix();
}
''',
    "main/InMemoryMessageRepository.java": r'''package %PKG%;

import org.springframework.stereotype.Repository;

/** PROVIDED bean: a trivial repository returning "Hello". */
@Repository
public class InMemoryMessageRepository implements MessageRepository {
    @Override
    public String greetingPrefix() {
        return "Hello";
    }
}
''',
    "main/GreetingService.java": r'''package %PKG%;

public interface GreetingService {
    String greet(String name);
}
''',
    "main/GreetingServiceImpl.java": r'''package %PKG%;

// TODO(%TAG%): register this class as a Spring bean with a stereotype annotation (@Service)
public class GreetingServiceImpl implements GreetingService {

    private final MessageRepository repository;

    // Single constructor => Spring injects the MessageRepository bean automatically (no @Autowired needed).
    public GreetingServiceImpl(MessageRepository repository) {
        this.repository = repository;
    }

    /** "<prefix>, <name>!" e.g. "Hello, Ada!". Blank or null name -> IllegalArgumentException. */
    @Override
    public String greet(String name) {
        // TODO(%TAG%): use the injected repository and validate the name
        throw new UnsupportedOperationException("TODO(%TAG%): implement greet");
    }
}
''',
    "main/AppConfig.java": r'''package %PKG%;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

/** PROVIDED: scans this package for stereotype-annotated classes. */
@Configuration
@ComponentScan
public class AppConfig {
}
''',
    "test/GreetingServiceTest.java": r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class GreetingServiceTest {

    @Test
    void greetsUsingTheInjectedRepository() {
        GreetingService service = new GreetingServiceImpl(() -> "Hi");
        assertThat(service.greet("Ada")).isEqualTo("Hi, Ada!");
    }

    @Test
    void rejectsBlankNames() {
        GreetingService service = new GreetingServiceImpl(() -> "Hi");
        assertThatThrownBy(() -> service.greet(" ")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.greet(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void containerWiresTheServiceWithConstructorInjection() {
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class)) {
            assertThat(ctx.getBeansOfType(GreetingService.class)).hasSize(1);
            assertThat(ctx.getBean(GreetingService.class).greet("Ada")).isEqualTo("Hello, Ada!");
        }
    }
}
''',
}
s1 = {"main/GreetingServiceImpl.java": r'''package %PKG%;

import org.springframework.stereotype.Service;

@Service
public class GreetingServiceImpl implements GreetingService {
    private final MessageRepository repository;
    public GreetingServiceImpl(MessageRepository repository) { this.repository = repository; }
    @Override
    public String greet(String name) {
        if (name == null || name.isBlank()) throw new IllegalArgumentException("name");
        return repository.greetingPrefix() + ", " + name + "!";
    }
}
'''}
k1 = task("constructor-injection", "Constructor Injection", "Warm-up", TYPE,
    "Register a service as a bean, inject its collaborator through the constructor, and prove it works both as a plain object and inside a container.",
    "boot", c1,
    ["Annotate `GreetingServiceImpl` with a stereotype annotation so component scanning registers it.", "Implement `greet` using the injected repository.",
     "Keep the dependency `final` and constructor-injected (no field injection)."],
    ["Blank or null names -> `IllegalArgumentException`.", "Exactly one `GreetingService` bean must exist."],
    ["`@Service` is a specialization of `@Component`.", "A class with one constructor needs no `@Autowired`."], starters=STARTERS, sol=s1)

# ------------------------------------------------------------ task 2
c2 = {
    "main/PaymentGateway.java": "package %PKG%;\n\npublic interface PaymentGateway {\n    String name();\n}\n",
    "main/SimpleGateway.java": r'''package %PKG%;

/** PROVIDED simple implementation. */
public class SimpleGateway implements PaymentGateway {
    private final String name;

    public SimpleGateway(String name) {
        this.name = name;
    }

    @Override
    public String name() {
        return name;
    }
}
''',
    "main/GatewayConfig.java": r'''package %PKG%;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@ComponentScan
public class GatewayConfig {

    // TODO(%TAG%): mark this bean as the default choice when a PaymentGateway is injected without a qualifier
    @Bean("stripe")
    public PaymentGateway stripe() {
        return new SimpleGateway("stripe");
    }

    @Bean("paypal")
    public PaymentGateway paypal() {
        return new SimpleGateway("paypal");
    }
}
''',
    "main/DefaultCheckout.java": r'''package %PKG%;

import org.springframework.stereotype.Service;

/** Uses whichever gateway is @Primary. */
@Service
public class DefaultCheckout {

    private final PaymentGateway gateway;

    public DefaultCheckout(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    /** "<gateway name>:<cents>"; cents &lt;= 0 -> IllegalArgumentException. */
    public String pay(int cents) {
        // TODO(%TAG%): delegate to the injected gateway
        throw new UnsupportedOperationException("TODO(%TAG%): implement pay");
    }
}
''',
    "main/PaypalCheckout.java": r'''package %PKG%;

import org.springframework.stereotype.Service;

/** Must always use the "paypal" gateway, regardless of @Primary. */
@Service
public class PaypalCheckout {

    private final PaymentGateway gateway;

    // TODO(%TAG%): select the bean named "paypal" for this parameter (@Qualifier)
    public PaypalCheckout(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    /** "<gateway name>:<cents>"; cents &lt;= 0 -> IllegalArgumentException. */
    public String pay(int cents) {
        // TODO(%TAG%): delegate to the injected gateway
        throw new UnsupportedOperationException("TODO(%TAG%): implement pay");
    }
}
''',
    "test/CheckoutTest.java": r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class CheckoutTest {

    @Test
    void unqualifiedInjectionPicksThePrimaryGateway() {
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(GatewayConfig.class)) {
            assertThat(ctx.getBean(PaymentGateway.class).name()).isEqualTo("stripe");
            assertThat(ctx.getBean(DefaultCheckout.class).pay(500)).isEqualTo("stripe:500");
        }
    }

    @Test
    void qualifierOverridesPrimary() {
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(GatewayConfig.class)) {
            assertThat(ctx.getBean(PaypalCheckout.class).pay(500)).isEqualTo("paypal:500");
            assertThat(ctx.getBeansOfType(PaymentGateway.class)).containsOnlyKeys("stripe", "paypal");
        }
    }

    @Test
    void rejectsNonPositiveAmounts() {
        assertThatThrownBy(() -> new DefaultCheckout(new SimpleGateway("x")).pay(0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new PaypalCheckout(new SimpleGateway("x")).pay(-5)).isInstanceOf(IllegalArgumentException.class);
    }
}
''',
}
s2 = {
    "main/GatewayConfig.java": c2["main/GatewayConfig.java"].replace("    @Bean(\"stripe\")", "    @org.springframework.context.annotation.Primary\n    @Bean(\"stripe\")"),
    "main/DefaultCheckout.java": c2["main/DefaultCheckout.java"].replace('        throw new UnsupportedOperationException("TODO(%TAG%): implement pay");',
        '        if (cents <= 0) throw new IllegalArgumentException("cents");\n        return gateway.name() + ":" + cents;'),
    "main/PaypalCheckout.java": c2["main/PaypalCheckout.java"].replace("public PaypalCheckout(PaymentGateway gateway)", 'public PaypalCheckout(@org.springframework.beans.factory.annotation.Qualifier("paypal") PaymentGateway gateway)').replace(
        '        throw new UnsupportedOperationException("TODO(%TAG%): implement pay");', '        if (cents <= 0) throw new IllegalArgumentException("cents");\n        return gateway.name() + ":" + cents;'),
}
k2 = task("qualifier-primary", "@Primary and @Qualifier", "Core", TYPE,
    "Resolve ambiguity between two beans of the same type with @Primary and override the default with @Qualifier at a single injection point.",
    "boot", c2,
    ["Mark the `stripe` bean as `@Primary`.", "Make `PaypalCheckout` inject the `paypal` bean with `@Qualifier`.", "Implement both `pay` methods."],
    ["Without `@Primary` the context fails with `NoUniqueBeanDefinitionException` — that is the lesson.", "Non-positive amounts are rejected."],
    ["`@Qualifier(\"paypal\")` matches the bean name given in `@Bean(\"paypal\")`.", "`@Primary` is a default; `@Qualifier` is an explicit choice."],
    starters=STARTERS, sol=s2)

# ------------------------------------------------------------ task 3
c3 = {
    "main/LifecycleRecorder.java": r'''package %PKG%;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.springframework.stereotype.Component;

/** PROVIDED: shared log of lifecycle events. */
@Component
public class LifecycleRecorder {
    private final List<String> events = Collections.synchronizedList(new ArrayList<>());

    public void record(String event) {
        events.add(event);
    }

    public List<String> events() {
        return List.copyOf(events);
    }
}
''',
    "main/LifecycleBean.java": r'''package %PKG%;

import org.springframework.stereotype.Component;

@Component
public class LifecycleBean {

    private final LifecycleRecorder recorder;

    public LifecycleBean(LifecycleRecorder recorder) {
        this.recorder = recorder;
        recorder.record("ctor");
    }

    // TODO(%TAG%): run this after dependency injection (@PostConstruct) and record "init"
    public void init() {
        throw new UnsupportedOperationException("TODO(%TAG%): implement init");
    }

    // TODO(%TAG%): run this on context shutdown (@PreDestroy) and record "destroy"
    public void close() {
        throw new UnsupportedOperationException("TODO(%TAG%): implement close");
    }
}
''',
    "main/ReportBuilder.java": r'''package %PKG%;

import org.springframework.stereotype.Component;

// TODO(%TAG%): every injection/lookup must get a NEW instance (prototype scope)
@Component
public class ReportBuilder {
    private final StringBuilder content = new StringBuilder();

    public ReportBuilder append(String line) {
        content.append(line).append('\n');
        return this;
    }

    public String build() {
        return content.toString();
    }
}
''',
    "main/LifecycleConfig.java": r'''package %PKG%;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@ComponentScan
public class LifecycleConfig {
}
''',
    "test/LifecycleTest.java": r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class LifecycleTest {

    @Test
    void initAndDestroyRecordEvents() {
        LifecycleRecorder rec = new LifecycleRecorder();
        LifecycleBean bean = new LifecycleBean(rec);
        bean.init();
        bean.close();
        assertThat(rec.events()).containsExactly("ctor", "init", "destroy");
    }

    @Test
    void containerCallsCallbacksInOrder() {
        AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(LifecycleConfig.class);
        LifecycleRecorder rec = ctx.getBean(LifecycleRecorder.class);
        assertThat(rec.events()).containsExactly("ctor", "init");
        ctx.close();
        assertThat(rec.events()).containsExactly("ctor", "init", "destroy");
    }

    @Test
    void singletonIsSharedPrototypeIsNot() {
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(LifecycleConfig.class)) {
            assertThat(ctx.getBean(LifecycleRecorder.class)).isSameAs(ctx.getBean(LifecycleRecorder.class));
            ReportBuilder a = ctx.getBean(ReportBuilder.class);
            ReportBuilder b = ctx.getBean(ReportBuilder.class);
            assertThat(a).isNotSameAs(b);
            assertThat(a.append("x").build()).isEqualTo("x\n");
            assertThat(b.build()).isEmpty();
        }
    }
}
''',
}
s3 = {
    "main/LifecycleBean.java": c3["main/LifecycleBean.java"].replace('    public void init() {\n        throw new UnsupportedOperationException("TODO(%TAG%): implement init");',
        '    @jakarta.annotation.PostConstruct\n    public void init() {\n        recorder.record("init");').replace('    public void close() {\n        throw new UnsupportedOperationException("TODO(%TAG%): implement close");',
        '    @jakarta.annotation.PreDestroy\n    public void close() {\n        recorder.record("destroy");'),
    "main/ReportBuilder.java": c3["main/ReportBuilder.java"].replace("@Component\n", '@Component\n@org.springframework.context.annotation.Scope("prototype")\n'),
}
k3 = task("bean-lifecycle", "Bean Lifecycle and Scope", "Core", TYPE,
    "Hook into construction, initialization and destruction with @PostConstruct/@PreDestroy and demonstrate singleton vs prototype scope.",
    "boot", c3,
    ["Implement `init` and `close` and register them as lifecycle callbacks.", "Make `ReportBuilder` a prototype-scoped bean.",
     "Explain the order constructor -> `@PostConstruct` -> use -> `@PreDestroy`."],
    ["Callbacks must not run before the context has injected dependencies.", "`ctx.close()` triggers destroy callbacks for singletons only."],
    ["Annotations live in `jakarta.annotation` (Spring Boot 3+).", "Prototype beans are not destroyed by the container."],
    starters=STARTERS, sol=s3)

# ------------------------------------------------------------ task 4
c4 = {
    "main/TaxPolicy.java": "package %PKG%;\n\n/** PROVIDED. rate is a fraction, e.g. 0.2 = 20%. */\npublic record TaxPolicy(double rate) {\n}\n",
    "main/PriceCalculator.java": r'''package %PKG%;

/** PROVIDED. */
public class PriceCalculator {
    private final TaxPolicy taxPolicy;

    public PriceCalculator(TaxPolicy taxPolicy) {
        this.taxPolicy = taxPolicy;
    }

    public long priceWithTax(long cents) {
        return Math.round(cents * (1 + taxPolicy.rate()));
    }
}
''',
    "main/PricingConfig.java": r'''package %PKG%;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class PricingConfig {

    /** Rate from property {@code tax.rate}, default 0.2. A rate outside [0, 1] -> IllegalArgumentException. */
    @Bean
    // TODO(%TAG%): inject the property: add @Value("${tax.rate:0.2}") to the parameter
    public TaxPolicy taxPolicy(double rate) {
        // TODO(%TAG%): validate the rate and return the policy
        throw new UnsupportedOperationException("TODO(%TAG%): implement taxPolicy");
    }

    @Bean
    public PriceCalculator priceCalculator(TaxPolicy taxPolicy) {
        // TODO(%TAG%): wire the calculator with the policy bean
        throw new UnsupportedOperationException("TODO(%TAG%): implement priceCalculator");
    }
}
''',
    "test/PricingConfigTest.java": r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.core.env.MapPropertySource;

class PricingConfigTest {

    private static AnnotationConfigApplicationContext context(Map<String, Object> props) {
        AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext();
        ctx.getEnvironment().getPropertySources().addFirst(new MapPropertySource("test", props));
        ctx.register(PricingConfig.class);
        ctx.refresh();
        return ctx;
    }

    @Test
    void defaultRateIsTwentyPercent() {
        try (AnnotationConfigApplicationContext ctx = context(Map.of())) {
            assertThat(ctx.getBean(TaxPolicy.class).rate()).isEqualTo(0.2);
            assertThat(ctx.getBean(PriceCalculator.class).priceWithTax(1000)).isEqualTo(1200);
        }
    }

    @Test
    void rateComesFromTheEnvironment() {
        try (AnnotationConfigApplicationContext ctx = context(Map.of("tax.rate", "0.1"))) {
            assertThat(ctx.getBean(PriceCalculator.class).priceWithTax(1000)).isEqualTo(1100);
        }
    }

    @Test
    void invalidRateFailsContextStartup() {
        assertThatThrownBy(() -> context(Map.of("tax.rate", "1.5")))
                .hasRootCauseInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void calculatorUsesTheSameTaxPolicyBean() {
        try (AnnotationConfigApplicationContext ctx = context(Map.of("tax.rate", "0.5"))) {
            assertThat(ctx.getBean(PriceCalculator.class).priceWithTax(200)).isEqualTo(300);
        }
    }
}
''',
}
s4 = {"main/PricingConfig.java": r'''package %PKG%;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class PricingConfig {
    @Bean
    public TaxPolicy taxPolicy(@Value("${tax.rate:0.2}") double rate) {
        if (rate < 0 || rate > 1) throw new IllegalArgumentException("rate");
        return new TaxPolicy(rate);
    }
    @Bean
    public PriceCalculator priceCalculator(TaxPolicy taxPolicy) { return new PriceCalculator(taxPolicy); }
}
'''}
k4 = task("config-bean-lab", "Java Config and @Value", "Challenge", TYPE,
    "Build beans with @Configuration/@Bean methods, inject a property with a default via @Value, validate it, and wire one bean into another.",
    "boot", c4,
    ["Add `@Value(\"${tax.rate:0.2}\")` to the `taxPolicy` parameter and validate the range.", "Implement both `@Bean` methods.", "Show the default and an overridden property both work."],
    ["Rate must be within 0..1 inclusive; otherwise context startup fails.", "Both beans are singletons: the calculator must receive the container's `TaxPolicy`."],
    ["Without `@Value` Spring cannot inject a primitive `double` and fails with `NoSuchBeanDefinitionException`.", "`${key:default}` supplies the default."],
    starters=STARTERS, sol=s4)

topics = [
    T("Inversion of Control, dependency injection, and the container",
      "**IoC** means objects do not create their collaborators; a container does. **Dependency injection (DI)** is the technique: the container reads configuration (annotations/Java config), creates **beans**, resolves their dependencies and hands them in — preferably through the **constructor**. The `ApplicationContext` is that container.",
      "Hard-coded `new` calls weld classes together, making tests hard and swaps painful. DI gives loose coupling (depend on interfaces), easy mocking, and central lifecycle management — the basis of everything in Spring Boot.",
      ["Loose coupling and testability (pass a fake via the constructor)", "Constructor injection makes dependencies explicit, final and non-null", "Container manages lifecycle and scope", "Cross-cutting features (AOP, transactions) hook in via proxies"],
      ["Wiring errors appear at startup (or runtime) instead of compile time", "Debugging proxies and bean graphs has a learning curve", "Overuse leads to 'everything is a bean' and hidden coupling"],
      "Field injection (`@Autowired private X x`) hides dependencies and makes plain unit tests impossible without reflection. Circular constructor dependencies fail with `BeanCurrentlyInCreationException`. Missing beans give `NoSuchBeanDefinitionException` / `UnsatisfiedDependencyException`.",
      "```java\n@Service\npublic class GreetingServiceImpl implements GreetingService {\n    private final MessageRepository repo;\n    public GreetingServiceImpl(MessageRepository repo) { this.repo = repo; } // no @Autowired needed (single ctor)\n}\n\n@Configuration @ComponentScan class AppConfig {}\nvar ctx = new AnnotationConfigApplicationContext(AppConfig.class);\nGreetingService s = ctx.getBean(GreetingService.class);\n```\nStereotypes: `@Component`, `@Service`, `@Repository` (adds exception translation), `@Controller`/`@RestController`.",
      [("Constructor injection vs `new`", "java", "// tightly coupled\nclass Bad { private final Repo r = new JdbcRepo(); }\n// injected\nclass Good { private final Repo r; Good(Repo r) { this.r = r; } }"),
       ("Unit test without Spring", "java", "GreetingService s = new GreetingServiceImpl(() -> \"Hi\");\nassertThat(s.greet(\"Ada\")).isEqualTo(\"Hi, Ada!\");"),
       ("Starting a container", "java", "try (var ctx = new AnnotationConfigApplicationContext(AppConfig.class)) {\n    System.out.println(ctx.getBeanDefinitionNames().length);\n}")],
      [("Why prefer constructor injection?", "Immutable, mandatory dependencies, easy unit tests, and cycles are detected early."),
       ("Is `@Autowired` required on a single-constructor bean?", "No, since Spring 4.3."),
       ("What do stereotypes add beyond @Component?", "Semantics, and for @Repository exception translation.")]),
    T("Choosing between beans: @Primary, @Qualifier, and component scanning",
      "When several beans share a type, Spring needs a rule. **`@Primary`** marks the default candidate; **`@Qualifier(\"name\")`** selects explicitly (by bean name or custom qualifier). **Component scanning** (`@ComponentScan`) discovers annotated classes under a base package; `@Bean` methods register beans explicitly.",
      "Real systems have multiple implementations (payment gateways, serializers, data sources). Explicit selection prevents ambiguous wiring and silent wrong choices.",
      ["Clear, declarative selection", "`@Primary` gives sane defaults with explicit overrides", "Collections injection (`List<PaymentGateway>`) enables strategy patterns", "Scanning removes XML/boilerplate"],
      ["String qualifiers are not refactor-safe", "Scanning can pick up unintended classes if packages are broad", "Too many primaries become confusing"],
      "Two candidates and no rule -> `NoUniqueBeanDefinitionException: expected single matching bean but found 2`. A mistyped qualifier gives `NoSuchBeanDefinitionException`. Scanning from the wrong package silently registers nothing.",
      "```java\n@Bean @Primary PaymentGateway stripe() { ... }\n@Bean PaymentGateway paypal() { ... }\n\n@Service class PaypalCheckout {\n    PaypalCheckout(@Qualifier(\"paypal\") PaymentGateway g) { ... }\n}\n```\nResolution order: type -> `@Primary` -> `@Priority` -> parameter name = bean name.",
      [("Two gateways", "java", "@Configuration class GatewayConfig {\n  @Bean @Primary PaymentGateway stripe() { return new Stripe(); }\n  @Bean PaymentGateway paypal() { return new Paypal(); }\n}"),
       ("Inject all implementations", "java", "@Service class Router {\n  Router(Map<String, PaymentGateway> byName) { ... } // keys are bean names\n}"),
       ("Custom base package", "java", "@Configuration @ComponentScan(basePackages = \"com.javaprep.shop\") class ShopConfig {}")],
      [("What happens with two candidates and no @Primary?", "`NoUniqueBeanDefinitionException` at injection time."),
       ("Qualifier vs Primary?", "Primary is the default for the type; Qualifier is a per-injection-point override."),
       ("How can you inject every implementation?", "Inject `List<T>` or `Map<String, T>`.")]),
    T("Bean lifecycle and scopes",
      "The container instantiates a bean, injects dependencies, applies post-processors, calls init callbacks (`@PostConstruct`, `InitializingBean`, `initMethod`), the bean is used, and on shutdown destroy callbacks (`@PreDestroy`, `DisposableBean`) run. **Scopes**: `singleton` (default, one per container), `prototype` (new per request), plus web scopes (`request`, `session`).",
      "Resources (pools, caches, schedulers) must be started after injection and released on shutdown. Scope decides whether state is shared — a major source of concurrency bugs.",
      ["Deterministic startup/shutdown hooks", "Singleton default saves memory", "Prototype gives per-use state", "Hooks keep resource handling out of business code"],
      ["Singletons must be thread-safe", "Prototype beans injected into singletons are created once (need `ObjectProvider`)", "Destroy callbacks are not called for prototypes"],
      "Mutable state in a singleton (`private List<X> cache`) causes race conditions. Using fields in the constructor that depend on injection before it finished causes `NullPointerException` — do it in `@PostConstruct`. A prototype injected into a singleton behaves like a singleton.",
      "```java\n@Component class Cache {\n  @PostConstruct void warm() { ... }\n  @PreDestroy void flush() { ... }\n}\n@Component @Scope(\"prototype\") class ReportBuilder { }\n```\nOrder: constructor -> injection -> `@PostConstruct` -> ready -> `@PreDestroy` on `ctx.close()`.",
      [("Events order", "text", "ctor -> init (after injection) -> ... -> destroy (context close)"),
       ("Prototype from singleton", "java", "@Component class Service {\n  private final ObjectProvider<ReportBuilder> builders;\n  void run() { ReportBuilder b = builders.getObject(); }\n}"),
       ("Initialization with @Bean", "java", "@Bean(initMethod = \"start\", destroyMethod = \"stop\") Server server() { return new Server(); }")],
      [("When is @PostConstruct called?", "After the bean is constructed and its dependencies are injected."),
       ("Is a singleton bean thread-safe by default?", "No — keep it stateless or synchronize/immutable."),
       ("Does Spring call @PreDestroy for prototypes?", "No; the container does not manage their destruction.")]),
    T("Java-based configuration, @Bean, and @Value",
      "`@Configuration` classes declare beans with `@Bean` methods, giving full control (third-party classes, conditional creation). Method parameters are injected from the container, so beans wire into each other. `@Value(\"${key:default}\")` injects externalized properties with defaults; Boot's `Environment` merges sources (env vars, `application.yml`, CLI).",
      "Third-party classes cannot be annotated; configuration classes centralize wiring and make construction explicit and testable.",
      ["Explicit and type-safe wiring", "Works for classes you do not own", "Properties externalized per environment", "Proxy-based `@Configuration` ensures singleton semantics between `@Bean` methods"],
      ["Boilerplate versus scanning", "`@Value` strings are untyped (prefer `@ConfigurationProperties`, Day 29)", "Misconfigured placeholders fail at startup"],
      "Missing property without default -> `IllegalArgumentException: Could not resolve placeholder 'x'`. Calling a `@Bean` method directly from a `@Component` (not `@Configuration`) creates a second instance.",
      "```java\n@Configuration\nclass PricingConfig {\n  @Bean TaxPolicy taxPolicy(@Value(\"${tax.rate:0.2}\") double rate) { return new TaxPolicy(rate); }\n  @Bean PriceCalculator calc(TaxPolicy p) { return new PriceCalculator(p); }\n}\n```",
      [("Property with default", "java", "@Value(\"${app.name:demo}\") String appName;"),
       ("Programmatic property override in tests", "java", "ctx.getEnvironment().getPropertySources().addFirst(new MapPropertySource(\"t\", Map.of(\"tax.rate\", \"0.1\")));"),
       ("Fail-fast validation", "java", "if (rate < 0 || rate > 1) throw new IllegalArgumentException(\"rate\");")],
      [("How are @Bean method parameters resolved?", "They are injected by type (and qualifier) from the container."),
       ("What does `${x:y}` mean?", "Use property `x`, falling back to `y`."),
       ("Why not use @Value everywhere?", "Strings are not type-safe or grouped; `@ConfigurationProperties` is better for structured settings.")]),
]

day(28, "Spring Core: IoC and Dependency Injection", "Spring Boot",
    "How the Spring container creates and wires objects: constructor injection, bean selection, lifecycle, scopes, and Java configuration",
    ["Explain IoC/DI and why constructor injection is preferred", "Register beans via stereotypes, component scanning and @Bean methods", "Resolve ambiguity with @Primary and @Qualifier",
     "Use @PostConstruct/@PreDestroy and understand singleton vs prototype scope", "Inject externalized properties with @Value and defaults"],
    ["Day 21–27 Java fundamentals and JDBC", "Interfaces and polymorphism"],
    topics, [k1, k2, k3, k4],
    [("What is IoC?", "A design principle where the framework controls object creation and wiring instead of your code."),
     ("Constructor vs setter vs field injection?", "Constructor for required deps (immutable, testable); setter for optional; field injection discouraged."),
     ("How does Spring resolve circular dependencies?", "Constructor cycles fail; singleton setter/field cycles can be resolved via early references but indicate bad design (and Boot disables by default)."),
     ("Singleton scope vs the Singleton pattern?", "Spring's singleton is one instance per container, not per JVM/classloader."),
     ("What is a BeanPostProcessor?", "A hook invoked around bean initialization; AOP proxies and @Autowired processing use them.")],
    ["Using field injection and then being unable to unit test.", "Putting stateful fields in singleton beans.", "Scanning a package the config class does not cover.", "Typos in `@Qualifier` names."],
    ["Spring Framework Reference: The IoC Container", "Spring Boot reference: Externalized Configuration"],
    [("Bean", "Object managed by the Spring container"), ("ApplicationContext", "The container interface"), ("Stereotype", "@Component/@Service/@Repository meta-annotations"),
     ("Scope", "Lifetime/visibility rules of a bean"), ("Primary", "Default candidate when several beans match")],
    "2–3 h theory + 3–5 h tasks", spring=True)
