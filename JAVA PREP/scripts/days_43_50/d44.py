from common import *

# ---- shared gateway model (PROVIDED in every task of this day) ----
REQ = r'''package %PKG%;

import java.util.LinkedHashMap;
import java.util.Map;

/** PROVIDED. Immutable request model used by the simulated gateway. */
public record GatewayRequest(String method, String path, Map<String, String> headers) {

    public GatewayRequest {
        headers = Map.copyOf(headers == null ? Map.of() : headers);
    }

    public static GatewayRequest get(String path) {
        return new GatewayRequest("GET", path, Map.of());
    }

    public GatewayRequest withPath(String newPath) {
        return new GatewayRequest(method, newPath, headers);
    }

    public GatewayRequest withHeader(String name, String value) {
        Map<String, String> copy = new LinkedHashMap<>(headers);
        copy.put(name, value);
        return new GatewayRequest(method, path, copy);
    }

    public String header(String name) {
        return headers.get(name);
    }
}
'''
RESP = "package %PKG%;\n\n/** PROVIDED. Minimal response model. */\npublic record GatewayResponse(int status, String body) {\n\n    public static GatewayResponse ok(String body) {\n        return new GatewayResponse(200, body);\n    }\n}\n"
HANDLER = "package %PKG%;\n\n/** PROVIDED. Terminal handler (a downstream service) or the rest of a filter chain. */\n@FunctionalInterface\npublic interface Handler {\n\n    GatewayResponse handle(GatewayRequest request);\n}\n"
FILTER = "package %PKG%;\n\n/** PROVIDED. A gateway filter may change the request, short-circuit, or change the response. */\n@FunctionalInterface\npublic interface GatewayFilter {\n\n    GatewayResponse filter(GatewayRequest request, Handler next);\n}\n"
ROUTE = "package %PKG%;\n\n/** PROVIDED. id, path predicate prefix (e.g. /api/users) and the target service URI. */\npublic record Route(String id, String pathPrefix, String targetUri) {\n}\n"
MODEL = {"main/GatewayRequest.java": REQ, "main/GatewayResponse.java": RESP, "main/Handler.java": HANDLER, "main/GatewayFilter.java": FILTER}

LOCATOR_REF = r'''package %PKG%;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;

/** PROVIDED (reference implementation from task 1). */
public class RouteLocator {

    private final List<Route> routes;

    public RouteLocator(List<Route> routes) {
        this.routes = List.copyOf(routes);
    }

    public Optional<Route> match(String path) {
        String p = path.contains("?") ? path.substring(0, path.indexOf('?')) : path;
        return routes.stream()
                .filter(r -> p.equals(r.pathPrefix()) || p.startsWith(r.pathPrefix() + "/"))
                .max(Comparator.comparingInt(r -> r.pathPrefix().length()));
    }
}
'''
CHAIN_REF = r'''package %PKG%;

import java.util.List;

/** PROVIDED (reference implementation from task 2). */
public final class FilterChain {

    private FilterChain() {
    }

    public static Handler build(List<GatewayFilter> filters, Handler terminal) {
        Handler next = terminal;
        List<GatewayFilter> copy = List.copyOf(filters);
        for (int i = copy.size() - 1; i >= 0; i--) {
            GatewayFilter f = copy.get(i);
            Handler downstream = next;
            next = request -> f.filter(request, downstream);
        }
        return next;
    }
}
'''

# ---------------- task 1
RL = r'''package %PKG%;

import java.util.List;
import java.util.Optional;

/** Predicate-based route matching, like a Spring Cloud Gateway {@code Path=} predicate. */
public class RouteLocator {

    private final List<Route> routes;

    public RouteLocator(List<Route> routes) {
        this.routes = List.copyOf(routes);
    }

    /**
     * A route matches when the path (ignoring any query string) equals the prefix or starts with prefix + "/".
     * If several routes match, the one with the LONGEST prefix wins. No match -> Optional.empty().
     */
    public Optional<Route> match(String path) {
        // TODO(%TAG%): strip the query string, filter matching routes (segment boundary!), pick the longest prefix
        throw new UnsupportedOperationException("TODO(%TAG%): implement match");
    }
}
'''
RL_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.Test;

