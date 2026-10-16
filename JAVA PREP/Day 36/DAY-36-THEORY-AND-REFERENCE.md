# Day 36 — OpenAPI, RestClient and CORS

**Phase:** Spring Boot  
**Primary theme:** Documenting, consuming and exposing HTTP APIs safely to browsers and other services  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-springdoc-openapi-docs`, `task-02-rest-client-basics`, `task-03-cors-policy`, `task-04-quote-gateway-challenge`  
**Instruction alignment:** Maps to Day 36 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Documenting, consuming and exposing HTTP APIs safely to browsers and other services. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. OpenAPI and springdoc
2. RestClient: calling other services
3. CORS: cross-origin resource sharing
4. Interview corner, common mistakes, glossary

## Subtopics

### OpenAPI and springdoc

#### What it is

**OpenAPI** (formerly Swagger) is a language-neutral description of HTTP APIs. **springdoc-openapi** scans Spring MVC mappings at runtime and serves the document at `/v3/api-docs` (and Swagger UI at `/swagger-ui.html` with the `-ui` starter). Annotations from `io.swagger.v3.oas.annotations` (`@Operation`, `@ApiResponse`, `@Tag`, `@Schema`, `@Parameter`) enrich the generated spec; an `OpenAPI` bean sets global info.

#### Why it exists / why it matters

Clients, QA and other teams need an accurate contract. Generated docs stay in sync with code and can drive client generation (openapi-generator) and contract testing.

#### Pros and cons

**Pros**

- Documentation derived from code
- Interactive try-out UI
- Client SDK generation
- Standard format understood by gateways and tools

**Cons / trade-offs**

- Annotations clutter controllers
- Generated spec may expose internals if DTOs are careless
- UI should be disabled or protected in production

#### What happens without it / when misused

Handwritten API docs rot within weeks. Without documenting error responses (400/404/409) clients must guess; exposing Swagger UI on production without protection reveals the attack surface.

#### Syntax and rules

```xml
<dependency>
  <groupId>org.springdoc</groupId>
  <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
  <version>2.7.0</version>
</dependency>
```
```java
@Operation(summary = "Find an item")
@ApiResponse(responseCode = "404", description = "Item not found")
@GetMapping("/{id}") ResponseEntity<Item> get(@PathVariable long id)
```
Properties: `springdoc.api-docs.path`, `springdoc.swagger-ui.enabled=false`.

#### Examples

**Example 1 — Global info**

```java
@Bean OpenAPI api() { return new OpenAPI().info(new Info().title("Items API").version("1.0.0")); }
```

**Example 2 — Field docs**

```java
record Item(@Schema(description = "Display name", example = "Laptop") String name) {}
```

**Example 3 — Hide an endpoint**

```java
@Operation(hidden = true)
```

#### Quick checks

1. Where is the spec served by default?
2. Why document error responses?
3. Should Swagger UI run in production?

### RestClient: calling other services

#### What it is

`RestClient` (Spring 6.1+) is the modern synchronous fluent HTTP client: `client.get().uri(...).retrieve().body(Type.class)`. It replaces most `RestTemplate` usage and shares message converters with MVC. Handle errors with `onStatus`, read generic types with `ParameterizedTypeReference`, access headers via `toEntity`/`toBodilessEntity`. `WebClient` remains the choice for reactive code.

#### Why it exists / why it matters

Microservices call each other and third-party APIs. A fluent client with clear error handling, timeouts and testability avoids ad-hoc `HttpURLConnection` code.

#### Pros and cons

**Pros**

- Fluent, readable API
- Pluggable request factory (timeouts, pooling)
- Easy testing with MockRestServiceServer
- Same JSON conversion as controllers

**Cons / trade-offs**

- Blocking: threads wait for the network (fine with virtual threads, Day 42)
- Default error handling throws exceptions for 4xx/5xx
- No built-in retry/circuit breaker (add Resilience4j or manual logic)

#### What happens without it / when misused

Calling remote services without timeouts hangs threads when the remote is slow. Swallowing errors hides outages; propagating raw `HttpServerErrorException` leaks infrastructure details into your own API.

#### Syntax and rules

```java
RestClient client = builder.baseUrl("https://api.example.com").defaultHeader("X-Api-Key", key).build();
Quote q = client.get().uri("/quotes/{id}", id).retrieve()
    .onStatus(HttpStatusCode::is5xxServerError, (req, res) -> { throw new UpstreamException(...); })
    .body(Quote.class);
