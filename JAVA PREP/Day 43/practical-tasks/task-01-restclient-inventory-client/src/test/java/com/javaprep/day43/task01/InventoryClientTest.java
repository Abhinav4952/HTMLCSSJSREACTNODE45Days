package com.javaprep.day43.task01;

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
