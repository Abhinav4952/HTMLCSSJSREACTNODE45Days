from sx import *

S = ["spring-boot-starter-data-jpa"]
DEPS = [H2]

HDR = '''package %PKG%;

import jakarta.persistence.*;
import java.util.*;

'''
STATS = "spring.jpa.properties.hibernate.generate_statistics=true\n"

# ------------------------------------------------------------ task 1
AUT = HDR + r'''@Entity
@Table(name = "authors")
public class Author {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    @OneToMany(mappedBy = "author", cascade = CascadeType.ALL)
    private List<Book> books = new ArrayList<>();

    protected Author() {
    }

    public Author(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public List<Book> getBooks() {
        return books;
    }

    public void addBook(Book b) {
        books.add(b);
        b.setAuthor(this);
    }
}
'''
BK = HDR + r'''@Entity
@Table(name = "books")
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id")
    private Author author;

    protected Book() {
    }

    public Book(String title) {
        this.title = title;
    }

    public String getTitle() {
        return title;
    }

    void setAuthor(Author a) {
        this.author = a;
    }
}
'''
AREPO = r'''package %PKG%;

import java.util.List;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface AuthorRepository extends JpaRepository<Author, Long> {

    //A! declare two methods that load authors TOGETHER with their books in ONE statement:
    //   findAllWithBooks()  -> JPQL "select distinct a from Author a join fetch a.books"
    //   findAllWithGraph()  -> @EntityGraph(attributePaths = "books") + @Query("select distinct a from Author a")
    @Query("select distinct a from Author a join fetch a.books")
    List<Author> findAllWithBooks();

    @EntityGraph(attributePaths = "books")
    @Query("select distinct a from Author a")
    List<Author> findAllWithGraph();
    //E!
}
'''
REPORT = r'''package %PKG%;

import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import org.springframework.stereotype.Component;

@Component
public class AuthorReport {

    private final AuthorRepository repository;

    public AuthorReport(AuthorRepository repository) {
        this.repository = repository;
    }

    /** PROVIDED: the classic N+1 trap (1 query for authors + 1 per author for books). */
    public Map<String, Integer> bookCountsNaive() {
        Map<String, Integer> out = new TreeMap<>();
        for (Author a : repository.findAll()) {
            out.put(a.getName(), a.getBooks().size());
        }
        return out;
    }

    /** author name -> number of books, using ONE SQL statement (join fetch). */
    public Map<String, Integer> bookCountsJoinFetch() {
        //B! use repository.findAllWithBooks()
        return toCounts(repository.findAllWithBooks());
        //E!
    }

    /** author name -> number of books, using ONE SQL statement (entity graph). */
    public Map<String, Integer> bookCountsEntityGraph() {
        //B! use repository.findAllWithGraph()
        return toCounts(repository.findAllWithGraph());
        //E!
    }

    private static Map<String, Integer> toCounts(List<Author> authors) {
        Map<String, Integer> out = new TreeMap<>();
        for (Author a : authors) {
            out.put(a.getName(), a.getBooks().size());
        }
        return out;
    }
}
'''
T1 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Map;
import org.hibernate.SessionFactory;
import org.hibernate.stat.Statistics;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(AuthorReport.class)
class NPlusOneTest {

    @Autowired
    TestEntityManager em;
    @Autowired
    AuthorReport report;

    Statistics stats;

    @BeforeEach
    void seed() {
        for (int i = 1; i <= 5; i++) {
            Author a = new Author("author" + i);
            for (int j = 1; j <= 3; j++) {
                a.addBook(new Book("book" + i + "-" + j));
            }
            em.persist(a);
        }
        em.flush();
        em.clear();
        stats = em.getEntityManager().getEntityManagerFactory().unwrap(SessionFactory.class).getStatistics();
        stats.clear();
    }

