package com.javaprep.peoplehub.gateway;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.cloud.gateway.route.RouteLocator;

/** Smoke test: the gateway context starts and the three PeopleHub routes are registered. No services need to run. */
@SpringBootTest
class GatewaySmokeTest {

    @Autowired
    private RouteLocator routeLocator;

    @Test
    void routesAreConfigured() {
        var routes = routeLocator.getRoutes().collectList().block();
        assertThat(routes.stream().map(r -> r.getId()).toList()).contains("employees", "leaves", "notifications");
    }
}
