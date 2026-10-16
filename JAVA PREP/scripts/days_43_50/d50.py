from common import *

H2RT = dep("com.h2database", "h2", None, "runtime")

# ---------------------------------------------------------------- task 1 (45 min): collections + streams
TS = r'''package %PKG%;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/** TIME BOX: 45 minutes for the whole task. */
public final class TextStats {

    private TextStats() {
    }

    /**
     * The n most frequent words. Lower-case the text, split on anything that is not a letter or digit, ignore empty tokens.
     * Order: higher count first, ties alphabetical. n &lt;= 0 -> IllegalArgumentException; fewer distinct words than n -> all of them.
     */
    public static List<String> topWords(String text, int n) {
        // TODO(%TAG%): count with a Map, sort with a Comparator (count desc, word asc), limit n
        throw new UnsupportedOperationException("TODO(%TAG%): implement topWords");
    }

    /**
     * Groups words that are anagrams of each other (case-sensitive letters). Each group keeps input order; groups are
     * ordered by the first appearance of any member. ["listen","google","silent","gogole"] -> [[listen,silent],[google,gogole]].
     */
    public static List<List<String>> groupAnagrams(List<String> words) {
        // TODO(%TAG%): key = sorted characters; use a LinkedHashMap
        throw new UnsupportedOperationException("TODO(%TAG%): implement groupAnagrams");
    }

    /** First character that occurs exactly once (case-sensitive), or Optional.empty(). */
    public static Optional<Character> firstNonRepeated(String s) {
        // TODO(%TAG%): LinkedHashMap<Character,Integer> counting, then first entry with count 1
        throw new UnsupportedOperationException("TODO(%TAG%): implement firstNonRepeated");
    }

    /** True when ()[]{} are balanced and properly nested; other characters are ignored; empty/null input -> true. */
    public static boolean isBalanced(String s) {
        // TODO(%TAG%): stack (Deque) of expected closers
        throw new UnsupportedOperationException("TODO(%TAG%): implement isBalanced");
    }
}
'''
TS_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import org.junit.jupiter.api.Test;

class TextStatsTest {

    @Test
    void topWordsCountsCaseInsensitivelyAndBreaksTiesAlphabetically() {
        String text = "The cat and the hat. The CAT sat; and sat!";
        assertThat(TextStats.topWords(text, 3)).containsExactly("the", "and", "cat");
    }

    @Test
    void topWordsEdgeCases() {
        assertThat(TextStats.topWords("", 5)).isEmpty();
        assertThat(TextStats.topWords("b a", 10)).containsExactly("a", "b");
        assertThatThrownBy(() -> TextStats.topWords("x", 0)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void groupsAnagramsInStableOrder() {
        assertThat(TextStats.groupAnagrams(List.of("listen", "google", "silent", "gogole", "cat")))
                .containsExactly(List.of("listen", "silent"), List.of("google", "gogole"), List.of("cat"));
    }

    @Test
    void firstNonRepeatedCharacter() {
        assertThat(TextStats.firstNonRepeated("swiss")).contains('w');
        assertThat(TextStats.firstNonRepeated("aabb")).isEmpty();
        assertThat(TextStats.firstNonRepeated("")).isEmpty();
        assertThat(TextStats.firstNonRepeated("aAb")).contains('a');
    }

    @Test
    void balancedBrackets() {
        assertThat(TextStats.isBalanced("{[()]}")).isTrue();
        assertThat(TextStats.isBalanced("a(b)c[d]{e}")).isTrue();
        assertThat(TextStats.isBalanced("")).isTrue();
        assertThat(TextStats.isBalanced(null)).isTrue();
        assertThat(TextStats.isBalanced("(]")).isFalse();
        assertThat(TextStats.isBalanced("((")).isFalse();
        assertThat(TextStats.isBalanced("())")).isFalse();
    }
}
'''
r1 = task("timed-collections-streams-45min", "Timed Round 1 (45 min): Collections and Streams", "Timed", "Core Java",
    "Four classic interview utilities (word frequency, anagram groups, first non-repeated character, balanced brackets). Start a 45-minute timer, then stop and note how far you got.",
    "plain", {"main/TextStats.java": TS, "test/TextStatsTest.java": TS_TEST},
    ["`topWords`: frequency count, deterministic ordering.", "`groupAnagrams`: stable grouping.", "`firstNonRepeated`: single pass counting with insertion order.", "`isBalanced`: stack-based matching."],
    ["Empty/null input.", "Ties in frequency.", "Case sensitivity differences between methods.", "Unbalanced closers at the start."],
    ["Think about the data structure first: `HashMap` vs `LinkedHashMap` vs `ArrayDeque`.", "`Comparator.comparing(...).reversed().thenComparing(...)` or `Map.Entry` comparators."],
    goals=["Practice solving a mixed collections problem set under time pressure", "Choose the right collection and complexity", "Explain trade-offs aloud as you would in an interview"],
    note=None)

# ---------------------------------------------------------------- task 2 (60 min): Spring + JPA bug hunt
PRODUCT = r'''package %PKG%;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/** PROVIDED. */
@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String sku;

    @Column(nullable = false)
    private int stock;

    @Column(name = "price_cents", nullable = false)
    private long priceCents;

    protected Product() {
    }

    public Product(String sku, int stock, long priceCents) {
        this.sku = sku;
        this.stock = stock;
        this.priceCents = priceCents;
    }

    public Long getId() {
        return id;
    }

    public String getSku() {
        return sku;
    }

    public int getStock() {
        return stock;
    }

    public void setStock(int stock) {
        this.stock = stock;
    }

    public long getPriceCents() {
        return priceCents;
    }
}
'''
PREPO = "package %PKG%;\n\nimport java.util.Optional;\nimport org.springframework.data.jpa.repository.JpaRepository;\n\n/** PROVIDED. */\npublic interface ProductRepository extends JpaRepository<Product, Long> {\n\n    Optional<Product> findBySku(String sku);\n}\n"
PSVC = r'''package %PKG%;

import java.util.List;
import java.util.NoSuchElementException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * TIME BOX: 60 minutes. This service was handed over with several defects (BUG-1..BUG-3) plus one unfinished method.
 * Read the Javadoc SPEC of each method, run the tests, find the root cause, fix it.
 */
@Service
public class ProductService {

