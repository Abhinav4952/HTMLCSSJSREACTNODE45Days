from sx import *

S = ["spring-boot-starter-web", "spring-boot-starter-security"]
SECTEST = dep("org.springframework.security", "spring-security-test", None, "test")

# ------------------------------------------------------------ task 1
DEMO = r'''package %PKG%;

import java.security.Principal;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED endpoints; your SecurityFilterChain decides who may call them. */
@RestController
public class DemoController {

    @GetMapping("/public/hello")
    public String hello() {
        return "hello";
    }

    @GetMapping("/api/me")
    public String me(Principal principal) {
        return principal.getName();
    }

    @GetMapping("/admin/stats")
    public Map<String, Integer> stats() {
        return Map.of("users", 42);
    }

    @PostMapping("/api/echo")
    public String echo(@RequestBody String body) {
        return body;
    }
}
'''
SC1 = r'''package %PKG%;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    /**
     * Rules (first match wins, most specific first):
     *  - /public/**  -> everyone
     *  - /admin/**   -> role ADMIN
     *  - anything else -> authenticated
     * Stateless REST API: CSRF disabled, no HTTP session, HTTP Basic for authentication (gives 401 + WWW-Authenticate).
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        //B! configure csrf, sessionManagement (STATELESS), authorizeHttpRequests and httpBasic, then return http.build()
        http.csrf(csrf -> csrf.disable())
                .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(a -> a
                        .requestMatchers("/public/**").permitAll()
                        .requestMatchers("/admin/**").hasRole("ADMIN")
                        .anyRequest().authenticated())
                .httpBasic(Customizer.withDefaults());
        return http.build();
        //E!
    }
}
'''
T1 = r'''package %PKG%;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class FilterChainTest {

    @Autowired
    MockMvc mvc;

    @Test
    void publicPathsAreOpen() throws Exception {
        mvc.perform(get("/public/hello")).andExpect(status().isOk()).andExpect(content().string("hello"));
    }

    @Test
    void anonymousGets401WithBasicChallenge() throws Exception {
        mvc.perform(get("/api/me")).andExpect(status().isUnauthorized())
                .andExpect(header().string("WWW-Authenticate", org.hamcrest.Matchers.startsWith("Basic")));
    }

    @Test
    void unknownPathsAreProtectedToo() throws Exception {
        mvc.perform(get("/something/else")).andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(username = "ann")
    void authenticatedUserSeesOwnName() throws Exception {
        mvc.perform(get("/api/me")).andExpect(status().isOk()).andExpect(content().string("ann"));
    }

    @Test
    @WithMockUser(roles = "USER")
    void plainUserCannotEnterAdminArea() throws Exception {
        mvc.perform(get("/admin/stats")).andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void adminCanEnterAdminArea() throws Exception {
        mvc.perform(get("/admin/stats")).andExpect(status().isOk());
    }

    @Test
    @WithMockUser
    void postWorksWithoutCsrfTokenForStatelessApi() throws Exception {
        mvc.perform(post("/api/echo").content("ping")).andExpect(status().isOk()).andExpect(content().string("ping"));
    }
}
'''
a1 = tk("security-filter-chain", "SecurityFilterChain: Rules, Basic Auth and Stateless Mode", "Warm-up",
    "Replace Boot's default security with your own SecurityFilterChain: path rules, role checks, HTTP Basic, CSRF off and stateless sessions.",
    {"main/Application.java": APP, "main/DemoController.java": DEMO, "main/SecurityConfig.java": SC1},
    {"test/FilterChainTest.java": T1},
    ["Implement `SecurityConfig.filterChain` with the documented rules.", "Make anonymous requests answer 401 with a Basic challenge."],
    ["Rule order matters: the first matching rule wins.", "Without `httpBasic` anonymous requests get 403 (no entry point).", "Disabling CSRF is only acceptable for stateless token/basic APIs, never for browser session apps."],
    ["`requestMatchers(\"/admin/**\").hasRole(\"ADMIN\")` checks authority `ROLE_ADMIN`.", "`anyRequest().authenticated()` must come last."],
    S, deps=[SECTEST])

