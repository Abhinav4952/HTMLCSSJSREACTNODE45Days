from sx import *

TYPE = "Spring Boot (Testing)"
W = ["spring-boot-starter-web"]
H2R = [dep("com.h2database", "h2", None, "runtime")]
SECTEST = dep("org.springframework.security", "spring-security-test", None, "test")


def with_sol(t, key, code):
    t["sol"][key] = code
    return t


# ------------------------------------------------------------ task 1
BOOK = "package %PKG%;\n\npublic record Book(long id, String title, String author) {\n}\n"
BSVC = r'''package %PKG%;

import java.util.List;
import java.util.Optional;

public interface BookService {
    Optional<Book> find(long id);

    List<Book> findAll();

    List<Book> byAuthor(String author);
}
'''
BCTL = r'''package %PKG%;

import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/books")
public class BookController {

    private final BookService service;

    public BookController(BookService service) {
        this.service = service;
    }

    /** 200 + book JSON or 404. */
    @GetMapping("/{id}")
    public ResponseEntity<Book> get(@PathVariable long id) {
        //B! return the book as 200 or answer 404
        return service.find(id).map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
        //E!
    }

    /** Without `author` -> service.findAll(); with `author` -> service.byAuthor(author) and NEVER findAll(). */
    @GetMapping
    public List<Book> list(@RequestParam(required = false) String author) {
        //B! delegate to findAll or byAuthor depending on the parameter
        return author == null ? service.findAll() : service.byAuthor(author);
        //E!
    }
}
'''
BTEST = r'''package %PKG%;

import static org.hamcrest.Matchers.hasSize;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

/** Web slice: only MVC infrastructure + BookController are loaded; the service is a Mockito mock. */
@WebMvcTest(BookController.class)
class BookControllerSliceTest {

    @Autowired MockMvc mvc;
    @MockitoBean BookService service;

    @Test
    void returnsBookJson() throws Exception {
        given(service.find(1)).willReturn(Optional.of(new Book(1, "Dune", "Herbert")));
        mvc.perform(get("/books/1")).andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Dune")).andExpect(jsonPath("$.author").value("Herbert"));
    }

    @Test
    void unknownBookIs404() throws Exception {
        given(service.find(9)).willReturn(Optional.empty());
        mvc.perform(get("/books/9")).andExpect(status().isNotFound());
    }

    @Test
    void listsAll() throws Exception {
        given(service.findAll()).willReturn(List.of(new Book(1, "A", "x"), new Book(2, "B", "y")));
        mvc.perform(get("/books")).andExpect(status().isOk()).andExpect(jsonPath("$", hasSize(2)));
        verify(service, never()).byAuthor(org.mockito.ArgumentMatchers.anyString());
    }

    @Test
    void filtersByAuthor() throws Exception {
        given(service.byAuthor("x")).willReturn(List.of(new Book(1, "A", "x")));
        mvc.perform(get("/books").param("author", "x")).andExpect(jsonPath("$", hasSize(1)));
        verify(service).byAuthor("x");
        verify(service, never()).findAll();
    }

    @Test
    void badIdTypeIs400() throws Exception {
        mvc.perform(get("/books/abc")).andExpect(status().isBadRequest());
    }
}
'''
t1 = tk("webmvc-slice-test", "@WebMvcTest Slice with a Mocked Service", "Warm-up",
    "Implement a controller and prove it with a web-layer slice test: MockMvc, @MockitoBean, BDD stubbing and interaction verification.",
    {"main/Application.java": APP, "main/Book.java": BOOK, "main/BookService.java": BSVC, "main/BookController.java": BCTL},
    {"test/BookControllerSliceTest.java": BTEST},
    ["Implement `get` and `list` in `BookController`.", "Add one more test of your own (e.g. a 404 body check).", "Explain what a slice does and does not load."],
    ["`list` with an author must never call `findAll()`.", "Type mismatch on `{id}` yields 400 without any code from you."],
    ["`@MockitoBean` (Spring Framework 6.2, Boot 3.4) replaces the older `@MockBean`.", "A web slice contains controllers, advice, converters and filters — not `@Service` beans."],
    W, ttype=TYPE)