    private final ProductRepository repository;

    public ProductService(ProductRepository repository) {
        this.repository = repository;
    }

    /** SPEC: products whose stock is STRICTLY below the threshold. */
    @Transactional(readOnly = true)
    public List<Product> lowStock(int threshold) {
        // TODO(%TAG%): BUG-1 - something about this comparison does not match the spec
        return repository.findAll().stream().filter(p -> p.getStock() <= threshold).toList();
    }

    /**
     * SPEC: price after a percentage discount using integer math rounded down: priceCents * (100 - percentOff) / 100.
     * percentOff outside 0..100 -> IllegalArgumentException.
     */
    public long discountedPriceCents(long priceCents, int percentOff) {
        // TODO(%TAG%): BUG-2 - integer division strikes again; also validate the range
        return priceCents * (1 - percentOff / 100);
    }

    /** SPEC: SKUs are stored upper-case; lookups ignore case and surrounding whitespace; null -> false. */
    @Transactional(readOnly = true)
    public boolean skuExists(String sku) {
        // TODO(%TAG%): BUG-3 - lookup does not normalise the input
        return repository.findBySku(sku).isPresent();
    }

    /**
     * SPEC: reduce the stock of the (normalised, see skuExists) SKU by qty and return the saved product.
     * qty &lt;= 0 -> IllegalArgumentException; unknown SKU -> NoSuchElementException; qty greater than stock ->
     * IllegalStateException and the stock stays unchanged. Must be transactional.
     */
    @Transactional
    public Product reserve(String sku, int qty) {
        // TODO(%TAG%): implement reserve according to the SPEC
        throw new UnsupportedOperationException("TODO(%TAG%): implement reserve");
    }
}
'''
PTEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.NoSuchElementException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(ProductService.class)
class ProductServiceTest {

    @Autowired
    private ProductRepository repo;
    @Autowired
    private ProductService service;

    @BeforeEach
    void seed() {
        repo.save(new Product("AB-1", 3, 1000));
        repo.save(new Product("AB-2", 5, 2000));
        repo.save(new Product("AB-3", 10, 3000));
    }

    @Test
    void lowStockIsStrictlyBelowThreshold() {
        assertThat(service.lowStock(5)).extracting(Product::getSku).containsExactly("AB-1");
    }

    @Test
    void discountUsesIntegerPercentMath() {
        assertThat(service.discountedPriceCents(1000, 10)).isEqualTo(900);
        assertThat(service.discountedPriceCents(999, 10)).isEqualTo(899);
        assertThat(service.discountedPriceCents(1000, 0)).isEqualTo(1000);
        assertThat(service.discountedPriceCents(1000, 100)).isZero();
    }

    @Test
    void discountRejectsOutOfRangePercent() {
        assertThatThrownBy(() -> service.discountedPriceCents(1000, 101)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.discountedPriceCents(1000, -1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void skuLookupIgnoresCaseAndWhitespace() {
        assertThat(service.skuExists(" ab-1 ")).isTrue();
        assertThat(service.skuExists("AB-1")).isTrue();
        assertThat(service.skuExists("zz-9")).isFalse();
        assertThat(service.skuExists(null)).isFalse();
    }

    @Test
    void reserveReducesStock() {
        Product p = service.reserve("ab-2", 2);
        assertThat(p.getStock()).isEqualTo(3);
        assertThat(repo.findBySku("AB-2").orElseThrow().getStock()).isEqualTo(3);
    }

    @Test
    void reserveRejectsBadRequestsWithoutChangingStock() {
        assertThatThrownBy(() -> service.reserve("AB-1", 4)).isInstanceOf(IllegalStateException.class);
        assertThat(repo.findBySku("AB-1").orElseThrow().getStock()).isEqualTo(3);
        assertThatThrownBy(() -> service.reserve("AB-1", 0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.reserve("NOPE", 1)).isInstanceOf(NoSuchElementException.class);
    }

    @Test
    void reservingExactlyTheStockIsAllowed() {
        assertThat(service.reserve("AB-1", 3).getStock()).isZero();
    }
}
'''
r2 = task("timed-spring-jpa-bug-hunt-60min", "Timed Round 2 (60 min): Spring + JPA Bug Hunt", "Timed", "Spring Boot (JPA)",
    "A handed-over service with three seeded defects and one missing method. Diagnose with the failing tests, fix each root cause, finish `reserve`. Start a 60-minute timer.",
    "boot", {"main/Application.java": APP, "main/Product.java": PRODUCT, "main/ProductRepository.java": PREPO, "main/ProductService.java": PSVC, "test/ProductServiceTest.java": PTEST},
    ["Fix BUG-1 (comparison), BUG-2 (integer math + validation) and BUG-3 (input normalisation).", "Implement `reserve` per the Javadoc SPEC (transactional, validated, no partial change).", "Do not change the tests."],
    ["Boundary value for `lowStock`.", "Rounding down in the discount.", "Null SKU.", "Failed reservation must not decrease stock."],
    ["Read the failing assertion first; reproduce in your head before editing.", "`sku.trim().toUpperCase(Locale.ROOT)`."],
    starters=["spring-boot-starter-data-jpa"], deps=[H2RT],
    goals=["Debug unfamiliar code from failing tests", "Spot classic defects: off-by-one, integer division, unnormalised input", "Write a small transactional service method"])

# ---------------------------------------------------------------- task 3 (90 min): concurrency
SC = r'''package %PKG%;

import java.util.function.Supplier;

/** Thread-safe counter. 8 threads x 10 000 increments must give exactly 80 000. */
public class SafeCounter {

    private long value;

    public void increment() {
        // TODO(%TAG%): make this thread-safe (AtomicLong, LongAdder, synchronized or a lock)
        throw new UnsupportedOperationException("TODO(%TAG%): implement increment");
    }

    public long get() {
        // TODO(%TAG%): return the current value consistently with increment()
        throw new UnsupportedOperationException("TODO(%TAG%): implement get");
    }
}
'''
LAZY = r'''package %PKG%;

import java.util.function.Supplier;

/** Lazily computes a value exactly ONCE, even when many threads call {@link #get()} simultaneously. */
public class LazyHolder<T> {

    private final Supplier<T> supplier;

    public LazyHolder(Supplier<T> supplier) {
        this.supplier = supplier;
    }

    /** All callers receive the same instance; the supplier runs at most once (supplier never returns null). */
    public T get() {
        // TODO(%TAG%): thread-safe lazy initialisation (double-checked locking with volatile, holder, or synchronized)
        throw new UnsupportedOperationException("TODO(%TAG%): implement get");
    }
}
'''
PSUM = r'''package %PKG%;

/** Parallel array sum with an explicit thread pool (no parallel streams). */
public final class ParallelSum {

    private ParallelSum() {
    }

    /**
     * Splits the array into {@code threads} contiguous chunks, sums each in an ExecutorService task, combines the partial
     * sums. threads &lt; 1 -> IllegalArgumentException; empty array -> 0. The pool must be shut down before returning.
     * Interrupted / failed tasks -> IllegalStateException.
     */
    public static long sum(int[] data, int threads) {
        // TODO(%TAG%): ExecutorService + Callable<Long> per chunk, collect Futures, shut down in finally
        throw new UnsupportedOperationException("TODO(%TAG%): implement sum");
    }
}
'''
CONC_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class ConcurrencyTest {

    private static <T> List<T> runConcurrently(int threads, Callable<T> task) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(threads);
        CountDownLatch ready = new CountDownLatch(threads);
        CountDownLatch go = new CountDownLatch(1);
        try {
            List<Future<T>> futures = new ArrayList<>();
            for (int i = 0; i < threads; i++) {
                futures.add(pool.submit(() -> {
                    ready.countDown();
                    go.await();
                    return task.call();
                }));
            }
            ready.await();
            go.countDown();
            List<T> results = new ArrayList<>();
            for (Future<T> f : futures) {
                results.add(f.get(20, TimeUnit.SECONDS));
            }
            return results;
        } finally {
            pool.shutdownNow();
        }
    }

