# Day 37 — Spring Security I: Filter Chain, UserDetailsService, BCrypt and Roles

**Phase:** Spring Boot  
**Primary theme:** Authentication and authorization fundamentals in Spring Security 6  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-security-filter-chain`, `task-02-user-details-service`, `task-03-bcrypt-password-service`, `task-04-role-rules-challenge`  
**Instruction alignment:** Maps to Day 37 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Authentication and authorization fundamentals in Spring Security 6. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. Spring Security architecture: the filter chain
2. UserDetailsService, authentication providers and roles
3. Password storage with BCrypt
4. Interview corner, common mistakes, glossary

## Subtopics

### Spring Security architecture: the filter chain

#### What it is

Spring Security is a chain of servlet filters (`DelegatingFilterProxy` -> `FilterChainProxy` -> `SecurityFilterChain`). Each request passes filters for CSRF, authentication (Basic, form, bearer), exception translation and authorization (`AuthorizationFilter`). You configure it with a `SecurityFilterChain` bean built from `HttpSecurity`. **Authentication** = who are you (`Authentication` in the `SecurityContext`); **authorization** = what may you do.

#### Why it exists / why it matters

Cross-cutting security should not be sprinkled through controllers. A central, ordered chain gives one place to enforce rules, defaults against common attacks (CSRF, session fixation, headers) and consistent 401/403 behavior.

#### Pros and cons

**Pros**

- Secure by default (everything authenticated)
- Declarative, composable configuration
- Pluggable authentication mechanisms
- Mature protections (headers, CSRF, fixation)

**Cons / trade-offs**

- Large surface and many concepts
- Configuration API changed across versions (lambda DSL from 6)
- Order of rules is easy to get wrong

#### What happens without it / when misused

Adding `spring-boot-starter-security` without config locks everything behind a generated password. Wrongly ordered rules (`anyRequest().permitAll()` first) silently open the app. Disabling CSRF in a browser/session app invites cross-site request forgery.

#### Syntax and rules

```java
@Bean SecurityFilterChain chain(HttpSecurity http) throws Exception {
  http.csrf(c -> c.disable())
      .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
      .authorizeHttpRequests(a -> a
          .requestMatchers("/public/**").permitAll()
          .requestMatchers("/admin/**").hasRole("ADMIN")
          .anyRequest().authenticated())
      .httpBasic(Customizer.withDefaults());
  return http.build();
}
```
401 = not authenticated (challenge), 403 = authenticated but not allowed.

#### Examples

**Example 1 — Test with a mock user**

```java
@Test @WithMockUser(roles = "ADMIN")
void adminOk() throws Exception { mvc.perform(get("/admin/stats")).andExpect(status().isOk()); }
```

**Example 2 — Method-specific rule**

```java
.requestMatchers(HttpMethod.DELETE, "/api/**").hasRole("ADMIN")
```

**Example 3 — Debug**

```properties
logging.level.org.springframework.security=DEBUG
```

#### Quick checks

1. 401 vs 403?
2. Which rule wins when several match?
3. When is disabling CSRF acceptable?

### UserDetailsService, authentication providers and roles

#### What it is

`UserDetailsService.loadUserByUsername` returns a `UserDetails` (username, encoded password, authorities, enabled/locked flags). `DaoAuthenticationProvider` loads the user, checks the password with the `PasswordEncoder` and the account flags, and produces an authenticated `Authentication`. **Roles** are authorities prefixed with `ROLE_`: `hasRole("ADMIN")` checks `ROLE_ADMIN`; `hasAuthority("ROLE_ADMIN")` is equivalent.

#### Why it exists / why it matters

Real applications keep users in a database or directory. The abstraction lets the framework authenticate against any store without knowing it.

#### Pros and cons

**Pros**

- Pluggable user stores
- Account state (disabled, locked, expired) built in
- Uniform authority model
- Easy unit testing

**Cons / trade-offs**

- Roles vs authorities prefix confusion
- Loading users on every request in stateless setups costs a query unless you embed claims (JWT, Day 38)
- Custom user details classes can bloat the session

#### What happens without it / when misused

Revealing 'user not found' vs 'wrong password' allows account enumeration; Spring hides this by default (`BadCredentialsException`). Forgetting to map `enabled=false` lets disabled users in.

#### Syntax and rules

```java
public UserDetails loadUserByUsername(String name) {
  UserRecord r = store.find(name).orElseThrow(() -> new UsernameNotFoundException(name));
  return User.withUsername(r.username()).password(r.passwordHash())
             .roles(r.roles().toArray(String[]::new)).disabled(!r.enabled()).build();
}
```
`InMemoryUserDetailsManager` and `JdbcUserDetailsManager` are ready-made implementations.

#### Examples

**Example 1 — In-memory users**

```java
new InMemoryUserDetailsManager(User.withUsername("bob").password(enc.encode("pw")).roles("USER").build());
```

**Example 2 — Authorities without prefix**

```java
User.withUsername("x").password(h).authorities("reports:read").build();
```

**Example 3 — Current user in a controller**

```java
@GetMapping("/me") String me(Authentication auth) { return auth.getName(); }
```

#### Quick checks

1. roles("ADMIN") vs authorities("ADMIN")?
2. Why the same error for unknown user and wrong password?
3. Where do account flags matter?

### Password storage with BCrypt

#### What it is

Passwords are never stored in plain text or with fast hashes. **BCrypt** is an adaptive, salted hash: each hash embeds salt and cost factor (`$2a$10$...`), so identical passwords give different hashes and cost can be raised over time. `PasswordEncoder` offers `encode`, `matches`, `upgradeEncoding`; `DelegatingPasswordEncoder` prefixes ids (`{bcrypt}`, `{argon2}`) to migrate algorithms.

#### Why it exists / why it matters

Databases leak. Slow salted hashes make offline cracking expensive and rainbow tables useless.

#### Pros and cons

**Pros**

- Built-in salt
- Tunable cost
- Standard, reviewed algorithm
- Seamless algorithm migration with delegating encoder

**Cons / trade-offs**

- CPU cost per login (by design)
- 72-byte input limit
- Not memory-hard (Argon2/SCrypt are stronger options)

#### What happens without it / when misused

Plain text or unsalted SHA-256 hashes allow instant mass cracking after a leak. Comparing hashes with `equals` leaks timing and fails because salts differ; always call `matches`.

#### Syntax and rules

```java
PasswordEncoder enc = new BCryptPasswordEncoder(10);
String hash = enc.encode(raw);          // $2a$10$...
boolean ok  = enc.matches(raw, hash);
if (enc.upgradeEncoding(hash)) { /* re-hash after successful login */ }
PasswordEncoder any = PasswordEncoderFactories.createDelegatingPasswordEncoder();   // {bcrypt}...
```
Tune the cost so a hash takes roughly 100-250 ms on production hardware.

#### Examples

**Example 1 — Bean**

```java
@Bean PasswordEncoder passwordEncoder() { return new BCryptPasswordEncoder(); }
```

**Example 2 — Registration**

```java
user.setPasswordHash(encoder.encode(request.password()));
```

**Example 3 — Never**

```java
// MessageDigest.getInstance("MD5") for passwords
```

#### Quick checks

1. Why do two hashes of the same password differ?
2. What does upgradeEncoding do?
3. Why not SHA-256?

## Interview corner

**Q1. Authentication vs authorization?**

Who you are vs what you may do.

**Q2. What is the SecurityFilterChain?**

An ordered set of filters matched to requests.

**Q3. Why BCrypt?**

Adaptive, salted password hashing.

**Q4. hasRole vs hasAuthority?**

hasRole adds the ROLE_ prefix.

**Q5. Why does Spring return the same error for bad user and bad password?**

To avoid user enumeration.

## Common mistakes & debugging

- Putting `anyRequest()` before specific rules.
- Storing raw passwords in InMemoryUserDetailsManager.
- Disabling CSRF on session-based browser apps.
- Forgetting `spring-security-test` for MockMvc tests.

## Further reading

- Spring Security Reference: Servlet Architecture, Authentication, Authorization
- OWASP Password Storage Cheat Sheet

## Glossary

| Term | Meaning |
|------|---------|
| SecurityContext | Holds the current Authentication |
| Authority | Granted permission string |
| BCrypt | Adaptive salted hash |
| CSRF | Cross-site request forgery |
| UserDetails | Spring's user abstraction |

## Answers

### Spring Security architecture: the filter chain

1. 401: no/invalid credentials; 403: authenticated but lacking permission.
2. The first one in declaration order.
3. For stateless APIs not relying on browser cookies for auth.

### UserDetailsService, authentication providers and roles

1. `roles` adds the ROLE_ prefix; `authorities` stores the string as is.
2. To prevent username enumeration.
3. The provider checks enabled/locked/expired before accepting credentials.

### Password storage with BCrypt

1. A random salt is generated per hash.
2. Signals that a hash uses weaker parameters than the current configuration.
3. It is fast; attackers can try billions of guesses per second.