class RouteLocatorTest {

    private final RouteLocator locator = new RouteLocator(List.of(
            new Route("api", "/api", "http://api-service"),
            new Route("users", "/api/users", "http://user-service"),
            new Route("orders", "/api/orders", "http://order-service")));

    @Test
    void exactPrefixMatches() {
        assertThat(locator.match("/api/users")).map(Route::id).contains("users");
    }

    @Test
    void nestedPathMatches() {
        assertThat(locator.match("/api/orders/42/items")).map(Route::id).contains("orders");
    }

    @Test
    void longestPrefixWins() {
        assertThat(locator.match("/api/users/7")).map(Route::id).contains("users");
        assertThat(locator.match("/api/other")).map(Route::id).contains("api");
    }

    @Test
    void segmentBoundaryIsRespected() {
        assertThat(locator.match("/api/usersX")).map(Route::id).contains("api");
        assertThat(locator.match("/apix")).isEmpty();
    }

    @Test
    void queryStringIsIgnored() {
        assertThat(locator.match("/api/users/7?expand=roles")).map(Route::id).contains("users");
    }

    @Test
    void unknownPathHasNoRoute() {
        assertThat(locator.match("/health")).isEmpty();
    }
}
'''
g1 = task("route-matching", "Route Predicate Matching", "Warm-up", "Java",
    "Simulate gateway route predicates: match request paths to routes by prefix with segment boundaries and longest-prefix-wins.",
    "plain", {**MODEL, "main/Route.java": ROUTE, "main/RouteLocator.java": RL, "test/RouteLocatorTest.java": RL_TEST},
    ["Ignore the query string when matching.", "Match only on whole path segments (`/api/users` must not match `/api/usersX`).", "Pick the route with the longest matching prefix.", "Return `Optional.empty()` when nothing matches."],
    ["Path equal to the prefix.", "Overlapping prefixes.", "Query strings."],
    ["`Comparator.comparingInt(...)` with `Stream.max`."])

# ---------------- task 2
FC = r'''package %PKG%;

import java.util.List;

/** Builds a chain of {@link GatewayFilter}s ending in a terminal {@link Handler} (like Spring's filter chains). */
public final class FilterChain {

    private FilterChain() {
    }

    /**
     * Filters run in list order on the way in and in reverse order on the way out. A filter may skip
     * {@code next.handle(...)} to short-circuit (the terminal is then never called). The list is copied at build time.
     */
    public static Handler build(List<GatewayFilter> filters, Handler terminal) {
        // TODO(%TAG%): compose the filters around the terminal handler (hint: iterate backwards)
        throw new UnsupportedOperationException("TODO(%TAG%): implement build");
    }
}
'''
FC_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class FilterChainTest {

    private final List<String> log = new ArrayList<>();

    private GatewayFilter logging(String name) {
        return (req, next) -> {
            log.add(name + "-pre");
            GatewayResponse r = next.handle(req);
            log.add(name + "-post");
            return r;
        };
    }

    @Test
    void filtersWrapTheTerminalInOrder() {
        Handler chain = FilterChain.build(List.of(logging("A"), logging("B")), req -> {
            log.add("terminal");
            return GatewayResponse.ok("done");
        });
        assertThat(chain.handle(GatewayRequest.get("/x")).body()).isEqualTo("done");
        assertThat(log).containsExactly("A-pre", "B-pre", "terminal", "B-post", "A-post");
    }

    @Test
    void emptyChainIsTheTerminal() {
        Handler chain = FilterChain.build(List.of(), req -> GatewayResponse.ok("t"));
        assertThat(chain.handle(GatewayRequest.get("/x")).body()).isEqualTo("t");
    }

    @Test
    void filterCanShortCircuit() {
        GatewayFilter deny = (req, next) -> new GatewayResponse(401, "denied");
        Handler chain = FilterChain.build(List.of(logging("A"), deny, logging("B")), req -> {
            log.add("terminal");
            return GatewayResponse.ok("done");
        });
        assertThat(chain.handle(GatewayRequest.get("/x")).status()).isEqualTo(401);
        assertThat(log).containsExactly("A-pre", "A-post");
    }

    @Test
    void filterCanChangeTheRequestForLaterFilters() {
        GatewayFilter tag = (req, next) -> next.handle(req.withHeader("X-Tag", "1"));
        Handler chain = FilterChain.build(List.of(tag), req -> GatewayResponse.ok(req.header("X-Tag")));
        assertThat(chain.handle(GatewayRequest.get("/x")).body()).isEqualTo("1");
    }

    @Test
    void listIsCopiedAtBuildTime() {
        List<GatewayFilter> filters = new ArrayList<>(List.of(logging("A")));
        Handler chain = FilterChain.build(filters, req -> GatewayResponse.ok("t"));
        filters.add(logging("LATE"));
        chain.handle(GatewayRequest.get("/x"));
        assertThat(log).containsExactly("A-pre", "A-post");
    }
}
'''
g2 = task("filter-chain", "Filter Chain Composition", "Core", "Java",
    "Compose gateway filters into a chain with pre/post phases and short-circuiting, the core idea behind Spring Cloud Gateway filters and servlet filters.",
    "plain", {**MODEL, "main/FilterChain.java": FC, "test/FilterChainTest.java": FC_TEST},
    ["Build a `Handler` that runs filters in list order (pre) and reverse order (post).", "Allow a filter to short-circuit by not calling `next`.", "An empty list returns the terminal handler behavior.", "Copy the filter list when building."],
    ["Short-circuit in the middle of the chain.", "List mutated after build."],
    ["Wrap from the last filter to the first: `next = req -> filter.filter(req, next)`."])

