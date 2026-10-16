from sx import *

TYPE = "Spring Boot (Security + JWT)"
SEC = ["spring-boot-starter-web", "spring-boot-starter-security"]
SECTEST = dep("org.springframework.security", "spring-security-test", None, "test")
JJWT = [dep("io.jsonwebtoken", "jjwt-api", "0.12.6"),
        dep("io.jsonwebtoken", "jjwt-impl", "0.12.6", "runtime"),
        dep("io.jsonwebtoken", "jjwt-jackson", "0.12.6", "runtime")]
JJWT_COMMENT = "    <!-- jjwt 0.12.x API: Jwts.builder().subject(..).signWith(key), Jwts.parser().verifyWith(key) -->\n"

JWTUTIL_BODY = r'''package %PKG%;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import java.nio.charset.StandardCharsets;
import java.time.Clock;
import java.time.Duration;
import java.util.Collection;
import java.util.Date;
import java.util.List;
import javax.crypto.SecretKey;

/** Issues and verifies HS256 JWTs. */
public class JwtUtil {

    private final SecretKey key;
    private final Duration ttl;
    private final Clock clock;

    public JwtUtil(String secret, Duration ttl) {
        this(secret, ttl, Clock.systemUTC());
    }

    /** secret must be at least 32 bytes (UTF-8) for HS256, otherwise IllegalArgumentException. */
    public JwtUtil(String secret, Duration ttl, Clock clock) {
        //B! validate the secret length and build the HMAC key with Keys.hmacShaKeyFor
        if (secret == null || secret.getBytes(StandardCharsets.UTF_8).length < 32) {
            throw new IllegalArgumentException("secret must be at least 32 bytes");
        }
        this.key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        this.ttl = ttl;
        this.clock = clock;
        //E!
    }

    /** Token with subject = username, claim "roles" = list of role names (no ROLE_ prefix), issuedAt = now, expiration = now + ttl. */
    public String generate(String username, Collection<String> roles) {
        //B! build and sign the token
        Date now = Date.from(clock.instant());
        return Jwts.builder().subject(username).claim("roles", List.copyOf(roles)).issuedAt(now)
                .expiration(Date.from(clock.instant().plus(ttl))).signWith(key).compact();
        //E!
    }

    private Claims claims(String token) {
        return Jwts.parser().verifyWith(key).clock(() -> Date.from(clock.instant())).build().parseSignedClaims(token).getPayload();
    }

    /** True only for a well-formed, correctly signed, unexpired token. Never throws (null/blank -> false). */
    public boolean isValid(String token) {
        //B! parse and catch JwtException / IllegalArgumentException
        if (token == null || token.isBlank()) {
            return false;
        }
        try {
            claims(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
        //E!
    }

    /** Subject of a VALID token; invalid tokens throw JwtException. */
    public String username(String token) {
        //B! return the subject
        return claims(token).getSubject();
        //E!
    }

    /** Roles claim of a VALID token (empty list when absent); invalid tokens throw JwtException. */
    public List<String> roles(String token) {
        //B! read the "roles" claim defensively
        Object raw = claims(token).get("roles");
        if (!(raw instanceof List<?> l)) {
            return List.of();
        }
        return l.stream().map(String::valueOf).toList();
        //E!
    }
}
'''
JWTUTIL_FULL = split_markers(JWTUTIL_BODY)[1]

# ------------------------------------------------------------ task 1
JUTEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import io.jsonwebtoken.JwtException;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.List;
import org.junit.jupiter.api.Test;

class JwtUtilTest {

    static final String SECRET = "0123456789-0123456789-0123456789-ab";
    static final Clock T0 = Clock.fixed(Instant.parse("2025-01-01T00:00:00Z"), ZoneOffset.UTC);

    private JwtUtil util(Clock clock) {
        return new JwtUtil(SECRET, Duration.ofMinutes(30), clock);
    }

    @Test
    void roundTrip() {
        JwtUtil u = util(T0);
        String token = u.generate("ann", List.of("USER", "ADMIN"));
        assertThat(token.split("\\.")).hasSize(3);
        assertThat(u.isValid(token)).isTrue();
        assertThat(u.username(token)).isEqualTo("ann");
        assertThat(u.roles(token)).containsExactly("USER", "ADMIN");
    }