    @Test
    void naiveVersionExecutesNPlusOneStatements() {
        Map<String, Integer> counts = report.bookCountsNaive();
        assertThat(counts).hasSize(5).containsEntry("author1", 3);
        assertThat(stats.getPrepareStatementCount()).isEqualTo(6);
    }

    @Test
    void joinFetchUsesOneStatement() {
        Map<String, Integer> counts = report.bookCountsJoinFetch();
        assertThat(counts).hasSize(5).containsEntry("author3", 3);
        assertThat(stats.getPrepareStatementCount()).isEqualTo(1);
    }

    @Test
    void entityGraphUsesOneStatement() {
        Map<String, Integer> counts = report.bookCountsEntityGraph();
        assertThat(counts).hasSize(5).containsEntry("author5", 3);
        assertThat(stats.getPrepareStatementCount()).isEqualTo(1);
    }

    @Test
    void bothOptimizedVersionsAgree() {
        assertThat(report.bookCountsJoinFetch()).isEqualTo(report.bookCountsEntityGraph());
    }
}
'''
a1 = tk("n-plus-one-join-fetch", "Detect and Fix N+1 Queries", "Warm-up",
    "Measure the N+1 problem with Hibernate statistics and fix it with join fetch and an entity graph.",
    {"main/Application.java": APP, "main/Author.java": AUT, "main/Book.java": BK, "main/AuthorRepository.java": AREPO, "main/AuthorReport.java": REPORT},
    {"test/NPlusOneTest.java": T1, "tres/application.properties": h2props("35", "1", STATS)},
    ["Add `findAllWithBooks` (join fetch) and `findAllWithGraph` (entity graph) to the repository.", "Implement the two optimized report methods; observe the statement counts."],
    ["`distinct` removes duplicate parents caused by the join.", "Never `join fetch` two collections (cartesian product / MultipleBagFetchException) and do not paginate in memory over fetched collections."],
    ["Statistics are cleared after seeding so only the report is counted.", "`@EntityGraph` can also be put directly on derived query methods."],
    S, deps=DEPS)

# ------------------------------------------------------------ task 2
BA = HDR + r'''import java.math.BigDecimal;

@Entity
@Table(name = "bank_accounts")
public class BankAccount {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String owner;

    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal balance;

    protected BankAccount() {
    }

    public BankAccount(String owner, String balance) {
        this.owner = owner;
        this.balance = new BigDecimal(balance);
    }

    public Long getId() {
        return id;
    }

    public String getOwner() {
        return owner;
    }

    public BigDecimal getBalance() {
        return balance;
    }

    public void setBalance(BigDecimal balance) {
        this.balance = balance;
    }
}
'''
BA = BA.replace("import java.util.*;\n\nimport java.math.BigDecimal;", "import java.math.BigDecimal;\nimport java.util.*;")
BAR = "package %PKG%;\n\nimport org.springframework.data.jpa.repository.JpaRepository;\n\npublic interface BankAccountRepository extends JpaRepository<BankAccount, Long> {\n}\n"
INSUF = "package %PKG%;\n\npublic class InsufficientFundsException extends RuntimeException {\n    public InsufficientFundsException(String message) {\n        super(message);\n    }\n}\n"
AUDITEX = "package %PKG%;\n\n/** CHECKED exception: Spring does NOT roll back for it by default. */\npublic class AuditUnavailableException extends Exception {\n    public AuditUnavailableException(String message) {\n        super(message);\n    }\n}\n"
TSVC = r'''package %PKG%;