# ---------------- task 3
FILTERS = {
"main/StripPrefixFilter.java": r'''package %PKG%;

/** Like Gateway's StripPrefix: removes the first N path segments before calling the downstream. */
public class StripPrefixFilter implements GatewayFilter {

    private final int parts;

    public StripPrefixFilter(int parts) {
        this.parts = parts;
    }

    /** "/api/users/1" with parts=1 -> "/users/1"; parts=2 -> "/1"; more parts than segments -> "/". */
    @Override
    public GatewayResponse filter(GatewayRequest request, Handler next) {
        // TODO(%TAG%): split the path into segments, drop the first `parts`, rebuild the path (keep query string)
        throw new UnsupportedOperationException("TODO(%TAG%): implement StripPrefixFilter");
    }
}
''',
"main/AddRequestHeaderFilter.java": r'''package %PKG%;

/** Like Gateway's AddRequestHeader: sets (overwrites) a header before calling the downstream. */
public class AddRequestHeaderFilter implements GatewayFilter {

    private final String name;
    private final String value;

    public AddRequestHeaderFilter(String name, String value) {
        this.name = name;
        this.value = value;
    }

    @Override
    public GatewayResponse filter(GatewayRequest request, Handler next) {
        // TODO(%TAG%): add the header (overwrite an existing one) and continue the chain
        throw new UnsupportedOperationException("TODO(%TAG%): implement AddRequestHeaderFilter");
    }
}
''',
"main/RewritePathFilter.java": r'''package %PKG%;

/** Like Gateway's RewritePath: regex replace on the path, e.g. "/old/(?<rest>.*)" -> "/new/${rest}". */
public class RewritePathFilter implements GatewayFilter {

    private final String regex;
    private final String replacement;

    public RewritePathFilter(String regex, String replacement) {
        this.regex = regex;
        this.replacement = replacement;
    }

    @Override
    public GatewayResponse filter(GatewayRequest request, Handler next) {
        // TODO(%TAG%): apply String.replaceAll(regex, replacement) to the path and continue
        throw new UnsupportedOperationException("TODO(%TAG%): implement RewritePathFilter");
    }
}
''',
}
F_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.Test;

class BuiltInFiltersTest {

    private final AtomicReference<GatewayRequest> seen = new AtomicReference<>();
    private final Handler capture = r -> {
        seen.set(r);
        return GatewayResponse.ok("x");
    };

    @Test
    void stripOnePrefixSegment() {
        new StripPrefixFilter(1).filter(GatewayRequest.get("/api/users/1"), capture);
        assertThat(seen.get().path()).isEqualTo("/users/1");
    }

