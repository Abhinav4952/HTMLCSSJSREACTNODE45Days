package com.javaprep.day44.task02;

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