import java.math.BigDecimal;
import java.util.NoSuchElementException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class TransferService {

    private final BankAccountRepository repository;

    public TransferService(BankAccountRepository repository) {
        this.repository = repository;
    }

    private BankAccount find(long id) {
        return repository.findById(id).orElseThrow(() -> new NoSuchElementException("Account " + id + " not found"));
    }

    /**
     * Moves money atomically.
     * 1. load source; if balance < amount -> InsufficientFundsException (nothing changed)
     * 2. debit the source and saveAndFlush it
     * 3. load the target (unknown id -> NoSuchElementException) and credit it
     * If ANY step fails after step 2, the debit must be rolled back.
     */
    //A! make this method run in a transaction
    @Transactional
    //E!
    public void transfer(long fromId, long toId, BigDecimal amount) {
        //B! implement steps 1-3
        BankAccount source = find(fromId);
        if (source.getBalance().compareTo(amount) < 0) {
            throw new InsufficientFundsException("Insufficient funds in account " + fromId);
        }
        source.setBalance(source.getBalance().subtract(amount));
        repository.saveAndFlush(source);
        BankAccount target = find(toId);
        target.setBalance(target.getBalance().add(amount));
        repository.save(target);
        //E!
    }

    /**
     * Same as transfer, then calls the audit system which is down: always throws AuditUnavailableException
     * AFTER the money moved. The whole transfer must be rolled back anyway.
     */
    //A! transactional, rolling back for the CHECKED exception too (rollbackFor)
    @Transactional(rollbackFor = AuditUnavailableException.class)
    //E!
    public void transferWithAudit(long fromId, long toId, BigDecimal amount) throws AuditUnavailableException {
        //B! call transfer logic (not through a proxy: inline the steps or call this.transfer) then throw AuditUnavailableException
        transfer(fromId, toId, amount);
        throw new AuditUnavailableException("audit service down");
        //E!
    }

    /** Read-only lookup. */
    //A! read-only transaction
    @Transactional(readOnly = true)
    //E!
    public BigDecimal balanceOf(long id) {
        //B! return the balance
        return find(id).getBalance();
        //E!
    }
}
'''
T2 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.math.BigDecimal;
import java.util.NoSuchElementException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class TransferServiceTest {

    @Autowired
    TransferService service;
    @Autowired
    BankAccountRepository repository;

    long a, b;

    @BeforeEach
    void setUp() {
        repository.deleteAll();
        a = repository.save(new BankAccount("Ann", "100.00")).getId();
        b = repository.save(new BankAccount("Bob", "20.00")).getId();
    }

    @Test
    void successfulTransferMovesMoney() {
        service.transfer(a, b, new BigDecimal("30.00"));
        assertThat(service.balanceOf(a)).isEqualByComparingTo("70");
        assertThat(service.balanceOf(b)).isEqualByComparingTo("50");
    }

    @Test
    void insufficientFundsChangesNothing() {
        assertThatThrownBy(() -> service.transfer(a, b, new BigDecimal("500"))).isInstanceOf(InsufficientFundsException.class);
        assertThat(service.balanceOf(a)).isEqualByComparingTo("100");
        assertThat(service.balanceOf(b)).isEqualByComparingTo("20");
    }

    @Test
    void failureAfterDebitRollsEverythingBack() {
        assertThatThrownBy(() -> service.transfer(a, 99999L, new BigDecimal("30"))).isInstanceOf(NoSuchElementException.class);
        assertThat(service.balanceOf(a)).isEqualByComparingTo("100");
    }

    @Test
    void checkedExceptionRollsBackBecauseOfRollbackFor() {
        assertThatThrownBy(() -> service.transferWithAudit(a, b, new BigDecimal("10")))
                .isInstanceOf(AuditUnavailableException.class);
        assertThat(service.balanceOf(a)).isEqualByComparingTo("100");
        assertThat(service.balanceOf(b)).isEqualByComparingTo("20");
    }

    @Test
    void unknownAccountBalanceThrows() {
        assertThatThrownBy(() -> service.balanceOf(424242L)).isInstanceOf(NoSuchElementException.class);
    }
}
'''
a2 = tk("transactional-transfer", "@Transactional: Atomic Transfer and Rollback Rules", "Core",
    "Make a money transfer atomic with @Transactional and learn that checked exceptions need rollbackFor.",
    {"main/Application.java": APP, "main/BankAccount.java": BA, "main/BankAccountRepository.java": BAR,
     "main/InsufficientFundsException.java": INSUF, "main/AuditUnavailableException.java": AUDITEX, "main/TransferService.java": TSVC},
    {"test/TransferServiceTest.java": T2, "tres/application.properties": h2props("35", "2")},
    ["Add `@Transactional` to `transfer`, `@Transactional(rollbackFor=...)` to `transferWithAudit`, `readOnly` to `balanceOf`.", "Implement the three method bodies."],
    ["`RuntimeException`/`Error` roll back by default; checked exceptions do not.", "Self-invocation (`this.transfer`) bypasses the proxy: the outer annotation must carry the transaction."],
    ["`saveAndFlush` makes the debit visible to the database inside the transaction - and proves rollback.", "Tests deliberately are not `@Transactional`; otherwise the test transaction would hide the behavior."],
    S, deps=DEPS)

