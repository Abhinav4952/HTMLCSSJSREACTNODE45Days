from common import *

APPCLS = APP
RETRY_DEP = dep("io.github.resilience4j", "resilience4j-retry", "2.2.0")
CB_DEP = dep("io.github.resilience4j", "resilience4j-circuitbreaker", "2.2.0")

# ------------------------------------------------------------------ task 1: RestClient
INV_CLIENT = r'''package %PKG%;

import java.util.Optional;
import org.springframework.web.client.RestClient;

/** Calls the Inventory service. The RestClient is injected (base URL already configured). */
public class InventoryClient {

    private final RestClient restClient;

    public InventoryClient(RestClient restClient) {
        this.restClient = restClient;
    }

    /**
     * GET /inventory/{sku}  ->  {"sku":"ABC","available":7}
     * 404 -> Optional.empty(); 5xx or I/O failure -> InventoryUnavailableException.
     */
    public Optional<Integer> availableStock(String sku) {
        // TODO(%TAG%): use restClient.get().uri("/inventory/{sku}", sku).retrieve()...body(StockResponse.class)
        // TODO(%TAG%): map 404, 5xx and ResourceAccessException as described above
        throw new UnsupportedOperationException("TODO(%TAG%): implement availableStock");
    }
}
'''
INV_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withStatus;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withSuccess;

import java.io.IOException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.web.client.RestClient;

class InventoryClientTest {

    private MockRestServiceServer server;
    private InventoryClient client;

    @BeforeEach
    void setUp() {
        RestClient.Builder builder = RestClient.builder().baseUrl("http://inventory");
        server = MockRestServiceServer.bindTo(builder).build();
        client = new InventoryClient(builder.build());
    }

    @Test
    void returnsAvailableStockOnSuccess() {
        server.expect(requestTo("http://inventory/inventory/ABC-1")).andExpect(method(HttpMethod.GET))
                .andRespond(withSuccess("{\"sku\":\"ABC-1\",\"available\":7}", MediaType.APPLICATION_JSON));
        assertThat(client.availableStock("ABC-1")).contains(7);
        server.verify();
    }

    @Test
    void unknownSkuIsEmpty() {
        server.expect(requestTo("http://inventory/inventory/NOPE")).andRespond(withStatus(HttpStatus.NOT_FOUND));
        assertThat(client.availableStock("NOPE")).isEmpty();
    }

    @Test
    void serverErrorBecomesInventoryUnavailable() {
        server.expect(requestTo("http://inventory/inventory/ABC-1")).andRespond(withStatus(HttpStatus.SERVICE_UNAVAILABLE));
        assertThatThrownBy(() -> client.availableStock("ABC-1")).isInstanceOf(InventoryUnavailableException.class);
    }

    @Test
    void ioFailureBecomesInventoryUnavailable() {
        server.expect(requestTo("http://inventory/inventory/ABC-1")).andRespond(request -> {
            throw new IOException("simulated timeout");
        });
        assertThatThrownBy(() -> client.availableStock("ABC-1")).isInstanceOf(InventoryUnavailableException.class);
    }

    @Test
    void skuIsUriEncoded() {
        server.expect(requestTo("http://inventory/inventory/A%20B"))
                .andRespond(withSuccess("{\"sku\":\"A B\",\"available\":1}", MediaType.APPLICATION_JSON));
        assertThat(client.availableStock("A B")).contains(1);
    }
}
'''
INV_EXC = r'''package %PKG%;

/** PROVIDED. Signals that the downstream inventory service could not give an answer. */
public class InventoryUnavailableException extends RuntimeException {