    @Test
    void counterDoesNotLoseUpdates() throws Exception {
        SafeCounter counter = new SafeCounter();
        runConcurrently(8, () -> {
            for (int i = 0; i < 10_000; i++) {
                counter.increment();
            }
            return null;
        });
        assertThat(counter.get()).isEqualTo(80_000);
    }

    @Test
    void lazyHolderRunsSupplierOnce() throws Exception {
        AtomicInteger created = new AtomicInteger();
        LazyHolder<Object> holder = new LazyHolder<>(() -> {
            created.incrementAndGet();
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return new Object();
        });
        List<Object> results = runConcurrently(16, holder::get);
        assertThat(created.get()).isEqualTo(1);
        assertThat(results).allSatisfy(o -> assertThat(o).isSameAs(results.get(0)));
    }

    @Test
    void parallelSumMatchesSequentialSum() {
        int[] data = new int[100_000];
        long expected = 0;
        for (int i = 0; i < data.length; i++) {
            data[i] = i + 1;
            expected += data[i];
        }
        assertThat(ParallelSum.sum(data, 1)).isEqualTo(expected);
        assertThat(ParallelSum.sum(data, 4)).isEqualTo(expected);
        assertThat(ParallelSum.sum(data, 7)).isEqualTo(expected);
    }