# ------------------------------------------------------------ task 3
AUDIT_CFG = r'''package %PKG%;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

//A! turn on JPA auditing for the application
@Configuration
@EnableJpaAuditing
//E!
public class AuditConfig {
}
'''
PRODUCT = HDR + r'''import java.time.LocalDateTime;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

//A! register the auditing listener on the entity
@EntityListeners(AuditingEntityListener.class)
//E!
@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    private int stock;

    //A! optimistic locking version column
    @Version
    //E!
    private Long version;

    //A! creation timestamp (not updatable)
    @CreatedDate
    @Column(name = "created_at", updatable = false)
    //E!
    private LocalDateTime createdAt;

    //A! last modification timestamp
    @LastModifiedDate
    @Column(name = "updated_at")
    //E!
    private LocalDateTime updatedAt;

    protected Product() {
    }

    public Product(String name, int stock) {
        this.name = name;
        this.stock = stock;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getStock() {
        return stock;
    }

    public void setStock(int stock) {
        this.stock = stock;
    }

    public Long getVersion() {
        return version;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
}
'''
PREPO = "package %PKG%;\n\nimport org.springframework.data.jpa.repository.JpaRepository;\n\npublic interface ProductRepository extends JpaRepository<Product, Long> {\n}\n"
STOCK = r'''package %PKG%;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class StockService {

    private final ProductRepository repository;

    public StockService(ProductRepository repository) {
        this.repository = repository;
    }

    @Transactional
    public Product create(String name, int stock) {
        //B! save a new product and return it
        return repository.saveAndFlush(new Product(name, stock));
        //E!
    }

    /** Changes stock by delta inside one transaction. Result below zero -> IllegalStateException("Stock cannot be negative"). */
    @Transactional
    public Product adjust(long id, int delta) {
        //B! load, apply delta with the rule, flush and return
        Product p = repository.findById(id).orElseThrow();
        int next = p.getStock() + delta;
        if (next < 0) {
            throw new IllegalStateException("Stock cannot be negative");
        }
        p.setStock(next);
        return repository.saveAndFlush(p);
        //E!
    }

    /** Saves a possibly stale, detached copy (merge). A stale version must surface as an optimistic locking failure. */
    @Transactional
    public Product saveDetached(Product detached) {
        //B! merge via repository.saveAndFlush
        return repository.saveAndFlush(detached);
        //E!
    }

    @Transactional(readOnly = true)
    public Product get(long id) {
        //B! load or throw
        return repository.findById(id).orElseThrow();
        //E!
    }
}
'''
T3 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.orm.ObjectOptimisticLockingFailureException;

@SpringBootTest
class VersionAndAuditingTest {

    @Autowired
    StockService service;

    @Test
    void newProductStartsAtVersionZeroWithAuditTimestamps() {
        Product p = service.create("Pen", 10);
        assertThat(p.getVersion()).isZero();
        assertThat(p.getCreatedAt()).isNotNull();
        assertThat(p.getUpdatedAt()).isNotNull();
    }

