package com.javaprep.day44.task04;

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