# ------------------------------------------------------------ task 2
UREC = "package %PKG%;\n\nimport java.util.List;\n\npublic record UserRecord(String username, String passwordHash, List<String> roles, boolean enabled) {\n}\n"
USTORE = r'''package %PKG%;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/** PROVIDED in-memory user table. */
public class UserStore {
    private final Map<String, UserRecord> users = new HashMap<>();

    public UserStore add(UserRecord user) {
        users.put(user.username().toLowerCase(), user);
        return this;
    }

    public Optional<UserRecord> find(String username) {
        return Optional.ofNullable(username == null ? null : users.get(username.toLowerCase()));
    }
}
'''
UDS = r'''package %PKG%;

import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

public class StoreUserDetailsService implements UserDetailsService {

    private final UserStore store;

    public StoreUserDetailsService(UserStore store) {
        this.store = store;
    }

    /**
     * Unknown user -> UsernameNotFoundException.
     * Otherwise build Spring's User with: username, the stored hash, roles (as "ROLE_x" authorities via .roles(...)),
     * and disabled(true) when the record is not enabled. Usernames are case-insensitive (store handles it).
     */
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        //B! look up the record and map it to UserDetails
        UserRecord r = store.find(username).orElseThrow(() -> new UsernameNotFoundException("User not found: " + username));
        return User.withUsername(r.username()).password(r.passwordHash()).roles(r.roles().toArray(String[]::new)).disabled(!r.enabled()).build();
        //E!
    }
}
'''
T2 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.DisabledException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

class UserDetailsServiceTest {

    BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(4);
    StoreUserDetailsService service;
    DaoAuthenticationProvider provider;

    @BeforeEach
    void setUp() {
        UserStore store = new UserStore()
                .add(new UserRecord("alice", encoder.encode("alicepw"), List.of("ADMIN", "USER"), true))
                .add(new UserRecord("bob", encoder.encode("bobpw"), List.of("USER"), true))
                .add(new UserRecord("carl", encoder.encode("carlpw"), List.of("USER"), false));
        service = new StoreUserDetailsService(store);
        provider = new DaoAuthenticationProvider();
        provider.setUserDetailsService(service);
        provider.setPasswordEncoder(encoder);
    }

    private Authentication login(String user, String pw) {
        return provider.authenticate(UsernamePasswordAuthenticationToken.unauthenticated(user, pw));
    }

    @Test
    void mapsRolesToPrefixedAuthorities() {
        UserDetails d = service.loadUserByUsername("alice");
        assertThat(d.getUsername()).isEqualTo("alice");
        assertThat(d.getAuthorities()).extracting(Object::toString).containsExactlyInAnyOrder("ROLE_ADMIN", "ROLE_USER");
        assertThat(d.isEnabled()).isTrue();
    }

    @Test
    void lookupIsCaseInsensitive() {
        assertThat(service.loadUserByUsername("BOB").getUsername()).isEqualTo("bob");
    }

    @Test
    void unknownUserThrows() {
        assertThatThrownBy(() -> service.loadUserByUsername("nobody")).isInstanceOf(UsernameNotFoundException.class);
    }

    @Test
    void disabledAccountIsReportedDisabled() {
        assertThat(service.loadUserByUsername("carl").isEnabled()).isFalse();
    }

    @Test
    void authenticationSucceedsWithRightPassword() {
        Authentication a = login("bob", "bobpw");
        assertThat(a.isAuthenticated()).isTrue();
        assertThat(a.getAuthorities()).extracting(Object::toString).containsExactly("ROLE_USER");
    }

    @Test
    void wrongPasswordAndUnknownUserLookTheSame() {
        assertThatThrownBy(() -> login("bob", "nope")).isInstanceOf(BadCredentialsException.class);
        assertThatThrownBy(() -> login("ghost", "x")).isInstanceOf(BadCredentialsException.class);
    }

    @Test
    void disabledUserCannotLogIn() {
        assertThatThrownBy(() -> login("carl", "carlpw")).isInstanceOf(DisabledException.class);
    }
}
'''
a2 = tk("user-details-service", "Custom UserDetailsService", "Core",
    "Bridge your own user storage to Spring Security by implementing UserDetailsService, then see DaoAuthenticationProvider use it.",
    {"main/Application.java": APP, "main/UserRecord.java": UREC, "main/UserStore.java": USTORE, "main/StoreUserDetailsService.java": UDS},
    {"test/UserDetailsServiceTest.java": T2},
    ["Implement `loadUserByUsername` using `User.withUsername(...)`.", "Throw `UsernameNotFoundException` for unknown users and honor the `enabled` flag."],
    ["`roles(\"ADMIN\")` adds the `ROLE_` prefix itself; `authorities(\"ADMIN\")` does not.", "Never reveal whether the username or the password was wrong (`BadCredentialsException`)."],
    ["`User.withUsername(name).password(hash).roles(...).disabled(bool).build()`.", "The hash must already be encoded: the provider compares with the `PasswordEncoder`."],
    S, deps=[SECTEST])

# ------------------------------------------------------------ task 3
PWS = r'''package %PKG%;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