    @Test
    void everyUpdateBumpsVersionAndLastModified() throws Exception {
        Product p = service.create("Pen", 10);
        Thread.sleep(5);
        Product after = service.adjust(p.getId(), -3);
        assertThat(after.getStock()).isEqualTo(7);
        assertThat(after.getVersion()).isEqualTo(1);
        assertThat(after.getUpdatedAt()).isAfter(p.getUpdatedAt());
        assertThat(after.getCreatedAt()).isEqualTo(service.get(p.getId()).getCreatedAt());
    }

    @Test
    void staleDetachedCopyIsRejected() {
        Product stale = service.create("Pen", 10);
        service.adjust(stale.getId(), 5);                 // someone else updates: version 1
        stale.setName("Renamed");
        assertThatThrownBy(() -> service.saveDetached(stale)).isInstanceOf(ObjectOptimisticLockingFailureException.class);
        assertThat(service.get(stale.getId()).getName()).isEqualTo("Pen");
    }

    @Test
    void freshCopyCanBeSaved() {
        Product p = service.create("Pen", 10);
        Product fresh = service.get(p.getId());
        fresh.setName("Pencil");
        Product saved = service.saveDetached(fresh);
        assertThat(saved.getName()).isEqualTo("Pencil");
        assertThat(saved.getVersion()).isEqualTo(1);
    }