    public InventoryUnavailableException(String message, Throwable cause) {
        super(message, cause);
    }
}
'''
INV_REC = "package %PKG%;\n\n/** PROVIDED. JSON body returned by the Inventory service. */\npublic record StockResponse(String sku, int available) {\n}\n"

t1 = task("restclient-inventory-client", "RestClient Inventory Client", "Warm-up", "Spring Boot",
    "Implement a service-to-service client with Spring's `RestClient`. The downstream service is simulated in-process with `MockRestServiceServer`, so no network or Docker is needed.",
    "boot", {"main/Application.java": APPCLS, "main/InventoryClient.java": INV_CLIENT, "main/StockResponse.java": INV_REC,
             "main/InventoryUnavailableException.java": INV_EXC, "test/InventoryClientTest.java": INV_TEST},
    ["Implement `availableStock(sku)` with `restClient.get().uri(\"/inventory/{sku}\", sku)`.",
     "Return the `available` count wrapped in `Optional` for 200 responses.",
     "Return `Optional.empty()` for HTTP 404.",
     "Throw `InventoryUnavailableException` for 5xx responses and for I/O failures (`ResourceAccessException`).",
     "Use a URI template variable so the SKU is encoded for you (never concatenate strings)."],
    ["SKU containing a space must be percent-encoded.", "A 4xx other than 404 may propagate (document your choice).", "Keep the original exception as `cause`."],
    ["`HttpClientErrorException.NotFound` and `HttpServerErrorException` are thrown by default for 4xx/5xx.", "`ResourceAccessException` wraps `IOException`.",
     "`.onStatus(...)` lets you convert statuses without try/catch."],
    starters=["spring-boot-starter-web"])

# ------------------------------------------------------------------ task 2: Retry
RC = r'''package %PKG%;

import java.time.Duration;
import java.util.function.Supplier;

public class ResilientCaller {

    /**
     * Calls {@code call}; if it throws {@code retryOn} (or a subclass) retries until {@code maxAttempts} total attempts
     * were made, waiting {@code wait} between attempts. The LAST exception is rethrown when attempts run out.
     * Other exception types are NOT retried. maxAttempts &lt; 1 -> IllegalArgumentException.
     */
    public <T> T callWithRetry(Supplier<T> call, int maxAttempts, Duration wait, Class<? extends Throwable> retryOn) {
        // TODO(%TAG%): build a RetryConfig (maxAttempts, waitDuration, retryExceptions) and decorate the supplier
        throw new UnsupportedOperationException("TODO(%TAG%): implement callWithRetry");
    }
}
'''
FLAKY = r'''package %PKG%;

import java.util.concurrent.atomic.AtomicInteger;

/** PROVIDED. Simulated downstream: fails the first {@code failures} calls, then answers "ok". */
public class FlakyDownstream {

    private final int failures;
    private final AtomicInteger calls = new AtomicInteger();

    public FlakyDownstream(int failures) {
        this.failures = failures;
    }

    public String call() {
        if (calls.incrementAndGet() <= failures) {
            throw new DownstreamException("downstream failure #" + calls.get());
        }
        return "ok";
    }

    public int calls() {
        return calls.get();
    }
}
'''
DEX = "package %PKG%;\n\n/** PROVIDED. Retryable failure of a downstream dependency. */\npublic class DownstreamException extends RuntimeException {\n\n    public DownstreamException(String message) {\n        super(message);\n    }\n}\n"
RC_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Duration;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class ResilientCallerTest {

    private final ResilientCaller caller = new ResilientCaller();
    private static final Duration WAIT = Duration.ofMillis(10);

    @Test
    void succeedsAfterTransientFailures() {
        FlakyDownstream downstream = new FlakyDownstream(2);
        assertThat(caller.callWithRetry(downstream::call, 3, WAIT, DownstreamException.class)).isEqualTo("ok");
        assertThat(downstream.calls()).isEqualTo(3);
    }

    @Test
    void givesUpAfterMaxAttemptsAndRethrowsLastFailure() {
        FlakyDownstream downstream = new FlakyDownstream(5);
        assertThatThrownBy(() -> caller.callWithRetry(downstream::call, 2, WAIT, DownstreamException.class))
                .isInstanceOf(DownstreamException.class).hasMessage("downstream failure #2");
        assertThat(downstream.calls()).isEqualTo(2);
    }

    @Test
    void nonRetryableExceptionsAreNotRetried() {
        AtomicInteger calls = new AtomicInteger();
        assertThatThrownBy(() -> caller.callWithRetry(() -> {
            calls.incrementAndGet();
            throw new IllegalArgumentException("bad input");
        }, 5, WAIT, DownstreamException.class)).isInstanceOf(IllegalArgumentException.class);
        assertThat(calls.get()).isEqualTo(1);
    }

    @Test
    void firstSuccessIsNotRepeated() {
        FlakyDownstream downstream = new FlakyDownstream(0);
        caller.callWithRetry(downstream::call, 4, WAIT, DownstreamException.class);
        assertThat(downstream.calls()).isEqualTo(1);
    }

    @Test
    void waitsBetweenAttempts() {
        FlakyDownstream downstream = new FlakyDownstream(2);
        long start = System.nanoTime();
        caller.callWithRetry(downstream::call, 3, Duration.ofMillis(50), DownstreamException.class);
        long elapsedMs = (System.nanoTime() - start) / 1_000_000;
        assertThat(elapsedMs).isGreaterThanOrEqualTo(90);
    }

    @Test
    void rejectsInvalidAttemptCount() {
        assertThatThrownBy(() -> caller.callWithRetry(() -> "x", 0, WAIT, DownstreamException.class))
                .isInstanceOf(IllegalArgumentException.class);
    }
}
'''
t2 = task("retry-with-backoff", "Retry with Resilience4j", "Core", "Java + Resilience4j",
    "Wrap a flaky in-process downstream with Resilience4j `Retry`: bounded attempts, wait between attempts, selective exception types.",
    "plain", {"main/ResilientCaller.java": RC, "main/FlakyDownstream.java": FLAKY, "main/DownstreamException.java": DEX, "test/ResilientCallerTest.java": RC_TEST},
    ["Build a `RetryConfig` with `maxAttempts`, `waitDuration` and `retryExceptions(retryOn)`.", "Decorate the supplier with `Retry.decorateSupplier` and execute it.",
     "Rethrow the last exception when attempts are exhausted.", "Do not retry exceptions outside `retryOn`.", "Reject `maxAttempts < 1` with `IllegalArgumentException`."],
    ["`maxAttempts` counts the first call too.", "Resilience4j requires a wait of at least a few milliseconds.", "Retrying non-idempotent calls is dangerous (discuss in theory)."],
    ["`Retry.of(\"name\", config)` creates the retry instance.", "The decorated supplier throws the original exception after the last attempt."],
    deps=[RETRY_DEP])

