from common import *

USER_REC = r'''package %PKG%;

/** PROVIDED value object. */
public record User(long id, String name, String email) {
}
'''

DS_HELPER_TEST = r'''
    private static DataSource newDataSource() {
        JdbcDataSource ds = new JdbcDataSource();
        ds.setURL("jdbc:h2:mem:day27_" + UUID.randomUUID().toString().replace("-", "") + ";DB_CLOSE_DELAY=-1");
        ds.setUser("sa");
        ds.setPassword("");
        return ds;
    }

    private static void exec(DataSource ds, String... sql) throws Exception {
        try (Connection c = ds.getConnection(); Statement st = c.createStatement()) {
            for (String s : sql) {
                st.execute(s);
            }
        }
    }
'''

TEST_IMPORTS = r'''import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.sql.Connection;
import java.sql.Statement;
import java.util.List;
import java.util.UUID;
import javax.sql.DataSource;
import org.h2.jdbcx.JdbcDataSource;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
'''

# ------------------------------------------------------------- task 1
DAO1 = r'''package %PKG%;

import java.util.List;
import java.util.Optional;
import javax.sql.DataSource;

/** Table: users(id BIGINT PK, name VARCHAR, email VARCHAR). */
public class UserDao {

    private final DataSource dataSource;

    public UserDao(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    /** Empty Optional when no row matches. Use try-with-resources for Connection/Statement/ResultSet. */
    public Optional<User> findById(long id) {
        // TODO(%TAG%): SELECT id, name, email FROM users WHERE id = ? using PreparedStatement
        throw new UnsupportedOperationException("TODO(%TAG%): implement findById");
    }

    /** All users ordered by id ascending. */
    public List<User> findAll() {
        // TODO(%TAG%): SELECT all users ordered by id; map each row with a private mapRow helper
        throw new UnsupportedOperationException("TODO(%TAG%): implement findAll");
    }

    public long count() {
        // TODO(%TAG%): SELECT COUNT(*) FROM users
        throw new UnsupportedOperationException("TODO(%TAG%): implement count");
    }
}
'''
DAO1_SOL = r'''package %PKG%;

import java.sql.*;
import java.util.*;
import javax.sql.DataSource;

public class UserDao {
    private final DataSource ds;
    public UserDao(DataSource ds) { this.ds = ds; }
    private static User map(ResultSet rs) throws SQLException { return new User(rs.getLong("id"), rs.getString("name"), rs.getString("email")); }
    public Optional<User> findById(long id) {
        try (Connection c = ds.getConnection(); PreparedStatement ps = c.prepareStatement("SELECT id, name, email FROM users WHERE id = ?")) {
            ps.setLong(1, id);
            try (ResultSet rs = ps.executeQuery()) { return rs.next() ? Optional.of(map(rs)) : Optional.empty(); }
        } catch (SQLException e) { throw new IllegalStateException(e); }
    }
    public List<User> findAll() {
        List<User> out = new ArrayList<>();
        try (Connection c = ds.getConnection(); Statement st = c.createStatement(); ResultSet rs = st.executeQuery("SELECT id, name, email FROM users ORDER BY id")) {
            while (rs.next()) out.add(map(rs));
            return out;
        } catch (SQLException e) { throw new IllegalStateException(e); }
    }
    public long count() {
        try (Connection c = ds.getConnection(); Statement st = c.createStatement(); ResultSet rs = st.executeQuery("SELECT COUNT(*) FROM users")) {
            rs.next(); return rs.getLong(1);
        } catch (SQLException e) { throw new IllegalStateException(e); }
    }
}
'''
TEST1 = "package %PKG%;\n\n" + TEST_IMPORTS + r'''
class UserDaoTest {

    private UserDao dao;

    @BeforeEach
    void setUp() throws Exception {
        DataSource ds = newDataSource();
        exec(ds, "create table users (id bigint primary key, name varchar(50), email varchar(100))",
                "insert into users values (2, 'Bo', 'bo@x.io')", "insert into users values (1, 'Ana', 'ana@x.io')",
                "insert into users values (3, 'Cy', 'cy@x.io')");
        dao = new UserDao(ds);
    }
''' + DS_HELPER_TEST + r'''
    @Test
    void findsExistingUser() {
        assertThat(dao.findById(1)).contains(new User(1, "Ana", "ana@x.io"));
    }

    @Test
    void missingUserIsEmpty() {
        assertThat(dao.findById(99)).isEmpty();
    }

    @Test
    void findAllIsOrderedById() {
        assertThat(dao.findAll()).extracting(User::name).containsExactly("Ana", "Bo", "Cy");
    }

    @Test
    void countsRows() {
        assertThat(dao.count()).isEqualTo(3);
    }
}
'''
k1 = task("jdbc-select-dao", "JDBC SELECT DAO", "Warm-up", "Plain Java + JDBC (H2)",
    "Implement a read-only DAO with try-with-resources: findById, findAll and count against an H2 DataSource.",
    "h2", {"main/User.java": USER_REC, "main/UserDao.java": DAO1, "test/UserDaoTest.java": TEST1},
    ["Implement `findById`, `findAll` (ordered by id) and `count` using JDBC only.", "Close every Connection, Statement and ResultSet with try-with-resources.",
     "Wrap `SQLException` in an unchecked exception (e.g. `IllegalStateException`) — never swallow it."],
    ["Missing id -> `Optional.empty()`, not null and not an exception.", "Empty table -> `findAll()` returns an empty list and `count()` returns 0."],
    ["`ResultSet` columns can be read by name: `rs.getLong(\"id\")`.", "Extract a `mapRow(ResultSet)` helper to avoid duplication."],
    sol={"main/UserDao.java": DAO1_SOL})

