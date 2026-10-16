package com.javaprep.day36.task04;

import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Component;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestClient;

@Component
public class QuoteGateway {

    private final RestClient client;

    public QuoteGateway(RestClient.Builder builder, @Value("${quotes.base-url:http://quotes.test}") String baseUrl) {
        this.client = builder.baseUrl(baseUrl).build();
    }

    /** GET /quotes?limit={limit}. */
    public List<Quote> all(int limit) {
        // TODO(Day36-task04): use uriBuilder with path /quotes and query param limit
        throw new UnsupportedOperationException("TODO(Day36-task04): use uriBuilder with path /quotes and query param limit");
    }

    /** Text of quote {id}, or fallback when the server answers 404. Other failures propagate as UpstreamException. */
    public String textOrDefault(long id, String fallback) {
        // TODO(Day36-task04): map 404 to fallback, 5xx to UpstreamException
        throw new UnsupportedOperationException("TODO(Day36-task04): map 404 to fallback, 5xx to UpstreamException");
    }

    /** Tries GET /quotes/{id} up to 2 times when the server answers 5xx; after the second failure throws UpstreamException. */
    public Quote fetchWithRetry(long id) {
        // TODO(Day36-task04): loop at most twice
        throw new UnsupportedOperationException("TODO(Day36-task04): loop at most twice");
    }

    /** Value of the ETag response header for GET /quotes/{id} (empty when absent). Use toBodilessEntity(). */
    public Optional<String> etagOf(long id) {
        // TODO(Day36-task04): read headers from ResponseEntity
        throw new UnsupportedOperationException("TODO(Day36-task04): read headers from ResponseEntity");
    }
}
