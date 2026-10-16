# Day 38 — Spring Security II: JWT, 401 vs 403, Method Security

**Phase:** Spring Boot  
**Primary theme:** Stateless authentication with signed tokens and fine-grained method authorization  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-jwt-util-sign-verify`, `task-02-jwt-filter`, `task-03-status-401-vs-403`, `task-04-preauthorize-method`  
**Instruction alignment:** Maps to Day 38 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Stateless authentication with signed tokens and fine-grained method authorization. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. JWT anatomy and signing
2. JWT authentication filter
3. 401 Unauthorized vs 403 Forbidden
4. Method security with @PreAuthorize
5. Interview corner, common mistakes, glossary

## Subtopics

### JWT anatomy and signing

#### What it is

A **JSON Web Token** is `base64url(header).base64url(payload).base64url(signature)`. The payload carries *claims*: registered ones (`sub`, `iat`, `exp`, `iss`, `aud`) and custom ones (`roles`). With **HS256** the signature is an HMAC over header+payload using a shared secret of at least 256 bits. The token is *signed, not encrypted* — anyone can read the claims.

#### Why it exists / why it matters

Stateless authentication: the server needs no session store; any instance can verify a token with the key alone.

#### Pros and cons

**Pros**

- Horizontally scalable
- Self-contained identity and roles
- Works for mobile/SPA/service-to-service
- Standardized (RFC 7519)

**Cons / trade-offs**

- Cannot be revoked before expiry without extra state
- Large headers vs session ids
- Easy to misuse (weak secrets, `alg=none`, secrets in claims)

#### What happens without it / when misused

Short secrets are brute-forced offline; storing PII in claims leaks it to anyone holding the token; long-lived tokens remain valid after logout or role change.

#### Syntax and rules

```java
SecretKey key = Keys.hmacShaKeyFor(secret.getBytes(UTF_8)); // >= 32 bytes
String token = Jwts.builder().subject("ann").claim("roles", List.of("USER"))
    .issuedAt(now).expiration(now.plus(ttl)).signWith(key).compact();
Claims c = Jwts.parser().verifyWith(key).build().parseSignedClaims(token).getPayload();
```

#### Examples

**Example 1 — Inspect a token**

```text
echo <payload> | base64 -d   # claims are readable
```

**Example 2 — Typical claims**

```json
{ "sub": "ann", "roles": ["USER"], "iat": 1735689600, "exp": 1735691400 }
```

**Example 3 — Asymmetric option**

```text
RS256/ES256: private key signs, public key verifies (resource servers need only the public key)
```

#### Quick checks

1. Is a JWT encrypted?
2. What does exp do?
3. Minimum HS256 key size?

### JWT authentication filter

#### What it is

A custom `OncePerRequestFilter` reads the `Authorization: Bearer ...` header, validates the token, and places an `Authentication` into the `SecurityContextHolder`. It does *not* reject requests: if no authentication exists, the authorization filter later decides (401 for anonymous on protected routes). The filter is added with `addFilterBefore(..., UsernamePasswordAuthenticationFilter.class)`.

#### Why it exists / why it matters

This is the glue between a stateless token and Spring Security's authorization model.

#### Pros and cons

**Pros**

- Reuses all existing authorization (URL and method security)
- Small, testable unit
- Clear separation: authenticate vs authorize

**Cons / trade-offs**

- Must clear/never trust stale context
- Registering the filter as a bean *and* in the chain runs it twice
- Easy to forget the `ROLE_` prefix

#### What happens without it / when misused

A filter that writes 401 itself breaks public endpoints; one that doesn't call `chain.doFilter` hangs the request; one that leaves a context between requests (non-stateless) leaks identity.

#### Syntax and rules

```java
String h = request.getHeader("Authorization");
if (h != null && h.startsWith("Bearer ") && jwt.isValid(h.substring(7))) {
  SecurityContextHolder.getContext().setAuthentication(
     new UsernamePasswordAuthenticationToken(user, null, authorities));
}
chain.doFilter(request, response);
```

#### Examples

**Example 1 — Registration**

```java
http.addFilterBefore(new JwtAuthFilter(jwtUtil), UsernamePasswordAuthenticationFilter.class);
```

**Example 2 — Avoid double registration**

```text
Don't annotate the filter with @Component; instantiate it in the chain config
```

**Example 3 — Testing**

```java
new JwtAuthFilter(jwt).doFilter(new MockHttpServletRequest(), new MockHttpServletResponse(), new MockFilterChain());
```

#### Quick checks

1. Should the filter reject invalid tokens?
2. Why not @Component?
3. Where is the user stored per request?

### 401 Unauthorized vs 403 Forbidden

#### What it is

**401** means authentication is missing or invalid (client should log in / refresh the token). **403** means the identity is known but lacks permission (logging in again won't help). Spring models this with `AuthenticationEntryPoint` (401) and `AccessDeniedHandler` (403); both can emit JSON so API clients can react programmatically.

#### Why it exists / why it matters

Front-ends redirect to login on 401 and show 'not allowed' on 403. Mixing them up produces infinite login loops or confusing UX.

#### Pros and cons

**Pros**

- Clear contract for clients
- Customizable JSON bodies
- Aligned with HTTP semantics

**Cons / trade-offs**

- The status name `Unauthorized` is misleading
- Defaults produce HTML or empty bodies
- Exposing too much detail helps attackers

#### What happens without it / when misused

Defaults return 403 for anonymous requests in some configurations; SPAs then cannot tell 'token expired' from 'not permitted'.

#### Syntax and rules

```java
http.exceptionHandling(e -> e
   .authenticationEntryPoint((req, res, ex) -> { res.setStatus(401); ... })
   .accessDeniedHandler((req, res, ex) -> { res.setStatus(403); ... }));
