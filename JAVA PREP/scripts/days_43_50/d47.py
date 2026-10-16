from common import *

H2RT = dep("com.h2database", "h2", None, "runtime")
YMLJPA = "spring:\n  jpa:\n    hibernate:\n      ddl-auto: create-drop\n    open-in-view: false\n"

USER = r'''package %PKG%;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/** PROVIDED. Account entity (no Lombok: explicit constructors and getters). */
@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(name = "password_hash", nullable = false)
    private String passwordHash;

    @Column(name = "display_name", nullable = false)
    private String displayName;

    protected User() {
    }

    public User(String email, String passwordHash, String displayName) {
        this.email = email;
        this.passwordHash = passwordHash;
        this.displayName = displayName;
    }

    public Long getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public String getPasswordHash() {
        return passwordHash;
    }

    public String getDisplayName() {
        return displayName;
    }
}
'''
USERREPO = "package %PKG%;\n\nimport java.util.Optional;\nimport org.springframework.data.jpa.repository.JpaRepository;\n\n/** PROVIDED. */\npublic interface UserRepository extends JpaRepository<User, Long> {\n\n    Optional<User> findByEmail(String email);\n\n    boolean existsByEmail(String email);\n}\n"

# ---- task 1
REG = r'''package %PKG%;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class RegistrationService {

    private final UserRepository users;
    private final PasswordEncoder encoder;

    public RegistrationService(UserRepository users, PasswordEncoder encoder) {
        this.users = users;
        this.encoder = encoder;
    }

    /**
     * Rules: email is trimmed + lower-cased and must contain exactly one '@' with text on both sides, otherwise
     * IllegalArgumentException; password shorter than 8 chars -> IllegalArgumentException; blank displayName -> IAE;
     * an already registered email (any casing) -> DuplicateEmailException; the password is stored ONLY as a BCrypt hash.
     */
    @Transactional
    public UserResponse register(RegisterRequest request) {
        // TODO(%TAG%): validate, normalise, check duplicates, encode the password, save, map to UserResponse
        throw new UnsupportedOperationException("TODO(%TAG%): implement register");
    }
}
'''
REG_FILES = {
    "main/Application.java": APP, "main/User.java": USER, "main/UserRepository.java": USERREPO,
    "main/RegisterRequest.java": "package %PKG%;\n\n/** PROVIDED. */\npublic record RegisterRequest(String email, String password, String displayName) {\n}\n",
    "main/UserResponse.java": "package %PKG%;\n\n/** PROVIDED. Never contains the password or its hash. */\npublic record UserResponse(Long id, String email, String displayName) {\n}\n",
    "main/DuplicateEmailException.java": "package %PKG%;\n\n/** PROVIDED. */\npublic class DuplicateEmailException extends RuntimeException {\n\n    public DuplicateEmailException(String email) {\n        super(\"email already registered: \" + email);\n    }\n}\n",
    "main/BeansConfig.java": "package %PKG%;\n\nimport org.springframework.context.annotation.Bean;\nimport org.springframework.context.annotation.Configuration;\nimport org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;\nimport org.springframework.security.crypto.password.PasswordEncoder;\n\n/** PROVIDED. */\n@Configuration\npublic class BeansConfig {\n\n    @Bean\n    public PasswordEncoder passwordEncoder() {\n        return new BCryptPasswordEncoder();\n    }\n}\n",
    "res/application.yml": YMLJPA,
}
REG_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;

@SpringBootTest
class RegistrationServiceTest {

    @Autowired
    private RegistrationService service;
    @Autowired
    private UserRepository users;
    @Autowired
    private PasswordEncoder encoder;

    @BeforeEach
    void clean() {
        users.deleteAll();
    }

    @Test
    void registersAndNormalisesEmail() {
        UserResponse r = service.register(new RegisterRequest("  Ana@Example.COM ", "s3cretpass", "Ana"));
        assertThat(r.id()).isNotNull();
        assertThat(r.email()).isEqualTo("ana@example.com");
        assertThat(r.displayName()).isEqualTo("Ana");
    }

    @Test
    void passwordIsStoredAsBcryptHash() {
        service.register(new RegisterRequest("ana@example.com", "s3cretpass", "Ana"));
        User stored = users.findByEmail("ana@example.com").orElseThrow();
        assertThat(stored.getPasswordHash()).isNotEqualTo("s3cretpass").startsWith("$2");
        assertThat(encoder.matches("s3cretpass", stored.getPasswordHash())).isTrue();
    }

