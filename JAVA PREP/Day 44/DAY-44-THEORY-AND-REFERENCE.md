# Day 44 — API Gateway, Filters, and Configuration Across Services

**Phase:** Microservices  
**Primary theme:** Routes, predicates and filters at the edge; authentication and rate limiting; configuration sharing across services  
**Estimated study time:** 2-3 h theory + 4-6 h tasks  
**Related tasks:** `task-01-route-matching`, `task-02-filter-chain`, `task-03-header-and-rewrite-filters`, `task-04-gateway-auth-rate-limit-challenge`  
**Instruction alignment:** Maps to Day 44 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, H2 2.3.232 (PostgreSQL mode)

## Overview

Routes, predicates and filters at the edge; authentication and rate limiting; configuration sharing across services. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. API gateway pattern and Spring Cloud Gateway concepts
2. Filter chains, ordering, and short-circuiting
3. Edge authentication, rate limiting, and configuration across services
4. Interview corner, common mistakes, glossary

## Subtopics

### API gateway pattern and Spring Cloud Gateway concepts

#### What it is

An **API gateway** is the single entry point for clients: it routes requests to services, and applies cross-cutting concerns (authentication, rate limiting, header manipulation, logging, CORS). Spring Cloud Gateway models this with **routes** (id, URI, predicates, filters), **predicates** (match path/method/header) and **filters** (pre/post processing).

#### Why it exists / why it matters

Without a gateway every client must know every service's address and each service re-implements auth and throttling. The gateway centralizes edge concerns and hides internal topology.

#### Pros and cons

**Pros**

- One public address, many private services
- Central auth, throttling, observability
- Request/response transformation
- Canary/blue-green routing

**Cons / trade-offs**

- Another hop (latency) and component to run
- Single point of failure if not scaled
- Risk of putting business logic in the gateway

#### What happens without it / when misused

Without it, clients call services directly: CORS, TLS, auth and rate limiting get duplicated and every internal refactor breaks clients.

#### Syntax and rules

