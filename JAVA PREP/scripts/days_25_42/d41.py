from sx import *

TYPE = "Spring Boot (Observability)"

# ------------------------------------------------------------ task 1
OP = r'''package %PKG%;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class OrderProcessor {

    private static final Logger log = LoggerFactory.getLogger(OrderProcessor.class);

    /**
     * Logging contract (use PARAMETERIZED messages, never string concatenation):
     *  1. INFO  "Processing order {} (amount={})"      args: orderId, amount
     *  2. amount <= 0  -> ERROR "Invalid amount for order {}" with args (orderId, exception) where exception is a
     *                     new IllegalArgumentException("amount must be positive"); return false
     *  3. amount > 1000 -> WARN "Large order {}"        arg: orderId
     *  4. DEBUG "Order {} validated"                    arg: orderId   (emitted only when DEBUG is enabled)
     *  5. return true
     */
    public boolean process(String orderId, double amount) {
        //B! implement the logging contract
        log.info("Processing order {} (amount={})", orderId, amount);
        if (amount <= 0) {
            log.error("Invalid amount for order {}", orderId, new IllegalArgumentException("amount must be positive"));
            return false;
        }
        if (amount > 1000) {
            log.warn("Large order {}", orderId);
        }
        log.debug("Order {} validated", orderId);
        return true;
        //E!
    }
}
'''
T1 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import java.util.List;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;

class LoggingContractTest {

    Logger logger;
    ListAppender<ILoggingEvent> appender;
    OrderProcessor processor = new OrderProcessor();

    @BeforeEach
    void attach() {
        logger = (Logger) LoggerFactory.getLogger(OrderProcessor.class);
        logger.setLevel(Level.INFO);
        appender = new ListAppender<>();
        appender.start();
        logger.addAppender(appender);
    }

    @AfterEach
    void detach() {
        logger.detachAppender(appender);
        logger.setLevel(null);
    }

    private List<ILoggingEvent> events() {
        return appender.list;
    }

    @Test
    void normalOrderLogsOneInfoLineWithParameters() {
        assertThat(processor.process("A-1", 50.0)).isTrue();
        assertThat(events()).hasSize(1);
        ILoggingEvent e = events().get(0);
        assertThat(e.getLevel()).isEqualTo(Level.INFO);
        assertThat(e.getMessage()).isEqualTo("Processing order {} (amount={})");
        assertThat(e.getArgumentArray()).containsExactly("A-1", 50.0);
        assertThat(e.getFormattedMessage()).isEqualTo("Processing order A-1 (amount=50.0)");
    }

    @Test
    void largeOrdersWarn() {
        processor.process("B-2", 5000.0);
        assertThat(events()).extracting(ILoggingEvent::getLevel).containsExactly(Level.INFO, Level.WARN);
        assertThat(events().get(1).getFormattedMessage()).isEqualTo("Large order B-2");
    }

    @Test
    void invalidAmountLogsErrorWithStackTraceAndReturnsFalse() {
        assertThat(processor.process("C-3", 0)).isFalse();
        ILoggingEvent e = events().get(1);
        assertThat(e.getLevel()).isEqualTo(Level.ERROR);
        assertThat(e.getFormattedMessage()).isEqualTo("Invalid amount for order C-3");
        assertThat(e.getThrowableProxy()).isNotNull();
        assertThat(e.getThrowableProxy().getMessage()).isEqualTo("amount must be positive");
    }

    @Test
    void debugLineOnlyWhenDebugIsEnabled() {
        processor.process("D-4", 10);
        assertThat(events()).noneMatch(e -> e.getLevel() == Level.DEBUG);
        events().clear();
        logger.setLevel(Level.DEBUG);
        processor.process("D-4", 10);
        assertThat(events()).extracting(ILoggingEvent::getFormattedMessage).contains("Order D-4 validated");
    }

