# Day 27 — JDBC, PreparedStatement, DAO, HikariCP, and SQL Injection

**Phase:** SQL/JDBC  
**Primary theme:** The JDBC primitives under every Java persistence framework: DAOs, safe parameters, transactions, and pooling  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-jdbc-select-dao`, `task-02-prepared-statement-safe`, `task-03-transaction-transfer`, `task-04-hikari-config-reader`  
**Instruction alignment:** Maps to Day 27 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, H2 2.3.232 (PostgreSQL mode)

## Overview

The JDBC primitives under every Java persistence framework: DAOs, safe parameters, transactions, and pooling. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. JDBC fundamentals and the DAO pattern
2. PreparedStatement and SQL injection
3. JDBC transactions
4. Connection pooling with HikariCP
5. Interview corner, common mistakes, glossary

## Subtopics

### JDBC fundamentals and the DAO pattern

#### What it is

**JDBC** is Java's standard API for relational databases: a `DataSource` hands out `Connection`s; a `Statement`/`PreparedStatement` executes SQL; a `ResultSet` iterates rows. A **DAO** (Data Access Object) hides this behind methods like `findById` so the rest of the code never touches SQL or `SQLException`.

#### Why it exists / why it matters

Every persistence framework (JPA, Spring JDBC, MyBatis) is built on JDBC. Understanding the primitives explains connection leaks, transaction boundaries and exception translation you will meet in Spring.

#### Pros and cons

**Pros**

- Standard, driver-independent API
- Full control of SQL and performance
- Simple to debug (what you write is what runs)
- DAO isolates persistence from business logic

**Cons / trade-offs**

- Verbose boilerplate (open/close/map)
- Manual mapping from rows to objects
- Checked `SQLException` everywhere

#### What happens without it / when misused

Not closing `Connection`/`Statement`/`ResultSet` leaks resources until the pool is exhausted (`Connection is not available, request timed out`). Swallowing `SQLException` hides failures and returns misleading empty results.

#### Syntax and rules

```java
try (Connection c = ds.getConnection();
     PreparedStatement ps = c.prepareStatement("SELECT id, name FROM users WHERE id = ?")) {
    ps.setLong(1, id);
    try (ResultSet rs = ps.executeQuery()) {
        return rs.next() ? Optional.of(map(rs)) : Optional.empty();
    }
} catch (SQLException e) { throw new IllegalStateException(e); }
```
ResultSet cursors start *before* the first row; `rs.next()` advances. Column indexes are 1-based.

#### Examples

**Example 1 — Read many rows**

```java
List<User> out = new ArrayList<>();
try (Connection c = ds.getConnection(); Statement st = c.createStatement();
     ResultSet rs = st.executeQuery("SELECT id, name FROM users ORDER BY id")) {
    while (rs.next()) out.add(new User(rs.getLong("id"), rs.getString("name")));
}
```

**Example 2 — H2 DataSource for tests**

```java
JdbcDataSource ds = new JdbcDataSource();
ds.setURL("jdbc:h2:mem:test;DB_CLOSE_DELAY=-1");
ds.setUser("sa");
```

**Example 3 — DAO interface**

```java
public interface UserDao {
    Optional<User> findById(long id);
    List<User> findAll();
}
```

#### Quick checks

1. Why try-with-resources for JDBC objects?
2. What does `rs.next()` return on an empty result?
3. Why wrap SQLException in an unchecked exception in a DAO?

### PreparedStatement and SQL injection

#### What it is

A `PreparedStatement` sends SQL with `?` placeholders and sends parameter values separately, so the database treats values as data, never as SQL. **SQL injection** is when untrusted input is concatenated into SQL and changes its meaning (`' OR '1'='1`).

#### Why it exists / why it matters

SQL injection is consistently a top web vulnerability: it leaks data, bypasses login, and deletes tables. Prepared statements also let the database cache plans and handle quoting/escaping/types correctly.

#### Pros and cons

**Pros**

- Eliminates injection for values
- Correct handling of quotes and special characters
- Plan reuse and better performance on repeated calls
- Type-safe setters (`setLong`, `setTimestamp`)

**Cons / trade-offs**

- Placeholders cannot be used for identifiers (table/column names) or `ORDER BY` direction — use a whitelist
- `LIKE` wildcards in user input still need escaping
- Lists in `IN (...)` need generated placeholders

#### What happens without it / when misused

`"... WHERE name = '" + name + "'"` with input `x' OR '1'='1` returns every row; `'; DROP TABLE users; --` can destroy data (depending on driver/multi-statement support). Quotes in valid names like `O'Brien` raise syntax errors.

#### Syntax and rules

```java
PreparedStatement ps = c.prepareStatement("SELECT * FROM users WHERE name = ?");
ps.setString(1, userInput);
```
For dynamic ORDER BY: `String col = switch (sort) { case "name" -> "name"; default -> "id"; };` and concatenate only the whitelisted constant. For LIKE: escape `\`, `%`, `_` then add your own `%`.

#### Examples

**Example 1 — Vulnerable vs safe**

```java
String bad  = "SELECT * FROM users WHERE name = '" + name + "'";   // NEVER
String good = "SELECT * FROM users WHERE name = ?";                  // setString(1, name)
```

**Example 2 — Generated keys**

```java
PreparedStatement ps = c.prepareStatement("INSERT INTO users(name) VALUES (?)", Statement.RETURN_GENERATED_KEYS);
ps.setString(1, "Cy"); ps.executeUpdate();
try (ResultSet k = ps.getGeneratedKeys()) { k.next(); long id = k.getLong(1); }
```

**Example 3 — Whitelist for ORDER BY**

```java
String col = switch (sort) { case "email" -> "email"; default -> "id"; };
String sql = "SELECT * FROM users ORDER BY " + col;
```

#### Quick checks

1. Can placeholders replace a column name?
2. What does `x' OR '1'='1` do in a concatenated query?
3. Is escaping quotes by hand a good defence?

### JDBC transactions

#### What it is

By default a JDBC connection is in **autocommit** mode: each statement is its own transaction. For multi-step work call `setAutoCommit(false)`, run statements on the **same connection**, then `commit()` or `rollback()`.

#### Why it exists / why it matters

Transfers, order placement and inventory updates must be all-or-nothing. Spring's `@Transactional` (Day 35) automates exactly this pattern.

#### Pros and cons

**Pros**

- Atomic multi-statement operations
- Explicit control over the unit of work
- Rollback on failure keeps data consistent
- Foundation for understanding `@Transactional`

**Cons / trade-offs**

- Easy to leak transactions (forgetting rollback/close)
- Long transactions hold locks
- Pooled connections must be reset to autocommit before reuse

#### What happens without it / when misused

With autocommit still on, a failure after the debit leaves money missing. Using two different connections for debit and credit makes them separate transactions. Forgetting `setAutoCommit(true)` hands a transactional connection to the next caller.

#### Syntax and rules

```java
try (Connection c = ds.getConnection()) {
    c.setAutoCommit(false);
    try {
        debit(c); credit(c);
        c.commit();
    } catch (Exception e) {
        c.rollback();
        throw e;
    } finally {
        c.setAutoCommit(true);
    }
}
```
Use `executeUpdate()` row counts to detect missing rows; use `Savepoint` for partial rollback.

#### Examples

**Example 1 — Commit/rollback skeleton**

```java
c.setAutoCommit(false);
try { work(c); c.commit(); } catch (RuntimeException e) { c.rollback(); throw e; }
```

**Example 2 — Detect unknown account**

```java
if (ps.executeUpdate() != 1) throw new IllegalArgumentException("unknown account");
```

**Example 3 — Isolation level**

```java
c.setTransactionIsolation(Connection.TRANSACTION_REPEATABLE_READ);
```

#### Quick checks

1. Why must debit and credit use one Connection?
2. What does rollback() do after a failed credit?
3. Why reset autoCommit in finally?

### Connection pooling with HikariCP

#### What it is

Opening a database connection is expensive (TCP, auth, session setup). A **connection pool** keeps a bounded set of open connections and lends them out. **HikariCP** is the fast default pool in Spring Boot. Key settings: `maximumPoolSize`, `minimumIdle`, `connectionTimeout`, `maxLifetime`, `idleTimeout`.

#### Why it exists / why it matters

Under load an unpooled app opens a new connection per request, overloading the database. A too-large pool also overloads it. Sizing and timeouts are core operations topics.

#### Pros and cons

**Pros**

- Reuses connections: far lower latency
- Bounds concurrency to protect the database
- Health checks and leak detection
- Boot auto-configures it from `spring.datasource.hikari.*`

**Cons / trade-offs**

- Wrong sizing causes timeouts or DB saturation
- Leaked connections exhaust the pool
- Pools hide transaction state bugs (autocommit not reset)

#### What happens without it / when misused

`HikariPool-1 - Connection is not available, request timed out after 30000ms` means all connections are in use (leak or too small a pool). Never log passwords from `HikariConfig`.

#### Syntax and rules

```java
HikariConfig cfg = new HikariConfig();
cfg.setJdbcUrl(url); cfg.setUsername(u); cfg.setPassword(p);
cfg.setMaximumPoolSize(10); cfg.setConnectionTimeout(30_000);
try (HikariDataSource ds = new HikariDataSource(cfg)) { ... }
```
Spring Boot: `spring.datasource.hikari.maximum-pool-size=10`. Rule of thumb: pool size ≈ (core_count * 2) + effective_spindle_count; start small.

#### Examples

**Example 1 — Programmatic pool**

```java
HikariConfig cfg = new HikariConfig();
cfg.setJdbcUrl("jdbc:h2:mem:app");
cfg.setMaximumPoolSize(5);
HikariDataSource ds = new HikariDataSource(cfg);
```

**Example 2 — Boot properties**

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/app
    hikari:
      maximum-pool-size: 10
      connection-timeout: 30000
```

