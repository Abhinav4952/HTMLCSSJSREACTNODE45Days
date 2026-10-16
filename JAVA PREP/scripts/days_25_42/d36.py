from sx import *

S = ["spring-boot-starter-web"]
SPRINGDOC = dep("org.springdoc", "springdoc-openapi-starter-webmvc-api", "2.7.0")

# ------------------------------------------------------------ task 1
ITEM = r'''package %PKG%;

import io.swagger.v3.oas.annotations.media.Schema;

public record Item(
        @Schema(description = "Unique identifier", example = "1")
        long id,
        //A! document this field: @Schema(description = "Display name", example = "Laptop")
        @Schema(description = "Display name", example = "Laptop")
        //E!
        String name,
        //A! document this field: @Schema(description = "Price in euro", example = "999.00")
        @Schema(description = "Price in euro", example = "999.00")
        //E!
        double price) {
}
'''
ICTL = r'''package %PKG%;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

//A! group the endpoints: @Tag(name = "Items", description = "Item catalogue")
@Tag(name = "Items", description = "Item catalogue")
//E!
@RestController
@RequestMapping("/api/items")
public class ItemController {

    private static final Map<Long, Item> ITEMS = Map.of(
            1L, new Item(1, "Laptop", 999.0),
            2L, new Item(2, "Mouse", 19.5));

    //A! @Operation(summary = "List all items")
    @Operation(summary = "List all items")
    //E!
    @GetMapping
    public List<Item> list() {
        return ITEMS.values().stream().sorted(java.util.Comparator.comparingLong(Item::id)).toList();
    }

    //A! @Operation(summary = "Find an item by id") and @ApiResponse(responseCode = "200", description = "Item found") and @ApiResponse(responseCode = "404", description = "Item not found")
    @Operation(summary = "Find an item by id")
    @ApiResponse(responseCode = "200", description = "Item found")
    @ApiResponse(responseCode = "404", description = "Item not found")
    //E!
    @GetMapping("/{id}")
    public ResponseEntity<Item> get(@PathVariable long id) {
        Item item = ITEMS.get(id);
        return item == null ? ResponseEntity.notFound().build() : ResponseEntity.ok(item);
    }
}
'''
OCFG = r'''package %PKG%;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    /** Title "Items API", version "1.0.0", description "Demo catalogue API". */
    @Bean
    public OpenAPI itemsOpenApi() {
        //B! build an OpenAPI with an Info(title, version, description)
        return new OpenAPI().info(new Info().title("Items API").version("1.0.0").description("Demo catalogue API"));
        //E!
    }
}
'''
OT = r'''package %PKG%;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class OpenApiDocsTest {

    @Autowired
    MockMvc mvc;

    @Test
    void docsAreServed() throws Exception {
        mvc.perform(get("/v3/api-docs")).andExpect(status().isOk()).andExpect(jsonPath("$.openapi").exists());
    }

    @Test
    void infoBlock() throws Exception {
        mvc.perform(get("/v3/api-docs")).andExpect(jsonPath("$.info.title").value("Items API"))
                .andExpect(jsonPath("$.info.version").value("1.0.0")).andExpect(jsonPath("$.info.description").value("Demo catalogue API"));
    }

    @Test
    void controllerIsGroupedUnderTag() throws Exception {
        mvc.perform(get("/v3/api-docs")).andExpect(jsonPath("$.paths['/api/items'].get.tags[0]").value("Items"))
                .andExpect(jsonPath("$.tags[?(@.name=='Items')].description").value("Item catalogue"));
    }

    @Test
    void operationsHaveSummaries() throws Exception {
        mvc.perform(get("/v3/api-docs")).andExpect(jsonPath("$.paths['/api/items'].get.summary").value("List all items"))
                .andExpect(jsonPath("$.paths['/api/items/{id}'].get.summary").value("Find an item by id"));
    }

    @Test
    void notFoundResponseIsDocumented() throws Exception {
        mvc.perform(get("/v3/api-docs")).andExpect(jsonPath("$.paths['/api/items/{id}'].get.responses['404'].description").value("Item not found"))
                .andExpect(jsonPath("$.paths['/api/items/{id}'].get.responses['200'].description").value("Item found"));
    }

    @Test
    void schemaFieldsAreDocumented() throws Exception {
        mvc.perform(get("/v3/api-docs")).andExpect(jsonPath("$.components.schemas.Item.properties.name.description").value("Display name"))
                .andExpect(jsonPath("$.components.schemas.Item.properties.name.example").value("Laptop"))
                .andExpect(jsonPath("$.components.schemas.Item.properties.price.description").value("Price in euro"));
    }
}
'''
a1 = tk("springdoc-openapi-docs", "OpenAPI Documentation with springdoc", "Warm-up",
    "Generate and enrich an OpenAPI 3 document: Info bean, @Tag, @Operation, @ApiResponse and @Schema.",
    {"main/Application.java": APP, "main/Item.java": ITEM, "main/ItemController.java": ICTL, "main/OpenApiConfig.java": OCFG},
    {"test/OpenApiDocsTest.java": OT},
    ["Build the `OpenAPI` bean with title, version and description.", "Add `@Tag`, `@Operation` and `@ApiResponse` annotations to the controller.", "Document the `Item` record fields with `@Schema`."],
    ["The 404 response must appear even though the method returns `ResponseEntity<Item>`.", "Docs are generated at runtime from the running mappings."],
    ["`@ApiResponse` is repeatable on a method.", "`OpenAPI` and `Info` live in `io.swagger.v3.oas.models`."],
    S, deps=[SPRINGDOC])