    @Test
    void expiresAfterTtl() {
        String token = util(T0).generate("ann", List.of("USER"));
        assertThat(util(Clock.offset(T0, Duration.ofMinutes(29))).isValid(token)).isTrue();
        assertThat(util(Clock.offset(T0, Duration.ofMinutes(31))).isValid(token)).isFalse();
    }

    @Test
    void tamperedPayloadIsRejected() {
        JwtUtil u = util(T0);
        String[] parts = u.generate("ann", List.of("USER")).split("\\.");
        String forged = java.util.Base64.getUrlEncoder().withoutPadding().encodeToString("{\"sub\":\"root\",\"roles\":[\"ADMIN\"]}".getBytes());
        assertThat(u.isValid(parts[0] + "." + forged + "." + parts[2])).isFalse();
    }

    @Test
    void differentSecretIsRejected() {
        String token = util(T0).generate("ann", List.of("USER"));
        JwtUtil other = new JwtUtil("zzzzzzzzzz-zzzzzzzzzz-zzzzzzzzzz-zz", Duration.ofMinutes(30), T0);
        assertThat(other.isValid(token)).isFalse();
    }

    @Test
    void garbageIsInvalidNotAnException() {
        JwtUtil u = util(T0);
        assertThat(u.isValid(null)).isFalse();
        assertThat(u.isValid("")).isFalse();
        assertThat(u.isValid("not.a.jwt")).isFalse();
        assertThatThrownBy(() -> u.username("not.a.jwt")).isInstanceOf(JwtException.class);
    }

    @Test
    void shortSecretIsRejected() {
        assertThatThrownBy(() -> new JwtUtil("too-short", Duration.ofMinutes(1))).isInstanceOf(IllegalArgumentException.class);
    }
}
'''
t1 = tk("jwt-util-sign-verify", "Sign and Verify JWTs with jjwt", "Core",
    "Build a small, testable JWT utility: HS256 signing key checks, claims, expiry driven by an injectable Clock, and safe validation.",
    {"main/JwtUtil.java": JWTUTIL_BODY}, {"test/JwtUtilTest.java": JUTEST},
    ["Implement the constructor, `generate`, `isValid`, `username`, `roles`.", "Reject secrets shorter than 32 bytes.", "Validation must never throw."],
    ["Tampered payloads must fail signature verification.", "A token is valid just before expiry and invalid just after."],
    ["jjwt 0.12: `Jwts.builder().subject(..).claim(..).signWith(key).compact()` and `Jwts.parser().verifyWith(key).build().parseSignedClaims(t)`.", "A JWT is signed, not encrypted: never put secrets in claims."],
    [], deps=[JJWT_COMMENT] + JJWT, ttype="Java + jjwt")
t1["kind"] = "plain"

# ------------------------------------------------------------ task 2
FILTER = r'''package %PKG%;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.filter.OncePerRequestFilter;

/** Reads "Authorization: Bearer <jwt>" and, when valid, authenticates the request. Never rejects requests itself. */
public class JwtAuthFilter extends OncePerRequestFilter {

    private final JwtUtil jwt;

    public JwtAuthFilter(JwtUtil jwt) {
        this.jwt = jwt;
    }