# ------------------------------------------------------------ task 2
PROD = r'''package %PKG%;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import java.math.BigDecimal;

@Entity
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String sku;
    private String category;
    private BigDecimal price;

    protected Product() {
    }

    public Product(String sku, String category, String price) {
        this.sku = sku;
        this.category = category;
        this.price = new BigDecimal(price);
    }

    public Long getId() { return id; }
    public String getSku() { return sku; }
    public String getCategory() { return category; }
    public BigDecimal getPrice() { return price; }
}
'''
PREPO_STUB = r'''package %PKG%;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * TODO(%TAG%): replace every `default` method below with an abstract Spring Data method:
 *  - findByCategoryOrderByPriceAsc(String)   derived query
 *  - existsBySku(String)                     derived existence query
 *  - findInPriceRange(BigDecimal min, BigDecimal max) with @Query ("... where p.price between :min and :max order by p.price") and @Param
 *  - countByCategory(String)                 derived count query
 */
public interface ProductRepository extends JpaRepository<Product, Long> {

    default List<Product> findByCategoryOrderByPriceAsc(String category) {
        throw new UnsupportedOperationException("TODO(%TAG%): derived query");
    }

    default boolean existsBySku(String sku) {
        throw new UnsupportedOperationException("TODO(%TAG%): derived exists query");
    }

    default List<Product> findInPriceRange(BigDecimal min, BigDecimal max) {
        throw new UnsupportedOperationException("TODO(%TAG%): @Query between");
    }

    default long countByCategory(String category) {
        throw new UnsupportedOperationException("TODO(%TAG%): derived count query");
    }
}
'''
PREPO_SOL = r'''package %PKG%;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface ProductRepository extends JpaRepository<Product, Long> {

    List<Product> findByCategoryOrderByPriceAsc(String category);

    boolean existsBySku(String sku);

    @Query("select p from Product p where p.price between :min and :max order by p.price")
    List<Product> findInPriceRange(@Param("min") BigDecimal min, @Param("max") BigDecimal max);

    long countByCategory(String category);
}
'''
PTEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;

/** JPA slice: entities, repositories and an embedded database; each test rolls back automatically. */
@DataJpaTest
class ProductRepositoryTest {

    @Autowired TestEntityManager em;
    @Autowired ProductRepository repo;

    @BeforeEach
    void seed() {
        em.persist(new Product("P-1", "tools", "30.00"));
        em.persist(new Product("P-2", "tools", "10.00"));
        em.persist(new Product("P-3", "toys", "20.00"));
        em.flush();
        em.clear();
    }

    @Test
    void ordersByPriceWithinCategory() {
        assertThat(repo.findByCategoryOrderByPriceAsc("tools")).extracting(Product::getSku).containsExactly("P-2", "P-1");
    }

    @Test
    void existsBySku() {
        assertThat(repo.existsBySku("P-3")).isTrue();
        assertThat(repo.existsBySku("nope")).isFalse();
    }

    @Test
    void priceRangeIsInclusiveAndSorted() {
        assertThat(repo.findInPriceRange(new BigDecimal("10.00"), new BigDecimal("20.00"))).extracting(Product::getSku)
                .containsExactly("P-2", "P-3");
    }

    @Test
    void countsByCategory() {
        assertThat(repo.countByCategory("tools")).isEqualTo(2);
        assertThat(repo.countByCategory("none")).isZero();
    }

    @Test
    void sliceRollsBackBetweenTests() {
        assertThat(repo.count()).isEqualTo(3);
    }
}
'''
t2 = tk("datajpa-slice", "@DataJpaTest Slice for Repositories", "Core",
    "Turn placeholder default methods into real Spring Data queries and verify them with a repository slice on an embedded database.",
    {"main/Application.java": APP, "main/Product.java": PROD},
    {"test/ProductRepositoryTest.java": PTEST},
    ["Replace each `default` placeholder with an abstract derived or `@Query` method.", "Use `@Param` for the named parameters.", "Write one extra test for a case you think is missing."],
    ["`between` is inclusive on both ends.", "The slice rolls each test back, so seeds from one test are not visible in the next."],
    ["`TestEntityManager` is the test-friendly `EntityManager`.", "Flush and clear to force a real database round trip."],
    ["spring-boot-starter-data-jpa"], deps=H2R, ttype=TYPE)
t2["files"]["main/ProductRepository.java"] = PREPO_STUB
with_sol(t2, "main/ProductRepository.java", PREPO_SOL)

# ------------------------------------------------------------ task 3
GEXC = "package %PKG%;\n\npublic class GatewayException extends RuntimeException {\n    public GatewayException(String m) {\n        super(m);\n    }\n}\n"
GW = "package %PKG%;\n\npublic interface EmailGateway {\n    /** Returns true when the provider accepted the message. May throw GatewayException. */\n    boolean send(String to, String body);\n}\n"
UL = "package %PKG%;\n\nimport java.util.Optional;\n\npublic interface UserLookup {\n    Optional<String> findEmail(long userId);\n}\n"
NSVC = r'''package %PKG%;