    @Test
    void duplicateEmailIsRejectedCaseInsensitively() {
        service.register(new RegisterRequest("ana@example.com", "s3cretpass", "Ana"));
        assertThatThrownBy(() -> service.register(new RegisterRequest("ANA@example.com", "other-pass1", "Other")))
                .isInstanceOf(DuplicateEmailException.class);
        assertThat(users.count()).isEqualTo(1);
    }

    @Test
    void invalidInputIsRejected() {
        assertThatThrownBy(() -> service.register(new RegisterRequest("no-at-sign", "s3cretpass", "A")))
                .isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.register(new RegisterRequest("@x.io", "s3cretpass", "A")))
                .isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.register(new RegisterRequest("a@x.io", "short", "A")))
                .isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.register(new RegisterRequest("a@x.io", "s3cretpass", "  ")))
                .isInstanceOf(IllegalArgumentException.class);
        assertThat(users.count()).isZero();
    }
}
'''
c1 = task("user-registration", "User Registration Service", "Warm-up", "Spring Boot (JPA + Security)",
    "First slice of the capstone API: register users with validation, normalized emails, duplicate detection and BCrypt-hashed passwords.",
    "boot", {**REG_FILES, "main/RegistrationService.java": REG, "test/RegistrationServiceTest.java": REG_TEST},
    ["Validate email, password length (>= 8) and display name.", "Normalize the email (trim + lower-case).", "Reject duplicates with `DuplicateEmailException`.", "Hash the password with the injected `PasswordEncoder`; never return it."],
    ["Case-variants of the same email.", "Whitespace-only display name."],
    ["`users.existsByEmail(normalized)`.", "`new User(email, encoder.encode(password), displayName)`."],
    starters=["spring-boot-starter-data-jpa", "spring-boot-starter-security"], deps=[H2RT])

# ---- task 2: JWT
CLAIMS = "package %PKG%;\n\nimport java.time.Instant;\nimport java.util.List;\n\n/** PROVIDED. Verified token contents. */\npublic record TokenClaims(String subject, List<String> roles, Instant expiresAt) {\n}\n"
IEX = "package %PKG%;\n\n/** PROVIDED. Any token that must not be trusted (bad format, bad signature, expired). */\npublic class InvalidTokenException extends RuntimeException {\n\n    public InvalidTokenException(String message) {\n        super(message);\n    }\n\n    public InvalidTokenException(String message, Throwable cause) {\n        super(message, cause);\n    }\n}\n"
TS = r'''package %PKG%;

import java.time.Clock;
import java.time.Duration;
import java.util.List;

/**
 * Minimal HS256 JWT implementation for learning purposes (production code should use a vetted library such as
 * Nimbus JOSE or jjwt). Format: base64url(header) . base64url(payload) . base64url(HMAC-SHA256(header.payload)).
 * Header JSON: {"alg":"HS256","typ":"JWT"}. Payload JSON: {"sub":..., "roles":[...], "iat":epochSec, "exp":epochSec}.
 */
public class TokenService {

    private final String secret;
    private final Clock clock;

    /** Secret shorter than 32 characters -> IllegalArgumentException. */
    public TokenService(String secret, Clock clock) {
        // TODO(%TAG%): validate the secret length and keep the fields
        this.secret = secret;
        this.clock = clock;
    }

    /** ttl must be positive (else IllegalArgumentException). exp = now + ttl. */
    public String issue(String subject, List<String> roles, Duration ttl) {
        // TODO(%TAG%): build header + payload JSON (Jackson ObjectMapper), base64url without padding, sign with HmacSHA256
        throw new UnsupportedOperationException("TODO(%TAG%): implement issue");
    }