    /**
     * Valid bearer token -> put a UsernamePasswordAuthenticationToken (principal = username, no credentials,
     * authorities = "ROLE_" + each role) into the SecurityContext. In ALL cases continue the filter chain.
     * Missing header, other schemes (Basic ...) and invalid tokens leave the context untouched.
     */
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        //B! parse the header, validate the token, populate SecurityContextHolder, always call chain.doFilter
        String header = request.getHeader("Authorization");
        if (header != null && header.startsWith("Bearer ")) {
            String token = header.substring(7).trim();
            if (jwt.isValid(token)) {
                List<GrantedAuthority> auths = jwt.roles(token).stream().map(r -> (GrantedAuthority) new SimpleGrantedAuthority("ROLE_" + r)).toList();
                SecurityContextHolder.getContext().setAuthentication(new UsernamePasswordAuthenticationToken(jwt.username(token), null, auths));
            }
        }
        chain.doFilter(request, response);
        //E!
    }
}
'''
FTEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import java.util.List;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockFilterChain;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;

class JwtAuthFilterTest {

    static final String SECRET = "0123456789-0123456789-0123456789-ab";
    final JwtUtil jwt = new JwtUtil(SECRET, Duration.ofMinutes(5));
    final JwtAuthFilter filter = new JwtAuthFilter(jwt);

    @AfterEach
    void clear() {
        SecurityContextHolder.clearContext();
    }

    private MockFilterChain run(String authorization) throws Exception {
        MockHttpServletRequest req = new MockHttpServletRequest();
        if (authorization != null) {
            req.addHeader("Authorization", authorization);
        }
        MockFilterChain chain = new MockFilterChain();
        filter.doFilter(req, new MockHttpServletResponse(), chain);
        return chain;
    }

    @Test
    void validTokenAuthenticates() throws Exception {
        MockFilterChain chain = run("Bearer " + jwt.generate("ann", List.of("USER", "ADMIN")));
        Authentication a = SecurityContextHolder.getContext().getAuthentication();
        assertThat(a).isNotNull();
        assertThat(a.getName()).isEqualTo("ann");
        assertThat(a.getAuthorities()).extracting(GrantedAuthority::getAuthority).containsExactlyInAnyOrder("ROLE_USER", "ROLE_ADMIN");
        assertThat(chain.getRequest()).as("chain continued").isNotNull();
    }

    @Test
    void missingHeaderLeavesContextEmpty() throws Exception {
        MockFilterChain chain = run(null);
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNull();
        assertThat(chain.getRequest()).isNotNull();
    }

    @Test
    void invalidTokenDoesNotAuthenticateButContinues() throws Exception {
        MockFilterChain chain = run("Bearer abc.def.ghi");
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNull();
        assertThat(chain.getRequest()).isNotNull();
    }

    @Test
    void otherSchemesAreIgnored() throws Exception {
        MockFilterChain chain = run("Basic YW5uOnB3");
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNull();
        assertThat(chain.getRequest()).isNotNull();
    }
}
'''
t2 = tk("jwt-filter", "A JWT Authentication Filter", "Core",
    "Write a OncePerRequestFilter that turns a Bearer token into a SecurityContext authentication — and never blocks the request itself.",
    {"main/JwtUtil.java": JWTUTIL_FULL, "main/JwtAuthFilter.java": FILTER},
    {"test/JwtAuthFilterTest.java": FTEST},
    ["Implement `doFilterInternal`.", "Prefix roles with `ROLE_` when creating authorities.", "Always continue the chain; authorization happens later."],
    ["Invalid tokens must not authenticate and must not crash the request.", "Non-Bearer schemes are ignored."],
    ["`JwtUtil` is provided: do not edit it.", "Do not register the filter as a `@Component` unless you also disable servlet auto-registration (it would run twice)."],
    SEC, deps=[JJWT_COMMENT] + JJWT, ttype=TYPE)
t2["files"]["main/JwtUtil.java"] = JWTUTIL_FULL