```

#### Examples

**Example 1 — Decision table**

```text
no/invalid token -> 401
valid token, wrong role -> 403
valid token, right role -> 200
```

**Example 2 — WWW-Authenticate**

```text
401 responses should include a challenge, e.g. WWW-Authenticate: Bearer
```

**Example 3 — JSON body**

```json
{"error":"forbidden"}
```

#### Quick checks

1. Which status for expired token?
2. Which for insufficient role?
3. Which Spring interface produces 403?

### Method security with @PreAuthorize

#### What it is

`@EnableMethodSecurity` activates annotations evaluated by a proxy around beans. `@PreAuthorize("hasRole('ADMIN')")` runs a SpEL expression *before* the method; expressions can reference arguments (`#owner`), `authentication`, `principal` and call beans. `@PostAuthorize` checks the return value; `@Secured` and JSR-250 are simpler alternatives.

#### Why it exists / why it matters

URL rules protect paths; business rules ('only the owner or an admin') belong next to the code they guard, and protect every entry point (controllers, schedulers, messaging).

#### Pros and cons

**Pros**

- Fine-grained, argument-aware rules
- Defense in depth beyond URLs
- Easy to unit-test with `@WithMockUser`

**Cons / trade-offs**

- Proxy-based: self-invocation bypasses it
- SpEL strings are not compile-checked
- Overuse scatters policy across code

#### What happens without it / when misused

Rely on URL rules only and a new controller endpoint calling the same service exposes the method; or call `this.deleteAll()` internally and wonder why the check vanishes.

#### Syntax and rules

```java
@Configuration @EnableMethodSecurity class MethodSecurityConfig {}

@PreAuthorize("#owner == authentication.name or hasRole('ADMIN')")
public String readFor(String owner) { ... }
```

#### Examples

**Example 1 — PostAuthorize**

```java
@PostAuthorize("returnObject.owner == authentication.name")
```

**Example 2 — Bean in SpEL**

```java
@PreAuthorize("@permissions.canEdit(#id, authentication)")
```

**Example 3 — Test**

```java
@WithMockUser(username = "ann", roles = "USER")
```

#### Quick checks

1. Pre vs Post authorize?
2. How do you reference an argument?
3. Why can it be bypassed internally?

## Interview corner

**Q1. Why can't you easily revoke a JWT?**

It's self-contained; you need a deny-list or short TTL + refresh tokens.

**Q2. 401 vs 403?**

Unauthenticated vs unauthorized.

**Q3. Where do you put the JWT filter?**

Before UsernamePasswordAuthenticationFilter.

**Q4. Does @PreAuthorize work on self-calls?**

No.

**Q5. Should you put roles in the JWT?**

Possible and convenient; stale until expiry.

## Common mistakes & debugging

- Weak or hard-coded secrets.
- Treating JWTs as encrypted.
- Registering the filter twice.
- Using 403 for expired tokens.

## Further reading

- RFC 7519 (JWT)
- jjwt README (0.12.x)
- Spring Security reference: Method Security

## Glossary

| Term | Meaning |
|------|---------|
| Claim | Statement inside a JWT payload |
| HS256 | HMAC with SHA-256 |
| Bearer token | Token presented in the Authorization header |
| Entry point | Component producing 401 |
| SpEL | Spring Expression Language |

## Answers

### JWT anatomy and signing

1. No, only signed (unless using JWE).
2. Defines expiry; validation fails afterwards.
3. 256 bits (32 bytes).

### JWT authentication filter

1. No, it leaves the context empty; authorization yields 401.
2. Boot would also register it as a servlet filter.
3. In the SecurityContextHolder (thread-bound).

### 401 Unauthorized vs 403 Forbidden

1. 401.
2. 403.
3. AccessDeniedHandler.

### Method security with @PreAuthorize

1. Before invocation vs after (on the return value).
2. #paramName.
3. Self-invocation doesn't go through the proxy.