import java.util.List;
import java.util.NoSuchElementException;
import org.springframework.stereotype.Service;

@Service
public class NotificationService {

    private final EmailGateway gateway;
    private final UserLookup users;

    public NotificationService(EmailGateway gateway, UserLookup users) {
        this.gateway = gateway;
        this.users = users;
    }

    /**
     * Blank/null message -> IllegalArgumentException BEFORE any collaborator is called.
     * Unknown user -> NoSuchElementException and the gateway is never called.
     * Otherwise send to the user's email; return the gateway's boolean. A GatewayException means false.
     */
    public boolean notifyUser(long userId, String message) {
        //B! validate, look up the email, call the gateway, translate GatewayException to false
        if (message == null || message.isBlank()) {
            throw new IllegalArgumentException("message");
        }
        String email = users.findEmail(userId).orElseThrow(() -> new NoSuchElementException("user " + userId));
        try {
            return gateway.send(email, message);
        } catch (GatewayException e) {
            return false;
        }
        //E!
    }

    /** Tries every id (unknown users and gateway failures are skipped, never abort the loop). Returns how many messages were accepted. */
    public int broadcast(List<Long> userIds, String message) {
        //B! loop over ids, count successes, skip unknown users
        int ok = 0;
        for (Long id : userIds) {
            try {
                if (notifyUser(id, message)) {
                    ok++;
                }
            } catch (NoSuchElementException ignored) {
                // skipped
            }
        }
        return ok;
        //E!
    }
}
'''
NTEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;

import java.util.List;
import java.util.NoSuchElementException;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

@SpringBootTest(classes = NotificationService.class)
class NotificationServiceTest {

    @Autowired NotificationService service;
    @MockitoBean EmailGateway gateway;
    @MockitoBean UserLookup users;

    @Test
    void sendsToLookedUpEmail() {
        given(users.findEmail(1)).willReturn(Optional.of("a@x.io"));
        given(gateway.send("a@x.io", "hi")).willReturn(true);
        assertThat(service.notifyUser(1, "hi")).isTrue();
        ArgumentCaptor<String> to = ArgumentCaptor.forClass(String.class);
        verify(gateway).send(to.capture(), org.mockito.ArgumentMatchers.eq("hi"));
        assertThat(to.getValue()).isEqualTo("a@x.io");
    }

    @Test
    void blankMessageTouchesNothing() {
        assertThatThrownBy(() -> service.notifyUser(1, " ")).isInstanceOf(IllegalArgumentException.class);
        verifyNoInteractions(gateway, users);
    }

    @Test
    void unknownUserNeverCallsGateway() {
        given(users.findEmail(2)).willReturn(Optional.empty());
        assertThatThrownBy(() -> service.notifyUser(2, "hi")).isInstanceOf(NoSuchElementException.class);
        verify(gateway, never()).send(anyString(), anyString());
    }

    @Test
    void gatewayFailureBecomesFalse() {
        given(users.findEmail(1)).willReturn(Optional.of("a@x.io"));
        given(gateway.send(anyString(), anyString())).willThrow(new GatewayException("down"));
        assertThat(service.notifyUser(1, "hi")).isFalse();
    }

    @Test
    void rejectedByProviderIsFalse() {
        given(users.findEmail(1)).willReturn(Optional.of("a@x.io"));
        given(gateway.send(anyString(), anyString())).willReturn(false);
        assertThat(service.notifyUser(1, "hi")).isFalse();
    }

    @Test
    void broadcastCountsOnlySuccessesAndKeepsGoing() {
        given(users.findEmail(1)).willReturn(Optional.of("a@x.io"));
        given(users.findEmail(2)).willReturn(Optional.empty());
        given(users.findEmail(3)).willReturn(Optional.of("c@x.io"));
        given(users.findEmail(4)).willReturn(Optional.of("d@x.io"));
        given(gateway.send("a@x.io", "news")).willReturn(true);
        given(gateway.send("c@x.io", "news")).willThrow(new GatewayException("boom"));
        given(gateway.send("d@x.io", "news")).willReturn(true);
        assertThat(service.broadcast(List.of(1L, 2L, 3L, 4L), "news")).isEqualTo(2);
        verify(gateway, times(3)).send(anyString(), org.mockito.ArgumentMatchers.eq("news"));
    }
}
'''
t3 = tk("mockbean-service", "Mocking Collaborators with @MockitoBean", "Core",
    "Test a service in isolation: stub with BDDMockito, capture arguments, verify absence of interactions, and simulate failures.",
    {"main/GatewayException.java": GEXC, "main/EmailGateway.java": GW, "main/UserLookup.java": UL, "main/NotificationService.java": NSVC},
    {"test/NotificationServiceTest.java": NTEST},
    ["Implement `notifyUser` following the documented order of checks.", "Implement `broadcast` so failures never abort the loop.", "List which collaborators each test needs and why."],
    ["Validation failures must not touch collaborators (`verifyNoInteractions`).", "A provider returning false and a provider throwing both mean `false`."],
    ["`@SpringBootTest(classes = ...)` builds a tiny context instead of scanning everything.", "Unstubbed Mockito methods return defaults (false, empty Optional is NOT guaranteed for Optional in older versions: stub explicitly)."],
    ["spring-boot-starter"], ttype=TYPE)