List<Quote> all = client.get().uri("/quotes").retrieve().body(new ParameterizedTypeReference<>() {});
```
Timeouts: configure the `ClientHttpRequestFactory` (`spring.http.client.connect-timeout` / `read-timeout` in Boot 3.4).

#### Examples

**Example 1 — POST JSON**

```java
client.post().uri("/quotes").contentType(APPLICATION_JSON).body(Map.of("text", t)).retrieve().body(Quote.class);
```

**Example 2 — Headers only**

```java
String etag = client.get().uri("/q/1").retrieve().toBodilessEntity().getHeaders().getETag();
```

**Example 3 — Test without network**

```java
MockRestServiceServer server = MockRestServiceServer.bindTo(builder).build();
```

#### Quick checks

1. RestClient vs RestTemplate?
2. How do you test a RestClient?
3. Why set timeouts?

### CORS: cross-origin resource sharing

#### What it is

Browsers block JavaScript on origin A from reading responses of origin B unless B opts in with CORS headers (`Access-Control-Allow-Origin`, `-Methods`, `-Headers`, `-Credentials`, `-Max-Age`). Non-simple requests are preceded by a **preflight** `OPTIONS` request. In Spring: `@CrossOrigin` per controller/method, or a global `WebMvcConfigurer.addCorsMappings`. With Spring Security you must enable CORS in the security filter chain as well (Day 37).

#### Why it exists / why it matters

SPAs on `https://app.example.com` call APIs on `https://api.example.com`. Without correct CORS the browser refuses, even though the server answered.

#### Pros and cons

**Pros**

- Fine-grained, declarative policy
- Preflight cached via max-age
- Centralized config avoids drift

**Cons / trade-offs**

- Only a browser protection - not authentication or CSRF defense
- Misconfiguration (`*` with credentials) is a security hole
- Hard to debug: failures appear in the browser console

#### What happens without it / when misused

Allowing every origin together with cookies/credentials lets any website act on behalf of your users. Missing CORS config shows up as opaque browser errors while curl works fine.

#### Syntax and rules

```java
@Configuration
class CorsConfig implements WebMvcConfigurer {
  public void addCorsMappings(CorsRegistry r) {
    r.addMapping("/api/**").allowedOrigins("https://app.example.com")
     .allowedMethods("GET","POST","PUT","DELETE").allowedHeaders("*")
     .allowCredentials(true).maxAge(3600);
  }
}
```
`allowedOriginPatterns("https://*.example.com")` for wildcards with credentials.

#### Examples

**Example 1 — Per endpoint**

```java
@CrossOrigin(origins = "https://app.example.com")
@GetMapping("/api/data") ...
```

**Example 2 — Preflight request**

```text
OPTIONS /api/data
Origin: https://app.example.com
Access-Control-Request-Method: POST
```

**Example 3 — Test**

```java
mvc.perform(options("/api/data").header("Origin", o).header("Access-Control-Request-Method", "POST")).andExpect(status().isOk());
```

#### Quick checks

1. What is a preflight request?
2. Is CORS a security feature for the server?
3. Can `*` be used with credentials?

## Interview corner

**Q1. How do you document a Spring REST API?**

springdoc-openapi plus OpenAPI annotations.

**Q2. RestClient vs WebClient?**

RestClient is synchronous/fluent; WebClient is reactive.

**Q3. What triggers a CORS preflight?**

Non-simple methods/headers (PUT, DELETE, custom headers, JSON content type).

**Q4. How to test code that calls external HTTP?**

MockRestServiceServer / WireMock, never the real network.

**Q5. Why not allowedOrigins("*") with credentials?**

Browsers reject it and it would be unsafe.

## Common mistakes & debugging

- Exposing Swagger UI in production unprotected.
- No timeouts on outbound calls.
- Believing CORS protects the API.
- Retrying non-idempotent requests blindly.

## Further reading

- springdoc-openapi documentation
- Spring Framework Reference: RestClient, CORS

## Glossary

| Term | Meaning |
|------|---------|
| OpenAPI | Standard API description format |
| Preflight | OPTIONS check before a cross-origin request |
| RestClient | Fluent synchronous HTTP client |
| MockRestServiceServer | Fake HTTP server for tests |
| Origin | Scheme + host + port |

## Answers

### OpenAPI and springdoc

1. `/v3/api-docs` (JSON), UI at `/swagger-ui.html`.
2. They are part of the contract; clients must handle them.
3. Usually disabled or protected.

### RestClient: calling other services

1. RestClient is the newer fluent API; RestTemplate is in maintenance mode.
2. `MockRestServiceServer` bound to the builder, or `@RestClientTest`.
3. To avoid thread starvation when a dependency is slow.

### CORS: cross-origin resource sharing

1. An OPTIONS request the browser sends to ask whether the real cross-origin request is allowed.
2. No, it protects browsers/users; servers must still authenticate and authorize.
3. No; list explicit origins or patterns.