Spring Cloud Gateway route in YAML:
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: users
          uri: http://localhost:8081
          predicates:
            - Path=/api/users/**
          filters:
            - StripPrefix=1
            - AddRequestHeader=X-Source, gateway
```
**Course decision:** Spring Cloud Gateway is reactive (WebFlux) and its release train (2024.0.x for Boot 3.4) must be matched to the Boot version. To keep the labs dependency-light and Boot-version-proof, the tasks **simulate** routes, predicates and the filter chain in plain Java. Project 03 (PeopleHub) uses the real `spring-cloud-starter-gateway` with the Spring Cloud BOM.

#### Examples

**Example 1 — Predicates**

```yaml
predicates:
  - Path=/api/orders/**
  - Method=GET,POST
  - Header=X-Tenant, \d+
```

**Example 2 — Custom filter (real Gateway)**

```java
@Component
class LogFilter implements GlobalFilter {
  public Mono<Void> filter(ServerWebExchange ex, GatewayFilterChain chain) {
    return chain.filter(ex).then(Mono.fromRunnable(() -> log.info("done")));
  }
}
```

#### Quick checks

1. Why not put business logic in the gateway?
2. What are predicates?

### Filter chains, ordering, and short-circuiting

#### What it is

A filter chain is an ordered list of filters; each receives the request and a `next` handle. Code before `next` is the **pre** phase, code after is the **post** phase. A filter that does not call `next` **short-circuits** (e.g. 401).

#### Why it exists / why it matters

Order decides behavior: authenticate before rate-limiting (so anonymous traffic cannot burn a user's quota), log outermost, add headers before the proxy call.

#### Pros and cons

**Pros**

- Composable, reusable cross-cutting logic
- Easy to unit test in isolation
- Same pattern as servlet filters and Spring Security

**Cons / trade-offs**

- Order bugs are subtle
- Too many filters add latency
- Debugging requires understanding the chain

#### What happens without it / when misused

A wrong order (rate limit before auth) lets attackers exhaust other users' quotas; forgetting to call `next` silently drops requests.

#### Syntax and rules

```java
Handler chain = FilterChain.build(List.of(auth, rateLimit, addHeaders), proxy);
```
Out path runs in reverse: `auth-pre, rate-pre, proxy, rate-post, auth-post`.

#### Examples

**Example 1 — Pre/post**

```java
(req, next) -> { log("pre"); var r = next.handle(req); log("post"); return r; }
```

#### Quick checks

1. Which runs last on the way out: first or last filter?
2. How does a filter reject a request?

### Edge authentication, rate limiting, and configuration across services

#### What it is

Edge concerns: validate credentials/JWT once at the gateway and forward identity headers; limit request rates (fixed window, sliding window, token bucket); and share configuration across services via externalized properties (Spring Cloud Config concept: one config repository, per-service and per-profile files).

#### Why it exists / why it matters

Central enforcement avoids inconsistent security. Configuration drift between services is a classic outage cause.

#### Pros and cons

**Pros**

- Consistent security at the perimeter
- Protects services from abuse
- One place to change shared settings

**Cons / trade-offs**

- Gateway must be trusted by services (network policy, mTLS or signed headers)
- Rate-limit state needs a shared store when scaled out (Redis)
- Config server is another moving part

#### What happens without it / when misused

If services trust an `X-User` header but are reachable directly, anyone can forge it. In-memory rate limits per gateway instance multiply the effective limit when you scale out.

#### Syntax and rules

Config layering (local files in this course): `application.yml` (shared) < `application-{profile}.yml` < environment variables. Config Server is covered conceptually: clients use `spring.config.import=configserver:http://host:8888`.

#### Examples

**Example 1 — Token bucket idea**

```text
bucket(capacity=10, refill=5/s): request takes 1 token; empty -> 429
```

**Example 2 — Shared + service-specific props**

```yaml
# application.yml (shared)
management.endpoints.web.exposure.include: health,info
# application-order.yml
server.port: 8082
```

#### Quick checks

1. Why is in-memory rate limiting insufficient at scale?
2. Why authenticate before rate limiting?

## Interview corner

**Q1. What is an API gateway?**

A single entry point that routes requests and applies cross-cutting concerns.

**Q2. Gateway vs load balancer?**

A load balancer spreads traffic across instances; a gateway understands HTTP semantics (routes, auth, transforms).

**Q3. How do services trust the gateway?**

Network isolation, mTLS, or verifying signed tokens in each service (zero trust).

**Q4. Where do you rate limit?**

At the gateway (coarse) and optionally in services for expensive operations.

**Q5. What is the Config Server pattern?**

A central service serving per-application, per-profile properties from a git repository.

## Common mistakes & debugging

- Wrong filter order.
- Forgetting to call `next`.
- Trusting identity headers from the public internet.
- Matching prefixes without segment boundaries.

## Further reading

- Spring Cloud Gateway Reference
- Spring Cloud release train compatibility matrix
- Spring Cloud Config reference

## Glossary

| Term | Meaning |
|------|---------|
| Route | id + target URI + predicates + filters |
| Predicate | Match condition |
| Filter | Pre/post processing step |
| Short-circuit | Responding without calling the next handler |
| Token bucket | Rate-limit algorithm with refilling tokens |
| Config Server | Central externalized configuration service |

## Answers

### API gateway pattern and Spring Cloud Gateway concepts

1. It becomes a bottleneck and a monolith at the edge; keep it to cross-cutting concerns.
2. Conditions that decide whether a route applies to a request.

### Filter chains, ordering, and short-circuiting

1. The first filter (outermost) runs its post phase last.
2. It returns a response without calling `next`.

### Edge authentication, rate limiting, and configuration across services

1. Each instance counts separately; use a shared store such as Redis.
2. So unauthenticated traffic cannot consume an authenticated client's quota.