    @Test
    void stripTwoPrefixSegments() {
        new StripPrefixFilter(2).filter(GatewayRequest.get("/api/users/1"), capture);
        assertThat(seen.get().path()).isEqualTo("/1");
    }

    @Test
    void stripMoreThanAvailableLeavesRoot() {
        new StripPrefixFilter(5).filter(GatewayRequest.get("/api/users"), capture);
        assertThat(seen.get().path()).isEqualTo("/");
    }

    @Test
    void stripKeepsQueryString() {
        new StripPrefixFilter(1).filter(GatewayRequest.get("/api/users?x=1"), capture);
        assertThat(seen.get().path()).isEqualTo("/users?x=1");
    }

    @Test
    void addHeaderSetsAndOverwrites() {
        GatewayRequest req = GatewayRequest.get("/x").withHeader("X-Source", "client");
        new AddRequestHeaderFilter("X-Source", "gateway").filter(req, capture);
        assertThat(seen.get().header("X-Source")).isEqualTo("gateway");
    }

    @Test
    void addHeaderReturnsDownstreamResponse() {
        GatewayResponse r = new AddRequestHeaderFilter("A", "b").filter(GatewayRequest.get("/x"), capture);
        assertThat(r.body()).isEqualTo("x");
    }

    @Test
    void rewritePathWithNamedGroup() {
        new RewritePathFilter("/old/(?<rest>.*)", "/new/${rest}").filter(GatewayRequest.get("/old/a/b"), capture);
        assertThat(seen.get().path()).isEqualTo("/new/a/b");
    }

    @Test
    void rewriteLeavesNonMatchingPathsAlone() {
        new RewritePathFilter("/old/(?<rest>.*)", "/new/${rest}").filter(GatewayRequest.get("/other"), capture);
        assertThat(seen.get().path()).isEqualTo("/other");
    }
}
'''
g3 = task("header-and-rewrite-filters", "Strip-Prefix, Header and Rewrite Filters", "Core", "Java",
    "Implement three classic gateway filters: StripPrefix, AddRequestHeader and RewritePath.",
    "plain", {**MODEL, **FILTERS, "test/BuiltInFiltersTest.java": F_TEST},
    ["`StripPrefixFilter` removes N leading segments and keeps the query string.", "`AddRequestHeaderFilter` sets/overwrites a header.", "`RewritePathFilter` applies a regex replacement to the path.", "Every filter must call `next` with the modified request and return its response."],
    ["More segments than available.", "Header already present.", "Non-matching rewrite."],
    ["Split the query string off first, then work on `path.split(\"/\")`."])

# ---------------- task 4
KEY = r'''package %PKG%;

import java.util.Set;

/** Rejects requests without a valid X-API-Key header. */
public class ApiKeyFilter implements GatewayFilter {

    private final Set<String> validKeys;

    public ApiKeyFilter(Set<String> validKeys) {
        this.validKeys = Set.copyOf(validKeys);
    }

    /** Missing or unknown key -> new GatewayResponse(401, "missing or invalid api key") and do NOT call next. */
    @Override
    public GatewayResponse filter(GatewayRequest request, Handler next) {
        // TODO(%TAG%): check the X-API-Key header against validKeys
        throw new UnsupportedOperationException("TODO(%TAG%): implement ApiKeyFilter");
    }
}
'''
RATE = r'''package %PKG%;

import java.time.Clock;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

/** Fixed-window rate limiter per X-API-Key (header absent -> client "anonymous"). */
public class RateLimitFilter implements GatewayFilter {

    private final int maxRequests;
    private final Duration window;
    private final Clock clock;
    private final Map<String, long[]> windows = new HashMap<>(); // client -> {windowStartMillis, count}

    public RateLimitFilter(int maxRequests, Duration window, Clock clock) {
        this.maxRequests = maxRequests;
        this.window = window;
        this.clock = clock;
    }

    /**
     * Allow at most maxRequests per client per window. The window starts at the client's first request; once
     * {@code window} has elapsed the counter resets. Over the limit -> new GatewayResponse(429, "rate limit exceeded").
     */
    @Override
    public synchronized GatewayResponse filter(GatewayRequest request, Handler next) {
        // TODO(%TAG%): look up/create the client's window, reset if expired, count, and allow or answer 429
        throw new UnsupportedOperationException("TODO(%TAG%): implement RateLimitFilter");
    }
}
'''
GW = r'''package %PKG%;