    @Test
    void businessRuleKeepsStockNonNegative() {
        Product p = service.create("Pen", 2);
        assertThatThrownBy(() -> service.adjust(p.getId(), -3)).isInstanceOf(IllegalStateException.class).hasMessage("Stock cannot be negative");
        assertThat(service.get(p.getId()).getStock()).isEqualTo(2);
    }
}
'''
a3 = tk("version-and-auditing", "Optimistic Locking and JPA Auditing", "Core",
    "Detect lost updates with @Version and stamp entities automatically with @CreatedDate/@LastModifiedDate.",
    {"main/Application.java": APP, "main/AuditConfig.java": AUDIT_CFG, "main/Product.java": PRODUCT, "main/ProductRepository.java": PREPO, "main/StockService.java": STOCK},
    {"test/VersionAndAuditingTest.java": T3, "tres/application.properties": h2props("35", "3")},
    ["Enable auditing (`@EnableJpaAuditing`) and register `AuditingEntityListener` on `Product`.", "Annotate `version`, `createdAt`, `updatedAt`.", "Implement `StockService`."],
    ["A stale detached copy must raise `ObjectOptimisticLockingFailureException`.", "`createdAt` must never change on update (`updatable = false`)."],
    ["`@Version` can be `Long`, `Integer` or a timestamp; null means new.", "Auditing needs both the listener and `@EnableJpaAuditing`."],
    S, deps=DEPS)

# ------------------------------------------------------------ task 4
ART = HDR + r'''@Entity
@Table(name = "articles")
public class Article {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 200)
    private String title;

    @Column(nullable = false, length = 20)
    private String status = "DRAFT";

    protected Article() {
    }

    public Article(String title) {
        this.title = title;
    }

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getStatus() {
        return status;
    }

    public void publish() {
        this.status = "PUBLISHED";
    }
}
'''
AREP = "package %PKG%;\n\nimport org.springframework.data.jpa.repository.JpaRepository;\n\npublic interface ArticleRepository extends JpaRepository<Article, Long> {\n}\n"
V1 = '''-- TODO(%TAG%): migration V1 - create table articles (id bigint generated by default as identity primary key,
--              title varchar(200) not null). Statements end with a semicolon.
'''
V1S = "create table articles (\n    id bigint generated by default as identity primary key,\n    title varchar(200) not null\n);\n"
V2 = '''-- TODO(%TAG%): migration V2 - add column status varchar(20) not null default 'DRAFT' to articles (ALTER TABLE ... ADD COLUMN).
--              Existing rows must get DRAFT. Never edit V1 once applied: add a NEW migration instead.
'''
V2S = "alter table articles add column status varchar(20) not null default 'DRAFT';\n"
T4 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;

@SpringBootTest
class FlywayMigrationTest {

    @Autowired
    ArticleRepository repository;
    @Autowired
    JdbcTemplate jdbc;

    @org.junit.jupiter.api.BeforeEach
    void clean() {
        repository.deleteAll();
    }

    @Test
    void bothMigrationsWereApplied() {
        Integer applied = jdbc.queryForObject("select count(*) from flyway_schema_history where success = true and \"version\" is not null", Integer.class);
        assertThat(applied).isEqualTo(2);
        String versions = jdbc.queryForList("select \"version\" from flyway_schema_history where \"version\" is not null order by installed_rank", String.class).toString();
        assertThat(versions).isEqualTo("[1, 2]");
    }

    @Test
    void hibernateOnlyValidatesBecauseFlywayOwnsTheSchema() {
        assertThat(repository.count()).isZero();
    }

    @Test
    void statusColumnDefaultsToDraft() {
        jdbc.update("insert into articles(title) values ('From SQL')");
        Article a = repository.findAll().get(0);
        assertThat(a.getStatus()).isEqualTo("DRAFT");
    }

    @Test
    void entityRoundTrip() {
        Article a = new Article("Hello");
        a.publish();
        Article saved = repository.saveAndFlush(a);
        assertThat(repository.findById(saved.getId()).orElseThrow().getStatus()).isEqualTo("PUBLISHED");
    }
}
'''
props4 = h2props("35", "4").replace("create-drop", "validate") + "spring.flyway.enabled=true\n"
a4 = tk("flyway-migrations", "Flyway Versioned Migrations", "Challenge",
    "Replace Hibernate schema generation with versioned Flyway migrations: write V1 and V2 and let Hibernate only validate.",
    {"main/Application.java": APP, "main/Article.java": ART, "main/ArticleRepository.java": AREP},
    {"test/FlywayMigrationTest.java": T4, "tres/application.properties": props4},
    ["Write `V1__create_articles.sql` under `src/main/resources/db/migration`.", "Write `V2__add_article_status.sql` adding the status column with a default."],
    ["File names follow `V<version>__<description>.sql` (two underscores).", "Applied migrations are immutable: Flyway checksums them.", "`ddl-auto=validate` fails fast when SQL and entity disagree."],
    ["`not null default 'DRAFT'` fills existing rows.", "Tests run against H2 in PostgreSQL mode; keep SQL portable."],
    S + [], deps=DEPS + [dep("org.flywaydb", "flyway-core")],
    extra={"res/db/migration/V1__create_articles.sql": V1, "res/db/migration/V2__add_article_status.sql": V2})
a4["sol"]["res/db/migration/V1__create_articles.sql"] = V1S
a4["sol"]["res/db/migration/V2__add_article_status.sql"] = V2S