# ------------------------------------------------------------ task 3
JWTCFG = r'''package %PKG%;

import java.time.Duration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** PROVIDED (do not edit). */
@Configuration
public class JwtConfig {
    @Bean
    public JwtUtil jwtUtil() {
        return new JwtUtil("0123456789-0123456789-0123456789-ab", Duration.ofMinutes(10));
    }
}
'''
FILTER_FULL = split_markers(FILTER)[1]
CTL3 = r'''package %PKG%;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ApiController {

    @GetMapping("/public/ping")
    public String ping() {
        return "pong";
    }

    @GetMapping("/api/hello")
    public String hello() {
        return "hello";
    }

    @GetMapping("/admin/stats")
    public String stats() {
        return "stats";
    }
}
'''
SEC3 = r'''package %PKG%;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    /** No/invalid credentials on a protected route -> 401, Content-Type application/json, body {"error":"unauthorized"}. */
    @Bean
    public AuthenticationEntryPoint authenticationEntryPoint() {
        //B! return an entry point that writes status 401 and the JSON body
        return (request, response, ex) -> {
            response.setStatus(401);
            response.setContentType(MediaType.APPLICATION_JSON_VALUE);
            response.getWriter().write("{\"error\":\"unauthorized\"}");
        };
        //E!
    }

    /** Authenticated but lacking the role -> 403, Content-Type application/json, body {"error":"forbidden"}. */
    @Bean
    public AccessDeniedHandler accessDeniedHandler() {
        //B! return a handler that writes status 403 and the JSON body
        return (request, response, ex) -> {
            response.setStatus(403);
            response.setContentType(MediaType.APPLICATION_JSON_VALUE);
            response.getWriter().write("{\"error\":\"forbidden\"}");
        };
        //E!
    }

    /**
     * /public/** open; /admin/** role ADMIN; everything else authenticated. CSRF off, STATELESS sessions,
     * JwtAuthFilter (new JwtAuthFilter(jwtUtil)) before UsernamePasswordAuthenticationFilter, and the two handlers above.
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http, JwtUtil jwtUtil, AuthenticationEntryPoint entryPoint, AccessDeniedHandler denied) throws Exception {
        //B! wire csrf, sessions, exception handling, authorization rules and the JWT filter
        http.csrf(c -> c.disable())
                .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .exceptionHandling(e -> e.authenticationEntryPoint(entryPoint).accessDeniedHandler(denied))
                .authorizeHttpRequests(a -> a
                        .requestMatchers("/public/**").permitAll()
                        .requestMatchers("/admin/**").hasRole("ADMIN")
                        .anyRequest().authenticated())
                .addFilterBefore(new JwtAuthFilter(jwtUtil), UsernamePasswordAuthenticationFilter.class);
        return http.build();
        //E!
    }
}
'''
T3TEST = r'''package %PKG%;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(ApiController.class)
@Import({SecurityConfig.class, JwtConfig.class})
class Status401Vs403Test {

    @Autowired MockMvc mvc;
    @Autowired JwtUtil jwt;

    private String bearer(String user, String... roles) {
        return "Bearer " + jwt.generate(user, List.of(roles));
    }

    @Test
    void publicIsOpen() throws Exception {
        mvc.perform(get("/public/ping")).andExpect(status().isOk()).andExpect(content().string("pong"));
    }

    @Test
    void noTokenIs401Json() throws Exception {
        mvc.perform(get("/api/hello")).andExpect(status().isUnauthorized())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.error").value("unauthorized"));
    }

    @Test
    void garbageTokenIs401() throws Exception {
        mvc.perform(get("/api/hello").header("Authorization", "Bearer nope")).andExpect(status().isUnauthorized());
    }

    @Test
    void userCanReadApiButNotAdmin() throws Exception {
        mvc.perform(get("/api/hello").header("Authorization", bearer("ann", "USER"))).andExpect(status().isOk());
        mvc.perform(get("/admin/stats").header("Authorization", bearer("ann", "USER"))).andExpect(status().isForbidden())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.error").value("forbidden"));
    }

    @Test
    void adminCanReadAdmin() throws Exception {
        mvc.perform(get("/admin/stats").header("Authorization", bearer("root", "ADMIN"))).andExpect(status().isOk());
    }
}
'''
t3 = tk("status-401-vs-403", "401 vs 403 with JSON Handlers", "Core",
    "Wire the JWT filter into a stateless security chain and make unauthenticated (401) and unauthorized (403) failures distinguishable JSON responses.",
    {"main/Application.java": APP, "main/JwtUtil.java": JWTUTIL_FULL, "main/JwtAuthFilter.java": FILTER_FULL, "main/JwtConfig.java": JWTCFG,
     "main/ApiController.java": CTL3, "main/SecurityConfig.java": SEC3},
    {"test/Status401Vs403Test.java": T3TEST},
    ["Implement the entry point and the access-denied handler.", "Assemble the filter chain: rules, stateless sessions, JWT filter placement, handlers.", "State precisely when each status code is correct."],
    ["A syntactically broken token is an authentication failure -> 401.", "Role mismatch for an authenticated user is 403."],
    ["`exceptionHandling` registers both handlers.", "`addFilterBefore` positions the JWT filter ahead of the username/password filter."],
    SEC, deps=[JJWT_COMMENT] + JJWT, ttype=TYPE)
for k in ("main/JwtUtil.java", "main/JwtAuthFilter.java"):
    t3["files"][k] = split_markers(JWTUTIL_BODY if "Util" in k else FILTER)[1]