# ------------------------------------------------------------ task 2
QUOTE = "package %PKG%;\n\npublic record Quote(long id, String text) {\n}\n"
QEX = "package %PKG%;\n\npublic class QuoteServiceException extends RuntimeException {\n    public QuoteServiceException(String message) {\n        super(message);\n    }\n}\n"
QC = r'''package %PKG%;

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
        //B! builder.baseUrl(baseUrl).defaultHeader X-Api-Key then build
        this.client = builder.baseUrl(baseUrl).defaultHeader("X-Api-Key", apiKey).build();
        //E!
    }

    /** GET /quotes/{id}; 404 -> Optional.empty(); 5xx -> QuoteServiceException("Upstream error: <status code value>"). */
    public Optional<Quote> find(long id) {
        //B! retrieve with onStatus handlers; map 404 to empty
        try {
            return Optional.ofNullable(client.get().uri("/quotes/{id}", id).retrieve()
                    .onStatus(HttpStatusCode::is5xxServerError, (req, res) -> {
                        throw new QuoteServiceException("Upstream error: " + res.getStatusCode().value());
                    })
                    .body(Quote.class));
        } catch (org.springframework.web.client.HttpClientErrorException.NotFound e) {
            return Optional.empty();
        }
        //E!
    }

    /** GET /quotes -> list of quotes (generic type needs ParameterizedTypeReference). */
    public List<Quote> list() {
        //B! GET and read a List<Quote>
        return client.get().uri("/quotes").retrieve().body(new ParameterizedTypeReference<List<Quote>>() { });
        //E!
    }

    /** POST /quotes with JSON {"text": "..."} -> the created Quote returned by the server. */
    public Quote create(String text) {
        //B! POST a body as JSON and read the Quote
        return client.post().uri("/quotes").contentType(MediaType.APPLICATION_JSON)
                .body(java.util.Map.of("text", text)).retrieve().body(Quote.class);
        //E!
    }
}
'''
QT = r'''package %PKG%;

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
'''
a2 = tk("rest-client-basics", "RestClient Basics with MockRestServiceServer", "Core",
    "Call an HTTP API with Spring 6.1's fluent RestClient: base URL, default header, status handling, generic lists and JSON posts.",
    {"main/Application.java": APP, "main/Quote.java": QUOTE, "main/QuoteServiceException.java": QEX, "main/QuoteClient.java": QC},
    {"test/QuoteClientTest.java": QT},
    ["Configure the builder with base URL and `X-Api-Key`.", "Implement `find` (404 -> empty, 5xx -> domain exception), `list` and `create`."],
    ["Without `onStatus`, 4xx/5xx raise `HttpClientErrorException`/`HttpServerErrorException`.", "Generic collections need `ParameterizedTypeReference`."],
    ["`MockRestServiceServer.bindTo(builder)` intercepts calls without a network.", "Never use real network calls in unit tests."],
    S)