topics = [
    T("The N+1 problem, join fetch and entity graphs",
      "N+1 happens when one query loads N parents and then each parent's lazy association triggers another query (1 + N statements). Fixes: `join fetch` in JPQL, `@EntityGraph(attributePaths=...)`, batch fetching (`hibernate.default_batch_fetch_size`), or projections that fetch only what is needed.",
      "It is the most common JPA performance bug: it looks fine with 5 rows in development and melts with 5,000 in production. Detecting it early (statistics, SQL logs, tests) is a core backend skill.",
      ["Single round trip for the needed graph", "Fix is local to the repository", "Entity graphs keep JPQL clean", "Batch fetching is a global safety net"],
      ["Join fetching a collection duplicates parent rows (use distinct / Hibernate 6 dedups)", "Fetching two collections at once creates cartesian products (`MultipleBagFetchException`)", "Cannot paginate fetched collections in the database (in-memory paging warning HHH90003004)"],
      "Looping over `findAll()` and calling `getBooks().size()` runs one query per author. Switching everything to EAGER makes it worse: unrelated queries load graphs nobody asked for.",
      "```java\n@Query(\"select distinct a from Author a join fetch a.books\")\nList<Author> findAllWithBooks();\n\n@EntityGraph(attributePaths = \"books\")\n@Query(\"select distinct a from Author a\")\nList<Author> findAllWithGraph();\n```\nEnable counting in tests: `spring.jpa.properties.hibernate.generate_statistics=true` and `sessionFactory.getStatistics().getPrepareStatementCount()`.",
      [("Spot it in logs", "properties", "spring.jpa.show-sql=true\nlogging.level.org.hibernate.SQL=DEBUG"),
       ("Batch fetching", "properties", "spring.jpa.properties.hibernate.default_batch_fetch_size=50"),
       ("Page parents, fetch children second", "java", "Page<Long> ids = repo.findIds(pageable);\nList<Author> authors = repo.findWithBooksByIdIn(ids.getContent());")],
      [("What is N+1?", "One query for parents plus one per parent for a lazy association."),
       ("Why not just make it EAGER?", "EAGER loads graphs for every query, often causing even more queries/joins."),
       ("How do you test for it?", "Use Hibernate statistics or a datasource proxy to assert the statement count.")]),
    T("@Transactional: propagation, rollback rules and pitfalls",
      "`@Transactional` is applied through a Spring proxy: `begin -> run method -> commit/rollback`. Default propagation `REQUIRED` joins an existing transaction. **Rollback rules**: runtime exceptions and errors roll back; checked exceptions commit unless `rollbackFor` says otherwise. `readOnly = true` hints that no writes occur. `REQUIRES_NEW` suspends the outer transaction (audit logs).",
      "Business operations must be atomic (all-or-nothing) and consistent. Transactions also define the lifetime of the persistence context (lazy loading, dirty checking).",
      ["Declarative, no try/catch/commit code", "Consistent semantics across JPA, JDBC, messaging", "Read-only hints optimize flushing", "Composable through propagation"],
      ["Proxy-based: self-invocation and private methods are not intercepted", "Long transactions hold locks/connections", "Checked-exception default surprises people"],
      "Without a transaction a two-step transfer can debit one account and fail before crediting the other. Calling `this.transfer(...)` from another method in the same class skips the proxy so annotations on the inner method are ignored. Catching the exception inside the method hides the failure from the proxy: no rollback.",
      "```java\n@Service\nclass TransferService {\n  @Transactional\n  void transfer(...) {...}\n  @Transactional(rollbackFor = AuditUnavailableException.class)\n  void withAudit(...) throws AuditUnavailableException {...}\n  @Transactional(readOnly = true)\n  BigDecimal balance(long id) {...}\n}\n```\nPlace on public service methods; keep transactions short; do not do remote calls inside them if you can avoid it.",
      [("REQUIRES_NEW", "java", "@Transactional(propagation = Propagation.REQUIRES_NEW)\nvoid writeAudit(String event) {...}"),
       ("Programmatic", "java", "new TransactionTemplate(txManager).executeWithoutResult(s -> repo.save(x));"),
       ("Test behavior", "java", "@SpringBootTest   // NOT @Transactional, so commits/rollbacks are real")],
      [("Which exceptions roll back by default?", "Unchecked exceptions (RuntimeException) and Errors."),
       ("Why does self-invocation bypass @Transactional?", "The proxy is not involved when a method calls another method on `this`."),
       ("What does readOnly do?", "Optimization hint (e.g. no dirty-check flush); not a security guarantee.")]),
    T("Optimistic locking, auditing and Flyway migrations",
      "`@Version` adds a version column; Hibernate appends `where version = ?` to updates and throws `ObjectOptimisticLockingFailureException` when another transaction changed the row (lost-update protection without DB locks). **Auditing** (`@EnableJpaAuditing`, `@EntityListeners(AuditingEntityListener.class)`, `@CreatedDate`, `@LastModifiedDate`, `@CreatedBy`) fills metadata automatically. **Flyway** applies versioned SQL scripts (`V1__init.sql`) tracked in `flyway_schema_history`; Hibernate then only `validate`s.",
      "Concurrent edits must not silently overwrite each other; audit columns support traceability; migrations make schema evolution reviewable, repeatable and identical across environments.",
      ["Lost updates detected cheaply", "Audit data without boilerplate", "Schema history in version control", "Rollout is deterministic across environments"],
      ["Clients must handle/retry conflicts", "Bulk JPQL updates bypass `@Version`", "Migrations are forever: mistakes need new migrations", "Flyway SQL must work on the real production database"],
      "Without `@Version`, two users editing the same row produce last-write-wins data loss. Hand-editing a production schema leads to drift between environments; editing an applied migration breaks the checksum validation.",
      "```java\n@Version private Long version;\n@CreatedDate @Column(updatable = false) private LocalDateTime createdAt;\n@LastModifiedDate private LocalDateTime updatedAt;\n```\n```sql\n-- src/main/resources/db/migration/V2__add_status.sql\nalter table articles add column status varchar(20) not null default 'DRAFT';\n```\n```properties\nspring.jpa.hibernate.ddl-auto=validate\nspring.flyway.enabled=true\n```",
      [("Handling a conflict", "java", "try { service.saveDetached(p); } catch (ObjectOptimisticLockingFailureException e) { /* reload and retry or return 409 */ }"),
       ("Migration naming", "text", "V1__create_articles.sql\nV2__add_article_status.sql\nR__refresh_views.sql   (repeatable)"),
       ("Pessimistic alternative", "java", "@Lock(LockModeType.PESSIMISTIC_WRITE) Optional<Product> findById(Long id);")],
      [("What does @Version do on update?", "Adds a version check to the WHERE clause and increments it; mismatches throw an optimistic locking failure."),
       ("Why `validate` with Flyway?", "Flyway owns the schema; Hibernate only checks that entities match."),
       ("Can you edit an applied migration?", "No - add a new one; checksums would fail otherwise.")]),
]

