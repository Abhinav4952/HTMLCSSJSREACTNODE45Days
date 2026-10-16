package com.javaprep.day36.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withServerError;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withStatus;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withSuccess;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.client.RestClientTest;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;

@RestClientTest(QuoteGateway.class)
class QuoteGatewayTest {

    @Autowired
    QuoteGateway gateway;
    @Autowired
    MockRestServiceServer server;

    @BeforeEach
    void reset() {
        server.reset();
    }

    @AfterEach
    void verify() {
        server.verify();
    }

    @Test
    void allUsesQueryParameter() {
        server.expect(requestTo("http://quotes.test/quotes?limit=3")).andExpect(method(HttpMethod.GET))
                .andRespond(withSuccess("[{\"id\":1,\"text\":\"a\"}]", MediaType.APPLICATION_JSON));
        assertThat(gateway.all(3)).hasSize(1);
    }

    @Test
    void fallbackOn404() {
        server.expect(requestTo("http://quotes.test/quotes/4")).andRespond(withStatus(HttpStatus.NOT_FOUND));
        assertThat(gateway.textOrDefault(4, "n/a")).isEqualTo("n/a");
    }

    @Test
    void textOnSuccess() {
        server.expect(requestTo("http://quotes.test/quotes/4")).andRespond(withSuccess("{\"id\":4,\"text\":\"hi\"}", MediaType.APPLICATION_JSON));
        assertThat(gateway.textOrDefault(4, "n/a")).isEqualTo("hi");
    }

    @Test
    void serverErrorBecomesUpstreamException() {
        server.expect(requestTo("http://quotes.test/quotes/4")).andRespond(withServerError());
        assertThatThrownBy(() -> gateway.textOrDefault(4, "n/a")).isInstanceOf(UpstreamException.class);
    }

    @Test
    void retryRecoversFromOneFailure() {
        server.expect(requestTo("http://quotes.test/quotes/5")).andRespond(withServerError());
        server.expect(requestTo("http://quotes.test/quotes/5")).andRespond(withSuccess("{\"id\":5,\"text\":\"ok\"}", MediaType.APPLICATION_JSON));
        assertThat(gateway.fetchWithRetry(5).text()).isEqualTo("ok");
    }

    @Test
    void retryGivesUpAfterTwoAttempts() {
        server.expect(requestTo("http://quotes.test/quotes/6")).andRespond(withServerError());
        server.expect(requestTo("http://quotes.test/quotes/6")).andRespond(withServerError());
        assertThatThrownBy(() -> gateway.fetchWithRetry(6)).isInstanceOf(UpstreamException.class);
    }

    @Test
    void etagIsReadFromHeaders() {
        server.expect(requestTo("http://quotes.test/quotes/8"))
                .andRespond(withSuccess("{}", MediaType.APPLICATION_JSON).header("ETag", "\"abc\""));
        assertThat(gateway.etagOf(8)).contains("\"abc\"");
    }

    @Test
    void missingEtagIsEmpty() {
        server.expect(requestTo("http://quotes.test/quotes/9")).andRespond(withSuccess("{}", MediaType.APPLICATION_JSON));
        assertThat(gateway.etagOf(9)).isEmpty();
    }
}