    @Test
    void messagesAreTemplatesNotConcatenated() {
        processor.process("E-5", 1);
        assertThat(events()).allSatisfy(e -> assertThat(e.getMessage()).doesNotContain("E-5"));
    }
}
'''
a1 = tk("slf4j-logging-contract", "SLF4J Logging Contract", "Warm-up",
    "Log with SLF4J levels and parameterized messages, attach exceptions correctly, and verify output with a Logback ListAppender.",
    {"main/OrderProcessor.java": OP},
    {"test/LoggingContractTest.java": T1},
    ["Implement `OrderProcessor.process` following the numbered logging contract."],
    ["The exception must be the LAST argument so SLF4J prints the stack trace.", "Debug messages must be skipped when the level is INFO.", "Never log secrets or full payloads."],
    ["`log.error(\"msg {}\", arg, exception)` treats the final Throwable as the exception.", "Parameterized messages avoid building strings when the level is disabled."],
    ["spring-boot-starter"], ttype=TYPE)

# ------------------------------------------------------------ task 2
ECHO = r'''package %PKG%;

import org.slf4j.MDC;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED: echoes the request id visible in the MDC while the request is handled. */
@RestController
public class EchoController {

    @GetMapping("/echo")
    public String echo() {
        return String.valueOf(MDC.get(RequestIdFilter.MDC_KEY));
    }
}
'''
RF = r'''package %PKG%;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.UUID;
import java.util.regex.Pattern;
import org.slf4j.MDC;
import org.springframework.web.filter.OncePerRequestFilter;

public class RequestIdFilter extends OncePerRequestFilter {

    public static final String HEADER = "X-Request-Id";
    public static final String MDC_KEY = "requestId";
    private static final Pattern SAFE = Pattern.compile("[A-Za-z0-9-]{1,64}");

    /**
     * 1. take the id from header X-Request-Id when it matches [A-Za-z0-9-]{1,64} (prevents log injection);
     *    otherwise generate UUID.randomUUID().toString()
     * 2. put it into the MDC under "requestId"
     * 3. echo it in the response header X-Request-Id
     * 4. continue the chain; ALWAYS remove the MDC key afterwards (threads are reused!)
     */
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        //B! implement the four steps
        String incoming = request.getHeader(HEADER);
        String id = incoming != null && SAFE.matcher(incoming).matches() ? incoming : UUID.randomUUID().toString();
        MDC.put(MDC_KEY, id);
        response.setHeader(HEADER, id);
        try {
            chain.doFilter(request, response);
        } finally {
            MDC.remove(MDC_KEY);
        }
        //E!
    }

    /** Logback console pattern that prints the request id: time [requestId] LEVEL logger - message */
    public static String logPattern() {
        //B! return the pattern using %X{requestId}
        return "%d{HH:mm:ss.SSS} [%X{requestId}] %-5level %logger{36} - %msg%n";
        //E!
    }
}
'''
T2 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.MDC;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

class RequestIdFilterTest {

    MockMvc mvc;

    @BeforeEach
    void setUp() {
        mvc = MockMvcBuilders.standaloneSetup(new EchoController()).addFilters(new RequestIdFilter()).build();
    }

    @Test
    void incomingIdIsUsedAndEchoed() throws Exception {
        mvc.perform(get("/echo").header("X-Request-Id", "abc-123")).andExpect(status().isOk())
                .andExpect(content().string("abc-123")).andExpect(header().string("X-Request-Id", "abc-123"));
    }

    @Test
    void missingIdIsGenerated() throws Exception {
        String id = mvc.perform(get("/echo")).andReturn().getResponse().getHeader("X-Request-Id");
        assertThat(id).isNotNull();
        assertThat(UUID.fromString(id)).isNotNull();
    }

    @Test
    void unsafeIdIsReplaced() throws Exception {
        String evil = "x\nFAKE LOG LINE";
        String id = mvc.perform(get("/echo").header("X-Request-Id", evil)).andReturn().getResponse().getHeader("X-Request-Id");
        assertThat(id).doesNotContain("FAKE").hasSize(36);
        String tooLong = "a".repeat(65);
        assertThat(mvc.perform(get("/echo").header("X-Request-Id", tooLong)).andReturn().getResponse().getHeader("X-Request-Id")).hasSize(36);
    }

    @Test
    void mdcIsClearedAfterTheRequest() throws Exception {
        mvc.perform(get("/echo").header("X-Request-Id", "keep-clean"));
        assertThat(MDC.get("requestId")).isNull();
    }

    @Test
    void patternReferencesTheMdcKey() {
        assertThat(RequestIdFilter.logPattern()).contains("%X{requestId}").contains("%msg%n");
    }
}
'''
a2 = tk("mdc-request-id-filter", "MDC Request Correlation Filter", "Core",
    "Correlate log lines per request: put a validated request id into the MDC, echo it in a header and always clean up.",
    {"main/EchoController.java": ECHO, "main/RequestIdFilter.java": RF},
    {"test/RequestIdFilterTest.java": T2},
    ["Implement `doFilterInternal` with validation, MDC handling, response header and cleanup.", "Return a Logback pattern that prints `%X{requestId}`."],
    ["MDC is thread-local: forgetting `remove` leaks ids into other requests on pooled threads.", "Untrusted header values can inject fake log lines (newlines)."],
    ["`OncePerRequestFilter` guarantees a single execution per request.", "Use try/finally around `chain.doFilter`."],
    ["spring-boot-starter-web"], ttype=TYPE)