# ------------------------------------------------------------- task 2
DAO2 = r'''package %PKG%;

import java.util.List;
import javax.sql.DataSource;

/** Table: users(id BIGINT AUTO_INCREMENT PK, name VARCHAR(50), email VARCHAR(100)). */
public class SafeSearchDao {

    private final DataSource dataSource;

    public SafeSearchDao(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    /** PROVIDED — shows the VULNERABLE pattern. Never execute this string. */
    public static String buildUnsafeSql(String name) {
        return "SELECT id, name, email FROM users WHERE name = '" + name + "'";
    }

    /** Exact name match using a PreparedStatement parameter; ordered by id. */
    public List<User> findByName(String name) {
        // TODO(%TAG%): prepared statement with a ? placeholder (no string concatenation)
        throw new UnsupportedOperationException("TODO(%TAG%): implement findByName");
    }

    /**
     * Names starting with the prefix, ordered by name. The prefix is LITERAL text: '%' and '_' in the prefix must be
     * escaped (use LIKE ? ESCAPE '\\' and escape \\, % and _ with a backslash).
     */
    public List<User> findByNamePrefix(String prefix) {
        // TODO(%TAG%): LIKE ? ESCAPE with an escaped prefix + "%"
        throw new UnsupportedOperationException("TODO(%TAG%): implement findByNamePrefix");
    }

    /** Inserts a user and returns the generated id (Statement.RETURN_GENERATED_KEYS). */
    public long insertUser(String name, String email) {
        // TODO(%TAG%): insert with a prepared statement and read the generated key
        throw new UnsupportedOperationException("TODO(%TAG%): implement insertUser");
    }
}
'''
DAO2_SOL = r'''package %PKG%;

import java.sql.*;
import java.util.*;
import javax.sql.DataSource;

public class SafeSearchDao {
    private final DataSource ds;
    public SafeSearchDao(DataSource ds) { this.ds = ds; }
    public static String buildUnsafeSql(String name) { return "SELECT id, name, email FROM users WHERE name = '" + name + "'"; }
    private List<User> query(String sql, String param) {
        List<User> out = new ArrayList<>();
        try (Connection c = ds.getConnection(); PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, param);
            try (ResultSet rs = ps.executeQuery()) { while (rs.next()) out.add(new User(rs.getLong(1), rs.getString(2), rs.getString(3))); }
            return out;
        } catch (SQLException e) { throw new IllegalStateException(e); }
    }
    public List<User> findByName(String name) { return query("SELECT id, name, email FROM users WHERE name = ? ORDER BY id", name); }
    public List<User> findByNamePrefix(String prefix) {
        String esc = prefix.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_");
        return query("SELECT id, name, email FROM users WHERE name LIKE ? ESCAPE '\\' ORDER BY name", esc + "%");
    }
    public long insertUser(String name, String email) {
        try (Connection c = ds.getConnection(); PreparedStatement ps = c.prepareStatement("INSERT INTO users(name, email) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, name); ps.setString(2, email); ps.executeUpdate();
            try (ResultSet k = ps.getGeneratedKeys()) { k.next(); return k.getLong(1); }
        } catch (SQLException e) { throw new IllegalStateException(e); }
    }
}
'''
TEST2 = "package %PKG%;\n\n" + TEST_IMPORTS + r'''
class SafeSearchDaoTest {

    private DataSource ds;
    private SafeSearchDao dao;

    @BeforeEach
    void setUp() throws Exception {
        ds = newDataSource();
        exec(ds, "create table users (id bigint auto_increment primary key, name varchar(50), email varchar(100))",
                "insert into users(name, email) values ('Ana', 'ana@x.io')",
                "insert into users(name, email) values ('Anders', 'an@x.io')",
                "insert into users(name, email) values ('Bob', 'bob@x.io')",
                "insert into users(name, email) values ('100%', 'pct@x.io')");
        dao = new SafeSearchDao(ds);
    }
''' + DS_HELPER_TEST + r'''
    @Test
    void unsafeSqlShowsTheInjection() {
        assertThat(SafeSearchDao.buildUnsafeSql("x' OR '1'='1")).contains("OR '1'='1");
    }

    @Test
    void findsByExactName() {
        assertThat(dao.findByName("Ana")).extracting(User::email).containsExactly("ana@x.io");
    }

    @Test
    void injectionPayloadIsJustAName() {
        assertThat(dao.findByName("x' OR '1'='1")).isEmpty();
        assertThat(dao.findByName("' OR 1=1 --")).isEmpty();
    }

    @Test
    void prefixSearchTreatsPercentLiterally() {
        assertThat(dao.findByNamePrefix("An")).extracting(User::name).containsExactly("Ana", "Anders");
        assertThat(dao.findByNamePrefix("%")).isEmpty();
        assertThat(dao.findByNamePrefix("100")).extracting(User::name).containsExactly("100%");
    }

    @Test
    void insertReturnsGeneratedIdAndPersists() {
        long id = dao.insertUser("Cy", "cy@x.io");
        assertThat(id).isGreaterThan(4);
        assertThat(dao.findByName("Cy")).extracting(User::id).containsExactly(id);
    }

    @Test
    void insertCanStoreQuotesSafely() {
        dao.insertUser("O'Brien", "ob@x.io");
        assertThat(dao.findByName("O'Brien")).hasSize(1);
    }
}
'''
k2 = task("prepared-statement-safe", "PreparedStatement and SQL Injection", "Core", "Plain Java + JDBC (H2)",
    "Replace vulnerable string concatenation with PreparedStatement parameters, escape LIKE wildcards, and return generated keys.",
    "h2", {"main/User.java": USER_REC, "main/SafeSearchDao.java": DAO2, "test/SafeSearchDaoTest.java": TEST2},
    ["Implement `findByName` with a `?` placeholder.", "Implement `findByNamePrefix` so `%` and `_` in user input are literal.", "Implement `insertUser` returning the generated id.",
     "Never concatenate user input into SQL (the provided `buildUnsafeSql` is the anti-example)."],
    ["Quotes in names (`O'Brien`) must work without escaping by hand.", "Injection payloads match nothing.", "Prefix `%` must not match every row."],
    ["Escape the user prefix first, then append the real wildcard `%`.", "`connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)`."],
    sol={"main/SafeSearchDao.java": DAO2_SOL})