# ------------------------------------------------------------ task 4
SUCTL = r'''package %PKG%;

import java.security.Principal;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NoteController {

    @GetMapping("/me")
    public String me(Principal principal) {
        return principal.getName();
    }

    @PostMapping("/notes")
    @ResponseStatus(HttpStatus.CREATED)
    public String create() {
        return "created";
    }

    @GetMapping("/admin")
    public String admin() {
        return "admin";
    }
}
'''
SUCFG = r'''package %PKG%;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

/** PROVIDED (do not edit). CSRF stays ON (default), so unsafe methods need a token. */
@Configuration
@EnableWebSecurity
public class AppSecurityConfig {

    @Bean
    SecurityFilterChain chain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(a -> a.requestMatchers("/admin").hasRole("ADMIN").anyRequest().authenticated())
                .httpBasic(Customizer.withDefaults());
        return http.build();
    }

    @Bean
    UserDetailsService users() {
        return new InMemoryUserDetailsManager(User.withUsername("ann").password("{noop}pw").roles("USER").build());
    }
}
'''
SUPPORT = r'''package %PKG%;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.httpBasic;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;

import org.springframework.test.web.servlet.request.RequestPostProcessor;

/**
 * Reusable helpers that keep security noise out of test bodies.
 * Every method returns a RequestPostProcessor usable as `mvc.perform(get("/x").with(...))`.
 */
public final class SecurityTestSupport {

    private SecurityTestSupport() {
    }

    /** Authenticated principal `name` with the single role USER. */
    public static RequestPostProcessor asUser(String name) {
        //B! build with SecurityMockMvcRequestPostProcessors.user(name).roles("USER")
        return user(name).roles("USER");
        //E!
    }

    /** Authenticated principal "admin" with roles ADMIN and USER. */
    public static RequestPostProcessor asAdmin() {
        //B! user("admin") with roles ADMIN and USER
        return user("admin").roles("ADMIN", "USER");
        //E!
    }

    /** Same as asUser(name) but ALSO carrying a valid CSRF token (for POST/PUT/DELETE). */
    public static RequestPostProcessor asUserWithCsrf(String name) {
        //B! combine asUser(name) and csrf()
        return request -> csrf().postProcessRequest(asUser(name).postProcessRequest(request));
        //E!
    }

    /** HTTP Basic credentials header. */
    public static RequestPostProcessor basic(String username, String password) {
        //B! delegate to httpBasic
        return httpBasic(username, password);
        //E!
    }
}
'''
SUTEST = r'''package %PKG%;

import static %PKG%.SecurityTestSupport.asAdmin;
import static %PKG%.SecurityTestSupport.asUser;
import static %PKG%.SecurityTestSupport.asUserWithCsrf;
import static %PKG%.SecurityTestSupport.basic;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(NoteController.class)
@Import(AppSecurityConfig.class)
class SecurityTestSupportTest {

    @Autowired MockMvc mvc;

    @Test
    void anonymousIs401() throws Exception {
        mvc.perform(get("/me")).andExpect(status().isUnauthorized());
    }

    @Test
    void userHelperSetsPrincipal() throws Exception {
        mvc.perform(get("/me").with(asUser("zed"))).andExpect(status().isOk()).andExpect(content().string("zed"));
    }

    @Test
    void userIsNotAdmin() throws Exception {
        mvc.perform(get("/admin").with(asUser("zed"))).andExpect(status().isForbidden());
    }

    @Test
    void adminHelperOpensAdmin() throws Exception {
        mvc.perform(get("/admin").with(asAdmin())).andExpect(status().isOk());
    }

    @Test
    void postWithoutCsrfIsForbidden() throws Exception {
        mvc.perform(post("/notes").with(asUser("zed"))).andExpect(status().isForbidden());
    }

    @Test
    void postWithCsrfHelperWorks() throws Exception {
        mvc.perform(post("/notes").with(asUserWithCsrf("zed"))).andExpect(status().isCreated());
    }

    @Test
    void basicHelperAuthenticatesRealUser() throws Exception {
        mvc.perform(get("/me").with(basic("ann", "pw"))).andExpect(content().string("ann"));
        mvc.perform(get("/me").with(basic("ann", "wrong"))).andExpect(status().isUnauthorized());
    }
}
'''
t4 = tk("security-test-util", "Reusable Security Test Helpers", "Challenge",
    "Write a small test-support class around spring-security-test post-processors, then use it to test a secured controller with CSRF enabled.",
    {"main/Application.java": APP, "main/NoteController.java": SUCTL, "main/AppSecurityConfig.java": SUCFG, "test/SecurityTestSupport.java": SUPPORT},
    {"test/SecurityTestSupportTest.java": SUTEST},
    ["Implement the four helper methods in `SecurityTestSupport`.", "Notice the stub lives in `src/test/java`: helpers are test code, not production code.", "Add a helper of your own, e.g. `asRole(String...)`."],
    ["POSTs fail with 403 unless a CSRF token accompanies the request.", "Wrong Basic credentials give 401 (authentication), a missing role gives 403."],
    ["`user(name).roles(..)` fabricates an authentication without a UserDetailsService lookup.", "`csrf()` adds a valid token for the request."],
    W + ["spring-boot-starter-security"], deps=[SECTEST], ttype=TYPE)