# ------------------------------------------------------------ task 3
QSTATS = r'''package %PKG%;

import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.stereotype.Component;

/** PROVIDED: pretend work queue statistics (capacity 100). */
@Component
public class QueueStats {
    private final AtomicInteger depth = new AtomicInteger();

    public int getDepth() {
        return depth.get();
    }

    public void setDepth(int value) {
        depth.set(value);
    }
}
'''
QHI = r'''package %PKG%;

import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.stereotype.Component;

//A! register as a Spring bean so Actuator picks it up as the component named "queue"
@Component("queueHealthIndicator")
//E!
public class QueueHealthIndicator implements HealthIndicator {

    private final QueueStats stats;

    public QueueHealthIndicator(QueueStats stats) {
        this.stats = stats;
    }

    /**
     * depth < 80      -> UP
     * 80 <= depth < 100 -> OUT_OF_SERVICE (draining: no new work, HTTP 503)
     * depth >= 100    -> DOWN
     * Always include details: depth (int) and capacity (100).
     */
    @Override
    public Health health() {
        //B! choose status by depth and add the two details
        int d = stats.getDepth();
        Health.Builder builder = d >= 100 ? Health.down() : d >= 80 ? Health.outOfService() : Health.up();
        return builder.withDetail("depth", d).withDetail("capacity", 100).build();
        //E!
    }
}
'''
PROPS3 = "management.endpoints.web.exposure.include=health,info,metrics\nmanagement.endpoint.health.show-details=always\n"
T3 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.actuate.health.Status;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class QueueHealthTest {

    @Autowired
    MockMvc mvc;
    @Autowired
    QueueStats stats;

    @BeforeEach
    void reset() {
        stats.setDepth(0);
    }

    @Test
    void unitLevelStatusMapping() {
        QueueHealthIndicator hi = new QueueHealthIndicator(stats);
        stats.setDepth(79);
        assertThat(hi.health().getStatus()).isEqualTo(Status.UP);
        stats.setDepth(80);
        assertThat(hi.health().getStatus()).isEqualTo(Status.OUT_OF_SERVICE);
        stats.setDepth(99);
        assertThat(hi.health().getStatus()).isEqualTo(Status.OUT_OF_SERVICE);
        stats.setDepth(100);
        assertThat(hi.health().getStatus()).isEqualTo(Status.DOWN);
    }

    @Test
    void detailsAreAlwaysPresent() {
        stats.setDepth(12);
        assertThat(new QueueHealthIndicator(stats).health().getDetails()).containsEntry("depth", 12).containsEntry("capacity", 100);
    }

    @Test
    void healthyQueueGivesHttp200AndComponentUp() throws Exception {
        stats.setDepth(10);
        mvc.perform(get("/actuator/health")).andExpect(status().isOk()).andExpect(jsonPath("$.status").value("UP"))
                .andExpect(jsonPath("$.components.queue.status").value("UP"))
                .andExpect(jsonPath("$.components.queue.details.depth").value(10));
    }

    @Test
    void drainingQueueGivesHttp503() throws Exception {
        stats.setDepth(90);
        mvc.perform(get("/actuator/health")).andExpect(status().isServiceUnavailable())
                .andExpect(jsonPath("$.status").value("OUT_OF_SERVICE")).andExpect(jsonPath("$.components.queue.status").value("OUT_OF_SERVICE"));
    }

    @Test
    void fullQueueMakesTheApplicationDown() throws Exception {
        stats.setDepth(150);
        mvc.perform(get("/actuator/health")).andExpect(status().isServiceUnavailable()).andExpect(jsonPath("$.status").value("DOWN"));
    }
}
'''
a3 = tk("custom-health-indicator", "Custom Actuator HealthIndicator", "Core",
    "Contribute your own component to /actuator/health with status mapping, details and HTTP 503 semantics.",
    {"main/Application.java": APP, "main/QueueStats.java": QSTATS, "main/QueueHealthIndicator.java": QHI},
    {"test/QueueHealthTest.java": T3},
    ["Register `QueueHealthIndicator` as a bean named `queueHealthIndicator` (shown as component `queue`).", "Map queue depth to UP / OUT_OF_SERVICE / DOWN and add details."],
    ["The component name is the bean name without the `HealthIndicator` suffix.", "Health checks must be fast and must not throw; exceptions turn into DOWN.", "Aggregate status: the worst component wins."],
    ["`Health.up()`, `Health.outOfService()`, `Health.down()` return builders.", "OUT_OF_SERVICE and DOWN map to HTTP 503 by default."],
    ["spring-boot-starter-web", "spring-boot-starter-actuator"], ttype=TYPE,
    extra={"res/application.properties": PROPS3})

# ------------------------------------------------------------ task 4
OM = r'''package %PKG%;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.DistributionSummary;
import io.micrometer.core.instrument.Gauge;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Supplier;