# ------------------------------------------------------------------ task 3: CircuitBreaker
BF = r'''package %PKG%;

import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import java.time.Duration;
import java.util.function.Supplier;

/** Protects a downstream call with a circuit breaker and answers "FALLBACK" when the call fails or is not permitted. */
public class BreakerFacade {

    private CircuitBreaker breaker;
    private Supplier<String> downstream;

    /**
     * Configuration required by the tests: COUNT_BASED window of 4 calls, minimum 4 calls, failure rate threshold 50 %,
     * open-state wait = {@code openWait}, exactly 1 permitted call in half-open state.
     */
    public BreakerFacade(Supplier<String> downstream, Duration openWait) {
        // TODO(%TAG%): create a CircuitBreakerConfig with the settings above and the CircuitBreaker
        throw new UnsupportedOperationException("TODO(%TAG%): implement BreakerFacade constructor");
    }

    /** Result of the downstream call, or "FALLBACK" on failure / open circuit (downstream is NOT invoked when open). */
    public String call() {
        // TODO(%TAG%): decorate the supplier, catch failures (including CallNotPermittedException) and return the fallback
        throw new UnsupportedOperationException("TODO(%TAG%): implement call");
    }

    public CircuitBreaker.State state() {
        // TODO(%TAG%): expose the breaker state
        throw new UnsupportedOperationException("TODO(%TAG%): implement state");
    }
}
'''
BF_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import java.time.Duration;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class BreakerFacadeTest {

    private final AtomicInteger calls = new AtomicInteger();
    private final AtomicBoolean healthy = new AtomicBoolean(false);

    private String downstream() {
        calls.incrementAndGet();
        if (!healthy.get()) {
            throw new IllegalStateException("down");
        }
        return "OK";
    }

    @Test
    void opensAfterFourFailuresAndStopsCallingDownstream() {
        BreakerFacade facade = new BreakerFacade(this::downstream, Duration.ofMillis(100));
        for (int i = 0; i < 4; i++) {
            assertThat(facade.call()).isEqualTo("FALLBACK");
        }
        assertThat(facade.state()).isEqualTo(CircuitBreaker.State.OPEN);
        int before = calls.get();
        assertThat(facade.call()).isEqualTo("FALLBACK");
        assertThat(calls.get()).isEqualTo(before);
    }

    @Test
    void recoversThroughHalfOpenWhenDownstreamIsHealthyAgain() throws Exception {
        BreakerFacade facade = new BreakerFacade(this::downstream, Duration.ofMillis(100));
        for (int i = 0; i < 4; i++) {
            facade.call();
        }
        healthy.set(true);
        Thread.sleep(250);
        assertThat(facade.call()).isEqualTo("OK");
        assertThat(facade.state()).isEqualTo(CircuitBreaker.State.CLOSED);
    }

    @Test
    void staysClosedBelowTheFailureThreshold() {
        BreakerFacade facade = new BreakerFacade(this::downstream, Duration.ofMillis(100));
        healthy.set(true);
        facade.call();
        facade.call();
        facade.call();
        healthy.set(false);
        assertThat(facade.call()).isEqualTo("FALLBACK");
        assertThat(facade.state()).isEqualTo(CircuitBreaker.State.CLOSED);
    }

    @Test
    void healthyCallsReturnTheRealValue() {
        healthy.set(true);
        BreakerFacade facade = new BreakerFacade(this::downstream, Duration.ofMillis(100));
        assertThat(facade.call()).isEqualTo("OK");
    }
}
'''
t3 = task("circuit-breaker-facade", "Circuit Breaker Facade", "Core", "Java + Resilience4j",
    "Protect a failing downstream with a Resilience4j `CircuitBreaker`, fall back when it fails, and watch the CLOSED -> OPEN -> HALF_OPEN -> CLOSED life cycle.",
    "plain", {"main/BreakerFacade.java": BF, "test/BreakerFacadeTest.java": BF_TEST},
    ["Configure the breaker: COUNT_BASED window 4, minimum 4 calls, 50 % failure threshold, wait in OPEN = `openWait`, 1 permitted call in HALF_OPEN.",
     "`call()` returns the downstream value or `\"FALLBACK\"` for any failure and for `CallNotPermittedException`.", "While OPEN the downstream supplier must not be invoked.",
     "`state()` exposes the current `CircuitBreaker.State`."],
    ["Transition OPEN -> HALF_OPEN happens on the first call after the wait elapsed.", "A single failure in a window of 4 stays below 50 %."],
    ["`CircuitBreakerConfig.custom()` is the builder.", "`CircuitBreaker.decorateSupplier(cb, supplier)` wraps the call."],
    deps=[CB_DEP])

# ------------------------------------------------------------------ task 4: OrderService
OS = r'''package %PKG%;