# ------------------------------------------------------------- task 3
SVC3 = r'''package %PKG%;

import javax.sql.DataSource;

/** Table: accounts(id BIGINT PK, balance_cents BIGINT NOT NULL CHECK (balance_cents >= 0)). */
public class TransferService {

    private final DataSource dataSource;

    public TransferService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public long balanceOf(long accountId) {
        // TODO(%TAG%): SELECT balance_cents; unknown account -> IllegalArgumentException
        throw new UnsupportedOperationException("TODO(%TAG%): implement balanceOf");
    }

    /**
     * Moves money atomically: setAutoCommit(false), debit, credit, commit. On ANY failure rollback and rethrow.
     * - amount &lt;= 0 or from == to  -> IllegalArgumentException (before touching the database)
     * - source balance &lt; amount     -> IllegalStateException("insufficient funds") and nothing changes
     * - unknown source/destination   -> IllegalArgumentException and nothing changes (no half transfer!)
     * Restore autoCommit(true) before the connection returns to the pool.
     */
    public void transfer(long fromId, long toId, long amountCents) {
        // TODO(%TAG%): implement the transactional transfer described above
        throw new UnsupportedOperationException("TODO(%TAG%): implement transfer");
    }
}
'''
SVC3_SOL = r'''package %PKG%;

import java.sql.*;
import javax.sql.DataSource;

public class TransferService {
    private final DataSource ds;
    public TransferService(DataSource ds) { this.ds = ds; }
    public long balanceOf(long id) {
        try (Connection c = ds.getConnection()) { return balance(c, id); } catch (SQLException e) { throw new IllegalStateException(e); }
    }
    private long balance(Connection c, long id) throws SQLException {
        try (PreparedStatement ps = c.prepareStatement("SELECT balance_cents FROM accounts WHERE id = ?")) {
            ps.setLong(1, id);
            try (ResultSet rs = ps.executeQuery()) { if (!rs.next()) throw new IllegalArgumentException("unknown account " + id); return rs.getLong(1); }
        }
    }
    private void add(Connection c, long id, long delta) throws SQLException {
        try (PreparedStatement ps = c.prepareStatement("UPDATE accounts SET balance_cents = balance_cents + ? WHERE id = ?")) {
            ps.setLong(1, delta); ps.setLong(2, id);
            if (ps.executeUpdate() != 1) throw new IllegalArgumentException("unknown account " + id);
        }
    }
    public void transfer(long from, long to, long amount) {
        if (amount <= 0 || from == to) throw new IllegalArgumentException("bad transfer");
        try (Connection c = ds.getConnection()) {
            c.setAutoCommit(false);
            try {
                if (balance(c, from) < amount) throw new IllegalStateException("insufficient funds");
                add(c, from, -amount);
                add(c, to, amount);
                c.commit();
            } catch (RuntimeException | SQLException e) {
                c.rollback();
                if (e instanceof SQLException se) throw new IllegalStateException(se);
                throw (RuntimeException) e;
            } finally { c.setAutoCommit(true); }
        } catch (SQLException e) { throw new IllegalStateException(e); }
    }
}
'''
TEST3 = "package %PKG%;\n\n" + TEST_IMPORTS + r'''
class TransferServiceTest {

    private TransferService svc;

    @BeforeEach
    void setUp() throws Exception {
        DataSource ds = newDataSource();
        exec(ds, "create table accounts (id bigint primary key, balance_cents bigint not null check (balance_cents >= 0))",
                "insert into accounts values (1, 10000)", "insert into accounts values (2, 5000)");
        svc = new TransferService(ds);
    }
''' + DS_HELPER_TEST + r'''
    @Test
    void transferMovesMoney() {
        svc.transfer(1, 2, 3000);
        assertThat(svc.balanceOf(1)).isEqualTo(7000);
        assertThat(svc.balanceOf(2)).isEqualTo(8000);
    }

    @Test
    void insufficientFundsChangesNothing() {
        assertThatThrownBy(() -> svc.transfer(2, 1, 5001)).isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("insufficient");
        assertThat(svc.balanceOf(1)).isEqualTo(10000);
        assertThat(svc.balanceOf(2)).isEqualTo(5000);
    }

    @Test
    void unknownDestinationRollsBackTheDebit() {
        assertThatThrownBy(() -> svc.transfer(1, 99, 100)).isInstanceOf(IllegalArgumentException.class);
        assertThat(svc.balanceOf(1)).isEqualTo(10000);
    }

    @Test
    void invalidArguments() {
        assertThatThrownBy(() -> svc.transfer(1, 2, 0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> svc.transfer(1, 1, 10)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> svc.balanceOf(42)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void totalMoneyIsConservedAfterManyTransfers() {
        for (int i = 0; i < 10; i++) {
            svc.transfer(1, 2, 100);
            svc.transfer(2, 1, 50);
        }
        assertThat(svc.balanceOf(1) + svc.balanceOf(2)).isEqualTo(15000);
    }
}
'''
k3 = task("transaction-transfer", "JDBC Transaction Transfer", "Core", "Plain Java + JDBC (H2)",
    "Implement an atomic money transfer with manual commit/rollback and restore autocommit afterwards.",
    "h2", {"main/TransferService.java": SVC3, "test/TransferServiceTest.java": TEST3},
    ["Implement `balanceOf`.", "Implement `transfer` in one transaction: validate, check funds, debit, credit, commit.", "Roll back on any failure and rethrow the original unchecked exception.",
     "Always restore `autoCommit(true)` in a finally block."],
    ["Unknown destination: the debit must be undone.", "`amount <= 0` or same account: reject before opening a transaction.", "Total money is invariant."],
    ["Do the unknown-account check by inspecting `executeUpdate()` row counts.", "Use one Connection for the whole transfer — transactions are per connection."],
    sol={"main/TransferService.java": SVC3_SOL})