public class OrderMetrics {

    private final MeterRegistry registry;

    public OrderMetrics(MeterRegistry registry) {
        this.registry = registry;
    }

    /** Counter "orders.placed" with ONE tag channel=<channel>; increments by 1 per call. */
    public void recordPlaced(String channel) {
        //B! registry.counter(name, tags...).increment()
        registry.counter("orders.placed", "channel", channel).increment();
        //E!
    }

    /** Runs the supplier inside Timer "orders.processing" and returns its value; the timer records even when it throws. */
    public <T> T timeProcessing(Supplier<T> work) {
        //B! Timer.builder(...).register(registry) then timer.record(supplier)
        Timer timer = Timer.builder("orders.processing").description("Order processing time").register(registry);
        return timer.record(work);
        //E!
    }

    /** Gauge "orders.queue.size" that always reports the CURRENT value of the given AtomicInteger. */
    public void registerQueueGauge(AtomicInteger queue) {
        //B! Gauge.builder(name, queue, AtomicInteger::get).register(registry)
        Gauge.builder("orders.queue.size", queue, AtomicInteger::get).register(registry);
        //E!
    }

    /** DistributionSummary "orders.amount" with base unit "eur": records the amount of each order. */
    public void recordAmount(double amount) {
        //B! DistributionSummary.builder(...).baseUnit(...).register(registry).record(amount)
        DistributionSummary.builder("orders.amount").baseUnit("eur").register(registry).record(amount);
        //E!
    }
}
'''
T4 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class MicrometerMetricsTest {

    SimpleMeterRegistry registry;
    OrderMetrics metrics;

    @BeforeEach
    void setUp() {
        registry = new SimpleMeterRegistry();
        metrics = new OrderMetrics(registry);
    }

    @Test
    void counterIsTaggedPerChannel() {
        metrics.recordPlaced("web");
        metrics.recordPlaced("web");
        metrics.recordPlaced("mobile");
        assertThat(registry.get("orders.placed").tag("channel", "web").counter().count()).isEqualTo(2.0);
        assertThat(registry.get("orders.placed").tag("channel", "mobile").counter().count()).isEqualTo(1.0);
    }

    @Test
    void timerRecordsDurationAndReturnsResult() {
        String result = metrics.timeProcessing(() -> {
            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "done";
        });
        assertThat(result).isEqualTo("done");
        var timer = registry.get("orders.processing").timer();
        assertThat(timer.count()).isEqualTo(1);
        assertThat(timer.totalTime(TimeUnit.MILLISECONDS)).isGreaterThanOrEqualTo(9.0);
    }

    @Test
    void timerAlsoCountsFailures() {
        assertThatThrownBy(() -> metrics.timeProcessing(() -> {
            throw new IllegalStateException("x");
        })).isInstanceOf(IllegalStateException.class);
        assertThat(registry.get("orders.processing").timer().count()).isEqualTo(1);
    }

    @Test
    void gaugeFollowsTheLiveValue() {
        AtomicInteger queue = new AtomicInteger(3);
        metrics.registerQueueGauge(queue);
        assertThat(registry.get("orders.queue.size").gauge().value()).isEqualTo(3.0);
        queue.set(11);
        assertThat(registry.get("orders.queue.size").gauge().value()).isEqualTo(11.0);
    }

    @Test
    void distributionSummaryTracksAmounts() {
        metrics.recordAmount(10);
        metrics.recordAmount(30);
        var summary = registry.get("orders.amount").summary();
        assertThat(summary.count()).isEqualTo(2);
        assertThat(summary.totalAmount()).isEqualTo(40.0);
        assertThat(summary.getId().getBaseUnit()).isEqualTo("eur");
        assertThat(summary.max()).isEqualTo(30.0);
    }
}
'''
a4 = tk("micrometer-order-metrics", "Micrometer Counters, Timers, Gauges and Summaries", "Challenge",
    "Instrument business code with Micrometer meters (tagged counter, timer, live gauge, distribution summary) and read them back from a SimpleMeterRegistry.",
    {"main/OrderMetrics.java": OM},
    {"test/MicrometerMetricsTest.java": T4},
    ["Implement the four `OrderMetrics` methods with the exact meter names, tags and units."],
    ["Gauges hold a weak reference to the observed object: keep it referenced elsewhere.", "Tag values must have bounded cardinality (never user ids).", "Timers must record even when the work throws."],
    ["`registry.counter(name, \"key\", \"value\")` creates/gets a tagged counter.", "`Timer#record(Supplier)` returns the supplier's value."],
    ["spring-boot-starter-actuator"], ttype=TYPE)

