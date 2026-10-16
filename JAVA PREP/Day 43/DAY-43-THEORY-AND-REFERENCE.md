# Day 43 — Microservices, RestClient, and Resilience4j

**Phase:** Microservices  
**Primary theme:** Service boundaries, synchronous communication with RestClient, and surviving downstream failures with retry, circuit breaker and fallback  
**Estimated study time:** 2-3 h theory + 4-6 h tasks  
**Related tasks:** `task-01-restclient-inventory-client`, `task-02-retry-with-backoff`, `task-03-circuit-breaker-facade`, `task-04-order-service-degradation-challenge`  
**Instruction alignment:** Maps to Day 43 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Service boundaries, synchronous communication with RestClient, and surviving downstream failures with retry, circuit breaker and fallback. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. Microservices architecture and service boundaries
2. Synchronous communication with RestClient
3. Failure modes, retry, and backoff
4. Circuit breaker, bulkhead, timeout, and fallback
5. Observability basics for microservices
6. Interview corner, common mistakes, glossary

## Subtopics

### Microservices architecture and service boundaries

#### What it is

A microservice architecture splits a system into small, independently deployable services, each owning its data and one business capability (orders, inventory, payments). Services talk over the network (HTTP/gRPC) or via messages (Kafka).

#### Why it exists / why it matters

A monolith scales and deploys as one unit. Splitting by business capability lets teams ship independently, scale hot spots separately and isolate failures — at the price of distributed-system complexity.

#### Pros and cons

**Pros**

- Independent deployment and scaling
- Fault isolation per service
- Technology freedom per team
- Clear ownership of data

**Cons / trade-offs**

- Network calls fail, are slow and are not transactional
- Operational overhead (deploy, monitor, trace)
- Data consistency becomes eventual
- Harder local debugging

#### What happens without it / when misused

A wrong split (a distributed monolith) gives you the costs of microservices without the benefits: services that must deploy together, shared databases, chatty synchronous chains.

#### Syntax and rules

Rules of thumb: one service = one bounded context; one database per service (no shared tables); communicate through APIs/events, never through another service's tables; prefer coarse-grained calls.

#### Examples

**Example 1 — Order service depends on inventory**

```text
client -> order-service --HTTP--> inventory-service
                     \--event--> notification-service
```

**Example 2 — Database per service**

```text
order-service      -> orders_db
inventory-service  -> inventory_db   (no cross-DB joins!)
```

#### Quick checks

1. What is a bounded context?
2. Why is a shared database an anti-pattern?

### Synchronous communication with RestClient

#### What it is

`RestClient` (Spring 6.1+) is the modern synchronous HTTP client with a fluent API: `get()/post()`, `uri(template, vars)`, `retrieve()`, `body(Class)`, `onStatus(...)`. It replaces most uses of `RestTemplate` and shares message converters with Spring MVC.

#### Why it exists / why it matters

Service-to-service calls need typed responses, URL encoding, status handling and timeouts in one readable place. A client class that hides these details keeps business code clean and testable.

#### Pros and cons

**Pros**

- Fluent, readable API
- Pluggable request factory (timeouts)
- Easy to test with `MockRestServiceServer`
- Base URL and default headers per client

**Cons / trade-offs**

- Blocking (use WebClient/virtual threads for high concurrency)
- Status-to-exception mapping must be explicit
- No built-in retry or circuit breaker

#### What happens without it / when misused

Calling `RestClient` without timeouts means a slow downstream can exhaust all your threads (default JDK client has no read timeout). String-concatenated URLs lead to encoding bugs and injection.

#### Syntax and rules

```java
RestClient rc = RestClient.builder().baseUrl("http://inventory").build();
StockResponse r = rc.get().uri("/inventory/{sku}", sku).retrieve().body(StockResponse.class);
```
Timeouts: configure the `ClientHttpRequestFactory` (connect + read timeout). Tests: `MockRestServiceServer.bindTo(builder).build()`.

#### Examples

**Example 1 — Handling statuses**

```java
rc.get().uri("/x").retrieve()
  .onStatus(HttpStatusCode::is5xxServerError, (req, res) -> { throw new UnavailableException(); })
  .body(String.class);
```

**Example 2 — Timeouts**

```java
var factory = new JdkClientHttpRequestFactory();
factory.setReadTimeout(Duration.ofSeconds(2));
RestClient rc = RestClient.builder().requestFactory(factory).build();
```

#### Quick checks

1. Why configure a read timeout?
2. How do you unit-test a RestClient without a server?

### Failure modes, retry, and backoff

#### What it is

Distributed calls fail in many ways: refused connections, timeouts, 5xx, partial responses. **Retry** repeats a failed call a bounded number of times, usually with a delay (fixed or exponential backoff with jitter).

#### Why it exists / why it matters

Most failures are transient (network blip, restart). A bounded retry hides them from the user. Unbounded or immediate retries, however, amplify outages (retry storms).

#### Pros and cons

**Pros**

- Masks transient faults
- Simple to reason about
- Configurable by exception type

**Cons / trade-offs**

- Multiplies load on a struggling service
- Only safe for idempotent operations
- Adds latency

#### What happens without it / when misused

Retrying a non-idempotent POST (payment) can charge twice. Retrying every exception (including 400 Bad Request) wastes calls that can never succeed.

#### Syntax and rules

```java
RetryConfig cfg = RetryConfig.custom().maxAttempts(3).waitDuration(Duration.ofMillis(200))
    .retryExceptions(IOException.class).build();
Retry retry = Retry.of("inventory", cfg);
Supplier<String> s = Retry.decorateSupplier(retry, () -> client.call());
```
Rules: retry only transient errors, only idempotent calls, cap attempts, add backoff + jitter.