# ------------------------------------------------------------- task 4
POOL_MAIN = r'''package %PKG%;

import com.zaxxer.hikari.HikariConfig;
import java.util.Properties;

/** Reads datasource settings the way Spring Boot/Hikari expect them. */
public final class PoolSettingsReader {

    private PoolSettingsReader() {
    }

    /** PROVIDED value object. */
    public record PoolSettings(String jdbcUrl, String username, String password, int maximumPoolSize,
                               int minimumIdle, long connectionTimeoutMs) {
    }

    /**
     * Keys: jdbcUrl (required, non-blank), username, password (default ""), maximumPoolSize (default 10, must be &gt;= 1),
     * minimumIdle (default = maximumPoolSize, must be 0..maximumPoolSize), connectionTimeoutMs (default 30000, must be &gt;= 250).
     * Any violation (including non-numeric numbers) -> IllegalArgumentException whose message names the key.
     */
    public static PoolSettings read(Properties props) {
        // TODO(%TAG%): parse + validate as documented
        throw new UnsupportedOperationException("TODO(%TAG%): implement read");
    }

    /** Copies the settings into a HikariConfig (jdbcUrl, username, password, maximumPoolSize, minimumIdle, connectionTimeout). */
    public static HikariConfig toHikariConfig(PoolSettings s) {
        // TODO(%TAG%): populate and return a HikariConfig
        throw new UnsupportedOperationException("TODO(%TAG%): implement toHikariConfig");
    }

    /**
     * Log-safe one-liner, exactly: {@code jdbcUrl=<url>; user=<user>; password=****; max=<n>; minIdle=<n>; timeoutMs=<n>}.
     * The real password must never appear.
     */
    public static String maskedSummary(PoolSettings s) {
        // TODO(%TAG%): build the masked summary string
        throw new UnsupportedOperationException("TODO(%TAG%): implement maskedSummary");
    }
}
'''
POOL_SOL = r'''package %PKG%;

import com.zaxxer.hikari.HikariConfig;
import java.util.Properties;

public final class PoolSettingsReader {
    public record PoolSettings(String jdbcUrl, String username, String password, int maximumPoolSize, int minimumIdle, long connectionTimeoutMs) { }
    private static int num(Properties p, String key, int def) {
        String v = p.getProperty(key);
        if (v == null || v.isBlank()) return def;
        try { return Integer.parseInt(v.trim()); } catch (NumberFormatException e) { throw new IllegalArgumentException(key + " must be a number", e); }
    }
    public static PoolSettings read(Properties p) {
        String url = p.getProperty("jdbcUrl");
        if (url == null || url.isBlank()) throw new IllegalArgumentException("jdbcUrl is required");
        int max = num(p, "maximumPoolSize", 10);
        if (max < 1) throw new IllegalArgumentException("maximumPoolSize must be >= 1");
        int min = num(p, "minimumIdle", max);
        if (min < 0 || min > max) throw new IllegalArgumentException("minimumIdle must be between 0 and maximumPoolSize");
        int timeout = num(p, "connectionTimeoutMs", 30000);
        if (timeout < 250) throw new IllegalArgumentException("connectionTimeoutMs must be >= 250");
        return new PoolSettings(url.trim(), p.getProperty("username", ""), p.getProperty("password", ""), max, min, timeout);
    }
    public static HikariConfig toHikariConfig(PoolSettings s) {
        HikariConfig c = new HikariConfig();
        c.setJdbcUrl(s.jdbcUrl()); c.setUsername(s.username()); c.setPassword(s.password());
        c.setMaximumPoolSize(s.maximumPoolSize()); c.setMinimumIdle(s.minimumIdle()); c.setConnectionTimeout(s.connectionTimeoutMs());
        return c;
    }
    public static String maskedSummary(PoolSettings s) {
        return "jdbcUrl=" + s.jdbcUrl() + "; user=" + s.username() + "; password=****; max=" + s.maximumPoolSize()
                + "; minIdle=" + s.minimumIdle() + "; timeoutMs=" + s.connectionTimeoutMs();
    }
}
'''
TEST4 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import java.sql.Connection;
import java.util.Properties;
import org.junit.jupiter.api.Test;