# ------------------------------------------------------------ task 4
MSCFG = r'''package %PKG%;

import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;

@Configuration
//A! switch on method security with @EnableMethodSecurity
@EnableMethodSecurity
//E!
public class MethodSecurityConfig {
}
'''
RSVC = r'''package %PKG%;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;

@Service
public class ReportService {

    /** Only ADMIN. */
    //A! restrict to ADMIN with @PreAuthorize("hasRole('ADMIN')")
    @PreAuthorize("hasRole('ADMIN')")
    //E!
    public String deleteAll() {
        return "deleted";
    }

    /** USER or ADMIN. */
    //A! restrict with @PreAuthorize("hasAnyRole('USER','ADMIN')")
    @PreAuthorize("hasAnyRole('USER','ADMIN')")
    //E!
    public String view() {
        return "report";
    }

    /** The owner themself or an ADMIN (compare the `owner` argument with authentication.name). */
    //A! restrict with @PreAuthorize("#owner == authentication.name or hasRole('ADMIN')")
    @PreAuthorize("#owner == authentication.name or hasRole('ADMIN')")
    //E!
    public String readFor(String owner) {
        return "report-of-" + owner;
    }
}
'''
MSTEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.AuthenticationCredentialsNotFoundException;
import org.springframework.security.test.context.support.WithMockUser;

@SpringBootTest
class MethodSecurityTest {

    @Autowired ReportService service;