import java.util.List;
import java.util.Map;
import java.util.Optional;

/** Edge entry point: route lookup, global filters, backend invocation. */
public class Gateway {

    private final RouteLocator locator;
    private final List<GatewayFilter> globalFilters;
    private final Map<String, Handler> backendsByRouteId;

    public Gateway(RouteLocator locator, List<GatewayFilter> globalFilters, Map<String, Handler> backendsByRouteId) {
        this.locator = locator;
        this.globalFilters = List.copyOf(globalFilters);
        this.backendsByRouteId = Map.copyOf(backendsByRouteId);
    }

    /**
     * 1) no matching route -> 404 "no route" (filters are NOT run)
     * 2) matching route without a backend registered -> 502 "no backend"
     * 3) otherwise run the global filters (in order) around the route's backend handler
     */
    public GatewayResponse handle(GatewayRequest request) {
        // TODO(%TAG%): use locator.match, backendsByRouteId and FilterChain.build
        throw new UnsupportedOperationException("TODO(%TAG%): implement handle");
    }
}
'''
GW_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class GatewayTest {

    static class MutableClock extends Clock {
        Instant now = Instant.parse("2025-01-01T00:00:00Z");

        @Override
        public ZoneId getZone() {
            return ZoneOffset.UTC;
        }

        @Override
        public Clock withZone(ZoneId zone) {
            return this;
        }

        @Override
        public Instant instant() {
            return now;
        }
    }

    private final MutableClock clock = new MutableClock();
    private Gateway gateway;

    @BeforeEach
    void setUp() {
        RouteLocator locator = new RouteLocator(List.of(new Route("users", "/api/users", "http://users"),
                new Route("orphan", "/api/orphan", "http://nowhere")));
        gateway = new Gateway(locator,
                List.of(new ApiKeyFilter(Set.of("k1", "k2")), new RateLimitFilter(2, Duration.ofSeconds(10), clock)),
                Map.of("users", req -> GatewayResponse.ok("users-ok")));
    }

    private GatewayRequest req(String path, String key) {
        GatewayRequest r = GatewayRequest.get(path);
        return key == null ? r : r.withHeader("X-API-Key", key);
    }

    @Test
    void validKeyReachesBackend() {
        assertThat(gateway.handle(req("/api/users/1", "k1")).body()).isEqualTo("users-ok");
    }

    @Test
    void missingOrWrongKeyIs401() {
        assertThat(gateway.handle(req("/api/users/1", null)).status()).isEqualTo(401);
        assertThat(gateway.handle(req("/api/users/1", "nope")).status()).isEqualTo(401);
    }

    @Test
    void unknownRouteIs404EvenWithoutKey() {
        assertThat(gateway.handle(req("/other", null)).status()).isEqualTo(404);
    }

    @Test
    void routeWithoutBackendIs502() {
        assertThat(gateway.handle(req("/api/orphan", "k1")).status()).isEqualTo(502);
    }

    @Test
    void thirdRequestInWindowIs429() {
        assertThat(gateway.handle(req("/api/users", "k1")).status()).isEqualTo(200);
        assertThat(gateway.handle(req("/api/users", "k1")).status()).isEqualTo(200);
        assertThat(gateway.handle(req("/api/users", "k1")).status()).isEqualTo(429);
    }

    @Test
    void limitsAreTrackedPerClient() {
        gateway.handle(req("/api/users", "k1"));
        gateway.handle(req("/api/users", "k1"));
        assertThat(gateway.handle(req("/api/users", "k2")).status()).isEqualTo(200);
    }

    @Test
    void windowResetsAfterItElapses() {
        gateway.handle(req("/api/users", "k1"));
        gateway.handle(req("/api/users", "k1"));
        assertThat(gateway.handle(req("/api/users", "k1")).status()).isEqualTo(429);
        clock.now = clock.now.plusSeconds(11);
        assertThat(gateway.handle(req("/api/users", "k1")).status()).isEqualTo(200);
    }

    @Test
    void rejectedRequestsDoNotConsumeRateLimit() {
        gateway.handle(req("/api/users", null));
        gateway.handle(req("/api/users", "bad"));
        gateway.handle(req("/api/users", "bad"));
        assertThat(gateway.handle(req("/api/users", "k1")).status()).isEqualTo(200);
    }
}
'''
g4 = task("gateway-auth-rate-limit-challenge", "Edge Gateway: API Key + Rate Limit (Challenge)", "Challenge", "Java",
    "Assemble a small gateway: route lookup, API-key authentication filter and a fixed-window rate limiter, all as ordered filters.",
    "plain", {**MODEL, "main/Route.java": ROUTE, "main/RouteLocator.java": LOCATOR_REF, "main/FilterChain.java": CHAIN_REF,
              "main/ApiKeyFilter.java": KEY, "main/RateLimitFilter.java": RATE, "main/Gateway.java": GW, "test/GatewayTest.java": GW_TEST},
    ["`ApiKeyFilter`: 401 for missing/unknown keys, otherwise continue.", "`RateLimitFilter`: per-client fixed window using the injected `Clock`; 429 when exceeded.",
     "`Gateway.handle`: 404 for unknown route, 502 when no backend, else filters around backend.", "Filter order matters: authentication happens before rate limiting."],
    ["Window expiry.", "Anonymous clients.", "Unauthenticated requests must not consume quota."],
    ["`clock.millis()` gives the current time; compare with the window start.", "`FilterChain.build` and `RouteLocator` are provided."])