public class OrderService {

    private final InventoryPort inventory;
    private final int maxAttempts;

    public OrderService(InventoryPort inventory, int maxAttempts) {
        this.inventory = inventory;
        this.maxAttempts = maxAttempts;
    }

    /**
     * Rules:
     * <ol>
     *   <li>qty &lt;= 0 -> IllegalArgumentException</li>
     *   <li>Ask inventory for the stock; retry ONLY on {@link InventoryUnavailableException}, up to maxAttempts calls in total</li>
     *   <li>stock &gt;= qty -> CONFIRMED; stock &lt; qty -> REJECTED_OUT_OF_STOCK (inventory called once)</li>
     *   <li>still unavailable after all attempts -> PENDING_INVENTORY_UNAVAILABLE (graceful degradation, no exception)</li>
     *   <li>any other exception propagates immediately</li>
     * </ol>
     */
    public OrderResult placeOrder(String sku, int qty) {
        // TODO(%TAG%): implement the rules above (hand-written loop or Resilience4j Retry)
        throw new UnsupportedOperationException("TODO(%TAG%): implement placeOrder");
    }
}
'''
OS_FILES = {
    "main/InventoryPort.java": "package %PKG%;\n\n/** PROVIDED. Port to the inventory service (may throw InventoryUnavailableException). */\npublic interface InventoryPort {\n\n    int available(String sku);\n}\n",
    "main/InventoryUnavailableException.java": "package %PKG%;\n\n/** PROVIDED. Retryable failure of the inventory service. */\npublic class InventoryUnavailableException extends RuntimeException {\n\n    public InventoryUnavailableException(String message) {\n        super(message);\n    }\n}\n",
    "main/OrderResult.java": "package %PKG%;\n\n/** PROVIDED. */\npublic record OrderResult(Status status, String sku, int quantity) {\n\n    public enum Status { CONFIRMED, REJECTED_OUT_OF_STOCK, PENDING_INVENTORY_UNAVAILABLE }\n}\n",
}
OS_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class OrderServiceTest {

    private final AtomicInteger calls = new AtomicInteger();

    private InventoryPort failingFirst(int failures, int stock) {
        return sku -> {
            if (calls.incrementAndGet() <= failures) {
                throw new InventoryUnavailableException("down");
            }
            return stock;
        };
    }

    @Test
    void confirmsWhenStockIsSufficient() {
        OrderService service = new OrderService(failingFirst(0, 10), 3);
        OrderResult r = service.placeOrder("A", 4);
        assertThat(r.status()).isEqualTo(OrderResult.Status.CONFIRMED);
        assertThat(r.sku()).isEqualTo("A");
        assertThat(r.quantity()).isEqualTo(4);
    }

    @Test
    void rejectsWithoutRetryWhenStockIsTooLow() {
        OrderService service = new OrderService(failingFirst(0, 1), 3);
        assertThat(service.placeOrder("A", 4).status()).isEqualTo(OrderResult.Status.REJECTED_OUT_OF_STOCK);
        assertThat(calls.get()).isEqualTo(1);
    }

    @Test
    void retriesTransientFailures() {
        OrderService service = new OrderService(failingFirst(2, 10), 3);
        assertThat(service.placeOrder("A", 1).status()).isEqualTo(OrderResult.Status.CONFIRMED);
        assertThat(calls.get()).isEqualTo(3);
    }

    @Test
    void degradesToPendingWhenInventoryStaysDown() {
        OrderService service = new OrderService(failingFirst(99, 10), 3);
        assertThat(service.placeOrder("A", 1).status()).isEqualTo(OrderResult.Status.PENDING_INVENTORY_UNAVAILABLE);
        assertThat(calls.get()).isEqualTo(3);
    }

    @Test
    void otherExceptionsPropagateImmediately() {
        OrderService service = new OrderService(sku -> {
            calls.incrementAndGet();
            throw new IllegalStateException("bug");
        }, 3);
        assertThatThrownBy(() -> service.placeOrder("A", 1)).isInstanceOf(IllegalStateException.class);
        assertThat(calls.get()).isEqualTo(1);
    }

    @Test
    void rejectsNonPositiveQuantity() {
        OrderService service = new OrderService(failingFirst(0, 10), 3);
        assertThatThrownBy(() -> service.placeOrder("A", 0)).isInstanceOf(IllegalArgumentException.class);
    }
}
'''
t4 = task("order-service-degradation-challenge", "Order Service with Graceful Degradation (Challenge)", "Challenge", "Java",
    "Combine retry and fallback in an order service: transient inventory failures are retried, permanent ones degrade to a PENDING order instead of an error.",
    "plain", {**OS_FILES, "main/OrderService.java": OS, "test/OrderServiceTest.java": OS_TEST},
    ["Validate quantity.", "Retry only `InventoryUnavailableException`, at most `maxAttempts` total calls.", "Map stock levels to `CONFIRMED` / `REJECTED_OUT_OF_STOCK`.",
     "Return `PENDING_INVENTORY_UNAVAILABLE` when all attempts failed.", "Let unexpected exceptions bubble up unchanged."],
    ["`maxAttempts` of 1 means no retry.", "Out-of-stock is a business answer, not a failure: never retried."],
    ["A plain `for` loop is enough; Resilience4j is optional.", "Think: which outcomes are failures and which are valid business results?"],
    deps=[RETRY_DEP])

