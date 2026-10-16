package com.javaprep.day44.task01;

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
