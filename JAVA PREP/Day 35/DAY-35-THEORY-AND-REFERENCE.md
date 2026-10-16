# Day 35 — Spring Data JPA IV: N+1, Transactions, Versioning, Auditing and Flyway

**Phase:** Spring Boot  
**Primary theme:** Performance and correctness of the persistence layer: fetching strategies, transactions, concurrency control and schema migrations  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-n-plus-one-join-fetch`, `task-02-transactional-transfer`, `task-03-version-and-auditing`, `task-04-flyway-migrations`  
**Instruction alignment:** Maps to Day 35 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Performance and correctness of the persistence layer: fetching strategies, transactions, concurrency control and schema migrations. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. The N+1 problem, join fetch and entity graphs
2. @Transactional: propagation, rollback rules and pitfalls
3. Optimistic locking, auditing and Flyway migrations
4. Interview corner, common mistakes, glossary

## Subtopics

### The N+1 problem, join fetch and entity graphs

#### What it is

N+1 happens when one query loads N parents and then each parent's lazy association triggers another query (1 + N statements). Fixes: `join fetch` in JPQL, `@EntityGraph(attributePaths=...)`, batch fetching (`hibernate.default_batch_fetch_size`), or projections that fetch only what is needed.

#### Why it exists / why it matters

It is the most common JPA performance bug: it looks fine with 5 rows in development and melts with 5,000 in production. Detecting it early (statistics, SQL logs, tests) is a core backend skill.

#### Pros and cons

**Pros**

- Single round trip for the needed graph
- Fix is local to the repository
- Entity graphs keep JPQL clean
- Batch fetching is a global safety net

**Cons / trade-offs**

- Join fetching a collection duplicates parent rows (use distinct / Hibernate 6 dedups)
- Fetching two collections at once creates cartesian products (`MultipleBagFetchException`)
- Cannot paginate fetched collections in the database (in-memory paging warning HHH90003004)

#### What happens without it / when misused

Looping over `findAll()` and calling `getBooks().size()` runs one query per author. Switching everything to EAGER makes it worse: unrelated queries load graphs nobody asked for.

#### Syntax and rules

```java
@Query("select distinct a from Author a join fetch a.books")
List<Author> findAllWithBooks();