topics = [
    T("Logging with SLF4J and Logback",
      "**SLF4J** is the logging facade your code uses (`LoggerFactory.getLogger(X.class)`); **Logback** is Spring Boot's default implementation. Levels: TRACE < DEBUG < INFO < WARN < ERROR. Use parameterized messages (`log.info(\"order {}\", id)`) and pass exceptions as the last argument. Configure levels with `logging.level.<package>=DEBUG`, file output with `logging.file.name`, patterns with `logging.pattern.console`, or `logback-spring.xml` for full control and profiles.",
      "Logs are the first tool when production misbehaves. Consistent levels and structured messages make incidents diagnosable; the facade lets you swap implementations without code changes.",
      ["Cheap when disabled (parameterized messages)", "Runtime-configurable levels via Actuator `/loggers`", "Rich appenders and rolling policies", "Stack traces printed correctly when the exception is the last argument"],
      ["Over-logging costs I/O and money", "Easy to leak personal data or secrets", "Inconsistent messages are hard to search"],
      "String concatenation (`\"order \" + id`) builds the string even when the level is off. `e.printStackTrace()` bypasses the logging pipeline. `log.error(\"failed: \" + e.getMessage())` loses the stack trace. Logging passwords, tokens or card numbers creates compliance problems.",
      "```java\nprivate static final Logger log = LoggerFactory.getLogger(OrderService.class);\nlog.info(\"Processing order {} (amount={})\", id, amount);\nlog.error(\"Payment failed for order {}\", id, ex);   // ex last -> stack trace\nif (log.isDebugEnabled()) log.debug(\"state={}\", expensiveDump());\n```\n```properties\nlogging.level.root=INFO\nlogging.level.com.acme.orders=DEBUG\nlogging.pattern.console=%d{HH:mm:ss.SSS} [%X{requestId}] %-5level %logger{36} - %msg%n\n```",
      [("Test logs with ListAppender", "java", "ListAppender<ILoggingEvent> app = new ListAppender<>(); app.start();\n((ch.qos.logback.classic.Logger) LoggerFactory.getLogger(X.class)).addAppender(app);"),
       ("Change level at runtime", "text", "POST /actuator/loggers/com.acme.orders  {\"configuredLevel\":\"DEBUG\"}"),
       ("Level guide", "text", "ERROR: needs action now; WARN: unexpected but handled; INFO: business milestones; DEBUG/TRACE: diagnostics")],
      [("Why parameterized messages?", "They avoid string building when the level is disabled and keep the template constant."),
       ("Where does the exception go?", "As the last argument so the stack trace is logged."),
       ("SLF4J vs Logback?", "SLF4J is the API; Logback is the implementation.")]),
    T("MDC and request correlation",
      "The **Mapped Diagnostic Context** (`org.slf4j.MDC`) is a thread-local map whose entries can be printed in every log line with `%X{key}`. A servlet filter typically sets `requestId` (and maybe user/tenant) at the start of a request and clears it at the end. Micrometer Tracing (Boot 3) can propagate `traceId`/`spanId` across services automatically.",
      "In a busy service thousands of log lines interleave. A correlation id lets you filter all lines of one request (and across microservices) in seconds.",
      ["Searchable per-request logs", "No need to pass ids through method signatures", "Works with every logger call automatically"],
      ["Thread-local: not propagated to other threads (`@Async`, executors) unless you copy it", "Must be cleaned up (pooled threads)", "Untrusted headers need validation"],
      "Without correlation ids debugging means guessing which lines belong together. Forgetting `MDC.remove` leaks one user's id into the next request on the same thread. Accepting arbitrary header values lets attackers forge log lines (log injection).",
      "```java\nMDC.put(\"requestId\", id);\ntry { chain.doFilter(req, res); } finally { MDC.remove(\"requestId\"); }\n```\n```properties\nlogging.pattern.level=%5p [%X{requestId}]\n```\nFor executors: wrap tasks (`TaskDecorator`) to copy `MDC.getCopyOfContextMap()`.",
      [("TaskDecorator", "java", "return task -> { var ctx = MDC.getCopyOfContextMap(); return () -> { MDC.setContextMap(ctx); try { task.run(); } finally { MDC.clear(); } }; };"),
       ("Response header", "java", "response.setHeader(\"X-Request-Id\", id);"),
       ("Trace ids", "properties", "management.tracing.sampling.probability=1.0")],
      [("Why clear the MDC?", "Threads are reused; stale values would leak into other requests."),
       ("Is MDC inherited by new threads?", "Not automatically; copy it explicitly."),
       ("What is log injection?", "Forging log lines via newline characters in user-controlled data.")]),
    T("Actuator health and Micrometer metrics",
      "**Actuator** exposes `/actuator/health` (aggregated `HealthIndicator`s such as db, diskSpace, ping or your own) and `/actuator/metrics`. Health statuses: UP, DOWN, OUT_OF_SERVICE, UNKNOWN; the worst wins and DOWN/OUT_OF_SERVICE return HTTP 503. Readiness/liveness groups serve Kubernetes probes. **Micrometer** is the metrics facade: `Counter`, `Gauge`, `Timer`, `DistributionSummary`, tags; registries export to Prometheus, Datadog, etc. (`/actuator/prometheus` with the Prometheus registry).",
      "Operations teams alert on health and metrics, not on log lines. Business metrics (orders placed, queue depth) reveal problems earlier than errors do.",
      ["Standard endpoints and probes", "Vendor-neutral metrics API", "Automatic JVM/HTTP/datasource metrics", "Easy to extend"],
      ["Exposure must be restricted and secured", "Unbounded tag cardinality can blow up the metrics backend", "Slow health checks can take down the app under frequent probing"],
      "Putting `userId` in a tag creates millions of time series. A health indicator that calls a slow third party makes probes time out and triggers restarts. Exposing all endpoints publicly leaks configuration.",
      "```java\nregistry.counter(\"orders.placed\", \"channel\", \"web\").increment();\nTimer.builder(\"orders.processing\").register(registry).record(() -> work());\nGauge.builder(\"orders.queue.size\", queue, AtomicInteger::get).register(registry);\n```\n```properties\nmanagement.endpoints.web.exposure.include=health,info,metrics,prometheus\nmanagement.endpoint.health.show-details=when-authorized\nmanagement.endpoint.health.probes.enabled=true\n```",
      [("Health indicator", "java", "@Component class QueueHealthIndicator implements HealthIndicator { public Health health() { return Health.up().withDetail(\"depth\", 3).build(); } }"),
       ("Read a metric", "text", "GET /actuator/metrics/http.server.requests?tag=status:200"),
       ("@Timed on a controller", "java", "@Timed(\"api.orders\") @GetMapping(\"/orders\") ...")],
      [("Which health statuses map to HTTP 503?", "DOWN and OUT_OF_SERVICE."),
       ("Why avoid unbounded tags?", "Each distinct tag combination is a separate time series."),
       ("Liveness vs readiness?", "Liveness: restart me if broken; readiness: send me traffic only when ready.")]),
]

