# Day 30 — REST I: Controllers, Mappings, Request Binding, ResponseEntity and Jackson

**Phase:** Spring Boot  
**Primary theme:** Building HTTP APIs with Spring MVC: mappings, request binding, status codes and JSON shaping  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-greeting-endpoints`, `task-02-books-response-entity`, `task-03-jackson-event-contract`, `task-04-notes-search-and-update`  
**Instruction alignment:** Maps to Day 30 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Building HTTP APIs with Spring MVC: mappings, request binding, status codes and JSON shaping. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. @RestController, request mappings and the DispatcherServlet
2. Path variables, query parameters, request bodies and headers
3. ResponseEntity, status codes and Jackson
4. Interview corner, common mistakes, glossary

## Subtopics

### @RestController, request mappings and the DispatcherServlet

#### What it is

A `@RestController` is a `@Controller` whose return values are written straight to the HTTP response body via `HttpMessageConverter`s (JSON through Jackson). `@RequestMapping` and the shortcuts `@GetMapping`, `@PostMapping`, `@PutMapping`, `@PatchMapping`, `@DeleteMapping` bind HTTP method + path to a Java method. Every request enters the `DispatcherServlet`, which finds a handler through `HandlerMapping`, resolves arguments, invokes the method and converts the result.

#### Why it exists / why it matters

REST APIs are how browsers, mobile apps and other services talk to your backend. A consistent mapping model lets you express resources (`/api/books/{id}`) and verbs declaratively instead of parsing servlet requests yourself.

#### Pros and cons

**Pros**

- Declarative routing with annotations
- Automatic argument binding and conversion
- Pluggable message converters (JSON, XML, text)
- Same model for MVC and testing (MockMvc)

**Cons / trade-offs**

- Annotation-heavy code can hide the request flow
- Ambiguous mappings fail at startup
- Content negotiation rules are subtle

#### What happens without it / when misused

With `@Controller` instead of `@RestController`, a returned String is interpreted as a view name and you get a 404 or template error. Two methods mapping to the same method+path throw `IllegalStateException: Ambiguous mapping` at startup.

#### Syntax and rules

```java
@RestController
@RequestMapping("/api/books")
class BookController {
  @GetMapping("/{id}") Book get(@PathVariable long id) {...}
  @PostMapping(consumes = "application/json") ... 
}
```
Class-level `@RequestMapping` prefixes every method path. `produces`/`consumes` narrow by media type. `@RequestMapping(method = GET)` is the long form of `@GetMapping`.

#### Examples

**Example 1 — Minimal controller**

```java
@RestController
class HelloController {
    @GetMapping("/hello")
    String hello() { return "hi"; }
}
```

**Example 2 — Class + method paths**

```java
@RestController
@RequestMapping("/api/v1/orders")
class OrderController {
    @GetMapping("/{id}/items") List<Item> items(@PathVariable long id) {...}
}
```

**Example 3 — Narrowing by media type**

```java
@PostMapping(path = "/import", consumes = "text/csv", produces = "application/json")
ImportResult importCsv(@RequestBody String csv) {...}
```

#### Quick checks

1. What does @RestController add over @Controller?
2. Which component picks the handler method?
3. What happens with two identical mappings?

### Path variables, query parameters, request bodies and headers

#### What it is

`@PathVariable` binds URI template segments, `@RequestParam` binds query/form parameters (with `required` and `defaultValue`), `@RequestBody` deserializes the body, `@RequestHeader` reads headers. Spring converts strings to `int`, `UUID`, enums, dates and so on using the `ConversionService`; failures produce HTTP 400.

#### Why it exists / why it matters

Clients express intent in different places: identity in the path, filters in the query, payload in the body, metadata in headers. Using each place correctly keeps APIs cacheable, predictable and easy to document.

#### Pros and cons

**Pros**

- Strong typing of inputs
- Defaults and optional parameters are one attribute away
- Automatic 400 on malformed input
- Works with records as request bodies

**Cons / trade-offs**

- Binding errors give generic messages unless handled (Day 31)
- Too many query parameters become unreadable (use a DTO with `@ModelAttribute`)
- Large bodies need limits

#### What happens without it / when misused

Reading an id from the query when it identifies a resource breaks caching and REST semantics. A missing required `@RequestParam` returns 400 `MissingServletRequestParameterException`. A `@RequestBody` with the wrong `Content-Type` yields 415.

#### Syntax and rules

```java
@GetMapping("/{id}") Book get(@PathVariable long id)
@GetMapping List<Book> list(@RequestParam(defaultValue = "0") int page, @RequestParam(required = false) String q)
@PostMapping Book create(@RequestBody CreateBookRequest r)
@GetMapping Foo h(@RequestHeader("X-Trace-Id") String id)
```
Name is inferred from the parameter name when compiled with `-parameters` (Boot's parent enables it).

#### Examples

**Example 1 — Optional filter**

```java
@GetMapping
List<Note> search(@RequestParam(required = false) String contains) {...}
```

**Example 2 — Body as record**

```java
record CreateBookRequest(String title, String author) {}
@PostMapping Book create(@RequestBody CreateBookRequest r) {...}
```

**Example 3 — Multiple variables**

```java
@GetMapping("/{orderId}/lines/{lineNo}")
Line line(@PathVariable long orderId, @PathVariable int lineNo) {...}
```

#### Quick checks

1. Path variable or query parameter for an entity id?
2. What status results from `?times=abc` for an int parameter?
3. How do you make a query parameter optional?

### ResponseEntity, status codes and Jackson

#### What it is

`ResponseEntity<T>` lets a method choose status, headers and body explicitly (`created(uri)`, `noContent()`, `notFound()`, `ok().header(..)`). `@ResponseStatus` fixes a status declaratively. Jackson converts objects to JSON; annotations (`@JsonProperty`, `@JsonIgnore`, `@JsonFormat`, `@JsonInclude`) and `spring.jackson.*` properties shape the contract.

#### Why it exists / why it matters

Status codes are part of the API contract: 201 + `Location` tells clients where the new resource lives, 204 says there is no body, 404/409/422 describe failures. Jackson settings decide what is exposed and how dates and numbers look.

#### Pros and cons

**Pros**

- Full control of the HTTP response
- Standards-compliant semantics (RFC 9110)
- Boot auto-configures a sane ObjectMapper
- Contract evolution via annotations without changing domain logic

**Cons / trade-offs**

- `ResponseEntity<?>` loses type information in signatures
- Leaking entities directly couples JSON to the database (use DTOs, Day 31)
- Jackson defaults (unknown properties) differ between plain Jackson and Boot

#### What happens without it / when misused

Returning 200 with `{"error": ...}` for failures breaks clients and monitoring. Serializing a JPA entity with lazy associations can throw or leak data. Without `@JsonIgnore` on secrets they end up in responses.

#### Syntax and rules

```java
return ResponseEntity.created(URI.create("/api/books/" + id)).body(book);   // 201
return ResponseEntity.noContent().build();                                  // 204
return ResponseEntity.notFound().build();                                   // 404
```
```yaml
spring.jackson.default-property-inclusion: non_null
spring.jackson.serialization.write-dates-as-timestamps: false
```

#### Examples

**Example 1 — Create with Location**

```java
return ResponseEntity.created(URI.create("/api/books/" + b.id())).body(b);
```

**Example 2 — Header + body**

```java
return ResponseEntity.ok().header("X-Total-Count", "42").body(items);
```

**Example 3 — Jackson annotations**

```java
record User(@JsonProperty("user_name") String name, @JsonIgnore String passwordHash) {}
```

#### Quick checks

1. Which status should POST create return?
2. When use 204?
3. Why avoid returning entities directly?

## Interview corner

**Q1. What is the difference between @Controller and @RestController?**

`@RestController` adds `@ResponseBody`, so return values are written to the response body.

**Q2. How does Spring MVC pick a handler?**

DispatcherServlet asks HandlerMappings; the matching HandlerMethod is invoked through a HandlerAdapter.

**Q3. PUT vs PATCH vs POST?**

POST creates/acts, PUT replaces idempotently, PATCH partially updates.

**Q4. What does @RequestBody do?**

Reads the body and converts it with an HttpMessageConverter (Jackson for JSON).

**Q5. How do you customize JSON output?**

Jackson annotations, `spring.jackson.*` properties or a Jackson2ObjectMapperBuilderCustomizer.

## Common mistakes & debugging

- Using @Controller and getting view resolution errors.
- Returning 200 for errors.
- Forgetting `Content-Type: application/json` on requests (415).
- Mapping ids in query strings instead of paths.

## Further reading

- Spring Framework Reference: Web MVC annotated controllers
- Jackson annotations wiki
- RFC 9110 HTTP Semantics

## Glossary

| Term | Meaning |
|------|---------|
| DispatcherServlet | Front controller of Spring MVC |
| HttpMessageConverter | Converts bodies to/from Java objects |
| ResponseEntity | Status + headers + body wrapper |
| Location header | URL of a newly created resource |
| MockMvc | Servlet-free MVC test client |

## Answers

### @RestController, request mappings and the DispatcherServlet

1. `@ResponseBody` on every method, so return values are serialized to the body instead of resolved as views.
2. `HandlerMapping` inside the `DispatcherServlet`.
3. Startup fails with an ambiguous mapping error.

### Path variables, query parameters, request bodies and headers

1. Path variable; it identifies the resource.
2. 400 Bad Request (type mismatch).
3. `required = false` or `defaultValue`.

### ResponseEntity, status codes and Jackson

1. 201 Created with a Location header.
2. Successful request with no response body (e.g. DELETE).
3. It couples the API to the persistence model and can leak fields or trigger lazy loading.