public class PasswordService {

    private final PasswordEncoder encoder;

    /** @param strength BCrypt cost factor (log rounds). */
    public PasswordService(int strength) {
        //B! create a BCryptPasswordEncoder with the given strength
        this.encoder = new BCryptPasswordEncoder(strength);
        //E!
    }

    /** Raw password must be non-null and at least 8 characters, else IllegalArgumentException("password too short"). */
    public String hash(String rawPassword) {
        //B! validate then encode
        if (rawPassword == null || rawPassword.length() < 8) {
            throw new IllegalArgumentException("password too short");
        }
        return encoder.encode(rawPassword);
        //E!
    }

    /** False for null arguments; true only when the raw password matches the stored hash. */
    public boolean matches(String rawPassword, String storedHash) {
        //B! null-safe matches
        if (rawPassword == null || storedHash == null) {
            return false;
        }
        return encoder.matches(rawPassword, storedHash);
        //E!
    }

    /** True when the stored hash was produced with a weaker cost than this service uses and should be re-hashed on next login. */
    public boolean needsUpgrade(String storedHash) {
        //B! ask the encoder
        return encoder.upgradeEncoding(storedHash);
        //E!
    }
}
'''
T3 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.factory.PasswordEncoderFactories;

class PasswordServiceTest {

    PasswordService service = new PasswordService(6);

    @Test
    void hashLooksLikeBcryptAndIsNotThePassword() {
        String h = service.hash("correct horse");
        assertThat(h).startsWith("$2a$06$").hasSize(60).doesNotContain("correct");
    }

    @Test
    void sameInputGivesDifferentHashesBecauseOfSalt() {
        assertThat(service.hash("correct horse")).isNotEqualTo(service.hash("correct horse"));
    }

    @Test
    void matchesAcceptsOnlyTheRightPassword() {
        String h = service.hash("correct horse");
        assertThat(service.matches("correct horse", h)).isTrue();
        assertThat(service.matches("Correct horse", h)).isFalse();
        assertThat(service.matches(null, h)).isFalse();
        assertThat(service.matches("correct horse", null)).isFalse();
    }

    @Test
    void shortOrMissingPasswordsAreRejected() {
        assertThatThrownBy(() -> service.hash("short")).isInstanceOf(IllegalArgumentException.class).hasMessage("password too short");
        assertThatThrownBy(() -> service.hash(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void weakerHashesNeedAnUpgrade() {
        String weak = new BCryptPasswordEncoder(4).encode("correct horse");
        assertThat(service.needsUpgrade(weak)).isTrue();
        assertThat(service.needsUpgrade(service.hash("correct horse"))).isFalse();
        assertThat(new PasswordService(4).needsUpgrade(weak)).isFalse();
    }

    @Test
    void delegatingEncoderUnderstandsIdPrefixes() {
        var delegating = PasswordEncoderFactories.createDelegatingPasswordEncoder();
        String stored = "{bcrypt}" + service.hash("correct horse").substring(0);
        assertThat(delegating.matches("correct horse", stored)).isTrue();
    }
}
'''
a3 = tk("bcrypt-password-service", "BCrypt Password Hashing", "Core",
    "Hash and verify passwords with BCrypt: salting, cost factor, upgrade detection and the DelegatingPasswordEncoder id prefix.",
    {"main/Application.java": APP, "main/PasswordService.java": PWS},
    {"test/PasswordServiceTest.java": T3},
    ["Create the encoder with the configurable strength.", "Implement `hash`, `matches` and `needsUpgrade` with the documented null/length rules."],
    ["Never log or store raw passwords.", "BCrypt only uses the first 72 bytes of input.", "Hash verification must be timing-safe: always use `matches`, never `equals`."],
    ["`PasswordEncoder.upgradeEncoding(hash)` compares the cost embedded in the hash with the configured cost.", "`{bcrypt}` is the id the delegating encoder uses to pick the algorithm."],
    S, deps=[SECTEST])

