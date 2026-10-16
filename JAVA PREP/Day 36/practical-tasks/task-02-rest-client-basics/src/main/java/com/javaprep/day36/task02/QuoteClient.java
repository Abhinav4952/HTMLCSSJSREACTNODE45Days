package com.javaprep.day36.task02;

import java.util.List;
import java.util.Optional;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.web.client.RestClient;

public class QuoteClient {

    private final RestClient client;

    /** Builds the client with the base URL and a default header X-Api-Key. */
    public QuoteClient(RestClient.Builder builder, String baseUrl, String apiKey) {
        // TODO(Day36-task02): builder.baseUrl(baseUrl).defaultHeader X-Api-Key then build
        throw new UnsupportedOperationException("TODO(Day36-task02): builder.baseUrl(baseUrl).defaultHeader X-Api-Key then build");
    }

    /** GET /quotes/{id}; 404 -> Optional.empty(); 5xx -> QuoteServiceException("Upstream error: <status code value>"). */
    public Optional<Quote> find(long id) {
        // TODO(Day36-task02): retrieve with onStatus handlers; map 404 to empty
        throw new UnsupportedOperationException("TODO(Day36-task02): retrieve with onStatus handlers; map 404 to empty");
    }

    /** GET /quotes -> list of quotes (generic type needs ParameterizedTypeReference). */
    public List<Quote> list() {
        // TODO(Day36-task02): GET and read a List<Quote>
        throw new UnsupportedOperationException("TODO(Day36-task02): GET and read a List<Quote>");
    }

    /** POST /quotes with JSON {"text": "..."} -> the created Quote returned by the server. */
    public Quote create(String text) {
        // TODO(Day36-task02): POST a body as JSON and read the Quote
        throw new UnsupportedOperationException("TODO(Day36-task02): POST a body as JSON and read the Quote");
    }
}