day(41, "Observability: SLF4J/Logback, MDC, Actuator Health and Micrometer Metrics", "Spring Boot",
    "Making services diagnosable and operable: logging, correlation ids, health checks and metrics",
    ["Log correctly with SLF4J levels and parameterized messages", "Correlate requests with MDC", "Write custom health indicators and understand status aggregation", "Instrument code with Micrometer meters", "Test logging and metrics without external systems"],
    ["Day 29 Actuator basics", "Day 36 RestClient/CORS"],
    topics, [a1, a2, a3, a4],
    [("Why SLF4J?", "A stable facade so libraries and apps are independent of the logging backend."),
     ("What is MDC?", "Thread-local context map included in log lines."),
     ("How do health groups help Kubernetes?", "Liveness and readiness probes can reflect different sets of indicators."),
     ("Counter vs Gauge vs Timer?", "Counter only goes up, Gauge samples a current value, Timer measures durations and counts."),
     ("What is metric cardinality?", "The number of distinct tag-value combinations.")],
    ["String concatenation in log calls.", "Logging secrets or personal data.", "Forgetting to clear MDC.", "High-cardinality tags.", "Exposing every Actuator endpoint."],
    ["Spring Boot Reference: Logging, Actuator, Metrics", "Micrometer documentation", "SLF4J FAQ"],
    [("SLF4J", "Logging facade"), ("Logback", "Default logging implementation"), ("MDC", "Mapped diagnostic context"),
     ("HealthIndicator", "Contributor to /actuator/health"), ("Micrometer", "Metrics facade")],
    "2–3 h theory + 3–5 h tasks", spring=True)
