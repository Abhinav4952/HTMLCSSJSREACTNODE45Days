# Day 41 — Observability: SLF4J/Logback, MDC, Actuator Health and Micrometer Metrics

**Phase:** Spring Boot  
**Primary theme:** Making services diagnosable and operable: logging, correlation ids, health checks and metrics  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-slf4j-logging-contract`, `task-02-mdc-request-id-filter`, `task-03-custom-health-indicator`, `task-04-micrometer-order-metrics`  
**Instruction alignment:** Maps to Day 41 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Making services diagnosable and operable: logging, correlation ids, health checks and metrics. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. Logging with SLF4J and Logback
2. MDC and request correlation
3. Actuator health and Micrometer metrics
4. Interview corner, common mistakes, glossary

## Subtopics

### Logging with SLF4J and Logback

#### What it is

**SLF4J** is the logging facade your code uses (`LoggerFactory.getLogger(X.class)`); **Logback** is Spring Boot's default implementation. Levels: TRACE < DEBUG < INFO < WARN < ERROR. Use parameterized messages (`log.info("order {}", id)`) and pass exceptions as the last argument. Configure levels with `logging.level.<package>=DEBUG`, file output with `logging.file.name`, patterns with `logging.pattern.console`, or `logback-spring.xml` for full control and profiles.

#### Why it exists / why it matters

Logs are the first tool when production misbehaves. Consistent levels and structured messages make incidents diagnosable; the facade lets you swap implementations without code changes.

#### Pros and cons

**Pros**

- Cheap when disabled (parameterized messages)
- Runtime-configurable levels via Actuator `/loggers`
- Rich appenders and rolling policies
- Stack traces printed correctly when the exception is the last argument

**Cons / trade-offs**

- Over-logging costs I/O and money
- Easy to leak personal data or secrets
- Inconsistent messages are hard to search

#### What happens without it / when misused

String concatenation (`"order " + id`) builds the string even when the level is off. `e.printStackTrace()` bypasses the logging pipeline. `log.error("failed: " + e.getMessage())` loses the stack trace. Logging passwords, tokens or card numbers creates compliance problems.

#### Syntax and rules

```java
private static final Logger log = LoggerFactory.getLogger(OrderService.class);
log.info("Processing order {} (amount={})", id, amount);
log.error("Payment failed for order {}", id, ex);   // ex last -> stack trace
if (log.isDebugEnabled()) log.debug("state={}", expensiveDump());
```
```properties
logging.level.root=INFO
logging.level.com.acme.orders=DEBUG
logging.pattern.console=%d{HH:mm:ss.SSS} [%X{requestId}] %-5level %logger{36} - %msg%n
```

#### Examples

**Example 1 — Test logs with ListAppender**

```java
ListAppender<ILoggingEvent> app = new ListAppender<>(); app.start();
((ch.qos.logback.classic.Logger) LoggerFactory.getLogger(X.class)).addAppender(app);
```

**Example 2 — Change level at runtime**

```text
POST /actuator/loggers/com.acme.orders  {"configuredLevel":"DEBUG"}
```

**Example 3 — Level guide**

```text
ERROR: needs action now; WARN: unexpected but handled; INFO: business milestones; DEBUG/TRACE: diagnostics
```

#### Quick checks

1. Why parameterized messages?
2. Where does the exception go?
3. SLF4J vs Logback?

### MDC and request correlation

#### What it is

The **Mapped Diagnostic Context** (`org.slf4j.MDC`) is a thread-local map whose entries can be printed in every log line with `%X{key}`. A servlet filter typically sets `requestId` (and maybe user/tenant) at the start of a request and clears it at the end. Micrometer Tracing (Boot 3) can propagate `traceId`/`spanId` across services automatically.

#### Why it exists / why it matters

In a busy service thousands of log lines interleave. A correlation id lets you filter all lines of one request (and across microservices) in seconds.

#### Pros and cons

**Pros**

- Searchable per-request logs
- No need to pass ids through method signatures
- Works with every logger call automatically

**Cons / trade-offs**

- Thread-local: not propagated to other threads (`@Async`, executors) unless you copy it
- Must be cleaned up (pooled threads)
- Untrusted headers need validation

#### What happens without it / when misused

Without correlation ids debugging means guessing which lines belong together. Forgetting `MDC.remove` leaks one user's id into the next request on the same thread. Accepting arbitrary header values lets attackers forge log lines (log injection).

#### Syntax and rules

```java
MDC.put("requestId", id);
try { chain.doFilter(req, res); } finally { MDC.remove("requestId"); }
```
```properties
logging.pattern.level=%5p [%X{requestId}]
```
For executors: wrap tasks (`TaskDecorator`) to copy `MDC.getCopyOfContextMap()`.

#### Examples

**Example 1 — TaskDecorator**

```java
return task -> { var ctx = MDC.getCopyOfContextMap(); return () -> { MDC.setContextMap(ctx); try { task.run(); } finally { MDC.clear(); } }; };
```

**Example 2 — Response header**

```java
response.setHeader("X-Request-Id", id);
```

**Example 3 — Trace ids**

```properties
management.tracing.sampling.probability=1.0
```

#### Quick checks

1. Why clear the MDC?
2. Is MDC inherited by new threads?
3. What is log injection?

### Actuator health and Micrometer metrics

#### What it is

**Actuator** exposes `/actuator/health` (aggregated `HealthIndicator`s such as db, diskSpace, ping or your own) and `/actuator/metrics`. Health statuses: UP, DOWN, OUT_OF_SERVICE, UNKNOWN; the worst wins and DOWN/OUT_OF_SERVICE return HTTP 503. Readiness/liveness groups serve Kubernetes probes. **Micrometer** is the metrics facade: `Counter`, `Gauge`, `Timer`, `DistributionSummary`, tags; registries export to Prometheus, Datadog, etc. (`/actuator/prometheus` with the Prometheus registry).

#### Why it exists / why it matters

Operations teams alert on health and metrics, not on log lines. Business metrics (orders placed, queue depth) reveal problems earlier than errors do.

#### Pros and cons

**Pros**

- Standard endpoints and probes
- Vendor-neutral metrics API
- Automatic JVM/HTTP/datasource metrics
- Easy to extend

**Cons / trade-offs**

- Exposure must be restricted and secured
- Unbounded tag cardinality can blow up the metrics backend
- Slow health checks can take down the app under frequent probing

#### What happens without it / when misused

Putting `userId` in a tag creates millions of time series. A health indicator that calls a slow third party makes probes time out and triggers restarts. Exposing all endpoints publicly leaks configuration.

#### Syntax and rules

```java
registry.counter("orders.placed", "channel", "web").increment();
Timer.builder("orders.processing").register(registry).record(() -> work());
Gauge.builder("orders.queue.size", queue, AtomicInteger::get).register(registry);
```
```properties
management.endpoints.web.exposure.include=health,info,metrics,prometheus
management.endpoint.health.show-details=when-authorized
management.endpoint.health.probes.enabled=true
```

#### Examples

**Example 1 — Health indicator**

```java
@Component class QueueHealthIndicator implements HealthIndicator { public Health health() { return Health.up().withDetail("depth", 3).build(); } }
```

**Example 2 — Read a metric**

```text
GET /actuator/metrics/http.server.requests?tag=status:200
```

**Example 3 — @Timed on a controller**

```java
@Timed("api.orders") @GetMapping("/orders") ...
```

#### Quick checks

1. Which health statuses map to HTTP 503?
2. Why avoid unbounded tags?
3. Liveness vs readiness?

## Interview corner

**Q1. Why SLF4J?**

A stable facade so libraries and apps are independent of the logging backend.

**Q2. What is MDC?**

Thread-local context map included in log lines.

**Q3. How do health groups help Kubernetes?**

Liveness and readiness probes can reflect different sets of indicators.

**Q4. Counter vs Gauge vs Timer?**

Counter only goes up, Gauge samples a current value, Timer measures durations and counts.

**Q5. What is metric cardinality?**

The number of distinct tag-value combinations.

## Common mistakes & debugging

- String concatenation in log calls.
- Logging secrets or personal data.
- Forgetting to clear MDC.
- High-cardinality tags.
- Exposing every Actuator endpoint.

## Further reading

- Spring Boot Reference: Logging, Actuator, Metrics
- Micrometer documentation
- SLF4J FAQ

## Glossary

| Term | Meaning |
|------|---------|
| SLF4J | Logging facade |
| Logback | Default logging implementation |
| MDC | Mapped diagnostic context |
| HealthIndicator | Contributor to /actuator/health |
| Micrometer | Metrics facade |

## Answers

### Logging with SLF4J and Logback

1. They avoid string building when the level is disabled and keep the template constant.
2. As the last argument so the stack trace is logged.
3. SLF4J is the API; Logback is the implementation.

### MDC and request correlation

1. Threads are reused; stale values would leak into other requests.
2. Not automatically; copy it explicitly.
3. Forging log lines via newline characters in user-controlled data.

### Actuator health and Micrometer metrics

1. DOWN and OUT_OF_SERVICE.
2. Each distinct tag combination is a separate time series.
3. Liveness: restart me if broken; readiness: send me traffic only when ready.