# ------------------------------------------------------------ task 3
CCTL = r'''package %PKG%;

import java.util.Map;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DataController {

    @GetMapping("/api/data")
    public Map<String, String> data() {
        return Map.of("status", "ok");
    }

    @PostMapping("/api/data")
    public Map<String, String> create() {
        return Map.of("status", "created");
    }

    @DeleteMapping("/api/data/{id}")
    public void delete(@PathVariable long id) {
    }

    @GetMapping("/other")
    public String other() {
        return "other";
    }

    //A! allow ANY origin for this single endpoint with @CrossOrigin(origins = "*")
    @CrossOrigin(origins = "*")
    //E!
    @GetMapping("/public/ping")
    public String ping() {
        return "pong";
    }
}
'''
CCFG = r'''package %PKG%;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * CORS policy for /api/**: origin https://app.example.com only; methods GET, POST, PUT, DELETE;
 * any request headers; credentials allowed; preflight cached for 3600 seconds.
 */
@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        //B! registry.addMapping on /api/** with origins, methods, headers, credentials and maxAge
        registry.addMapping("/api/**")
                .allowedOrigins("https://app.example.com")
                .allowedMethods("GET", "POST", "PUT", "DELETE")
                .allowedHeaders("*")
                .allowCredentials(true)
                .maxAge(3600);
        //E!
    }
}
'''
CT = r'''package %PKG%;

import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.options;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(DataController.class)
@Import(CorsConfig.class)
class CorsTest {

    static final String ALLOWED = "https://app.example.com";

    @Autowired
    MockMvc mvc;

    @Test
    void preflightFromAllowedOrigin() throws Exception {
        mvc.perform(options("/api/data").header("Origin", ALLOWED).header("Access-Control-Request-Method", "POST")
                        .header("Access-Control-Request-Headers", "content-type"))
                .andExpect(status().isOk())
                .andExpect(header().string("Access-Control-Allow-Origin", ALLOWED))
                .andExpect(header().string("Access-Control-Allow-Credentials", "true"))
                .andExpect(header().string("Access-Control-Max-Age", "3600"))
                .andExpect(header().string("Access-Control-Allow-Methods", containsString("POST")))
                .andExpect(header().string("Access-Control-Allow-Headers", containsString("content-type")));
    }

    @Test
    void deleteIsAllowedButPatchIsNot() throws Exception {
        mvc.perform(options("/api/data/5").header("Origin", ALLOWED).header("Access-Control-Request-Method", "DELETE"))
                .andExpect(status().isOk());
        mvc.perform(options("/api/data").header("Origin", ALLOWED).header("Access-Control-Request-Method", "PATCH"))
                .andExpect(status().isForbidden());
    }

    @Test
    void preflightFromOtherOriginIsForbidden() throws Exception {
        mvc.perform(options("/api/data").header("Origin", "https://evil.example").header("Access-Control-Request-Method", "GET"))
                .andExpect(status().isForbidden());
    }

    @Test
    void simpleRequestGetsAllowOriginHeader() throws Exception {
        mvc.perform(get("/api/data").header("Origin", ALLOWED)).andExpect(status().isOk())
                .andExpect(header().string("Access-Control-Allow-Origin", ALLOWED));
    }

    @Test
    void noOriginNoCorsHeaders() throws Exception {
        mvc.perform(get("/api/data")).andExpect(status().isOk()).andExpect(header().doesNotExist("Access-Control-Allow-Origin"));
    }

    @Test
    void pathsOutsideTheMappingGetNoCorsHeaders() throws Exception {
        mvc.perform(get("/other").header("Origin", ALLOWED)).andExpect(header().doesNotExist("Access-Control-Allow-Origin"));
    }

    @Test
    void crossOriginAnnotationOpensOnlyThePingEndpoint() throws Exception {
        mvc.perform(get("/public/ping").header("Origin", "https://anyone.example")).andExpect(status().isOk())
                .andExpect(header().string("Access-Control-Allow-Origin", "*"));
    }
}
'''
a3 = tk("cors-policy", "CORS Policy", "Core",
    "Configure a global CORS policy with WebMvcConfigurer and open a single endpoint with @CrossOrigin, then verify preflight behavior.",
    {"main/Application.java": APP, "main/DataController.java": CCTL, "main/CorsConfig.java": CCFG},
    {"test/CorsTest.java": CT},
    ["Implement `CorsConfig.addCorsMappings` for `/api/**`.", "Add `@CrossOrigin(origins = \"*\")` to the ping endpoint."],
    ["`allowedOrigins(\"*\")` cannot be combined with `allowCredentials(true)`.", "CORS is enforced by browsers; it is not authentication.", "Preflight is an `OPTIONS` request with `Origin` and `Access-Control-Request-Method` headers."],
    ["`maxAge` is in seconds.", "Forbidden (403) is how Spring rejects an invalid CORS request."],
    S)