**Example 3 — Masking secrets**

```java
String summary = "jdbcUrl=" + url + "; password=****";
```

#### Quick checks

1. What error signals pool exhaustion?
2. Why is a bigger pool not always better?
3. How do you find a leaked connection?

## Interview corner

**Q1. Why PreparedStatement over Statement?**

Prevents SQL injection, handles escaping/types, allows plan caching.

**Q2. What is a connection pool and why use it?**

A set of reusable open connections; avoids per-request connection cost and bounds DB load.

**Q3. How does JDBC transaction control work?**

setAutoCommit(false), run statements on one connection, commit() or rollback().

**Q4. What's the difference between Statement.execute, executeQuery, executeUpdate?**

execute is generic; executeQuery returns a ResultSet; executeUpdate returns an affected-row count.

**Q5. How do you pick a pool size?**

Start small (about 2x cores + disks), measure; increase only if threads wait and the database has headroom.

## Common mistakes & debugging

- Concatenating input into `ORDER BY`/table names without a whitelist.
- Forgetting to close ResultSet/Statement (use try-with-resources).
- Starting a transaction on one connection and querying with another.
- Logging full JDBC properties including passwords.

## Further reading

- Oracle JDBC tutorial; `java.sql` Javadoc
- HikariCP README (About Pool Sizing)
- OWASP SQL Injection Prevention Cheat Sheet

## Glossary

| Term | Meaning |
|------|---------|
| DAO | Data Access Object |
| DataSource | Factory for Connections, usually pooled |
| Autocommit | Each statement commits automatically |
| SQL injection | Attacker-controlled input altering SQL structure |
| HikariCP | High-performance JDBC connection pool |

## Answers

### JDBC fundamentals and the DAO pattern

1. They implement AutoCloseable; closing guarantees the connection returns to the pool even on exceptions.
2. false; no row is available.
3. Callers usually cannot recover; unchecked exceptions keep business code clean (Spring does the same).

### PreparedStatement and SQL injection

1. No — only values; use a whitelist for identifiers.
2. Closes the string literal and appends an always-true condition, returning all rows.
3. No; it is error-prone and encoding-dependent — use parameters.

### JDBC transactions

1. A transaction is bound to a connection; separate connections commit independently.
2. Undoes the earlier debit made on the same connection.
3. Pooled connections are reused; leaving it false changes behavior for the next borrower.

### Connection pooling with HikariCP

1. `Connection is not available, request timed out` from HikariPool.
2. More concurrent queries can overload the database and slow everything.
3. Enable `leakDetectionThreshold` and inspect the stack trace it logs.