# ------------------------------------------------------------ theory
topics = [
    T("The test pyramid in Spring Boot",
      "Fast, focused tests at the bottom (plain JUnit on POJOs), **slice tests** in the middle (`@WebMvcTest`, `@DataJpaTest`, `@JsonTest`, `@RestClientTest`) loading only one layer, and a few full `@SpringBootTest` integration tests at the top. Slices use *test auto-configuration* so only relevant beans start.",
      "Full-context tests take seconds each; a suite of hundreds becomes unusable. Slices give layer-specific confidence in milliseconds.",
      ["Fast feedback", "Failures point to one layer", "Less accidental coupling", "Context caching reuses slices with identical configuration"],
      ["Slices don't prove wiring between layers", "Each distinct mock set creates a new cached context", "Easy to over-mock"],
      "Everything as `@SpringBootTest`: slow CI, flaky ports/databases, and failures that don't say which layer broke.",
      "```java\n@WebMvcTest(BookController.class)  class BookControllerSliceTest { @Autowired MockMvc mvc; @MockitoBean BookService service; }\n@DataJpaTest                      class ProductRepositoryTest { @Autowired TestEntityManager em; }\n@SpringBootTest                   class ApplicationIT { /* few, critical journeys */ }\n```",
      [("JSON slice", "java", "@JsonTest class EventJsonTest { @Autowired JacksonTester<Event> json; }"),
       ("Rule of thumb", "text", "Many unit tests, some slices, few integration tests"),
       ("Context caching", "text", "Same annotations + same @MockitoBean set => context reused across classes")],
      [("What does @WebMvcTest load?", "Controllers, advice, converters, filters — not services/repositories."),
       ("Why slices?", "Speed and focus."),
       ("What is context caching?", "Spring reuses an application context for tests with identical configuration.")]),
    T("@WebMvcTest and MockMvc",
      "`@WebMvcTest` starts the Spring MVC infrastructure without a server. `MockMvc` performs requests through the full DispatcherServlet pipeline (mapping, binding, validation, advice, converters) and asserts on status, headers and JSON paths. Collaborators are replaced with `@MockitoBean` (Boot 3.4+/Spring 6.2; formerly `@MockBean`).",
      "Controller behaviour — status codes, validation errors, serialization — is where most HTTP contract bugs live.",
      ["No port, no server, milliseconds per test", "Full MVC behaviour including content negotiation", "jsonPath assertions"],
      ["Doesn't test servlet container behaviour", "Needs explicit imports for security/config classes", "Mocks can drift from real behaviour"],
      "Calling controller methods directly in unit tests misses annotations, binding and advice, so a missing `@RequestBody` passes tests but fails in production.",
      "```java\ngiven(service.find(1)).willReturn(Optional.of(book));\nmvc.perform(get(\"/books/1\")).andExpect(status().isOk()).andExpect(jsonPath(\"$.title\").value(\"Dune\"));\nverify(service).find(1);\n```",
      [("Import config", "java", "@WebMvcTest(Ctl.class) @Import(SecurityConfig.class)"),
       ("Send JSON", "java", "post(\"/x\").contentType(APPLICATION_JSON).content(\"{...}\")"),
       ("Print on failure", "java", "mvc.perform(...).andDo(print())")],
      [("MockMvc vs TestRestTemplate?", "MockMvc: no server, mock servlet; TestRestTemplate: real HTTP on a port."),
       ("Replacement for @MockBean?", "@MockitoBean (Boot 3.4+)."),
       ("How to include a @Configuration in a slice?", "@Import it.")]),
    T("@DataJpaTest and repository testing",
      "`@DataJpaTest` configures entities, Spring Data repositories, an embedded database (H2) and `TestEntityManager`; each test is `@Transactional` and rolls back. Use `flush()` + `clear()` to force SQL and reload fresh instances. For production-like dialect behaviour use Testcontainers with `@AutoConfigureTestDatabase(replace = NONE)`.",
      "Derived query names and `@Query` strings are code that only fail at runtime. A repository slice catches typos immediately.",
      ["Fast, isolated DB tests", "Automatic rollback", "Validates mapping and queries"],
      ["H2 differs from production databases", "Rollback hides commit-time problems (constraints deferred, `@Transactional` boundaries)", "Forgetting flush/clear gives false positives from the first-level cache"],
      "Tests that only call `save()` and `findById()` inside one persistence context never hit the database and pass even with broken mappings.",
      "```java\n@DataJpaTest class ProductRepositoryTest {\n  @Autowired TestEntityManager em; @Autowired ProductRepository repo;\n  @Test void query() { em.persist(p); em.flush(); em.clear(); assertThat(repo.findByCategory(\"x\")).hasSize(1); }\n}\n```",
      [("Use real DB", "java", "@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)"),
       ("Show SQL", "text", "spring.jpa.show-sql=true or logging.level.org.hibernate.SQL=DEBUG"),
       ("Testcontainers", "java", "@ServiceConnection static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>(\"postgres:16\");")],
      [("Why flush and clear?", "To force SQL and bypass the first-level cache."),
       ("Does @DataJpaTest commit?", "No, it rolls back."),
       ("How to test against Postgres?", "Testcontainers with @ServiceConnection.")]),
    T("Mockito essentials with Spring",
      "Mockito creates test doubles: **mock** (programmable, records calls), **spy** (real object, partially stubbed), **captor** (captures arguments). Stub with `given(...).willReturn/willThrow`; verify with `verify(mock).method(...)`, `times`, `never`, `verifyNoInteractions`. `@MockitoBean` registers a mock in the Spring context (replacing any bean of that type); `@MockitoSpyBean` wraps the real bean.",
      "Services with collaborators (gateways, repositories) are tested for decisions and interactions without sending emails or touching a database.",
      ["Isolates the unit", "Simulates failures that are hard to trigger", "Verifies ordering and absence of calls"],
      ["Over-specified verification makes refactors painful", "Mocking types you don't own (JPA, HTTP clients) gives false confidence", "Context pollution: each unique mock combination creates a new context"],
      "Verifying every call of every collaborator couples tests to implementation; unstubbed mocks silently return null/false causing misleading passes.",
      "```java\ngiven(users.findEmail(1)).willReturn(Optional.of(\"a@x.io\"));\ngiven(gateway.send(anyString(), anyString())).willThrow(new GatewayException(\"down\"));\nverify(gateway, never()).send(anyString(), anyString());\nArgumentCaptor<String> c = ArgumentCaptor.forClass(String.class);\n```",
      [("Consecutive results", "java", "given(m.next()).willReturn(1, 2, 3);"),
       ("Spy", "java", "@MockitoSpyBean RealService service;"),
       ("No more interactions", "java", "verifyNoMoreInteractions(gateway);")],
      [("Mock vs spy?", "Mock replaces behaviour entirely; spy wraps a real object."),
       ("Why avoid mocking everything?", "Tests become brittle and verify implementation not behaviour."),
       ("What does verifyNoInteractions assert?", "That the mock was never called.")]),
    T("spring-security-test utilities",
      "`spring-security-test` supplies `@WithMockUser`, `@WithUserDetails`, and MockMvc **request post-processors**: `user(..)`, `httpBasic(..)`, `csrf()`, `jwt()`. They set up an authenticated context without executing the login flow. With CSRF enabled, unsafe methods need `.with(csrf())`.",
      "Security rules need tests for each role and for anonymous access; ceremony must not drown the intent of the test.",
      ["Fast authorization tests", "No real login needed", "Wrap in helper methods for readability"],
      ["Fabricated principals bypass your `UserDetailsService`", "Easy to forget CSRF and chase confusing 403s", "Method security needs a full or partial context, not just a slice"],
      "Disabling security in tests (`addFilters = false`) removes exactly what you wanted to verify.",
      "```java\nmvc.perform(post(\"/notes\").with(user(\"ann\").roles(\"USER\")).with(csrf())).andExpect(status().isCreated());\nmvc.perform(get(\"/admin\").with(httpBasic(\"ann\", \"pw\")));\n```",
      [("Annotation style", "java", "@Test @WithMockUser(username = \"ann\", roles = \"ADMIN\") void admin() { ... }"),
       ("JWT resource server", "java", "mvc.perform(get(\"/api\").with(jwt().authorities(new SimpleGrantedAuthority(\"SCOPE_read\"))))"),
       ("Anti-pattern", "java", "@AutoConfigureMockMvc(addFilters = false) // removes security from the test")],
      [("Why 403 on POST in tests?", "CSRF token missing."),
       ("@WithMockUser vs user() post-processor?", "Annotation sets context for the whole test; post-processor is per request."),
       ("Why not addFilters=false?", "It disables the security you are testing.")]),
]