# ------------------------------------------------------------ task 4
QG = r'''package %PKG%;

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
        //B! use uriBuilder with path /quotes and query param limit
        return client.get().uri(b -> b.path("/quotes").queryParam("limit", limit).build()).retrieve()
                .body(new ParameterizedTypeReference<List<Quote>>() { });
        //E!
    }

    /** Text of quote {id}, or fallback when the server answers 404. Other failures propagate as UpstreamException. */
    public String textOrDefault(long id, String fallback) {
        //B! map 404 to fallback, 5xx to UpstreamException
        try {
            Quote q = client.get().uri("/quotes/{id}", id).retrieve()
                    .onStatus(HttpStatusCode::is5xxServerError, (req, res) -> {
                        throw new UpstreamException("Upstream error " + res.getStatusCode().value());
                    })
                    .body(Quote.class);
            return q == null ? fallback : q.text();
        } catch (HttpClientErrorException.NotFound e) {
            return fallback;
        }
        //E!
    }

    /** Tries GET /quotes/{id} up to 2 times when the server answers 5xx; after the second failure throws UpstreamException. */
    public Quote fetchWithRetry(long id) {
        //B! loop at most twice
        UpstreamException last = null;
        for (int attempt = 1; attempt <= 2; attempt++) {
            try {
                return client.get().uri("/quotes/{id}", id).retrieve()
                        .onStatus(HttpStatusCode::is5xxServerError, (req, res) -> {
                            throw new UpstreamException("Upstream error " + res.getStatusCode().value());
                        })
                        .body(Quote.class);
            } catch (UpstreamException e) {
                last = e;
            }
        }
        throw last;
        //E!
    }

    /** Value of the ETag response header for GET /quotes/{id} (empty when absent). Use toBodilessEntity(). */
    public Optional<String> etagOf(long id) {
        //B! read headers from ResponseEntity
        return Optional.ofNullable(client.get().uri("/quotes/{id}", id).retrieve().toBodilessEntity().getHeaders().getETag());
        //E!
    }
}
'''
UEX = "package %PKG%;\n\npublic class UpstreamException extends RuntimeException {\n    public UpstreamException(String message) {\n        super(message);\n    }\n}\n"
QGT = r'''package %PKG%;

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
'''
a4 = tk("quote-gateway-challenge", "HTTP Gateway: Retry, Fallback and Headers", "Challenge",
    "Wrap a remote API behind a Spring-managed gateway: query building, fallback on 404, bounded retry on 5xx and response header access.",
    {"main/Application.java": APP, "main/Quote.java": QUOTE, "main/UpstreamException.java": UEX, "main/QuoteGateway.java": QG},
    {"test/QuoteGatewayTest.java": QGT},
    ["Implement all four gateway methods using the injected `RestClient`.", "Retry exactly once on 5xx; never retry 4xx."],
    ["Build URIs with `uriBuilder`, never string concatenation.", "`toBodilessEntity()` still exposes headers and status.", "Retry loops must be bounded."],
    ["`@RestClientTest` provides a `MockRestServiceServer` bound to the auto-configured `RestClient.Builder`.", "Throw from `onStatus` to translate errors."],
    S)