    /**
     * Returns the claims of a valid token. Throws InvalidTokenException for: wrong number of parts, signature mismatch
     * (compare in constant time), header alg other than HS256 (reject "none"!), unreadable JSON, or exp <= now.
     */
    public TokenClaims verify(String token) {
        // TODO(%TAG%): split, check header, recompute and compare the signature, then parse payload and check expiry
        throw new UnsupportedOperationException("TODO(%TAG%): implement verify");
    }
}
'''
TS_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.nio.charset.StandardCharsets;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.Base64;
import java.util.List;
import org.junit.jupiter.api.Test;

class TokenServiceTest {

    private static final String SECRET = "0123456789abcdef0123456789abcdef-secret";
    private static final Instant T0 = Instant.parse("2025-01-01T00:00:00Z");

    private TokenService at(Instant now) {
        return new TokenService(SECRET, Clock.fixed(now, ZoneOffset.UTC));
    }

    private static String b64(String s) {
        return Base64.getUrlEncoder().withoutPadding().encodeToString(s.getBytes(StandardCharsets.UTF_8));
    }

    @Test
    void issuedTokenVerifiesAndCarriesClaims() {
        String token = at(T0).issue("ana@example.com", List.of("USER", "ADMIN"), Duration.ofMinutes(15));
        TokenClaims claims = at(T0.plusSeconds(60)).verify(token);
        assertThat(claims.subject()).isEqualTo("ana@example.com");
        assertThat(claims.roles()).containsExactly("USER", "ADMIN");
        assertThat(claims.expiresAt()).isEqualTo(T0.plusSeconds(900));
    }

    @Test
    void tokenHasThreeBase64UrlPartsAndHs256Header() {
        String token = at(T0).issue("a", List.of(), Duration.ofMinutes(1));
        String[] parts = token.split("\\.");
        assertThat(parts).hasSize(3);
        assertThat(token).doesNotContain("=").doesNotContain("+").doesNotContain("/");
        assertThat(new String(Base64.getUrlDecoder().decode(parts[0]), StandardCharsets.UTF_8)).contains("HS256");
    }

    @Test
    void expiredTokenIsRejected() {
        String token = at(T0).issue("a", List.of(), Duration.ofMinutes(1));
        assertThatThrownBy(() -> at(T0.plusSeconds(61)).verify(token)).isInstanceOf(InvalidTokenException.class);
    }

    @Test
    void tamperedPayloadIsRejected() {
        String[] parts = at(T0).issue("a", List.of("USER"), Duration.ofMinutes(5)).split("\\.");
        String forged = b64("{\"sub\":\"a\",\"roles\":[\"ADMIN\"],\"iat\":1735689600,\"exp\":1735690000}");
        assertThatThrownBy(() -> at(T0).verify(parts[0] + "." + forged + "." + parts[2])).isInstanceOf(InvalidTokenException.class);
    }

    @Test
    void wrongSecretIsRejected() {
        String token = new TokenService("another-secret-another-secret-another", Clock.fixed(T0, ZoneOffset.UTC))
                .issue("a", List.of(), Duration.ofMinutes(5));
        assertThatThrownBy(() -> at(T0).verify(token)).isInstanceOf(InvalidTokenException.class);
    }

    @Test
    void algNoneTokenIsRejected() {
        String token = b64("{\"alg\":\"none\",\"typ\":\"JWT\"}") + "." + b64("{\"sub\":\"a\",\"roles\":[],\"exp\":9999999999}") + ".";
        assertThatThrownBy(() -> at(T0).verify(token)).isInstanceOf(InvalidTokenException.class);
    }

    @Test
    void garbageIsRejected() {
        assertThatThrownBy(() -> at(T0).verify("not-a-jwt")).isInstanceOf(InvalidTokenException.class);
        assertThatThrownBy(() -> at(T0).verify("a.b.c")).isInstanceOf(InvalidTokenException.class);
    }

    @Test
    void invalidArgumentsAreRejected() {
        assertThatThrownBy(() -> new TokenService("short", Clock.systemUTC())).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> at(T0).issue("a", List.of(), Duration.ZERO)).isInstanceOf(IllegalArgumentException.class);
    }
}
'''
c2 = task("jwt-token-service", "HS256 JWT Token Service", "Core", "Spring Boot (security concepts)",
    "Implement signing and verification of a JWT by hand (HMAC-SHA256, base64url) to understand exactly what a library does and which attacks (tampering, alg=none, expiry) you must reject.",
    "boot", {"main/Application.java": APP, "main/TokenClaims.java": CLAIMS, "main/InvalidTokenException.java": IEX, "main/TokenService.java": TS, "test/TokenServiceTest.java": TS_TEST},
    ["Constructor rejects secrets shorter than 32 chars.", "`issue` builds header and payload JSON and signs `header.payload` with HmacSHA256.", "`verify` validates structure, algorithm, signature (constant time) and expiry.", "All failures raise `InvalidTokenException`."],
    ["`alg: none`.", "Tampered payload with a valid-looking signature part.", "Expiry boundary (`exp <= now` is expired).", "Padding characters in base64url."],
    ["`Mac.getInstance(\"HmacSHA256\")` + `SecretKeySpec`.", "`MessageDigest.isEqual(a, b)` for constant-time comparison.", "`Base64.getUrlEncoder().withoutPadding()`."],
    starters=["spring-boot-starter-json"])