#### Examples

**Example 1 — Exponential backoff**

```java
RetryConfig.custom().maxAttempts(4)
  .intervalFunction(IntervalFunction.ofExponentialRandomBackoff(100, 2.0, 0.5)).build();
```

**Example 2 — Idempotency key**

```text
POST /payments  Idempotency-Key: 7f3a...   (safe to retry)
```

#### Quick checks

1. Which HTTP errors are worth retrying?
2. Why add jitter?

### Circuit breaker, bulkhead, timeout, and fallback

#### What it is

A **circuit breaker** watches recent calls. When the failure rate crosses a threshold it OPENs and fails fast; after a wait it goes HALF_OPEN, lets a few probe calls through and CLOSEs again if they succeed. **Bulkhead** limits concurrent calls; **time limiter** bounds duration; a **fallback** returns a degraded answer.

#### Why it exists / why it matters

Without protection one slow dependency makes callers pile up threads, which cascades into a full outage. Failing fast protects both sides and gives the downstream room to recover.

#### Pros and cons

**Pros**

- Stops cascading failures
- Gives the downstream time to recover
- Fast, predictable errors
- Degraded but available behavior

**Cons / trade-offs**

- Thresholds need tuning
- Fallback data may be stale/wrong
- More states to test and monitor

#### What happens without it / when misused

No breaker: every request waits for the full timeout against a dead service, thread pool exhausts, unrelated endpoints die too. Over-aggressive breaker: opens on harmless blips.

#### Syntax and rules

States: CLOSED -> (failure rate >= threshold) -> OPEN -> (wait elapsed) -> HALF_OPEN -> (probe ok) CLOSED / (probe fails) OPEN.
```java
CircuitBreakerConfig cfg = CircuitBreakerConfig.custom().slidingWindowSize(10)
   .failureRateThreshold(50).waitDurationInOpenState(Duration.ofSeconds(10)).build();
```
`CallNotPermittedException` is thrown while OPEN.

#### Examples

**Example 1 — Decorate**

```java
Supplier<String> guarded = CircuitBreaker.decorateSupplier(cb, () -> client.call());
try { return guarded.get(); } catch (Exception e) { return "FALLBACK"; }
```

**Example 2 — Order of decorators**

```text
Retry( CircuitBreaker( TimeLimiter( call ) ) )  - typical nesting
```

#### Quick checks

1. What happens in HALF_OPEN?
2. Retry or breaker first?

### Observability basics for microservices

#### What it is

Three pillars: **logs** (with correlation IDs), **metrics** (rates, errors, durations — Micrometer/Actuator) and **traces** (a request across services). Resilience4j publishes breaker/retry metrics automatically with Micrometer.

#### Why it exists / why it matters

In a distributed system you cannot attach a debugger to a request. Correlation IDs and metrics are how you answer "which service failed and why?".

#### Pros and cons

**Pros**

- Faster incident diagnosis
- Data-driven tuning of thresholds

**Cons / trade-offs**

- Extra infrastructure and storage
- Cardinality and cost management

#### What happens without it / when misused

Without correlation IDs, logs of five services cannot be joined; without metrics you only learn about outages from users.

#### Syntax and rules

Propagate `X-Request-Id` on every outbound call; log it with MDC; expose `/actuator/health` and `/actuator/metrics`.

#### Examples

**Example 1 — Propagate a correlation id**

```java
restClient.get().uri("/x").header("X-Request-Id", MDC.get("requestId"))...
```

#### Quick checks

1. What is a correlation id?

## Interview corner

**Q1. When would you NOT use microservices?**

Small teams/simple domains: a modular monolith is cheaper and easier.

**Q2. Retry vs circuit breaker?**

Retry handles transient faults; the breaker stops calling a service that is persistently failing.

**Q3. What is idempotency and why does retry need it?**

Repeating the call has the same effect as one call; otherwise retries duplicate side effects.

**Q4. How do you test downstream failures without a network?**

Stubs, `MockRestServiceServer`, WireMock, or in-process fakes that fail on demand.

**Q5. What is a fallback?**

A degraded but safe response used when the real call fails.

## Common mistakes & debugging

- Retrying non-idempotent operations.
- No timeouts on HTTP clients.
- Retrying 4xx errors.
- Sharing a database between services.
- Breaker thresholds that open on a single failure.

## Further reading

- Spring Framework Reference: RestClient
- Resilience4j documentation: CircuitBreaker, Retry
- Sam Newman, Building Microservices (chapters on resilience)

## Glossary

| Term | Meaning |
|------|---------|
| Bounded context | Boundary of a consistent domain model |
| Idempotent | Safe to repeat |
| Backoff | Increasing delay between retries |
| Circuit breaker | Fail-fast guard with CLOSED/OPEN/HALF_OPEN states |
| Fallback | Degraded answer on failure |
| Bulkhead | Concurrency limit per dependency |

## Answers

### Microservices architecture and service boundaries

1. A boundary inside which a domain model and its vocabulary are consistent; a good candidate for a service.
2. It couples services through the schema and prevents independent change and deployment.

### Synchronous communication with RestClient

1. So a hung downstream cannot block your threads forever.
2. Bind a `MockRestServiceServer` to the builder.

### Failure modes, retry, and backoff

1. Timeouts, 502/503/504 and connection errors — not 4xx.
2. To desynchronize clients so they do not retry in lockstep.

### Circuit breaker, bulkhead, timeout, and fallback

1. A limited number of probe calls decide whether to close or re-open.
2. Usually retry wraps the breaker so each attempt is counted, and an OPEN breaker short-circuits retries.

### Observability basics for microservices

1. An identifier passed along every hop of a request so logs can be joined.