topics = [
    T("OpenAPI and springdoc",
      "**OpenAPI** (formerly Swagger) is a language-neutral description of HTTP APIs. **springdoc-openapi** scans Spring MVC mappings at runtime and serves the document at `/v3/api-docs` (and Swagger UI at `/swagger-ui.html` with the `-ui` starter). Annotations from `io.swagger.v3.oas.annotations` (`@Operation`, `@ApiResponse`, `@Tag`, `@Schema`, `@Parameter`) enrich the generated spec; an `OpenAPI` bean sets global info.",
      "Clients, QA and other teams need an accurate contract. Generated docs stay in sync with code and can drive client generation (openapi-generator) and contract testing.",
      ["Documentation derived from code", "Interactive try-out UI", "Client SDK generation", "Standard format understood by gateways and tools"],
      ["Annotations clutter controllers", "Generated spec may expose internals if DTOs are careless", "UI should be disabled or protected in production"],
      "Handwritten API docs rot within weeks. Without documenting error responses (400/404/409) clients must guess; exposing Swagger UI on production without protection reveals the attack surface.",
      "```xml\n<dependency>\n  <groupId>org.springdoc</groupId>\n  <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>\n  <version>2.7.0</version>\n</dependency>\n```\n```java\n@Operation(summary = \"Find an item\")\n@ApiResponse(responseCode = \"404\", description = \"Item not found\")\n@GetMapping(\"/{id}\") ResponseEntity<Item> get(@PathVariable long id)\n```\nProperties: `springdoc.api-docs.path`, `springdoc.swagger-ui.enabled=false`.",
      [("Global info", "java", "@Bean OpenAPI api() { return new OpenAPI().info(new Info().title(\"Items API\").version(\"1.0.0\")); }"),
       ("Field docs", "java", "record Item(@Schema(description = \"Display name\", example = \"Laptop\") String name) {}"),
       ("Hide an endpoint", "java", "@Operation(hidden = true)")],
      [("Where is the spec served by default?", "`/v3/api-docs` (JSON), UI at `/swagger-ui.html`."),
       ("Why document error responses?", "They are part of the contract; clients must handle them."),
       ("Should Swagger UI run in production?", "Usually disabled or protected.")]),
    T("RestClient: calling other services",
      "`RestClient` (Spring 6.1+) is the modern synchronous fluent HTTP client: `client.get().uri(...).retrieve().body(Type.class)`. It replaces most `RestTemplate` usage and shares message converters with MVC. Handle errors with `onStatus`, read generic types with `ParameterizedTypeReference`, access headers via `toEntity`/`toBodilessEntity`. `WebClient` remains the choice for reactive code.",
      "Microservices call each other and third-party APIs. A fluent client with clear error handling, timeouts and testability avoids ad-hoc `HttpURLConnection` code.",
      ["Fluent, readable API", "Pluggable request factory (timeouts, pooling)", "Easy testing with MockRestServiceServer", "Same JSON conversion as controllers"],
      ["Blocking: threads wait for the network (fine with virtual threads, Day 42)", "Default error handling throws exceptions for 4xx/5xx", "No built-in retry/circuit breaker (add Resilience4j or manual logic)"],
      "Calling remote services without timeouts hangs threads when the remote is slow. Swallowing errors hides outages; propagating raw `HttpServerErrorException` leaks infrastructure details into your own API.",
      "```java\nRestClient client = builder.baseUrl(\"https://api.example.com\").defaultHeader(\"X-Api-Key\", key).build();\nQuote q = client.get().uri(\"/quotes/{id}\", id).retrieve()\n    .onStatus(HttpStatusCode::is5xxServerError, (req, res) -> { throw new UpstreamException(...); })\n    .body(Quote.class);\nList<Quote> all = client.get().uri(\"/quotes\").retrieve().body(new ParameterizedTypeReference<>() {});\n```\nTimeouts: configure the `ClientHttpRequestFactory` (`spring.http.client.connect-timeout` / `read-timeout` in Boot 3.4).",
      [("POST JSON", "java", "client.post().uri(\"/quotes\").contentType(APPLICATION_JSON).body(Map.of(\"text\", t)).retrieve().body(Quote.class);"),
       ("Headers only", "java", "String etag = client.get().uri(\"/q/1\").retrieve().toBodilessEntity().getHeaders().getETag();"),
       ("Test without network", "java", "MockRestServiceServer server = MockRestServiceServer.bindTo(builder).build();")],
      [("RestClient vs RestTemplate?", "RestClient is the newer fluent API; RestTemplate is in maintenance mode."),
       ("How do you test a RestClient?", "`MockRestServiceServer` bound to the builder, or `@RestClientTest`."),
       ("Why set timeouts?", "To avoid thread starvation when a dependency is slow.")]),
    T("CORS: cross-origin resource sharing",
      "Browsers block JavaScript on origin A from reading responses of origin B unless B opts in with CORS headers (`Access-Control-Allow-Origin`, `-Methods`, `-Headers`, `-Credentials`, `-Max-Age`). Non-simple requests are preceded by a **preflight** `OPTIONS` request. In Spring: `@CrossOrigin` per controller/method, or a global `WebMvcConfigurer.addCorsMappings`. With Spring Security you must enable CORS in the security filter chain as well (Day 37).",
      "SPAs on `https://app.example.com` call APIs on `https://api.example.com`. Without correct CORS the browser refuses, even though the server answered.",
      ["Fine-grained, declarative policy", "Preflight cached via max-age", "Centralized config avoids drift"],
      ["Only a browser protection - not authentication or CSRF defense", "Misconfiguration (`*` with credentials) is a security hole", "Hard to debug: failures appear in the browser console"],
      "Allowing every origin together with cookies/credentials lets any website act on behalf of your users. Missing CORS config shows up as opaque browser errors while curl works fine.",
      "```java\n@Configuration\nclass CorsConfig implements WebMvcConfigurer {\n  public void addCorsMappings(CorsRegistry r) {\n    r.addMapping(\"/api/**\").allowedOrigins(\"https://app.example.com\")\n     .allowedMethods(\"GET\",\"POST\",\"PUT\",\"DELETE\").allowedHeaders(\"*\")\n     .allowCredentials(true).maxAge(3600);\n  }\n}\n```\n`allowedOriginPatterns(\"https://*.example.com\")` for wildcards with credentials.",
      [("Per endpoint", "java", "@CrossOrigin(origins = \"https://app.example.com\")\n@GetMapping(\"/api/data\") ..."),
       ("Preflight request", "text", "OPTIONS /api/data\nOrigin: https://app.example.com\nAccess-Control-Request-Method: POST"),
       ("Test", "java", "mvc.perform(options(\"/api/data\").header(\"Origin\", o).header(\"Access-Control-Request-Method\", \"POST\")).andExpect(status().isOk());")],
      [("What is a preflight request?", "An OPTIONS request the browser sends to ask whether the real cross-origin request is allowed."),
       ("Is CORS a security feature for the server?", "No, it protects browsers/users; servers must still authenticate and authorize."),
       ("Can `*` be used with credentials?", "No; list explicit origins or patterns.")]),
]