TOPICS = [
    T("Microservices architecture and service boundaries",
      "A microservice architecture splits a system into small, independently deployable services, each owning its data and one business capability (orders, inventory, payments). Services talk over the network (HTTP/gRPC) or via messages (Kafka).",
      "A monolith scales and deploys as one unit. Splitting by business capability lets teams ship independently, scale hot spots separately and isolate failures — at the price of distributed-system complexity.",
      ["Independent deployment and scaling", "Fault isolation per service", "Technology freedom per team", "Clear ownership of data"],
      ["Network calls fail, are slow and are not transactional", "Operational overhead (deploy, monitor, trace)", "Data consistency becomes eventual", "Harder local debugging"],
      "A wrong split (a distributed monolith) gives you the costs of microservices without the benefits: services that must deploy together, shared databases, chatty synchronous chains.",
      "Rules of thumb: one service = one bounded context; one database per service (no shared tables); communicate through APIs/events, never through another service's tables; prefer coarse-grained calls.",
      [("Order service depends on inventory", "text", "client -> order-service --HTTP--> inventory-service\n                     \\--event--> notification-service"),
       ("Database per service", "text", "order-service      -> orders_db\ninventory-service  -> inventory_db   (no cross-DB joins!)")],
      [("What is a bounded context?", "A boundary inside which a domain model and its vocabulary are consistent; a good candidate for a service."),
       ("Why is a shared database an anti-pattern?", "It couples services through the schema and prevents independent change and deployment.")]),
    T("Synchronous communication with RestClient",
      "`RestClient` (Spring 6.1+) is the modern synchronous HTTP client with a fluent API: `get()/post()`, `uri(template, vars)`, `retrieve()`, `body(Class)`, `onStatus(...)`. It replaces most uses of `RestTemplate` and shares message converters with Spring MVC.",
      "Service-to-service calls need typed responses, URL encoding, status handling and timeouts in one readable place. A client class that hides these details keeps business code clean and testable.",
      ["Fluent, readable API", "Pluggable request factory (timeouts)", "Easy to test with `MockRestServiceServer`", "Base URL and default headers per client"],
      ["Blocking (use WebClient/virtual threads for high concurrency)", "Status-to-exception mapping must be explicit", "No built-in retry or circuit breaker"],
      "Calling `RestClient` without timeouts means a slow downstream can exhaust all your threads (default JDK client has no read timeout). String-concatenated URLs lead to encoding bugs and injection.",
      "```java\nRestClient rc = RestClient.builder().baseUrl(\"http://inventory\").build();\nStockResponse r = rc.get().uri(\"/inventory/{sku}\", sku).retrieve().body(StockResponse.class);\n```\nTimeouts: configure the `ClientHttpRequestFactory` (connect + read timeout). Tests: `MockRestServiceServer.bindTo(builder).build()`.",
      [("Handling statuses", "java", "rc.get().uri(\"/x\").retrieve()\n  .onStatus(HttpStatusCode::is5xxServerError, (req, res) -> { throw new UnavailableException(); })\n  .body(String.class);"),
       ("Timeouts", "java", "var factory = new JdkClientHttpRequestFactory();\nfactory.setReadTimeout(Duration.ofSeconds(2));\nRestClient rc = RestClient.builder().requestFactory(factory).build();")],
      [("Why configure a read timeout?", "So a hung downstream cannot block your threads forever."),
       ("How do you unit-test a RestClient without a server?", "Bind a `MockRestServiceServer` to the builder.")]),
    T("Failure modes, retry, and backoff",
      "Distributed calls fail in many ways: refused connections, timeouts, 5xx, partial responses. **Retry** repeats a failed call a bounded number of times, usually with a delay (fixed or exponential backoff with jitter).",
      "Most failures are transient (network blip, restart). A bounded retry hides them from the user. Unbounded or immediate retries, however, amplify outages (retry storms).",
      ["Masks transient faults", "Simple to reason about", "Configurable by exception type"],
      ["Multiplies load on a struggling service", "Only safe for idempotent operations", "Adds latency"],
      "Retrying a non-idempotent POST (payment) can charge twice. Retrying every exception (including 400 Bad Request) wastes calls that can never succeed.",
      "```java\nRetryConfig cfg = RetryConfig.custom().maxAttempts(3).waitDuration(Duration.ofMillis(200))\n    .retryExceptions(IOException.class).build();\nRetry retry = Retry.of(\"inventory\", cfg);\nSupplier<String> s = Retry.decorateSupplier(retry, () -> client.call());\n```\nRules: retry only transient errors, only idempotent calls, cap attempts, add backoff + jitter.",
      [("Exponential backoff", "java", "RetryConfig.custom().maxAttempts(4)\n  .intervalFunction(IntervalFunction.ofExponentialRandomBackoff(100, 2.0, 0.5)).build();"),
       ("Idempotency key", "text", "POST /payments  Idempotency-Key: 7f3a...   (safe to retry)")],
      [("Which HTTP errors are worth retrying?", "Timeouts, 502/503/504 and connection errors — not 4xx."),
       ("Why add jitter?", "To desynchronize clients so they do not retry in lockstep.")]),
    T("Circuit breaker, bulkhead, timeout, and fallback",
      "A **circuit breaker** watches recent calls. When the failure rate crosses a threshold it OPENs and fails fast; after a wait it goes HALF_OPEN, lets a few probe calls through and CLOSEs again if they succeed. **Bulkhead** limits concurrent calls; **time limiter** bounds duration; a **fallback** returns a degraded answer.",
      "Without protection one slow dependency makes callers pile up threads, which cascades into a full outage. Failing fast protects both sides and gives the downstream room to recover.",
      ["Stops cascading failures", "Gives the downstream time to recover", "Fast, predictable errors", "Degraded but available behavior"],
      ["Thresholds need tuning", "Fallback data may be stale/wrong", "More states to test and monitor"],
      "No breaker: every request waits for the full timeout against a dead service, thread pool exhausts, unrelated endpoints die too. Over-aggressive breaker: opens on harmless blips.",
      "States: CLOSED -> (failure rate >= threshold) -> OPEN -> (wait elapsed) -> HALF_OPEN -> (probe ok) CLOSED / (probe fails) OPEN.\n```java\nCircuitBreakerConfig cfg = CircuitBreakerConfig.custom().slidingWindowSize(10)\n   .failureRateThreshold(50).waitDurationInOpenState(Duration.ofSeconds(10)).build();\n```\n`CallNotPermittedException` is thrown while OPEN.",
      [("Decorate", "java", "Supplier<String> guarded = CircuitBreaker.decorateSupplier(cb, () -> client.call());\ntry { return guarded.get(); } catch (Exception e) { return \"FALLBACK\"; }"),
       ("Order of decorators", "text", "Retry( CircuitBreaker( TimeLimiter( call ) ) )  - typical nesting")],
      [("What happens in HALF_OPEN?", "A limited number of probe calls decide whether to close or re-open."),
       ("Retry or breaker first?", "Usually retry wraps the breaker so each attempt is counted, and an OPEN breaker short-circuits retries.")]),
    T("Observability basics for microservices",
      "Three pillars: **logs** (with correlation IDs), **metrics** (rates, errors, durations — Micrometer/Actuator) and **traces** (a request across services). Resilience4j publishes breaker/retry metrics automatically with Micrometer.",
      "In a distributed system you cannot attach a debugger to a request. Correlation IDs and metrics are how you answer \"which service failed and why?\".",
      ["Faster incident diagnosis", "Data-driven tuning of thresholds"],
      ["Extra infrastructure and storage", "Cardinality and cost management"],
      "Without correlation IDs, logs of five services cannot be joined; without metrics you only learn about outages from users.",
      "Propagate `X-Request-Id` on every outbound call; log it with MDC; expose `/actuator/health` and `/actuator/metrics`.",
      [("Propagate a correlation id", "java", "restClient.get().uri(\"/x\").header(\"X-Request-Id\", MDC.get(\"requestId\"))...")],
      [("What is a correlation id?", "An identifier passed along every hop of a request so logs can be joined.")]),
]