# ------------------------------------------------------------ task 4
REP = r'''package %PKG%;

import java.util.List;
import java.util.Map;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED endpoints. */
@RestController
public class ReportController {

    @GetMapping("/api/reports")
    public List<String> reports() {
        return List.of("q1", "q2");
    }

    @GetMapping("/api/whoami")
    public Map<String, Object> whoami(Authentication authentication) {
        return Map.of("name", authentication.getName(),
                "authorities", authentication.getAuthorities().stream().map(Object::toString).sorted().toList());
    }

    @DeleteMapping("/api/reports/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable String id) {
    }

    @GetMapping("/public/ping")
    public String ping() {
        return "pong";
    }
}
'''
SC4 = r'''package %PKG%;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    /** BCrypt with low strength 4 (fast tests). */
    @Bean
    public PasswordEncoder passwordEncoder() {
        //B! return a BCryptPasswordEncoder(4)
        return new BCryptPasswordEncoder(4);
        //E!
    }

    /** Users: alice / alicepw with role ADMIN, bob / bobpw with role USER. Store only ENCODED passwords. */
    @Bean
    public UserDetailsService userDetailsService(PasswordEncoder encoder) {
        //B! InMemoryUserDetailsManager with the two users
        return new InMemoryUserDetailsManager(
                User.withUsername("alice").password(encoder.encode("alicepw")).roles("ADMIN").build(),
                User.withUsername("bob").password(encoder.encode("bobpw")).roles("USER").build());
        //E!
    }

    /**
     * Rules:
     *  /public/**                 everyone
     *  GET    /api/reports/** and /api/reports   USER or ADMIN
     *  DELETE /api/reports/**                    ADMIN only
     *  everything else (e.g. /api/whoami)        authenticated
     * Stateless, CSRF disabled, HTTP Basic.
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        //B! authorizeHttpRequests with HttpMethod-specific matchers; stateless; basic
        http.csrf(c -> c.disable())
                .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(a -> a
                        .requestMatchers("/public/**").permitAll()
                        .requestMatchers(HttpMethod.GET, "/api/reports", "/api/reports/**").hasAnyRole("USER", "ADMIN")
                        .requestMatchers(HttpMethod.DELETE, "/api/reports/**").hasRole("ADMIN")
                        .anyRequest().authenticated())
                .httpBasic(Customizer.withDefaults());
        return http.build();
        //E!
    }
}
'''
T4 = r'''package %PKG%;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.httpBasic;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
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
class RoleRulesTest {

    @Autowired
    MockMvc mvc;

    @Test
    void publicIsOpen() throws Exception {
        mvc.perform(get("/public/ping")).andExpect(status().isOk());
    }

    @Test
    void anonymousIsRejected() throws Exception {
        mvc.perform(get("/api/reports")).andExpect(status().isUnauthorized());
    }

    @Test
    void wrongPasswordIsRejected() throws Exception {
        mvc.perform(get("/api/reports").with(httpBasic("bob", "wrong"))).andExpect(status().isUnauthorized());
        mvc.perform(get("/api/reports").with(httpBasic("ghost", "bobpw"))).andExpect(status().isUnauthorized());
    }

    @Test
    void userCanReadReports() throws Exception {
        mvc.perform(get("/api/reports").with(httpBasic("bob", "bobpw"))).andExpect(status().isOk()).andExpect(jsonPath("$[0]").value("q1"));
    }

    @Test
    void userCannotDelete() throws Exception {
        mvc.perform(delete("/api/reports/q1").with(httpBasic("bob", "bobpw"))).andExpect(status().isForbidden());
    }

    @Test
    void adminCanDelete() throws Exception {
        mvc.perform(delete("/api/reports/q1").with(httpBasic("alice", "alicepw"))).andExpect(status().isNoContent());
    }

    @Test
    void whoamiShowsAuthorities() throws Exception {
        mvc.perform(get("/api/whoami").with(httpBasic("alice", "alicepw"))).andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("alice")).andExpect(jsonPath("$.authorities[0]").value("ROLE_ADMIN"));
    }
}
'''
a4 = tk("role-rules-challenge", "Users, Encoder and Role Rules Together", "Challenge",
    "Wire a PasswordEncoder, an in-memory user store and method-specific URL rules into a working Basic-auth API.",
    {"main/Application.java": APP, "main/ReportController.java": REP, "main/SecurityConfig.java": SC4},
    {"test/RoleRulesTest.java": T4},
    ["Define the `PasswordEncoder`, the `UserDetailsService` with two users and the `SecurityFilterChain`.", "403 for authenticated-but-forbidden, 401 for unauthenticated."],
    ["Store encoded passwords only.", "Matchers with an HTTP method are more specific than path-only ones: order them before `anyRequest()`.", "A defined `UserDetailsService` bean disables Boot's generated default user."],
    ["`hasAnyRole(\"USER\", \"ADMIN\")` accepts either.", "`InMemoryUserDetailsManager` takes varargs of `UserDetails`."],
    S, deps=[SECTEST])