# ---- task 3: relationships
PROJECT = r'''package %PKG%;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Entity
@Table(name = "projects")
public class Project {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    // TODO(%TAG%): map the owner: many projects belong to one User -> @ManyToOne(fetch = LAZY, optional = false) + @JoinColumn(name = "owner_id")
    private User owner;

    // TODO(%TAG%): one project has many tasks -> @OneToMany(mappedBy = "project", cascade = ALL, orphanRemoval = true)
    private List<TaskItem> tasks = new ArrayList<>();

    protected Project() {
    }

    public Project(String name, User owner) {
        this.name = name;
        this.owner = owner;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public User getOwner() {
        return owner;
    }

    public List<TaskItem> getTasks() {
        return Collections.unmodifiableList(tasks);
    }

    /** Keeps BOTH sides of the relationship in sync (adds to the list and sets task.project). */
    public void addTask(TaskItem task) {
        // TODO(%TAG%): tasks.add(task); task.setProject(this);
        throw new UnsupportedOperationException("TODO(%TAG%): implement addTask");
    }

    /** Removes the task from the list and clears task.project so orphanRemoval deletes the row. */
    public void removeTask(TaskItem task) {
        // TODO(%TAG%): tasks.remove(task); task.setProject(null);
        throw new UnsupportedOperationException("TODO(%TAG%): implement removeTask");
    }
}
'''
TASKITEM = r'''package %PKG%;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "task_items")
public class TaskItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    private boolean done;

    // TODO(%TAG%): owning side of the relationship -> @ManyToOne(fetch = LAZY, optional = false) + @JoinColumn(name = "project_id")
    private Project project;

    protected TaskItem() {
    }

    public TaskItem(String title) {
        this.title = title;
    }

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public boolean isDone() {
        return done;
    }

    public void setDone(boolean done) {
        this.done = done;
    }

    public Project getProject() {
        return project;
    }

    void setProject(Project project) {
        this.project = project;
    }
}
'''
PREPO = "package %PKG%;\n\nimport java.util.List;\nimport org.springframework.data.jpa.repository.JpaRepository;\n\n/** PROVIDED. */\npublic interface ProjectRepository extends JpaRepository<Project, Long> {\n\n    List<Project> findByOwnerId(Long ownerId);\n}\n"
MAP_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;

@DataJpaTest
class ProjectMappingTest {

    @Autowired
    private TestEntityManager em;
    @Autowired
    private ProjectRepository projects;

    private Project persistProject(User owner, String name, String... taskTitles) {
        Project p = new Project(name, owner);
        for (String t : taskTitles) {
            p.addTask(new TaskItem(t));
        }
        em.persist(p);
        em.flush();
        em.clear();
        return p;
    }

    private long taskRows() {
        return em.getEntityManager().createQuery("select count(t) from TaskItem t", Long.class).getSingleResult();
    }

    @Test
    void tasksArePersistedWithTheProjectAndReloaded() {
        User owner = em.persist(new User("a@x.io", "hash", "A"));
        Project p = persistProject(owner, "Apollo", "design", "build");
        Project loaded = projects.findById(p.getId()).orElseThrow();
        assertThat(loaded.getTasks()).extracting(TaskItem::getTitle).containsExactlyInAnyOrder("design", "build");
        assertThat(loaded.getTasks().get(0).getProject().getId()).isEqualTo(p.getId());
        assertThat(loaded.getOwner().getId()).isEqualTo(owner.getId());
    }

    @Test
    void removingATaskDeletesItsRow() {
        User owner = em.persist(new User("a@x.io", "hash", "A"));
        Project p = persistProject(owner, "Apollo", "design", "build");
        Project loaded = projects.findById(p.getId()).orElseThrow();
        loaded.removeTask(loaded.getTasks().get(0));
        em.flush();
        em.clear();
        assertThat(taskRows()).isEqualTo(1);
    }