day(43, "Microservices, RestClient, and Resilience4j", "Microservices",
    "Service boundaries, synchronous communication with RestClient, and surviving downstream failures with retry, circuit breaker and fallback",
    ["Explain when to split a system into services and how to size boundaries", "Call another service with `RestClient` and map failures", "Apply retry with backoff safely (idempotency)", "Configure and test a circuit breaker life cycle", "Design graceful degradation instead of cascading failures"],
    ["Day 31-33 REST + validation", "Day 40 Spring Boot testing basics"],
    TOPICS, [t1, t2, t3, t4],
    [("When would you NOT use microservices?", "Small teams/simple domains: a modular monolith is cheaper and easier."),
     ("Retry vs circuit breaker?", "Retry handles transient faults; the breaker stops calling a service that is persistently failing."),
     ("What is idempotency and why does retry need it?", "Repeating the call has the same effect as one call; otherwise retries duplicate side effects."),
     ("How do you test downstream failures without a network?", "Stubs, `MockRestServiceServer`, WireMock, or in-process fakes that fail on demand."),
     ("What is a fallback?", "A degraded but safe response used when the real call fails.")],
    ["Retrying non-idempotent operations.", "No timeouts on HTTP clients.", "Retrying 4xx errors.", "Sharing a database between services.", "Breaker thresholds that open on a single failure."],
    ["Spring Framework Reference: RestClient", "Resilience4j documentation: CircuitBreaker, Retry", "Sam Newman, Building Microservices (chapters on resilience)"],
    [("Bounded context", "Boundary of a consistent domain model"), ("Idempotent", "Safe to repeat"), ("Backoff", "Increasing delay between retries"),
     ("Circuit breaker", "Fail-fast guard with CLOSED/OPEN/HALF_OPEN states"), ("Fallback", "Degraded answer on failure"), ("Bulkhead", "Concurrency limit per dependency")],
    "2-3 h theory + 4-6 h tasks", spring=True)