topics = [
    T("Spring Security architecture: the filter chain",
      "Spring Security is a chain of servlet filters (`DelegatingFilterProxy` -> `FilterChainProxy` -> `SecurityFilterChain`). Each request passes filters for CSRF, authentication (Basic, form, bearer), exception translation and authorization (`AuthorizationFilter`). You configure it with a `SecurityFilterChain` bean built from `HttpSecurity`. **Authentication** = who are you (`Authentication` in the `SecurityContext`); **authorization** = what may you do.",
      "Cross-cutting security should not be sprinkled through controllers. A central, ordered chain gives one place to enforce rules, defaults against common attacks (CSRF, session fixation, headers) and consistent 401/403 behavior.",
      ["Secure by default (everything authenticated)", "Declarative, composable configuration", "Pluggable authentication mechanisms", "Mature protections (headers, CSRF, fixation)"],
      ["Large surface and many concepts", "Configuration API changed across versions (lambda DSL from 6)", "Order of rules is easy to get wrong"],
      "Adding `spring-boot-starter-security` without config locks everything behind a generated password. Wrongly ordered rules (`anyRequest().permitAll()` first) silently open the app. Disabling CSRF in a browser/session app invites cross-site request forgery.",
      "```java\n@Bean SecurityFilterChain chain(HttpSecurity http) throws Exception {\n  http.csrf(c -> c.disable())\n      .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))\n      .authorizeHttpRequests(a -> a\n          .requestMatchers(\"/public/**\").permitAll()\n          .requestMatchers(\"/admin/**\").hasRole(\"ADMIN\")\n          .anyRequest().authenticated())\n      .httpBasic(Customizer.withDefaults());\n  return http.build();\n}\n```\n401 = not authenticated (challenge), 403 = authenticated but not allowed.",
      [("Test with a mock user", "java", "@Test @WithMockUser(roles = \"ADMIN\")\nvoid adminOk() throws Exception { mvc.perform(get(\"/admin/stats\")).andExpect(status().isOk()); }"),
       ("Method-specific rule", "java", ".requestMatchers(HttpMethod.DELETE, \"/api/**\").hasRole(\"ADMIN\")"),
       ("Debug", "properties", "logging.level.org.springframework.security=DEBUG")],
      [("401 vs 403?", "401: no/invalid credentials; 403: authenticated but lacking permission."),
       ("Which rule wins when several match?", "The first one in declaration order."),
       ("When is disabling CSRF acceptable?", "For stateless APIs not relying on browser cookies for auth.")]),
    T("UserDetailsService, authentication providers and roles",
      "`UserDetailsService.loadUserByUsername` returns a `UserDetails` (username, encoded password, authorities, enabled/locked flags). `DaoAuthenticationProvider` loads the user, checks the password with the `PasswordEncoder` and the account flags, and produces an authenticated `Authentication`. **Roles** are authorities prefixed with `ROLE_`: `hasRole(\"ADMIN\")` checks `ROLE_ADMIN`; `hasAuthority(\"ROLE_ADMIN\")` is equivalent.",
      "Real applications keep users in a database or directory. The abstraction lets the framework authenticate against any store without knowing it.",
      ["Pluggable user stores", "Account state (disabled, locked, expired) built in", "Uniform authority model", "Easy unit testing"],
      ["Roles vs authorities prefix confusion", "Loading users on every request in stateless setups costs a query unless you embed claims (JWT, Day 38)", "Custom user details classes can bloat the session"],
      "Revealing 'user not found' vs 'wrong password' allows account enumeration; Spring hides this by default (`BadCredentialsException`). Forgetting to map `enabled=false` lets disabled users in.",
      "```java\npublic UserDetails loadUserByUsername(String name) {\n  UserRecord r = store.find(name).orElseThrow(() -> new UsernameNotFoundException(name));\n  return User.withUsername(r.username()).password(r.passwordHash())\n             .roles(r.roles().toArray(String[]::new)).disabled(!r.enabled()).build();\n}\n```\n`InMemoryUserDetailsManager` and `JdbcUserDetailsManager` are ready-made implementations.",
      [("In-memory users", "java", "new InMemoryUserDetailsManager(User.withUsername(\"bob\").password(enc.encode(\"pw\")).roles(\"USER\").build());"),
       ("Authorities without prefix", "java", "User.withUsername(\"x\").password(h).authorities(\"reports:read\").build();"),
       ("Current user in a controller", "java", "@GetMapping(\"/me\") String me(Authentication auth) { return auth.getName(); }")],
      [("roles(\"ADMIN\") vs authorities(\"ADMIN\")?", "`roles` adds the ROLE_ prefix; `authorities` stores the string as is."),
       ("Why the same error for unknown user and wrong password?", "To prevent username enumeration."),
       ("Where do account flags matter?", "The provider checks enabled/locked/expired before accepting credentials.")]),
    T("Password storage with BCrypt",
      "Passwords are never stored in plain text or with fast hashes. **BCrypt** is an adaptive, salted hash: each hash embeds salt and cost factor (`$2a$10$...`), so identical passwords give different hashes and cost can be raised over time. `PasswordEncoder` offers `encode`, `matches`, `upgradeEncoding`; `DelegatingPasswordEncoder` prefixes ids (`{bcrypt}`, `{argon2}`) to migrate algorithms.",
      "Databases leak. Slow salted hashes make offline cracking expensive and rainbow tables useless.",
      ["Built-in salt", "Tunable cost", "Standard, reviewed algorithm", "Seamless algorithm migration with delegating encoder"],
      ["CPU cost per login (by design)", "72-byte input limit", "Not memory-hard (Argon2/SCrypt are stronger options)"],
      "Plain text or unsalted SHA-256 hashes allow instant mass cracking after a leak. Comparing hashes with `equals` leaks timing and fails because salts differ; always call `matches`.",
      "```java\nPasswordEncoder enc = new BCryptPasswordEncoder(10);\nString hash = enc.encode(raw);          // $2a$10$...\nboolean ok  = enc.matches(raw, hash);\nif (enc.upgradeEncoding(hash)) { /* re-hash after successful login */ }\nPasswordEncoder any = PasswordEncoderFactories.createDelegatingPasswordEncoder();   // {bcrypt}...\n```\nTune the cost so a hash takes roughly 100-250 ms on production hardware.",
      [("Bean", "java", "@Bean PasswordEncoder passwordEncoder() { return new BCryptPasswordEncoder(); }"),
       ("Registration", "java", "user.setPasswordHash(encoder.encode(request.password()));"),
       ("Never", "java", "// MessageDigest.getInstance(\"MD5\") for passwords")],
      [("Why do two hashes of the same password differ?", "A random salt is generated per hash."),
       ("What does upgradeEncoding do?", "Signals that a hash uses weaker parameters than the current configuration."),
       ("Why not SHA-256?", "It is fast; attackers can try billions of guesses per second.")]),
]