    @Test
    void parallelSumEdgeCases() {
        assertThat(ParallelSum.sum(new int[0], 4)).isZero();
        assertThat(ParallelSum.sum(new int[] {5, 6}, 8)).isEqualTo(11);
        assertThatThrownBy(() -> ParallelSum.sum(new int[] {1}, 0)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void parallelSumDoesNotLeakThreads() {
        long before = Thread.getAllStackTraces().keySet().stream().filter(t -> t.getName().startsWith("pool-")).count();
        for (int i = 0; i < 20; i++) {
            ParallelSum.sum(new int[] {1, 2, 3, 4}, 4);
        }
        try {
            Thread.sleep(200);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        long after = Thread.getAllStackTraces().keySet().stream().filter(t -> t.getName().startsWith("pool-")).count();
        assertThat(after - before).isLessThan(10);
    }
}
'''
r3 = task("timed-concurrency-fix-90min", "Timed Round 3 (90 min): Concurrency Fixes", "Timed", "Core Java",
    "Make three small components thread-safe: a counter, a lazy holder and an executor-based parallel sum. Start a 90-minute timer.",
    "plain", {"main/SafeCounter.java": SC, "main/LazyHolder.java": LAZY, "main/ParallelSum.java": PSUM, "test/ConcurrencyTest.java": CONC_TEST},
    ["`SafeCounter`: no lost updates under contention.", "`LazyHolder`: exactly-once initialisation, same instance for everyone.", "`ParallelSum`: chunking, futures, correct shutdown and error handling."],
    ["`threads` greater than array length.", "Interrupted threads.", "Visibility (volatile / happens-before).", "Leaking executors."],
    ["`AtomicLong` is the simplest correct counter; `synchronized` also works.", "`Executors.newFixedThreadPool(n)` and always `shutdown()` in `finally`.", "Empty chunks are fine: their sum is 0."],
    goals=["Recognize and fix race conditions and visibility problems", "Choose between atomics, locks and executors", "Manage thread-pool lifecycle correctly"])

# ---------------------------------------------------------------- task 4 (60 min): SQL
RQ = r'''package %PKG%;

/**
 * TIME BOX: 60 minutes. Schema (provided by the test):
 *   customers(id, name)
 *   orders(id, customer_id, total_cents, status)   status in ('PAID','CANCELLED','NEW')
 * Write ONE SQL statement per method (no trailing semicolon needed).
 */
public final class ReportQueries {

    private ReportQueries() {
    }

    /**
     * The 2 customers with the highest total of PAID orders. Columns, in order: name, total_spent.
     * Highest total first. Customers without PAID orders do not appear.
     */
    public static String topCustomersSql() {
        // TODO(%TAG%): join + where status = 'PAID' + group by + order by total desc + limit 2
        throw new UnsupportedOperationException("TODO(%TAG%): implement topCustomersSql");
    }

    /**
     * Names of customers that have NO PAID order (customers with no orders at all or only CANCELLED/NEW ones),
     * ordered by name. Single column: name. Use NOT EXISTS (anti-join), not NOT IN.
     */
    public static String customersWithoutPaidOrdersSql() {
        // TODO(%TAG%): select name from customers c where not exists (...) order by name
        throw new UnsupportedOperationException("TODO(%TAG%): implement customersWithoutPaidOrdersSql");
    }

    /**
     * A CREATE INDEX statement named idx_orders_customer_status on orders(customer_id, status) that would speed up both
     * queries above (equality on status plus join on customer_id).
     */
    public static String supportingIndexDdl() {
        // TODO(%TAG%): create index idx_orders_customer_status on orders (customer_id, status)
        throw new UnsupportedOperationException("TODO(%TAG%): implement supportingIndexDdl");
    }
}
'''
RQ_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ReportQueriesTest {

    private Connection conn;

    @BeforeEach
    void setUp() throws Exception {
        conn = DriverManager.getConnection("jdbc:h2:mem:day50t4_" + UUID.randomUUID() + ";DB_CLOSE_DELAY=-1", "sa", "");
        try (Statement st = conn.createStatement()) {
            st.execute("create table customers (id int primary key, name varchar(50) not null)");
            st.execute("create table orders (id int primary key, customer_id int not null, total_cents bigint not null, status varchar(10) not null)");
            st.execute("insert into customers values (1,'Alice'),(2,'Bob'),(3,'Cara'),(4,'Dan'),(5,'Eve')");
            st.execute("insert into orders values (1,1,1000,'PAID'),(2,1,2500,'PAID'),(3,2,500,'PAID'),(4,2,9000,'CANCELLED'),"
                    + "(5,3,1200,'PAID'),(6,5,700,'CANCELLED'),(7,5,300,'NEW')");
        }
    }

    @AfterEach
    void tearDown() throws Exception {
        conn.close();
    }

    @Test
    void topCustomersByPaidTotal() throws Exception {
        List<String> rows = new ArrayList<>();
        try (Statement st = conn.createStatement(); ResultSet rs = st.executeQuery(ReportQueries.topCustomersSql())) {
            while (rs.next()) {
                rows.add(rs.getString(1) + "=" + rs.getLong(2));
            }
        }
        assertThat(rows).containsExactly("Alice=3500", "Cara=1200");
    }

    @Test
    void customersWithoutPaidOrders() throws Exception {
        List<String> names = new ArrayList<>();
        try (Statement st = conn.createStatement(); ResultSet rs = st.executeQuery(ReportQueries.customersWithoutPaidOrdersSql())) {
            while (rs.next()) {
                names.add(rs.getString(1));
            }
        }
        assertThat(names).containsExactly("Dan", "Eve");
    }

    @Test
    void antiJoinUsesNotExists() {
        assertThat(ReportQueries.customersWithoutPaidOrdersSql().toLowerCase()).contains("not exists").doesNotContain("not in");
    }

    @Test
    void supportingIndexIsCreatedWithTheExpectedName() throws Exception {
        try (Statement st = conn.createStatement()) {
            st.execute(ReportQueries.supportingIndexDdl());
        }
        boolean found = false;
        try (ResultSet rs = conn.getMetaData().getIndexInfo(null, null, "ORDERS", false, false)) {
            while (rs.next()) {
                String name = rs.getString("INDEX_NAME");
                if (name != null && name.equalsIgnoreCase("idx_orders_customer_status")) {
                    found = true;
                }
            }
        }
        assertThat(found).isTrue();
    }
}
'''
r4 = task("timed-sql-reasoning-60min", "Timed Round 4 (60 min): SQL Reporting and Index Reasoning", "Timed", "SQL + JDBC (H2)",
    "Write two reporting queries (aggregate with join, anti-join) and the index that supports them, then explain your choices in a short note in your commit message. Start a 60-minute timer.",
    "h2", {"main/ReportQueries.java": RQ, "test/ReportQueriesTest.java": RQ_TEST},
    ["`topCustomersSql`: PAID totals per customer, top 2, name + total.", "`customersWithoutPaidOrdersSql`: anti-join with `NOT EXISTS`, ordered by name.", "`supportingIndexDdl`: composite index `(customer_id, status)` named `idx_orders_customer_status`.", "Be ready to explain: why `NOT EXISTS` over `NOT IN` (NULL semantics), and why the column order of the index matters."],
    ["Customers with no orders.", "Cancelled orders must not count.", "NULL handling in `NOT IN`."],
    ["`join` is inner: customers without paid orders vanish automatically in query 1.", "`select ... from customers c where not exists (select 1 from orders o where o.customer_id = c.id and o.status = 'PAID')`."])

TOPICS = [
    T("Core Java and collections rapid review",
      "Core Java interview staples: `equals`/`hashCode` contract, immutability (`String`, records), `HashMap` internals (buckets, treeification at 8, resize at 0.75 load), `ArrayList` vs `LinkedList`, `TreeMap` ordering, fail-fast iterators, generics (type erasure, PECS), `Optional`, exceptions (checked vs unchecked, try-with-resources), streams (lazy, short-circuit, collectors), `var`, records, sealed types, switch patterns (Java 21).",
      "Interviewers use these topics to test whether you understand the tools you use daily, not only their syntax.",
      ["Foundation for every framework", "Quick to rehearse with code snippets"],
      ["Easy to know the API but not the reasoning", "Trick questions reward precise vocabulary"],
      "Mutable keys in a HashMap, equals without hashCode, or modifying a list while iterating produce subtle bugs that interviewers love to probe.",
      "Complexities: `HashMap` get/put O(1) avg, `TreeMap` O(log n), `ArrayList` get O(1) / insert middle O(n), `ArrayDeque` O(1) at both ends. `Comparator.comparing(A::x).thenComparing(A::y)`. Streams: `collect(groupingBy(f, counting()))`.",
      [("equals/hashCode contract", "java", "// equal objects MUST have equal hash codes (not vice versa)\nrecord Point(int x, int y) {}  // gets both for free"),
       ("PECS", "java", "void copy(List<? super Integer> dst, List<? extends Integer> src) { dst.addAll(src); }")],
      [("Why must keys be effectively immutable?", "Changing a key after insertion changes its hash bucket, so the entry becomes unreachable."),
       ("Checked vs unchecked exceptions?", "Checked must be handled/declared (recoverable conditions); unchecked signal programming errors.")]),
    T("Concurrency and JVM review",
      "Threads, `Runnable`/`Callable`, executors, `synchronized` (monitor, reentrant), `volatile` (visibility, no atomicity), atomics (CAS), `ConcurrentHashMap`, `CompletableFuture`, virtual threads (Java 21). The **Java Memory Model**: happens-before. JVM: heap (young/old), GC basics, stack frames, class loading, JIT, `OutOfMemoryError` vs `StackOverflowError`.",
      "Concurrency bugs are rare in tests and common in production; interviewers check you can reason about visibility, atomicity and deadlocks.",
      ["Better throughput", "Virtual threads simplify blocking I/O code"],
      ["Races, deadlocks and visibility bugs are hard to reproduce", "Over-synchronization kills performance"],
      "`count++` on a shared field loses updates; double-checked locking without `volatile` can publish a half-constructed object; unbounded thread pools exhaust memory.",
      "Rules: prefer immutability; confine state; use `java.util.concurrent` over wait/notify; always shut executors down; lock ordering prevents deadlocks.",
      [("Atomic counter", "java", "AtomicLong n = new AtomicLong();\nn.incrementAndGet();"),
       ("Executor lifecycle", "java", "ExecutorService pool = Executors.newFixedThreadPool(4);\ntry { /* submit */ } finally { pool.shutdown(); }")],
      [("volatile vs synchronized?", "volatile gives visibility only; synchronized gives visibility plus mutual exclusion."),
       ("What causes a deadlock?", "Circular wait on locks held by each other; avoid by consistent lock ordering or timeouts.")]),
    T("SQL, transactions, and JPA review",
      "SQL: joins, aggregation, `GROUP BY/HAVING`, subqueries, anti-joins (`NOT EXISTS`), window functions, indexes (B-tree, composite order, covering), `EXPLAIN`. Transactions: ACID, isolation levels (read committed, repeatable read, serializable), locks, optimistic (`@Version`) vs pessimistic locking. JPA: entity states, lazy vs eager, N+1 problem and `JOIN FETCH`, `@Transactional` boundaries and proxy limits (self-invocation), dirty checking.",
      "Persistence mistakes are the dominant cause of production slowness and data corruption.",
      ["High interview signal", "Directly applies to Projects 01-03"],
      ["Database-specific behavior", "ORM hides SQL until it hurts"],
      "N+1 queries from lazy collections in a loop; `@Transactional` ignored on `private` or self-invoked methods; missing index on a foreign key; `NOT IN` with NULLs returning no rows.",
      "Composite index `(a, b)` helps filters on `a` and `a,b` but not `b` alone (left-most prefix). Use `@Version` for optimistic locking, retry on `OptimisticLockException`. Fix N+1 with `join fetch` or `@EntityGraph`.",
      [("Anti-join", "sql", "select c.name from customers c where not exists (select 1 from orders o where o.customer_id = c.id)"),
       ("Optimistic lock", "java", "@Version private long version;")],
      [("What is the N+1 problem?", "One query for the parents plus one per parent for lazy children; fix with fetch joins or batching."),
       ("Why can @Transactional fail on self-invocation?", "The proxy is bypassed when a bean calls its own method.")]),
    T("Spring, REST, and security review",
      "Spring: IoC/DI, bean scopes and life cycle, auto-configuration, `@Configuration` vs `@Component`, constructor injection, profiles, `@ConfigurationProperties`. Web: request mapping, validation, `@RestControllerAdvice`, `ProblemDetail`, idempotent methods, status codes. Security: authentication vs authorization, BCrypt, JWT pitfalls, CSRF, CORS, BOLA. Testing: pyramid, `@WebMvcTest`, `@DataJpaTest`, Mockito.",
      "Most backend interviews are Spring-heavy; clear definitions plus a concrete example set strong candidates apart.",
      ["Reusable answers across companies"],
      ["Frameworks change; focus on principles"],
      "Field injection hides dependencies and hurts tests; exposing entities from controllers leaks internals; catching `Exception` broadly hides bugs.",
      "Be ready to draw: request -> filter chain -> DispatcherServlet -> controller -> service -> repository -> DB, and explain where transactions and security apply.",
      [("Constructor injection", "java", "@Service class A { private final B b; A(B b) { this.b = b; } }")],
      [("Singleton scope and thread-safety?", "Singleton beans are shared across threads, so they must be stateless or properly synchronized."),
       ("PUT vs PATCH vs POST?", "PUT replaces and is idempotent, PATCH partially updates, POST creates/processes and is not idempotent by default.")]),
    T("System design talking points and how to run a timed round",
      "Design discussions: clarify requirements, estimate scale, draw components (API, DB, cache, queue), choose data model and consistency, discuss failure modes (retries, circuit breakers, idempotency, outbox), security and observability, then trade-offs. For timed coding: read all requirements, plan 5 minutes, get tests green incrementally, narrate trade-offs, leave 5 minutes for review.",
      "Interviews evaluate communication and judgment as much as code.",
      ["Structure reduces panic", "Reusable template for any design question"],
      ["Over-engineering in a short slot", "Talking without writing tests"],
      "Jumping into code without clarifying edge cases or silently choosing a design wastes time and loses points.",
      "Template: requirements -> API -> data model -> high-level design -> deep dive (one hard part) -> failure modes -> scaling -> security -> monitoring. Examples to prepare: URL shortener, wallet transfer (idempotency + locking), hotel booking (date overlap), HR notifications with Kafka.",
      [("Wallet transfer talking points", "text", "debit+credit in one DB transaction; @Version or SELECT FOR UPDATE; idempotency key; ledger rows immutable; reconcile job")],
      [("How do you handle a question you do not know?", "State assumptions, reason from first principles, ask clarifying questions, and say what you would verify."),
       ("What do you do when time is almost out?", "Make the tests for the core path pass, document what is unfinished and why.")]),
]

Q = lambda q, a: (q, a)
BANK = [
    Q("Explain the equals/hashCode contract.", "Equal objects must return equal hash codes; hashCode must be consistent; equals must be reflexive, symmetric, transitive, consistent and false for null."),
    Q("Why is String immutable?", "Security, caching of hash codes, safe sharing across threads, and string-pool interning."),
    Q("ArrayList vs LinkedList?", "ArrayList: contiguous array, O(1) index access, amortized O(1) append. LinkedList: O(1) at ends via references but O(n) index; rarely better in practice - use ArrayDeque for queues."),
    Q("How does HashMap work?", "Array of buckets; index from hash; collisions are chained and treeified at 8 entries per bucket; resizes at load factor 0.75; allows one null key."),
    Q("HashMap vs ConcurrentHashMap?", "ConcurrentHashMap is thread-safe with fine-grained locking/CAS, no null keys/values, and weakly consistent iterators."),
    Q("What are generics' type erasure consequences?", "No runtime type info: no `new T()`, no `instanceof List<String>`, overloads that differ only by type args clash."),
    Q("Checked vs unchecked exceptions?", "Checked extend Exception (not RuntimeException) and must be declared/handled; unchecked are programming errors or unrecoverable conditions."),
    Q("What does try-with-resources do?", "Automatically closes AutoCloseable resources in reverse order, suppressing secondary exceptions."),
    Q("Stream laziness?", "Intermediate operations build a pipeline; nothing runs until a terminal operation; short-circuiting ops can stop early."),
    Q("map vs flatMap?", "map transforms one element to one; flatMap transforms each element to a stream and flattens."),
    Q("What are records and sealed types?", "Records: concise immutable data carriers with generated accessors/equals/hashCode. Sealed types restrict which classes may extend/implement, enabling exhaustive switches."),
    Q("What are virtual threads?", "Lightweight JVM-managed threads (Java 21) that make blocking code scale; do not pool them and avoid pinning with synchronized around blocking I/O."),
    Q("volatile vs synchronized vs atomic?", "volatile: visibility; synchronized: visibility + mutual exclusion; atomic: lock-free atomic read-modify-write via CAS."),
    Q("What is a deadlock and how do you avoid it?", "Circular waiting for locks; use lock ordering, timeouts (tryLock) or fewer locks."),
    Q("How does garbage collection decide what to free?", "Objects unreachable from GC roots (stacks, statics, JNI) are collectable; generational collectors optimize for short-lived objects."),
    Q("OutOfMemoryError vs StackOverflowError?", "Heap exhaustion (leak, huge data) vs too-deep recursion exhausting thread stack."),
    Q("Inner join vs left join?", "Inner keeps matching rows only; left keeps all left rows with NULLs where no match."),
    Q("Why NOT EXISTS over NOT IN?", "NOT IN returns no rows if the subquery yields NULL; NOT EXISTS is NULL-safe and often better optimized."),
    Q("What is an index and its cost?", "A sorted structure (B-tree) that speeds lookups; costs storage and slows writes."),
    Q("Composite index column order?", "Left-most prefix rule: put equality columns first; the index serves queries using a prefix of its columns."),
    Q("Explain ACID.", "Atomicity, Consistency, Isolation, Durability."),
    Q("Isolation levels and anomalies?", "Read uncommitted (dirty reads), read committed (non-repeatable reads), repeatable read (phantoms in some DBs), serializable (none)."),
    Q("Optimistic vs pessimistic locking?", "Optimistic uses a version column and fails on conflict (good for low contention); pessimistic locks rows (SELECT FOR UPDATE) up front."),
    Q("What is the N+1 select problem?", "Loading N children with N extra queries; fix with join fetch, entity graphs or batch fetching."),
    Q("JPA entity states?", "Transient, managed, detached, removed."),
    Q("Why might @Transactional not work?", "Self-invocation, private/final methods, wrong proxy type, exception types not rolled back (checked by default)."),
    Q("Bean scopes?", "singleton (default), prototype, request, session, application."),
    Q("Constructor vs field injection?", "Constructor: immutability, required dependencies, easy tests; field injection hides dependencies."),
    Q("How does Spring Boot auto-configuration work?", "Conditional configuration classes listed in AutoConfiguration.imports activate based on classpath, beans and properties."),
    Q("REST idempotency?", "GET, PUT, DELETE are idempotent; POST is not unless an idempotency key is used."),
    Q("Which status codes do you use for validation vs conflict vs auth errors?", "400 validation, 401 unauthenticated, 403 forbidden, 404 not found, 409 conflict, 422 semantic validation (team policy), 429 rate limit."),
    Q("What is CSRF and when does it matter?", "Forged cross-site requests using automatic browser credentials (cookies); irrelevant for pure bearer-token APIs."),
    Q("JWT pitfalls?", "alg=none, weak secrets, no expiry check, sensitive data in payload, hard revocation."),
    Q("What is BOLA?", "Broken object-level authorization: accessing other users' objects by id."),
    Q("Test pyramid in Spring?", "Many unit tests, fewer slice tests (@WebMvcTest, @DataJpaTest), few @SpringBootTest integration tests."),
    Q("Mockito: mock vs spy?", "A mock replaces behavior entirely; a spy wraps a real object and lets you stub selectively."),
    Q("Circuit breaker states?", "CLOSED, OPEN, HALF_OPEN."),
    Q("Why use Kafka keys?", "Per-key ordering via partitioning."),
    Q("How do you make a Kafka consumer idempotent?", "Store processed event ids (unique key) in the same transaction as the side effect."),
    Q("What is the outbox pattern?", "Write business data and event row in one DB transaction; relay events to the broker afterwards."),
    Q("How would you design a wallet transfer?", "One transaction debits and credits, optimistic version or row locks, idempotency key, immutable ledger entries, reconciliation."),
    Q("How would you prevent double bookings in a hotel system?", "Date-overlap check plus a DB constraint (exclusion constraint in PostgreSQL) or locking the room row inside the transaction."),
    Q("What do you put in CI for a Spring project?", "Build, unit/integration tests, style checks, dependency/security scan; run on every PR."),
    Q("Where do secrets live in production?", "Environment variables/secret manager; never in the repository."),
]

day(50, "Interview Review: Core Java, Spring, and Timed Rounds", "Capstone",
    "Rapid review of Core Java, collections, concurrency, JVM, SQL, JPA, Spring and security, plus four timed mixed coding rounds",
    ["Answer core Java, Spring, JPA, SQL and security questions precisely", "Solve collection/stream problems under time pressure", "Debug seeded defects in a Spring + JPA service", "Fix concurrency problems with atomics, locks and executors", "Reason about SQL queries and indexes; structure a system-design answer"],
    ["Days 1-49 (use the question bank as a self-test)"],
    TOPICS, [r1, r2, r3, r4],
    BANK,
    ["Optimizing before correctness.", "Silent coding: not narrating assumptions.", "Ignoring edge cases (null, empty, boundaries).", "Unbounded executors and unclosed resources.", "Over-reliance on memorized answers."],
    ["Effective Java (Bloch), items on equals/hashCode, immutability, generics", "Java Concurrency in Practice (Goetz)", "Use The Index, Luke (SQL indexing)", "Spring Framework and Spring Boot reference documentation"],
    [("PECS", "Producer extends, consumer super"), ("CAS", "Compare-and-swap atomic primitive"), ("N+1", "One query plus one per row"), ("BOLA", "Broken object-level authorization"),
     ("Happens-before", "JMM ordering guarantee"), ("Anti-join", "Rows with no match, via NOT EXISTS")],
    "3-4 h review + 4 timed rounds (45/60/90/60 min)", spring=True)