class PoolSettingsReaderTest {

    private static Properties base() {
        Properties p = new Properties();
        p.setProperty("jdbcUrl", "jdbc:h2:mem:pool_test;DB_CLOSE_DELAY=-1");
        p.setProperty("username", "sa");
        p.setProperty("password", "s3cret");
        return p;
    }

    @Test
    void appliesDefaults() {
        PoolSettingsReader.PoolSettings s = PoolSettingsReader.read(base());
        assertThat(s.maximumPoolSize()).isEqualTo(10);
        assertThat(s.minimumIdle()).isEqualTo(10);
        assertThat(s.connectionTimeoutMs()).isEqualTo(30000);
        assertThat(s.username()).isEqualTo("sa");
    }

    @Test
    void readsExplicitValues() {
        Properties p = base();
        p.setProperty("maximumPoolSize", "5");
        p.setProperty("minimumIdle", "2");
        p.setProperty("connectionTimeoutMs", "1000");
        PoolSettingsReader.PoolSettings s = PoolSettingsReader.read(p);
        assertThat(s.maximumPoolSize()).isEqualTo(5);
        assertThat(s.minimumIdle()).isEqualTo(2);
        assertThat(s.connectionTimeoutMs()).isEqualTo(1000);
    }

    @Test
    void rejectsInvalidSettings() {
        Properties noUrl = new Properties();
        assertThatThrownBy(() -> PoolSettingsReader.read(noUrl)).isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("jdbcUrl");
        Properties zero = base();
        zero.setProperty("maximumPoolSize", "0");
        assertThatThrownBy(() -> PoolSettingsReader.read(zero)).isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("maximumPoolSize");
        Properties idle = base();
        idle.setProperty("maximumPoolSize", "3");
        idle.setProperty("minimumIdle", "4");
        assertThatThrownBy(() -> PoolSettingsReader.read(idle)).isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("minimumIdle");
        Properties nan = base();
        nan.setProperty("maximumPoolSize", "many");
        assertThatThrownBy(() -> PoolSettingsReader.read(nan)).isInstanceOf(IllegalArgumentException.class);
        Properties timeout = base();
        timeout.setProperty("connectionTimeoutMs", "10");
        assertThatThrownBy(() -> PoolSettingsReader.read(timeout)).isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("connectionTimeoutMs");
    }

