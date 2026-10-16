# Day 47 — Capstone API Slice I: Authentication, Entities, and Relationships

**Phase:** Capstone  
**Primary theme:** Register/login foundations, JWT mechanics, the core entity graph and the security rules matrix of the capstone API  
**Estimated study time:** 2-3 h theory + 5-7 h tasks  
**Related tasks:** `task-01-user-registration`, `task-02-jwt-token-service`, `task-03-project-task-relationships`, `task-04-security-rules-matrix`  
**Instruction alignment:** Maps to Day 47 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Register/login foundations, JWT mechanics, the core entity graph and the security rules matrix of the capstone API. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. Registration and password storage
2. Stateless authentication with JWT
3. Entity relationships and the capstone domain
4. Authorization rules and the 401 vs 403 distinction
5. Interview corner, common mistakes, glossary

## Subtopics

### Registration and password storage

#### What it is

Registration creates an account: validate input, normalize identifiers (lower-case email), enforce uniqueness, and store only a **salted adaptive hash** of the password (BCrypt/Argon2 via Spring Security's `PasswordEncoder`).

#### Why it exists / why it matters

Databases leak. Slow, salted hashes make stolen password tables expensive to crack; plain or fast hashes (MD5/SHA-1) are effectively plain text.

#### Pros and cons

**Pros**

- BCrypt includes a random salt and work factor
- `PasswordEncoder` abstraction allows migration (`DelegatingPasswordEncoder`)

**Cons / trade-offs**

- Hashing is CPU-heavy by design
- Cannot recover forgotten passwords (only reset)

#### What happens without it / when misused

Storing plain passwords, or returning the hash from the API, turns any read bug into account takeover.

#### Syntax and rules

```java
PasswordEncoder enc = new BCryptPasswordEncoder();
String hash = enc.encode(raw);          // $2a$10$...
boolean ok = enc.matches(raw, hash);
```
Uniqueness: database unique constraint AND a service check (race conditions are caught by the constraint).

#### Examples

**Example 1 — Duplicate guard**

```java
if (users.existsByEmail(email)) throw new DuplicateEmailException(email);
```

#### Quick checks

1. Why not SHA-256 for passwords?
2. Why keep a DB unique constraint when you check in code?

### Stateless authentication with JWT

#### What it is

A JSON Web Token has three base64url parts: header, payload (claims) and signature. With HS256 the server signs `header.payload` with a shared secret; any tampering invalidates the signature. Standard claims: `sub`, `iat`, `exp`. The client sends `Authorization: Bearer <token>`.

#### Why it exists / why it matters

Stateless tokens let any instance authenticate a request without a session store, which suits horizontally scaled APIs and microservices.

#### Pros and cons

**Pros**

- No server-side session
- Self-contained identity and roles
- Works across services

**Cons / trade-offs**

- Hard to revoke before expiry (use short TTL + refresh tokens/deny-list)
- Payload is readable (not secret)
- Key management matters

#### What happens without it / when misused

Accepting `alg: none`, skipping expiry checks, using short or guessable secrets, or storing sensitive data in the payload are classic vulnerabilities.

#### Syntax and rules

Verify: split in 3 -> check header alg -> recompute HMAC and compare in constant time -> parse payload -> check `exp`. Use a vetted library in production.

#### Examples

**Example 1 — Header and payload**

```json
{"alg":"HS256","typ":"JWT"}
{"sub":"ana@example.com","roles":["USER"],"exp":1735690000}
```

#### Quick checks

1. Is the JWT payload encrypted?
2. How do you log a user out with JWT?

### Entity relationships and the capstone domain

#### What it is

JPA relationships: `@ManyToOne` (owning side with the foreign key), `@OneToMany(mappedBy=...)` (inverse side), cascade and `orphanRemoval` for parent-owned children. Capstone domain: `User` 1-* `Project` 1-* `TaskItem`.

#### Why it exists / why it matters

Correct mapping decides your SQL: wrong ownership creates extra join tables, N+1 queries or orphaned rows.

#### Pros and cons

**Pros**

- Object navigation matches the schema
- Cascade removes manual child handling

**Cons / trade-offs**

- Bidirectional sync is manual
- Lazy loading pitfalls
- Large collections must not be loaded eagerly

#### What happens without it / when misused

Missing `mappedBy` => join table; modifying only the inverse side => the FK is never written; `FetchType.EAGER` on collections => performance bugs.

#### Syntax and rules

```java
@ManyToOne(fetch = LAZY, optional = false) @JoinColumn(name = "owner_id") private User owner;
@OneToMany(mappedBy = "project", cascade = ALL, orphanRemoval = true) private List<TaskItem> tasks;
```

#### Examples

**Example 1 — Helper keeps both sides in sync**

```java
public void addTask(TaskItem t) { tasks.add(t); t.setProject(this); }
```

#### Quick checks

1. Which side owns the relationship?
2. What does orphanRemoval do?

### Authorization rules and the 401 vs 403 distinction

#### What it is

**Authentication** proves who you are (401 when missing/invalid); **authorization** decides what you may do (403 when authenticated but forbidden). Spring Security's `SecurityFilterChain` declares URL rules; method security (`@PreAuthorize`) protects service methods.

#### Why it exists / why it matters

A single misordered rule can expose admin APIs. A rules matrix test (who may call what) is the cheapest security regression suite.

#### Pros and cons

**Pros**

- Declarative rules
- Testable with `@WithMockUser`
- Defense in depth with method security

**Cons / trade-offs**

- Rule order is significant
- URL rules alone do not protect data ownership (need object-level checks, Day 48)

#### What happens without it / when misused

`anyRequest().permitAll()` left from a demo, or `authenticated()` before a more specific matcher, silently opens endpoints.

#### Syntax and rules

```java
http.csrf(c -> c.disable())
    .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
    .authorizeHttpRequests(a -> a.requestMatchers("/api/auth/**").permitAll()
        .requestMatchers("/api/admin/**").hasRole("ADMIN").anyRequest().authenticated())
    .httpBasic(Customizer.withDefaults());
```

#### Examples

**Example 1 — Test**

```java
mvc.perform(get("/api/admin/stats")).andExpect(status().isForbidden());
```

#### Quick checks

1. Why disable CSRF for a token API?
2. 401 or 403 for a logged-in non-admin on /admin?

## Interview corner

**Q1. Authentication vs authorization?**

Who you are vs what you may do.

**Q2. How would you secure passwords?**

Adaptive salted hash (BCrypt/Argon2), never reversible encryption.

**Q3. What is the owning side?**

The entity whose table holds the foreign key.

**Q4. JWT vs session?**

JWT is stateless but harder to revoke; sessions are server-side and easy to invalidate.

**Q5. What goes wrong with alg=none?**

A library that trusts the header may accept unsigned tokens; always enforce the expected algorithm.

## Common mistakes & debugging

- Returning entities (with hashes) from controllers.
- Skipping the DB unique constraint.
- Updating only the inverse side of a relationship.
- Wrong matcher order.
- Long-lived tokens.

## Further reading

- Spring Security Reference: Authorization, Password Storage
- RFC 7519 (JWT)
- Vlad Mihalcea: best way to map @OneToMany

## Glossary

| Term | Meaning |
|------|---------|
| BCrypt | Adaptive salted password hash |
| JWT | Signed token with claims |
| Owning side | Side holding the FK |
| Cascade | Propagating operations to children |
| Orphan removal | Delete children removed from the parent collection |
| CSRF | Cross-site request forgery |

## Answers

### Registration and password storage

1. It is fast, so brute force is cheap; use an adaptive hash.
2. Two concurrent requests can both pass the check.

### Stateless authentication with JWT

1. No, only signed (unless using JWE); never put secrets in it.
2. Short-lived access tokens, rotating refresh tokens, and optionally a deny-list.

### Entity relationships and the capstone domain

1. The side with the foreign key (`@ManyToOne`), i.e. the one without `mappedBy`.
2. Deletes a child row when it is removed from the parent collection.

### Authorization rules and the 401 vs 403 distinction

1. CSRF exploits automatic browser credentials (cookies); bearer tokens are not sent automatically.
2. 403.
