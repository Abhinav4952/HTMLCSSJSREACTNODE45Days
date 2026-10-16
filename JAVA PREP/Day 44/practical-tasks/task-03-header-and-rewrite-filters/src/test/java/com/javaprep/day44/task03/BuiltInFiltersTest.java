package com.javaprep.day44.task03;

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