day(37, "Spring Security I: Filter Chain, UserDetailsService, BCrypt and Roles", "Spring Boot",
    "Authentication and authorization fundamentals in Spring Security 6",
    ["Explain the servlet filter chain and configure a SecurityFilterChain", "Implement UserDetailsService and understand DaoAuthenticationProvider", "Hash and verify passwords with BCrypt", "Apply role-based URL rules and test them with MockMvc"],
    ["Day 31 REST II", "Day 36 CORS"],
    topics, [a1, a2, a3, a4],
    [("Authentication vs authorization?", "Who you are vs what you may do."),
     ("What is the SecurityFilterChain?", "An ordered set of filters matched to requests."),
     ("Why BCrypt?", "Adaptive, salted password hashing."),
     ("hasRole vs hasAuthority?", "hasRole adds the ROLE_ prefix."),
     ("Why does Spring return the same error for bad user and bad password?", "To avoid user enumeration.")],
    ["Putting `anyRequest()` before specific rules.", "Storing raw passwords in InMemoryUserDetailsManager.", "Disabling CSRF on session-based browser apps.", "Forgetting `spring-security-test` for MockMvc tests."],
    ["Spring Security Reference: Servlet Architecture, Authentication, Authorization", "OWASP Password Storage Cheat Sheet"],
    [("SecurityContext", "Holds the current Authentication"), ("Authority", "Granted permission string"), ("BCrypt", "Adaptive salted hash"),
     ("CSRF", "Cross-site request forgery"), ("UserDetails", "Spring's user abstraction")],
    "2–3 h theory + 3–5 h tasks", spring=True)