    @Test
    void deletingTheProjectDeletesItsTasks() {
        User owner = em.persist(new User("a@x.io", "hash", "A"));
        Project p = persistProject(owner, "Apollo", "design", "build");
        projects.delete(projects.findById(p.getId()).orElseThrow());
        em.flush();
        assertThat(taskRows()).isZero();
    }

    @Test
    void projectsCanBeFoundByOwner() {
        User a = em.persist(new User("a@x.io", "hash", "A"));
        User b = em.persist(new User("b@x.io", "hash", "B"));
        persistProject(a, "A1");
        persistProject(a, "A2");
        persistProject(b, "B1");
        assertThat(projects.findByOwnerId(a.getId())).extracting(Project::getName).containsExactlyInAnyOrder("A1", "A2");
        assertThat(projects.findByOwnerId(b.getId())).hasSize(1);
    }
}
'''
c3 = task("project-task-relationships", "Entity Relationships: User - Project - Task", "Core", "Spring Boot (JPA)",
    "Map the capstone's core relationships (many projects per user, many tasks per project) correctly: owning side, mappedBy, cascade, orphan removal and helper methods that keep both sides in sync.",
    "boot", {"main/Application.java": APP, "main/User.java": USER, "main/Project.java": PROJECT, "main/TaskItem.java": TASKITEM, "main/ProjectRepository.java": PREPO, "test/ProjectMappingTest.java": MAP_TEST},
    ["Map `Project.owner` as a lazy mandatory `@ManyToOne` with `owner_id`.", "Map `Project.tasks` as `@OneToMany(mappedBy = \"project\", cascade = ALL, orphanRemoval = true)`.", "Map `TaskItem.project` as the owning `@ManyToOne` with `project_id`.", "Implement `addTask` / `removeTask` so both sides stay consistent."],
    ["Forgetting `mappedBy` creates a join table.", "Removing from the list without clearing the back reference.", "Lazy loading outside a transaction (not an issue inside `@DataJpaTest`)."],
    ["Annotations come from `jakarta.persistence`.", "The `User` entity is provided and persisted by the test."],
    starters=["spring-boot-starter-data-jpa"], deps=[H2RT])

# ---- task 4: security matrix
PROBE = r'''package %PKG%;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED. Dummy endpoints used to verify the security rules. */
@RestController
public class ProbeController {

    @GetMapping("/public/ping")
    public String ping() {
        return "pong";
    }

    @PostMapping("/api/auth/login")
    public String login() {
        return "login";
    }

    @GetMapping("/api/projects")
    public String projects() {
        return "projects";
    }

    @PostMapping("/api/projects")
    public String createProject() {
        return "created";
    }