day(36, "OpenAPI, RestClient and CORS", "Spring Boot",
    "Documenting, consuming and exposing HTTP APIs safely to browsers and other services",
    ["Generate OpenAPI documents with springdoc and enrich them", "Call remote services with RestClient and handle failures", "Test HTTP clients with MockRestServiceServer", "Configure and verify CORS policies"],
    ["Day 30-31 REST", "Day 35 transactions (for context)"],
    topics, [a1, a2, a3, a4],
    [("How do you document a Spring REST API?", "springdoc-openapi plus OpenAPI annotations."),
     ("RestClient vs WebClient?", "RestClient is synchronous/fluent; WebClient is reactive."),
     ("What triggers a CORS preflight?", "Non-simple methods/headers (PUT, DELETE, custom headers, JSON content type)."),
     ("How to test code that calls external HTTP?", "MockRestServiceServer / WireMock, never the real network."),
     ("Why not allowedOrigins(\"*\") with credentials?", "Browsers reject it and it would be unsafe.")],
    ["Exposing Swagger UI in production unprotected.", "No timeouts on outbound calls.", "Believing CORS protects the API.", "Retrying non-idempotent requests blindly."],
    ["springdoc-openapi documentation", "Spring Framework Reference: RestClient, CORS"],
    [("OpenAPI", "Standard API description format"), ("Preflight", "OPTIONS check before a cross-origin request"), ("RestClient", "Fluent synchronous HTTP client"),
     ("MockRestServiceServer", "Fake HTTP server for tests"), ("Origin", "Scheme + host + port")],
    "2–3 h theory + 3–5 h tasks", spring=True)