TOPICS = [
    T("API gateway pattern and Spring Cloud Gateway concepts",
      "An **API gateway** is the single entry point for clients: it routes requests to services, and applies cross-cutting concerns (authentication, rate limiting, header manipulation, logging, CORS). Spring Cloud Gateway models this with **routes** (id, URI, predicates, filters), **predicates** (match path/method/header) and **filters** (pre/post processing).",
      "Without a gateway every client must know every service's address and each service re-implements auth and throttling. The gateway centralizes edge concerns and hides internal topology.",
      ["One public address, many private services", "Central auth, throttling, observability", "Request/response transformation", "Canary/blue-green routing"],
      ["Another hop (latency) and component to run", "Single point of failure if not scaled", "Risk of putting business logic in the gateway"],
      "Without it, clients call services directly: CORS, TLS, auth and rate limiting get duplicated and every internal refactor breaks clients.",
      "Spring Cloud Gateway route in YAML:\n```yaml\nspring:\n  cloud:\n    gateway:\n      routes:\n        - id: users\n          uri: http://localhost:8081\n          predicates:\n            - Path=/api/users/**\n          filters:\n            - StripPrefix=1\n            - AddRequestHeader=X-Source, gateway\n```\n**Course decision:** Spring Cloud Gateway is reactive (WebFlux) and its release train (2024.0.x for Boot 3.4) must be matched to the Boot version. To keep the labs dependency-light and Boot-version-proof, the tasks **simulate** routes, predicates and the filter chain in plain Java. Project 03 (PeopleHub) uses the real `spring-cloud-starter-gateway` with the Spring Cloud BOM.",
      [("Predicates", "yaml", "predicates:\n  - Path=/api/orders/**\n  - Method=GET,POST\n  - Header=X-Tenant, \\d+"),
       ("Custom filter (real Gateway)", "java", "@Component\nclass LogFilter implements GlobalFilter {\n  public Mono<Void> filter(ServerWebExchange ex, GatewayFilterChain chain) {\n    return chain.filter(ex).then(Mono.fromRunnable(() -> log.info(\"done\")));\n  }\n}")],
      [("Why not put business logic in the gateway?", "It becomes a bottleneck and a monolith at the edge; keep it to cross-cutting concerns."),
       ("What are predicates?", "Conditions that decide whether a route applies to a request.")]),
    T("Filter chains, ordering, and short-circuiting",
      "A filter chain is an ordered list of filters; each receives the request and a `next` handle. Code before `next` is the **pre** phase, code after is the **post** phase. A filter that does not call `next` **short-circuits** (e.g. 401).",
      "Order decides behavior: authenticate before rate-limiting (so anonymous traffic cannot burn a user's quota), log outermost, add headers before the proxy call.",
      ["Composable, reusable cross-cutting logic", "Easy to unit test in isolation", "Same pattern as servlet filters and Spring Security"],
      ["Order bugs are subtle", "Too many filters add latency", "Debugging requires understanding the chain"],
      "A wrong order (rate limit before auth) lets attackers exhaust other users' quotas; forgetting to call `next` silently drops requests.",
      "```java\nHandler chain = FilterChain.build(List.of(auth, rateLimit, addHeaders), proxy);\n```\nOut path runs in reverse: `auth-pre, rate-pre, proxy, rate-post, auth-post`.",
      [("Pre/post", "java", "(req, next) -> { log(\"pre\"); var r = next.handle(req); log(\"post\"); return r; }")],
      [("Which runs last on the way out: first or last filter?", "The first filter (outermost) runs its post phase last."),
       ("How does a filter reject a request?", "It returns a response without calling `next`.")]),
    T("Edge authentication, rate limiting, and configuration across services",
      "Edge concerns: validate credentials/JWT once at the gateway and forward identity headers; limit request rates (fixed window, sliding window, token bucket); and share configuration across services via externalized properties (Spring Cloud Config concept: one config repository, per-service and per-profile files).",
      "Central enforcement avoids inconsistent security. Configuration drift between services is a classic outage cause.",
      ["Consistent security at the perimeter", "Protects services from abuse", "One place to change shared settings"],
      ["Gateway must be trusted by services (network policy, mTLS or signed headers)", "Rate-limit state needs a shared store when scaled out (Redis)", "Config server is another moving part"],
      "If services trust an `X-User` header but are reachable directly, anyone can forge it. In-memory rate limits per gateway instance multiply the effective limit when you scale out.",
      "Config layering (local files in this course): `application.yml` (shared) < `application-{profile}.yml` < environment variables. Config Server is covered conceptually: clients use `spring.config.import=configserver:http://host:8888`.",
      [("Token bucket idea", "text", "bucket(capacity=10, refill=5/s): request takes 1 token; empty -> 429"),
       ("Shared + service-specific props", "yaml", "# application.yml (shared)\nmanagement.endpoints.web.exposure.include: health,info\n# application-order.yml\nserver.port: 8082")],
      [("Why is in-memory rate limiting insufficient at scale?", "Each instance counts separately; use a shared store such as Redis."),
       ("Why authenticate before rate limiting?", "So unauthenticated traffic cannot consume an authenticated client's quota.")]),
]