    @GetMapping("/api/admin/stats")
    public String stats() {
        return "stats";
    }
}
'''
SEC = r'''package %PKG%;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    /**
     * Rules matrix:
     *   /public/**, /api/auth/**  -> anyone
     *   /api/admin/**             -> role ADMIN
     *   everything else           -> authenticated
     * Also: stateless sessions, CSRF disabled (token API), HTTP Basic enabled so anonymous access answers 401 (not 403).
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        // TODO(%TAG%): http.csrf(...).sessionManagement(...).authorizeHttpRequests(...).httpBasic(...); return http.build();
        throw new UnsupportedOperationException("TODO(%TAG%): implement filterChain");
    }
}
'''
SEC_TEST = r'''package %PKG%;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(ProbeController.class)
@Import(SecurityConfig.class)
class SecurityRulesTest {

    @Autowired
    private MockMvc mvc;

    @Test
    void publicEndpointsAreOpen() throws Exception {
        mvc.perform(get("/public/ping")).andExpect(status().isOk());
        mvc.perform(post("/api/auth/login")).andExpect(status().isOk());
    }

    @Test
    void anonymousGets401OnProtectedEndpoints() throws Exception {
        mvc.perform(get("/api/projects")).andExpect(status().isUnauthorized());
        mvc.perform(get("/api/admin/stats")).andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(roles = "USER")
    void userCanUseProtectedButNotAdminEndpoints() throws Exception {
        mvc.perform(get("/api/projects")).andExpect(status().isOk());
        mvc.perform(get("/api/admin/stats")).andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void adminCanUseAdminEndpoints() throws Exception {
        mvc.perform(get("/api/admin/stats")).andExpect(status().isOk());
    }

    @Test
    @WithMockUser(roles = "USER")
    void postWorksWithoutCsrfToken() throws Exception {
        mvc.perform(post("/api/projects")).andExpect(status().isOk());
    }
}
'''
c4 = task("security-rules-matrix", "Security Rules Matrix", "Challenge", "Spring Boot (Security)",
    "Write the `SecurityFilterChain` that protects the capstone API: public auth endpoints, admin-only area, authenticated everything else, stateless and CSRF-free, answering 401 vs 403 correctly.",
    "boot", {"main/Application.java": APP, "main/ProbeController.java": PROBE, "main/SecurityConfig.java": SEC, "test/SecurityRulesTest.java": SEC_TEST},
    ["Permit `/public/**` and `/api/auth/**`.", "Require role `ADMIN` for `/api/admin/**`.", "Require authentication for every other request.", "Disable CSRF and use `SessionCreationPolicy.STATELESS`.", "Enable HTTP Basic so anonymous requests receive 401."],
    ["401 (not authenticated) vs 403 (authenticated but not allowed).", "Rule order: specific matchers before `anyRequest()`."],
    ["`Customizer.withDefaults()` for `httpBasic`.", "`hasRole(\"ADMIN\")` expects the authority `ROLE_ADMIN`."],
    starters=["spring-boot-starter-web", "spring-boot-starter-security"], deps=[dep("org.springframework.security", "spring-security-test", None, "test")])

TOPICS = [
    T("Registration and password storage",
      "Registration creates an account: validate input, normalize identifiers (lower-case email), enforce uniqueness, and store only a **salted adaptive hash** of the password (BCrypt/Argon2 via Spring Security's `PasswordEncoder`).",
      "Databases leak. Slow, salted hashes make stolen password tables expensive to crack; plain or fast hashes (MD5/SHA-1) are effectively plain text.",
      ["BCrypt includes a random salt and work factor", "`PasswordEncoder` abstraction allows migration (`DelegatingPasswordEncoder`)"],
      ["Hashing is CPU-heavy by design", "Cannot recover forgotten passwords (only reset)"],
      "Storing plain passwords, or returning the hash from the API, turns any read bug into account takeover.",
      "```java\nPasswordEncoder enc = new BCryptPasswordEncoder();\nString hash = enc.encode(raw);          // $2a$10$...\nboolean ok = enc.matches(raw, hash);\n```\nUniqueness: database unique constraint AND a service check (race conditions are caught by the constraint).",
      [("Duplicate guard", "java", "if (users.existsByEmail(email)) throw new DuplicateEmailException(email);")],
      [("Why not SHA-256 for passwords?", "It is fast, so brute force is cheap; use an adaptive hash."),
       ("Why keep a DB unique constraint when you check in code?", "Two concurrent requests can both pass the check.")]),
    T("Stateless authentication with JWT",
      "A JSON Web Token has three base64url parts: header, payload (claims) and signature. With HS256 the server signs `header.payload` with a shared secret; any tampering invalidates the signature. Standard claims: `sub`, `iat`, `exp`. The client sends `Authorization: Bearer <token>`.",
      "Stateless tokens let any instance authenticate a request without a session store, which suits horizontally scaled APIs and microservices.",
      ["No server-side session", "Self-contained identity and roles", "Works across services"],
      ["Hard to revoke before expiry (use short TTL + refresh tokens/deny-list)", "Payload is readable (not secret)", "Key management matters"],
      "Accepting `alg: none`, skipping expiry checks, using short or guessable secrets, or storing sensitive data in the payload are classic vulnerabilities.",
      "Verify: split in 3 -> check header alg -> recompute HMAC and compare in constant time -> parse payload -> check `exp`. Use a vetted library in production.",
      [("Header and payload", "json", "{\"alg\":\"HS256\",\"typ\":\"JWT\"}\n{\"sub\":\"ana@example.com\",\"roles\":[\"USER\"],\"exp\":1735690000}")],
      [("Is the JWT payload encrypted?", "No, only signed (unless using JWE); never put secrets in it."),
       ("How do you log a user out with JWT?", "Short-lived access tokens, rotating refresh tokens, and optionally a deny-list.")]),
    T("Entity relationships and the capstone domain",
      "JPA relationships: `@ManyToOne` (owning side with the foreign key), `@OneToMany(mappedBy=...)` (inverse side), cascade and `orphanRemoval` for parent-owned children. Capstone domain: `User` 1-* `Project` 1-* `TaskItem`.",
      "Correct mapping decides your SQL: wrong ownership creates extra join tables, N+1 queries or orphaned rows.",
      ["Object navigation matches the schema", "Cascade removes manual child handling"],
      ["Bidirectional sync is manual", "Lazy loading pitfalls", "Large collections must not be loaded eagerly"],
      "Missing `mappedBy` => join table; modifying only the inverse side => the FK is never written; `FetchType.EAGER` on collections => performance bugs.",
      "```java\n@ManyToOne(fetch = LAZY, optional = false) @JoinColumn(name = \"owner_id\") private User owner;\n@OneToMany(mappedBy = \"project\", cascade = ALL, orphanRemoval = true) private List<TaskItem> tasks;\n```",
      [("Helper keeps both sides in sync", "java", "public void addTask(TaskItem t) { tasks.add(t); t.setProject(this); }")],
      [("Which side owns the relationship?", "The side with the foreign key (`@ManyToOne`), i.e. the one without `mappedBy`."),
       ("What does orphanRemoval do?", "Deletes a child row when it is removed from the parent collection.")]),
    T("Authorization rules and the 401 vs 403 distinction",
      "**Authentication** proves who you are (401 when missing/invalid); **authorization** decides what you may do (403 when authenticated but forbidden). Spring Security's `SecurityFilterChain` declares URL rules; method security (`@PreAuthorize`) protects service methods.",
      "A single misordered rule can expose admin APIs. A rules matrix test (who may call what) is the cheapest security regression suite.",
      ["Declarative rules", "Testable with `@WithMockUser`", "Defense in depth with method security"],
      ["Rule order is significant", "URL rules alone do not protect data ownership (need object-level checks, Day 48)"],
      "`anyRequest().permitAll()` left from a demo, or `authenticated()` before a more specific matcher, silently opens endpoints.",
      "```java\nhttp.csrf(c -> c.disable())\n    .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))\n    .authorizeHttpRequests(a -> a.requestMatchers(\"/api/auth/**\").permitAll()\n        .requestMatchers(\"/api/admin/**\").hasRole(\"ADMIN\").anyRequest().authenticated())\n    .httpBasic(Customizer.withDefaults());\n```",
      [("Test", "java", "mvc.perform(get(\"/api/admin/stats\")).andExpect(status().isForbidden());")],
      [("Why disable CSRF for a token API?", "CSRF exploits automatic browser credentials (cookies); bearer tokens are not sent automatically."),
       ("401 or 403 for a logged-in non-admin on /admin?", "403.")]),
]

day(47, "Capstone API Slice I: Authentication, Entities, and Relationships", "Capstone",
    "Register/login foundations, JWT mechanics, the core entity graph and the security rules matrix of the capstone API",
    ["Implement registration with validation and BCrypt", "Explain and implement JWT issue/verify (and its attack surface)", "Map User-Project-Task relationships with correct ownership and cascade", "Express and test a URL security rules matrix", "Prepare the structure that Project 01/02 will reuse"],
    ["Days 31-40 REST, JPA, Security", "Day 45-46 optional (events)"],
    TOPICS, [c1, c2, c3, c4],
    [("Authentication vs authorization?", "Who you are vs what you may do."),
     ("How would you secure passwords?", "Adaptive salted hash (BCrypt/Argon2), never reversible encryption."),
     ("What is the owning side?", "The entity whose table holds the foreign key."),
     ("JWT vs session?", "JWT is stateless but harder to revoke; sessions are server-side and easy to invalidate."),
     ("What goes wrong with alg=none?", "A library that trusts the header may accept unsigned tokens; always enforce the expected algorithm.")],
    ["Returning entities (with hashes) from controllers.", "Skipping the DB unique constraint.", "Updating only the inverse side of a relationship.", "Wrong matcher order.", "Long-lived tokens."],
    ["Spring Security Reference: Authorization, Password Storage", "RFC 7519 (JWT)", "Vlad Mihalcea: best way to map @OneToMany"],
    [("BCrypt", "Adaptive salted password hash"), ("JWT", "Signed token with claims"), ("Owning side", "Side holding the FK"), ("Cascade", "Propagating operations to children"),
     ("Orphan removal", "Delete children removed from the parent collection"), ("CSRF", "Cross-site request forgery")],
    "2-3 h theory + 5-7 h tasks", spring=True)