    @Test
    @WithMockUser(roles = "USER")
    void userCannotDeleteAll() {
        assertThatThrownBy(service::deleteAll).isInstanceOf(AccessDeniedException.class);
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void adminCanDeleteAll() {
        assertThat(service.deleteAll()).isEqualTo("deleted");
    }

    @Test
    @WithMockUser(roles = "USER")
    void userCanView() {
        assertThat(service.view()).isEqualTo("report");
    }

    @Test
    @WithMockUser(roles = "GUEST")
    void guestCannotView() {
        assertThatThrownBy(service::view).isInstanceOf(AccessDeniedException.class);
    }

    @Test
    @WithMockUser(username = "ann", roles = "USER")
    void ownerReadsOwnReportOnly() {
        assertThat(service.readFor("ann")).isEqualTo("report-of-ann");
        assertThatThrownBy(() -> service.readFor("bob")).isInstanceOf(AccessDeniedException.class);
    }

    @Test
    @WithMockUser(username = "root", roles = "ADMIN")
    void adminReadsAnyReport() {
        assertThat(service.readFor("bob")).isEqualTo("report-of-bob");
    }

    @Test
    void anonymousCallsAreRejected() {
        assertThatThrownBy(service::view).isInstanceOfAny(AccessDeniedException.class, AuthenticationCredentialsNotFoundException.class);
    }
}
'''
t4 = tk("preauthorize-method", "Method Security with @PreAuthorize", "Challenge",
    "Protect service methods instead of URLs: enable method security, write SpEL expressions with roles and argument checks.",
    {"main/Application.java": APP, "main/MethodSecurityConfig.java": MSCFG, "main/ReportService.java": RSVC},
    {"test/MethodSecurityTest.java": MSTEST},
    ["Enable method security on the configuration class.", "Add the three documented `@PreAuthorize` expressions.", "Explain why method security is safer than URL rules alone."],
    ["`#owner` refers to the method parameter by name (compile with `-parameters`, which Boot's parent pom enables).", "Anonymous callers must be rejected, not given a default pass."],
    ["Calls within the same class bypass the proxy and therefore the check.", "`authentication.name` is the principal's username."],
    ["spring-boot-starter", "spring-boot-starter-security"], deps=[SECTEST], ttype=TYPE)

# ------------------------------------------------------------ theory
topics = [
    T("JWT anatomy and signing",
      "A **JSON Web Token** is `base64url(header).base64url(payload).base64url(signature)`. The payload carries *claims*: registered ones (`sub`, `iat`, `exp`, `iss`, `aud`) and custom ones (`roles`). With **HS256** the signature is an HMAC over header+payload using a shared secret of at least 256 bits. The token is *signed, not encrypted* — anyone can read the claims.",
      "Stateless authentication: the server needs no session store; any instance can verify a token with the key alone.",
      ["Horizontally scalable", "Self-contained identity and roles", "Works for mobile/SPA/service-to-service", "Standardized (RFC 7519)"],
      ["Cannot be revoked before expiry without extra state", "Large headers vs session ids", "Easy to misuse (weak secrets, `alg=none`, secrets in claims)"],
      "Short secrets are brute-forced offline; storing PII in claims leaks it to anyone holding the token; long-lived tokens remain valid after logout or role change.",
      "```java\nSecretKey key = Keys.hmacShaKeyFor(secret.getBytes(UTF_8)); // >= 32 bytes\nString token = Jwts.builder().subject(\"ann\").claim(\"roles\", List.of(\"USER\"))\n    .issuedAt(now).expiration(now.plus(ttl)).signWith(key).compact();\nClaims c = Jwts.parser().verifyWith(key).build().parseSignedClaims(token).getPayload();\n```",
      [("Inspect a token", "text", "echo <payload> | base64 -d   # claims are readable"),
       ("Typical claims", "json", "{ \"sub\": \"ann\", \"roles\": [\"USER\"], \"iat\": 1735689600, \"exp\": 1735691400 }"),
       ("Asymmetric option", "text", "RS256/ES256: private key signs, public key verifies (resource servers need only the public key)")],
      [("Is a JWT encrypted?", "No, only signed (unless using JWE)."),
       ("What does exp do?", "Defines expiry; validation fails afterwards."),
       ("Minimum HS256 key size?", "256 bits (32 bytes).")]),
    T("JWT authentication filter",
      "A custom `OncePerRequestFilter` reads the `Authorization: Bearer ...` header, validates the token, and places an `Authentication` into the `SecurityContextHolder`. It does *not* reject requests: if no authentication exists, the authorization filter later decides (401 for anonymous on protected routes). The filter is added with `addFilterBefore(..., UsernamePasswordAuthenticationFilter.class)`.",
      "This is the glue between a stateless token and Spring Security's authorization model.",
      ["Reuses all existing authorization (URL and method security)", "Small, testable unit", "Clear separation: authenticate vs authorize"],
      ["Must clear/never trust stale context", "Registering the filter as a bean *and* in the chain runs it twice", "Easy to forget the `ROLE_` prefix"],
      "A filter that writes 401 itself breaks public endpoints; one that doesn't call `chain.doFilter` hangs the request; one that leaves a context between requests (non-stateless) leaks identity.",
      "```java\nString h = request.getHeader(\"Authorization\");\nif (h != null && h.startsWith(\"Bearer \") && jwt.isValid(h.substring(7))) {\n  SecurityContextHolder.getContext().setAuthentication(\n     new UsernamePasswordAuthenticationToken(user, null, authorities));\n}\nchain.doFilter(request, response);\n```",
      [("Registration", "java", "http.addFilterBefore(new JwtAuthFilter(jwtUtil), UsernamePasswordAuthenticationFilter.class);"),
       ("Avoid double registration", "text", "Don't annotate the filter with @Component; instantiate it in the chain config"),
       ("Testing", "java", "new JwtAuthFilter(jwt).doFilter(new MockHttpServletRequest(), new MockHttpServletResponse(), new MockFilterChain());")],
      [("Should the filter reject invalid tokens?", "No, it leaves the context empty; authorization yields 401."),
       ("Why not @Component?", "Boot would also register it as a servlet filter."),
       ("Where is the user stored per request?", "In the SecurityContextHolder (thread-bound).")]),
    T("401 Unauthorized vs 403 Forbidden",
      "**401** means authentication is missing or invalid (client should log in / refresh the token). **403** means the identity is known but lacks permission (logging in again won't help). Spring models this with `AuthenticationEntryPoint` (401) and `AccessDeniedHandler` (403); both can emit JSON so API clients can react programmatically.",
      "Front-ends redirect to login on 401 and show 'not allowed' on 403. Mixing them up produces infinite login loops or confusing UX.",
      ["Clear contract for clients", "Customizable JSON bodies", "Aligned with HTTP semantics"],
      ["The status name `Unauthorized` is misleading", "Defaults produce HTML or empty bodies", "Exposing too much detail helps attackers"],
      "Defaults return 403 for anonymous requests in some configurations; SPAs then cannot tell 'token expired' from 'not permitted'.",
      "```java\nhttp.exceptionHandling(e -> e\n   .authenticationEntryPoint((req, res, ex) -> { res.setStatus(401); ... })\n   .accessDeniedHandler((req, res, ex) -> { res.setStatus(403); ... }));\n```",
      [("Decision table", "text", "no/invalid token -> 401\nvalid token, wrong role -> 403\nvalid token, right role -> 200"),
       ("WWW-Authenticate", "text", "401 responses should include a challenge, e.g. WWW-Authenticate: Bearer"),
       ("JSON body", "json", "{\"error\":\"forbidden\"}")],
      [("Which status for expired token?", "401."),
       ("Which for insufficient role?", "403."),
       ("Which Spring interface produces 403?", "AccessDeniedHandler.")]),
    T("Method security with @PreAuthorize",
      "`@EnableMethodSecurity` activates annotations evaluated by a proxy around beans. `@PreAuthorize(\"hasRole('ADMIN')\")` runs a SpEL expression *before* the method; expressions can reference arguments (`#owner`), `authentication`, `principal` and call beans. `@PostAuthorize` checks the return value; `@Secured` and JSR-250 are simpler alternatives.",
      "URL rules protect paths; business rules ('only the owner or an admin') belong next to the code they guard, and protect every entry point (controllers, schedulers, messaging).",
      ["Fine-grained, argument-aware rules", "Defense in depth beyond URLs", "Easy to unit-test with `@WithMockUser`"],
      ["Proxy-based: self-invocation bypasses it", "SpEL strings are not compile-checked", "Overuse scatters policy across code"],
      "Rely on URL rules only and a new controller endpoint calling the same service exposes the method; or call `this.deleteAll()` internally and wonder why the check vanishes.",
      "```java\n@Configuration @EnableMethodSecurity class MethodSecurityConfig {}\n\n@PreAuthorize(\"#owner == authentication.name or hasRole('ADMIN')\")\npublic String readFor(String owner) { ... }\n```",
      [("PostAuthorize", "java", "@PostAuthorize(\"returnObject.owner == authentication.name\")"),
       ("Bean in SpEL", "java", "@PreAuthorize(\"@permissions.canEdit(#id, authentication)\")"),
       ("Test", "java", "@WithMockUser(username = \"ann\", roles = \"USER\")")],
      [("Pre vs Post authorize?", "Before invocation vs after (on the return value)."),
       ("How do you reference an argument?", "#paramName."),
       ("Why can it be bypassed internally?", "Self-invocation doesn't go through the proxy.")]),
]

day(38, "Spring Security II: JWT, 401 vs 403, Method Security", "Spring Boot",
    "Stateless authentication with signed tokens and fine-grained method authorization",
    ["Create and verify HS256 JWTs with jjwt 0.12", "Build a Bearer-token authentication filter", "Return correct 401/403 JSON responses", "Apply @PreAuthorize with SpEL", "Understand JWT trade-offs (revocation, claims, secrets)"],
    ["Day 37 Spring Security I"],
    topics, [t1, t2, t3, t4],
    [("Why can't you easily revoke a JWT?", "It's self-contained; you need a deny-list or short TTL + refresh tokens."),
     ("401 vs 403?", "Unauthenticated vs unauthorized."),
     ("Where do you put the JWT filter?", "Before UsernamePasswordAuthenticationFilter."),
     ("Does @PreAuthorize work on self-calls?", "No."),
     ("Should you put roles in the JWT?", "Possible and convenient; stale until expiry.")],
    ["Weak or hard-coded secrets.", "Treating JWTs as encrypted.", "Registering the filter twice.", "Using 403 for expired tokens."],
    ["RFC 7519 (JWT)", "jjwt README (0.12.x)", "Spring Security reference: Method Security"],
    [("Claim", "Statement inside a JWT payload"), ("HS256", "HMAC with SHA-256"), ("Bearer token", "Token presented in the Authorization header"), ("Entry point", "Component producing 401"), ("SpEL", "Spring Expression Language")],
    "2–3 h theory + 3–5 h tasks", spring=True)