    @Test
    void summaryNeverLeaksPassword() {
        PoolSettingsReader.PoolSettings s = PoolSettingsReader.read(base());
        String summary = PoolSettingsReader.maskedSummary(s);
        assertThat(summary).doesNotContain("s3cret").contains("password=****");
        assertThat(summary).isEqualTo("jdbcUrl=jdbc:h2:mem:pool_test;DB_CLOSE_DELAY=-1; user=sa; password=****; max=10; minIdle=10; timeoutMs=30000");
    }

    @Test
    void hikariConfigIsUsableToOpenAPool() throws Exception {
        Properties p = base();
        p.setProperty("maximumPoolSize", "2");
        p.setProperty("minimumIdle", "1");
        HikariConfig cfg = PoolSettingsReader.toHikariConfig(PoolSettingsReader.read(p));
        assertThat(cfg.getMaximumPoolSize()).isEqualTo(2);
        assertThat(cfg.getMinimumIdle()).isEqualTo(1);
        assertThat(cfg.getUsername()).isEqualTo("sa");
        try (HikariDataSource ds = new HikariDataSource(cfg); Connection c = ds.getConnection()) {
            assertThat(c.isValid(1)).isTrue();
        }
    }
}
'''
k4 = task("hikari-config-reader", "HikariCP Config Reader", "Challenge", "Plain Java + JDBC (H2)",
    "Parse and validate connection-pool settings from Properties, build a HikariConfig, and produce a log-safe summary that masks the password.",
    "h2", {"main/PoolSettingsReader.java": POOL_MAIN, "test/PoolSettingsReaderTest.java": TEST4},
    ["Implement `read` with defaults and validation (messages must mention the offending key).", "Implement `toHikariConfig`.", "Implement `maskedSummary` with the exact format.",
     "Open a real HikariCP pool in the last test to prove the config works."],
    ["Blank or missing `jdbcUrl` is an error.", "`minimumIdle` defaults to `maximumPoolSize`.", "Non-numeric values -> `IllegalArgumentException`.", "The password must never appear in the summary."],
    ["`Integer.parseInt` throws `NumberFormatException` (a subclass of `IllegalArgumentException`) — still add the key name to the message.", "HikariCP 6.2.1 is an optional dependency used only by this task."],
    deps=[dep("com.zaxxer", "HikariCP", "6.2.1")], sol={"main/PoolSettingsReader.java": POOL_SOL})

topics = [
    T("JDBC fundamentals and the DAO pattern",
      "**JDBC** is Java's standard API for relational databases: a `DataSource` hands out `Connection`s; a `Statement`/`PreparedStatement` executes SQL; a `ResultSet` iterates rows. A **DAO** (Data Access Object) hides this behind methods like `findById` so the rest of the code never touches SQL or `SQLException`.",
      "Every persistence framework (JPA, Spring JDBC, MyBatis) is built on JDBC. Understanding the primitives explains connection leaks, transaction boundaries and exception translation you will meet in Spring.",
      ["Standard, driver-independent API", "Full control of SQL and performance", "Simple to debug (what you write is what runs)", "DAO isolates persistence from business logic"],
      ["Verbose boilerplate (open/close/map)", "Manual mapping from rows to objects", "Checked `SQLException` everywhere"],
      "Not closing `Connection`/`Statement`/`ResultSet` leaks resources until the pool is exhausted (`Connection is not available, request timed out`). Swallowing `SQLException` hides failures and returns misleading empty results.",
      "```java\ntry (Connection c = ds.getConnection();\n     PreparedStatement ps = c.prepareStatement(\"SELECT id, name FROM users WHERE id = ?\")) {\n    ps.setLong(1, id);\n    try (ResultSet rs = ps.executeQuery()) {\n        return rs.next() ? Optional.of(map(rs)) : Optional.empty();\n    }\n} catch (SQLException e) { throw new IllegalStateException(e); }\n```\nResultSet cursors start *before* the first row; `rs.next()` advances. Column indexes are 1-based.",
      [("Read many rows", "java", "List<User> out = new ArrayList<>();\ntry (Connection c = ds.getConnection(); Statement st = c.createStatement();\n     ResultSet rs = st.executeQuery(\"SELECT id, name FROM users ORDER BY id\")) {\n    while (rs.next()) out.add(new User(rs.getLong(\"id\"), rs.getString(\"name\")));\n}"),
       ("H2 DataSource for tests", "java", "JdbcDataSource ds = new JdbcDataSource();\nds.setURL(\"jdbc:h2:mem:test;DB_CLOSE_DELAY=-1\");\nds.setUser(\"sa\");"),
       ("DAO interface", "java", "public interface UserDao {\n    Optional<User> findById(long id);\n    List<User> findAll();\n}")],
      [("Why try-with-resources for JDBC objects?", "They implement AutoCloseable; closing guarantees the connection returns to the pool even on exceptions."),
       ("What does `rs.next()` return on an empty result?", "false; no row is available."),
       ("Why wrap SQLException in an unchecked exception in a DAO?", "Callers usually cannot recover; unchecked exceptions keep business code clean (Spring does the same).")]),
    T("PreparedStatement and SQL injection",
      "A `PreparedStatement` sends SQL with `?` placeholders and sends parameter values separately, so the database treats values as data, never as SQL. **SQL injection** is when untrusted input is concatenated into SQL and changes its meaning (`' OR '1'='1`).",
      "SQL injection is consistently a top web vulnerability: it leaks data, bypasses login, and deletes tables. Prepared statements also let the database cache plans and handle quoting/escaping/types correctly.",
      ["Eliminates injection for values", "Correct handling of quotes and special characters", "Plan reuse and better performance on repeated calls", "Type-safe setters (`setLong`, `setTimestamp`)"],
      ["Placeholders cannot be used for identifiers (table/column names) or `ORDER BY` direction — use a whitelist", "`LIKE` wildcards in user input still need escaping", "Lists in `IN (...)` need generated placeholders"],
      "`\"... WHERE name = '\" + name + \"'\"` with input `x' OR '1'='1` returns every row; `'; DROP TABLE users; --` can destroy data (depending on driver/multi-statement support). Quotes in valid names like `O'Brien` raise syntax errors.",
      "```java\nPreparedStatement ps = c.prepareStatement(\"SELECT * FROM users WHERE name = ?\");\nps.setString(1, userInput);\n```\nFor dynamic ORDER BY: `String col = switch (sort) { case \"name\" -> \"name\"; default -> \"id\"; };` and concatenate only the whitelisted constant. For LIKE: escape `\\`, `%`, `_` then add your own `%`.",
      [("Vulnerable vs safe", "java", "String bad  = \"SELECT * FROM users WHERE name = '\" + name + \"'\";   // NEVER\nString good = \"SELECT * FROM users WHERE name = ?\";                  // setString(1, name)"),
       ("Generated keys", "java", "PreparedStatement ps = c.prepareStatement(\"INSERT INTO users(name) VALUES (?)\", Statement.RETURN_GENERATED_KEYS);\nps.setString(1, \"Cy\"); ps.executeUpdate();\ntry (ResultSet k = ps.getGeneratedKeys()) { k.next(); long id = k.getLong(1); }"),
       ("Whitelist for ORDER BY", "java", "String col = switch (sort) { case \"email\" -> \"email\"; default -> \"id\"; };\nString sql = \"SELECT * FROM users ORDER BY \" + col;")],
      [("Can placeholders replace a column name?", "No — only values; use a whitelist for identifiers."),
       ("What does `x' OR '1'='1` do in a concatenated query?", "Closes the string literal and appends an always-true condition, returning all rows."),
       ("Is escaping quotes by hand a good defence?", "No; it is error-prone and encoding-dependent — use parameters.")]),
    T("JDBC transactions",
      "By default a JDBC connection is in **autocommit** mode: each statement is its own transaction. For multi-step work call `setAutoCommit(false)`, run statements on the **same connection**, then `commit()` or `rollback()`.",
      "Transfers, order placement and inventory updates must be all-or-nothing. Spring's `@Transactional` (Day 35) automates exactly this pattern.",
      ["Atomic multi-statement operations", "Explicit control over the unit of work", "Rollback on failure keeps data consistent", "Foundation for understanding `@Transactional`"],
      ["Easy to leak transactions (forgetting rollback/close)", "Long transactions hold locks", "Pooled connections must be reset to autocommit before reuse"],
      "With autocommit still on, a failure after the debit leaves money missing. Using two different connections for debit and credit makes them separate transactions. Forgetting `setAutoCommit(true)` hands a transactional connection to the next caller.",
      "```java\ntry (Connection c = ds.getConnection()) {\n    c.setAutoCommit(false);\n    try {\n        debit(c); credit(c);\n        c.commit();\n    } catch (Exception e) {\n        c.rollback();\n        throw e;\n    } finally {\n        c.setAutoCommit(true);\n    }\n}\n```\nUse `executeUpdate()` row counts to detect missing rows; use `Savepoint` for partial rollback.",
      [("Commit/rollback skeleton", "java", "c.setAutoCommit(false);\ntry { work(c); c.commit(); } catch (RuntimeException e) { c.rollback(); throw e; }"),
       ("Detect unknown account", "java", "if (ps.executeUpdate() != 1) throw new IllegalArgumentException(\"unknown account\");"),
       ("Isolation level", "java", "c.setTransactionIsolation(Connection.TRANSACTION_REPEATABLE_READ);")],
      [("Why must debit and credit use one Connection?", "A transaction is bound to a connection; separate connections commit independently."),
       ("What does rollback() do after a failed credit?", "Undoes the earlier debit made on the same connection."),
       ("Why reset autoCommit in finally?", "Pooled connections are reused; leaving it false changes behavior for the next borrower.")]),
    T("Connection pooling with HikariCP",
      "Opening a database connection is expensive (TCP, auth, session setup). A **connection pool** keeps a bounded set of open connections and lends them out. **HikariCP** is the fast default pool in Spring Boot. Key settings: `maximumPoolSize`, `minimumIdle`, `connectionTimeout`, `maxLifetime`, `idleTimeout`.",
      "Under load an unpooled app opens a new connection per request, overloading the database. A too-large pool also overloads it. Sizing and timeouts are core operations topics.",
      ["Reuses connections: far lower latency", "Bounds concurrency to protect the database", "Health checks and leak detection", "Boot auto-configures it from `spring.datasource.hikari.*`"],
      ["Wrong sizing causes timeouts or DB saturation", "Leaked connections exhaust the pool", "Pools hide transaction state bugs (autocommit not reset)"],
      "`HikariPool-1 - Connection is not available, request timed out after 30000ms` means all connections are in use (leak or too small a pool). Never log passwords from `HikariConfig`.",
      "```java\nHikariConfig cfg = new HikariConfig();\ncfg.setJdbcUrl(url); cfg.setUsername(u); cfg.setPassword(p);\ncfg.setMaximumPoolSize(10); cfg.setConnectionTimeout(30_000);\ntry (HikariDataSource ds = new HikariDataSource(cfg)) { ... }\n```\nSpring Boot: `spring.datasource.hikari.maximum-pool-size=10`. Rule of thumb: pool size ≈ (core_count * 2) + effective_spindle_count; start small.",
      [("Programmatic pool", "java", "HikariConfig cfg = new HikariConfig();\ncfg.setJdbcUrl(\"jdbc:h2:mem:app\");\ncfg.setMaximumPoolSize(5);\nHikariDataSource ds = new HikariDataSource(cfg);"),
       ("Boot properties", "yaml", "spring:\n  datasource:\n    url: jdbc:postgresql://localhost:5432/app\n    hikari:\n      maximum-pool-size: 10\n      connection-timeout: 30000"),
       ("Masking secrets", "java", "String summary = \"jdbcUrl=\" + url + \"; password=****\";")],
      [("What error signals pool exhaustion?", "`Connection is not available, request timed out` from HikariPool."),
       ("Why is a bigger pool not always better?", "More concurrent queries can overload the database and slow everything."),
       ("How do you find a leaked connection?", "Enable `leakDetectionThreshold` and inspect the stack trace it logs.")]),
]

day(27, "JDBC, PreparedStatement, DAO, HikariCP, and SQL Injection", "SQL/JDBC",
    "The JDBC primitives under every Java persistence framework: DAOs, safe parameters, transactions, and pooling",
    ["Write a DAO with try-with-resources over DataSource/Connection/PreparedStatement/ResultSet", "Demonstrate and prevent SQL injection with parameters and whitelists",
     "Implement atomic JDBC transactions with commit/rollback", "Read and validate HikariCP pool settings and build a HikariConfig", "Explain pool exhaustion and sizing"],
    ["Day 25–26 SQL fundamentals", "Exceptions and try-with-resources from earlier core Java days"],
    topics, [k1, k2, k3, k4],
    [("Why PreparedStatement over Statement?", "Prevents SQL injection, handles escaping/types, allows plan caching."),
     ("What is a connection pool and why use it?", "A set of reusable open connections; avoids per-request connection cost and bounds DB load."),
     ("How does JDBC transaction control work?", "setAutoCommit(false), run statements on one connection, commit() or rollback()."),
     ("What's the difference between Statement.execute, executeQuery, executeUpdate?", "execute is generic; executeQuery returns a ResultSet; executeUpdate returns an affected-row count."),
     ("How do you pick a pool size?", "Start small (about 2x cores + disks), measure; increase only if threads wait and the database has headroom.")],
    ["Concatenating input into `ORDER BY`/table names without a whitelist.", "Forgetting to close ResultSet/Statement (use try-with-resources).", "Starting a transaction on one connection and querying with another.",
     "Logging full JDBC properties including passwords."],
    ["Oracle JDBC tutorial; `java.sql` Javadoc", "HikariCP README (About Pool Sizing)", "OWASP SQL Injection Prevention Cheat Sheet"],
    [("DAO", "Data Access Object"), ("DataSource", "Factory for Connections, usually pooled"), ("Autocommit", "Each statement commits automatically"),
     ("SQL injection", "Attacker-controlled input altering SQL structure"), ("HikariCP", "High-performance JDBC connection pool")],
    "2–3 h theory + 3–5 h tasks")