day(39, "Spring Testing: Slices, Mockito, and Security Tests", "Spring Boot",
    "Fast, layered tests for controllers, repositories, services, and secured endpoints",
    ["Choose between unit, slice and integration tests", "Test controllers with @WebMvcTest and MockMvc", "Test repositories with @DataJpaTest", "Use @MockitoBean, captors and verification", "Test authorization with spring-security-test"],
    ["Day 30–38 REST, JPA, Security"],
    topics, [t1, t2, t3, t4],
    [("What are slice tests?", "Tests loading only one layer's beans via test auto-configuration."),
     ("@MockBean vs @MockitoBean?", "@MockitoBean is the Spring 6.2 / Boot 3.4 replacement."),
     ("Why flush and clear in JPA tests?", "To hit the database rather than the first-level cache."),
     ("When use @SpringBootTest?", "A few end-to-end wiring tests."),
     ("How to test a secured endpoint?", "Use user()/httpBasic()/csrf() post-processors or @WithMockUser.")],
    ["Everything as @SpringBootTest.", "Mocking types you don't own.", "Not clearing the persistence context.", "Disabling security filters in tests."],
    ["Spring Boot reference: Testing", "Mockito documentation", "Spring Security reference: Testing"],
    [("Slice test", "Test loading only one layer"), ("MockMvc", "Server-less MVC test harness"), ("Mock", "Programmable test double"), ("Captor", "Mockito argument capture"), ("Post-processor", "Customizes a MockMvc request")],
    "2–3 h theory + 3–5 h tasks", spring=True)