day(35, "Spring Data JPA IV: N+1, Transactions, Versioning, Auditing and Flyway", "Spring Boot",
    "Performance and correctness of the persistence layer: fetching strategies, transactions, concurrency control and schema migrations",
    ["Detect and fix N+1 problems", "Apply @Transactional with correct rollback rules", "Use @Version for optimistic locking", "Add JPA auditing", "Manage schema evolution with Flyway"],
    ["Day 34 relationships"],
    topics, [a1, a2, a3, a4],
    [("How do you fix N+1?", "join fetch, entity graph, batch size, or projections."),
     ("Checked exceptions and @Transactional?", "They do not roll back unless rollbackFor is set."),
     ("Optimistic vs pessimistic locking?", "Optimistic detects conflicts at commit via version; pessimistic locks rows up front."),
     ("Why Flyway/Liquibase?", "Versioned, repeatable, reviewable schema changes."),
     ("What does open-in-view do?", "Keeps the EntityManager open during the web request, hiding lazy loading problems; disable for APIs.")],
    ["Join fetching multiple bags.", "Self-invocation of transactional methods.", "Editing applied Flyway migrations.", "Ignoring optimistic lock exceptions in APIs (should be 409)."],
    ["Hibernate User Guide: Fetching", "Spring Framework Reference: Transaction Management", "Flyway documentation"],
    [("N+1", "1 + N queries for lazy associations"), ("Entity graph", "Declarative fetch plan"), ("Propagation", "How transactions nest"),
     ("Optimistic lock", "Version-based conflict detection"), ("Migration", "Versioned schema change script")],
    "2–3 h theory + 3–5 h tasks", spring=True)
