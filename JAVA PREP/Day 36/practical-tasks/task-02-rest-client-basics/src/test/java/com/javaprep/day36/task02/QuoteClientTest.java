package com.javaprep.day36.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.content;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.header;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withServerError;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withStatus;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withSuccess;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.web.client.RestClient;

class QuoteClientTest {

    MockRestServiceServer server;
    QuoteClient client;

    @BeforeEach
    void setUp() {
        RestClient.Builder builder = RestClient.builder();
        server = MockRestServiceServer.bindTo(builder).build();
        client = new QuoteClient(builder, "http://api.test", "k3y");
    }

    @Test
    void findSendsApiKeyAndMapsJson() {
        server.expect(requestTo("http://api.test/quotes/7")).andExpect(method(HttpMethod.GET)).andExpect(header("X-Api-Key", "k3y"))
                .andRespond(withSuccess("{\"id\":7,\"text\":\"Hello\"}", MediaType.APPLICATION_JSON));
        assertThat(client.find(7)).contains(new Quote(7, "Hello"));
        server.verify();
    }

    @Test
    void notFoundBecomesEmpty() {
        server.expect(requestTo("http://api.test/quotes/9")).andRespond(withStatus(HttpStatus.NOT_FOUND));
        assertThat(client.find(9)).isEmpty();
    }

    @Test
    void serverErrorBecomesDomainException() {
        server.expect(requestTo("http://api.test/quotes/1")).andRespond(withServerError());
        assertThatThrownBy(() -> client.find(1)).isInstanceOf(QuoteServiceException.class).hasMessage("Upstream error: 500");
    }

    @Test
    void listReadsGenericCollection() {
        server.expect(requestTo("http://api.test/quotes"))
                .andRespond(withSuccess("[{\"id\":1,\"text\":\"a\"},{\"id\":2,\"text\":\"b\"}]", MediaType.APPLICATION_JSON));
        assertThat(client.list()).extracting(Quote::text).containsExactly("a", "b");
    }

    @Test
    void createPostsJsonBody() {
        server.expect(requestTo("http://api.test/quotes")).andExpect(method(HttpMethod.POST))
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(content().json("{\"text\":\"New\"}"))
                .andRespond(withSuccess("{\"id\":10,\"text\":\"New\"}", MediaType.APPLICATION_JSON));
        assertThat(client.create("New")).isEqualTo(new Quote(10, "New"));
        server.verify();
    }
}
