# Day 39 — Spring Testing: Slices, Mockito, and Security Tests

**Phase:** Spring Boot  
**Primary theme:** Fast, layered tests for controllers, repositories, services, and secured endpoints  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-webmvc-slice-test`, `task-02-datajpa-slice`, `task-03-mockbean-service`, `task-04-security-test-util`  
**Instruction alignment:** Maps to Day 39 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Fast, layered tests for controllers, repositories, services, and secured endpoints. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. The test pyramid in Spring Boot
2. @WebMvcTest and MockMvc
3. @DataJpaTest and repository testing
4. Mockito essentials with Spring
5. spring-security-test utilities
6. Interview corner, common mistakes, glossary

## Subtopics

### The test pyramid in Spring Boot

#### What it is

Fast, focused tests at the bottom (plain JUnit on POJOs), **slice tests** in the middle (`@WebMvcTest`, `@DataJpaTest`, `@JsonTest`, `@RestClientTest`) loading only one layer, and a few full `@SpringBootTest` integration tests at the top. Slices use *test auto-configuration* so only relevant beans start.

#### Why it exists / why it matters

Full-context tests take seconds each; a suite of hundreds becomes unusable. Slices give layer-specific confidence in milliseconds.

#### Pros and cons

**Pros**

- Fast feedback
- Failures point to one layer
- Less accidental coupling
- Context caching reuses slices with identical configuration

**Cons / trade-offs**

- Slices don't prove wiring between layers
- Each distinct mock set creates a new cached context
- Easy to over-mock

#### What happens without it / when misused

Everything as `@SpringBootTest`: slow CI, flaky ports/databases, and failures that don't say which layer broke.

#### Syntax and rules

```java
@WebMvcTest(BookController.class)  class BookControllerSliceTest { @Autowired MockMvc mvc; @MockitoBean BookService service; }
@DataJpaTest                      class ProductRepositoryTest { @Autowired TestEntityManager em; }
@SpringBootTest                   class ApplicationIT { /* few, critical journeys */ }
```

#### Examples

**Example 1 — JSON slice**

```java
@JsonTest class EventJsonTest { @Autowired JacksonTester<Event> json; }
```

**Example 2 — Rule of thumb**

```text
Many unit tests, some slices, few integration tests
```

**Example 3 — Context caching**

```text
Same annotations + same @MockitoBean set => context reused across classes
```

#### Quick checks

1. What does @WebMvcTest load?
2. Why slices?
3. What is context caching?

### @WebMvcTest and MockMvc

#### What it is

`@WebMvcTest` starts the Spring MVC infrastructure without a server. `MockMvc` performs requests through the full DispatcherServlet pipeline (mapping, binding, validation, advice, converters) and asserts on status, headers and JSON paths. Collaborators are replaced with `@MockitoBean` (Boot 3.4+/Spring 6.2; formerly `@MockBean`).

#### Why it exists / why it matters

Controller behaviour — status codes, validation errors, serialization — is where most HTTP contract bugs live.

#### Pros and cons

**Pros**

- No port, no server, milliseconds per test
- Full MVC behaviour including content negotiation
- jsonPath assertions

**Cons / trade-offs**

- Doesn't test servlet container behaviour
- Needs explicit imports for security/config classes
- Mocks can drift from real behaviour

#### What happens without it / when misused

Calling controller methods directly in unit tests misses annotations, binding and advice, so a missing `@RequestBody` passes tests but fails in production.

#### Syntax and rules

```java
given(service.find(1)).willReturn(Optional.of(book));
mvc.perform(get("/books/1")).andExpect(status().isOk()).andExpect(jsonPath("$.title").value("Dune"));
verify(service).find(1);
```

#### Examples

**Example 1 — Import config**

```java
@WebMvcTest(Ctl.class) @Import(SecurityConfig.class)
```

**Example 2 — Send JSON**

```java
post("/x").contentType(APPLICATION_JSON).content("{...}")
```

**Example 3 — Print on failure**

```java
mvc.perform(...).andDo(print())
```

#### Quick checks

1. MockMvc vs TestRestTemplate?
2. Replacement for @MockBean?
3. How to include a @Configuration in a slice?

### @DataJpaTest and repository testing

#### What it is

`@DataJpaTest` configures entities, Spring Data repositories, an embedded database (H2) and `TestEntityManager`; each test is `@Transactional` and rolls back. Use `flush()` + `clear()` to force SQL and reload fresh instances. For production-like dialect behaviour use Testcontainers with `@AutoConfigureTestDatabase(replace = NONE)`.

#### Why it exists / why it matters

Derived query names and `@Query` strings are code that only fail at runtime. A repository slice catches typos immediately.

#### Pros and cons

**Pros**

- Fast, isolated DB tests
- Automatic rollback
- Validates mapping and queries

**Cons / trade-offs**

- H2 differs from production databases
- Rollback hides commit-time problems (constraints deferred, `@Transactional` boundaries)
- Forgetting flush/clear gives false positives from the first-level cache

#### What happens without it / when misused

Tests that only call `save()` and `findById()` inside one persistence context never hit the database and pass even with broken mappings.

#### Syntax and rules

```java
@DataJpaTest class ProductRepositoryTest {
  @Autowired TestEntityManager em; @Autowired ProductRepository repo;
  @Test void query() { em.persist(p); em.flush(); em.clear(); assertThat(repo.findByCategory("x")).hasSize(1); }
}
```

#### Examples

**Example 1 — Use real DB**

```java
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
```

**Example 2 — Show SQL**

```text
spring.jpa.show-sql=true or logging.level.org.hibernate.SQL=DEBUG
```

**Example 3 — Testcontainers**

```java
@ServiceConnection static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16");
```

#### Quick checks

1. Why flush and clear?
2. Does @DataJpaTest commit?
3. How to test against Postgres?

### Mockito essentials with Spring

#### What it is

Mockito creates test doubles: **mock** (programmable, records calls), **spy** (real object, partially stubbed), **captor** (captures arguments). Stub with `given(...).willReturn/willThrow`; verify with `verify(mock).method(...)`, `times`, `never`, `verifyNoInteractions`. `@MockitoBean` registers a mock in the Spring context (replacing any bean of that type); `@MockitoSpyBean` wraps the real bean.

#### Why it exists / why it matters

Services with collaborators (gateways, repositories) are tested for decisions and interactions without sending emails or touching a database.

#### Pros and cons

**Pros**

- Isolates the unit
- Simulates failures that are hard to trigger
- Verifies ordering and absence of calls

**Cons / trade-offs**

- Over-specified verification makes refactors painful
- Mocking types you don't own (JPA, HTTP clients) gives false confidence
- Context pollution: each unique mock combination creates a new context

#### What happens without it / when misused

Verifying every call of every collaborator couples tests to implementation; unstubbed mocks silently return null/false causing misleading passes.

#### Syntax and rules

```java
given(users.findEmail(1)).willReturn(Optional.of("a@x.io"));
given(gateway.send(anyString(), anyString())).willThrow(new GatewayException("down"));
verify(gateway, never()).send(anyString(), anyString());
ArgumentCaptor<String> c = ArgumentCaptor.forClass(String.class);
```

#### Examples

**Example 1 — Consecutive results**

```java
given(m.next()).willReturn(1, 2, 3);
```

**Example 2 — Spy**

```java
@MockitoSpyBean RealService service;
```

**Example 3 — No more interactions**

```java
verifyNoMoreInteractions(gateway);
```

#### Quick checks

1. Mock vs spy?
2. Why avoid mocking everything?
3. What does verifyNoInteractions assert?

### spring-security-test utilities

#### What it is

`spring-security-test` supplies `@WithMockUser`, `@WithUserDetails`, and MockMvc **request post-processors**: `user(..)`, `httpBasic(..)`, `csrf()`, `jwt()`. They set up an authenticated context without executing the login flow. With CSRF enabled, unsafe methods need `.with(csrf())`.

#### Why it exists / why it matters

Security rules need tests for each role and for anonymous access; ceremony must not drown the intent of the test.

#### Pros and cons

**Pros**

- Fast authorization tests
- No real login needed
- Wrap in helper methods for readability

**Cons / trade-offs**

- Fabricated principals bypass your `UserDetailsService`
- Easy to forget CSRF and chase confusing 403s
- Method security needs a full or partial context, not just a slice

#### What happens without it / when misused

Disabling security in tests (`addFilters = false`) removes exactly what you wanted to verify.

#### Syntax and rules

```java
mvc.perform(post("/notes").with(user("ann").roles("USER")).with(csrf())).andExpect(status().isCreated());
mvc.perform(get("/admin").with(httpBasic("ann", "pw")));
```

#### Examples

**Example 1 — Annotation style**

```java
@Test @WithMockUser(username = "ann", roles = "ADMIN") void admin() { ... }
```

**Example 2 — JWT resource server**

```java
mvc.perform(get("/api").with(jwt().authorities(new SimpleGrantedAuthority("SCOPE_read"))))
```

**Example 3 — Anti-pattern**

```java
@AutoConfigureMockMvc(addFilters = false) // removes security from the test
```

#### Quick checks

1. Why 403 on POST in tests?
2. @WithMockUser vs user() post-processor?
3. Why not addFilters=false?

## Interview corner

**Q1. What are slice tests?**

Tests loading only one layer's beans via test auto-configuration.

**Q2. @MockBean vs @MockitoBean?**

@MockitoBean is the Spring 6.2 / Boot 3.4 replacement.

**Q3. Why flush and clear in JPA tests?**

To hit the database rather than the first-level cache.

**Q4. When use @SpringBootTest?**

A few end-to-end wiring tests.

**Q5. How to test a secured endpoint?**

Use user()/httpBasic()/csrf() post-processors or @WithMockUser.

## Common mistakes & debugging

- Everything as @SpringBootTest.
- Mocking types you don't own.
- Not clearing the persistence context.
- Disabling security filters in tests.

## Further reading

- Spring Boot reference: Testing
- Mockito documentation
- Spring Security reference: Testing

## Glossary

| Term | Meaning |
|------|---------|
| Slice test | Test loading only one layer |
| MockMvc | Server-less MVC test harness |
| Mock | Programmable test double |
| Captor | Mockito argument capture |
| Post-processor | Customizes a MockMvc request |

## Answers

### The test pyramid in Spring Boot

1. Controllers, advice, converters, filters — not services/repositories.
2. Speed and focus.
3. Spring reuses an application context for tests with identical configuration.

### @WebMvcTest and MockMvc

1. MockMvc: no server, mock servlet; TestRestTemplate: real HTTP on a port.
2. @MockitoBean (Boot 3.4+).
3. @Import it.

### @DataJpaTest and repository testing

1. To force SQL and bypass the first-level cache.
2. No, it rolls back.
3. Testcontainers with @ServiceConnection.

### Mockito essentials with Spring

1. Mock replaces behaviour entirely; spy wraps a real object.
2. Tests become brittle and verify implementation not behaviour.
3. That the mock was never called.

### spring-security-test utilities

1. CSRF token missing.
2. Annotation sets context for the whole test; post-processor is per request.
3. It disables the security you are testing.