@EntityGraph(attributePaths = "books")
@Query("select distinct a from Author a")
List<Author> findAllWithGraph();
```
Enable counting in tests: `spring.jpa.properties.hibernate.generate_statistics=true` and `sessionFactory.getStatistics().getPrepareStatementCount()`.

#### Examples

**Example 1 — Spot it in logs**

```properties
spring.jpa.show-sql=true
logging.level.org.hibernate.SQL=DEBUG
```

**Example 2 — Batch fetching**

```properties
spring.jpa.properties.hibernate.default_batch_fetch_size=50
```

**Example 3 — Page parents, fetch children second**

```java
Page<Long> ids = repo.findIds(pageable);
List<Author> authors = repo.findWithBooksByIdIn(ids.getContent());
```

#### Quick checks

1. What is N+1?
2. Why not just make it EAGER?
3. How do you test for it?

### @Transactional: propagation, rollback rules and pitfalls

#### What it is

`@Transactional` is applied through a Spring proxy: `begin -> run method -> commit/rollback`. Default propagation `REQUIRED` joins an existing transaction. **Rollback rules**: runtime exceptions and errors roll back; checked exceptions commit unless `rollbackFor` says otherwise. `readOnly = true` hints that no writes occur. `REQUIRES_NEW` suspends the outer transaction (audit logs).

#### Why it exists / why it matters

Business operations must be atomic (all-or-nothing) and consistent. Transactions also define the lifetime of the persistence context (lazy loading, dirty checking).

#### Pros and cons

**Pros**

- Declarative, no try/catch/commit code
- Consistent semantics across JPA, JDBC, messaging
- Read-only hints optimize flushing
- Composable through propagation

**Cons / trade-offs**

- Proxy-based: self-invocation and private methods are not intercepted
- Long transactions hold locks/connections
- Checked-exception default surprises people

#### What happens without it / when misused

Without a transaction a two-step transfer can debit one account and fail before crediting the other. Calling `this.transfer(...)` from another method in the same class skips the proxy so annotations on the inner method are ignored. Catching the exception inside the method hides the failure from the proxy: no rollback.

#### Syntax and rules

```java
@Service
class TransferService {
  @Transactional
  void transfer(...) {...}
  @Transactional(rollbackFor = AuditUnavailableException.class)
  void withAudit(...) throws AuditUnavailableException {...}
  @Transactional(readOnly = true)
  BigDecimal balance(long id) {...}
}
```
Place on public service methods; keep transactions short; do not do remote calls inside them if you can avoid it.

#### Examples

**Example 1 — REQUIRES_NEW**

```java
@Transactional(propagation = Propagation.REQUIRES_NEW)
void writeAudit(String event) {...}
```

**Example 2 — Programmatic**

```java
new TransactionTemplate(txManager).executeWithoutResult(s -> repo.save(x));
```

**Example 3 — Test behavior**

```java
@SpringBootTest   // NOT @Transactional, so commits/rollbacks are real
```

#### Quick checks

1. Which exceptions roll back by default?
2. Why does self-invocation bypass @Transactional?
3. What does readOnly do?

### Optimistic locking, auditing and Flyway migrations

#### What it is

`@Version` adds a version column; Hibernate appends `where version = ?` to updates and throws `ObjectOptimisticLockingFailureException` when another transaction changed the row (lost-update protection without DB locks). **Auditing** (`@EnableJpaAuditing`, `@EntityListeners(AuditingEntityListener.class)`, `@CreatedDate`, `@LastModifiedDate`, `@CreatedBy`) fills metadata automatically. **Flyway** applies versioned SQL scripts (`V1__init.sql`) tracked in `flyway_schema_history`; Hibernate then only `validate`s.

#### Why it exists / why it matters

Concurrent edits must not silently overwrite each other; audit columns support traceability; migrations make schema evolution reviewable, repeatable and identical across environments.

#### Pros and cons

**Pros**

- Lost updates detected cheaply
- Audit data without boilerplate
- Schema history in version control
- Rollout is deterministic across environments

**Cons / trade-offs**

- Clients must handle/retry conflicts
- Bulk JPQL updates bypass `@Version`
- Migrations are forever: mistakes need new migrations
- Flyway SQL must work on the real production database

#### What happens without it / when misused

Without `@Version`, two users editing the same row produce last-write-wins data loss. Hand-editing a production schema leads to drift between environments; editing an applied migration breaks the checksum validation.

#### Syntax and rules

```java
@Version private Long version;
@CreatedDate @Column(updatable = false) private LocalDateTime createdAt;
@LastModifiedDate private LocalDateTime updatedAt;
```
```sql
-- src/main/resources/db/migration/V2__add_status.sql
alter table articles add column status varchar(20) not null default 'DRAFT';
```
```properties
spring.jpa.hibernate.ddl-auto=validate
spring.flyway.enabled=true
```

#### Examples

**Example 1 — Handling a conflict**

```java
try { service.saveDetached(p); } catch (ObjectOptimisticLockingFailureException e) { /* reload and retry or return 409 */ }
```

**Example 2 — Migration naming**

```text
V1__create_articles.sql
V2__add_article_status.sql
R__refresh_views.sql   (repeatable)
```

**Example 3 — Pessimistic alternative**

```java
@Lock(LockModeType.PESSIMISTIC_WRITE) Optional<Product> findById(Long id);
```

#### Quick checks

1. What does @Version do on update?
2. Why `validate` with Flyway?
3. Can you edit an applied migration?

## Interview corner

**Q1. How do you fix N+1?**

join fetch, entity graph, batch size, or projections.

**Q2. Checked exceptions and @Transactional?**

They do not roll back unless rollbackFor is set.

**Q3. Optimistic vs pessimistic locking?**

Optimistic detects conflicts at commit via version; pessimistic locks rows up front.

**Q4. Why Flyway/Liquibase?**

Versioned, repeatable, reviewable schema changes.

**Q5. What does open-in-view do?**

Keeps the EntityManager open during the web request, hiding lazy loading problems; disable for APIs.

## Common mistakes & debugging

- Join fetching multiple bags.
- Self-invocation of transactional methods.
- Editing applied Flyway migrations.
- Ignoring optimistic lock exceptions in APIs (should be 409).

## Further reading

- Hibernate User Guide: Fetching
- Spring Framework Reference: Transaction Management
- Flyway documentation

## Glossary

| Term | Meaning |
|------|---------|
| N+1 | 1 + N queries for lazy associations |
| Entity graph | Declarative fetch plan |
| Propagation | How transactions nest |
| Optimistic lock | Version-based conflict detection |
| Migration | Versioned schema change script |

## Answers

### The N+1 problem, join fetch and entity graphs

1. One query for parents plus one per parent for a lazy association.
2. EAGER loads graphs for every query, often causing even more queries/joins.
3. Use Hibernate statistics or a datasource proxy to assert the statement count.

### @Transactional: propagation, rollback rules and pitfalls

1. Unchecked exceptions (RuntimeException) and Errors.
2. The proxy is not involved when a method calls another method on `this`.
3. Optimization hint (e.g. no dirty-check flush); not a security guarantee.

### Optimistic locking, auditing and Flyway migrations

1. Adds a version check to the WHERE clause and increments it; mismatches throw an optimistic locking failure.
2. Flyway owns the schema; Hibernate only checks that entities match.
3. No - add a new one; checksums would fail otherwise.