day(44, "API Gateway, Filters, and Configuration Across Services", "Microservices",
    "Routes, predicates and filters at the edge; authentication and rate limiting; configuration sharing across services",
    ["Explain the gateway pattern and what belongs at the edge", "Model routes, predicates and filter chains", "Implement StripPrefix/AddHeader/Rewrite style filters", "Build API-key authentication and rate limiting as ordered filters", "Describe config sharing (profiles, Config Server concept)"],
    ["Day 43 Microservices and Resilience4j"],
    TOPICS, [g1, g2, g3, g4],
    [("What is an API gateway?", "A single entry point that routes requests and applies cross-cutting concerns."),
     ("Gateway vs load balancer?", "A load balancer spreads traffic across instances; a gateway understands HTTP semantics (routes, auth, transforms)."),
     ("How do services trust the gateway?", "Network isolation, mTLS, or verifying signed tokens in each service (zero trust)."),
     ("Where do you rate limit?", "At the gateway (coarse) and optionally in services for expensive operations."),
     ("What is the Config Server pattern?", "A central service serving per-application, per-profile properties from a git repository.")],
    ["Wrong filter order.", "Forgetting to call `next`.", "Trusting identity headers from the public internet.", "Matching prefixes without segment boundaries."],
    ["Spring Cloud Gateway Reference", "Spring Cloud release train compatibility matrix", "Spring Cloud Config reference"],
    [("Route", "id + target URI + predicates + filters"), ("Predicate", "Match condition"), ("Filter", "Pre/post processing step"), ("Short-circuit", "Responding without calling the next handler"),
     ("Token bucket", "Rate-limit algorithm with refilling tokens"), ("Config Server", "Central externalized configuration service")],
    "2-3 h theory + 4-6 h tasks", spring=False)
