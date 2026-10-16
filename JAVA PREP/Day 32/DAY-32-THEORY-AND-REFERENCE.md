# Day 32 — Spring Data JPA I: Entities, Repositories, CRUD and Datasource

**Phase:** Spring Boot  
**Primary theme:** Persisting data with JPA/Hibernate through Spring Data repositories and configuring the database layer  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-book-entity-mapping`, `task-02-customer-crud-service`, `task-03-schema-sql-validate`, `task-04-datasource-properties-lab`  
**Instruction alignment:** Maps to Day 32 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Persisting data with JPA/Hibernate through Spring Data repositories and configuring the database layer. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. JPA entities and mapping annotations
2. Spring Data JPA repositories and CRUD
3. DataSource configuration, ddl-auto versus SQL scripts
4. Interview corner, common mistakes, glossary

## Subtopics

### JPA entities and mapping annotations

#### What it is

**JPA** (Jakarta Persistence) maps Java classes to relational tables; **Hibernate** is the implementation Spring Boot uses. An `@Entity` needs an `@Id`, a no-arg constructor and non-final class. `@Table`, `@Column` (nullable, unique, length, precision), `@Enumerated(EnumType.STRING)`, `@GeneratedValue` (IDENTITY, SEQUENCE) describe the mapping. Spring Boot's naming strategy converts `createdAt` to `created_at`.

#### Why it exists / why it matters

Object-relational mapping removes boilerplate JDBC (result-set parsing, SQL for simple CRUD) and gives identity tracking, dirty checking and caching in a persistence context.

#### Pros and cons

**Pros**

- Less boilerplate
- Entities carry constraints that Hibernate can turn into DDL
- Dirty checking writes only changed state
- Portable across databases

**Cons / trade-offs**

- Leaky abstraction: you still must know SQL
- Lazy loading and N+1 surprises (Day 35)
- Entities with Lombok-style equals/hashCode on mutable fields cause bugs

#### What happens without it / when misused

`EnumType.ORDINAL` (the default!) breaks data when someone reorders constants. Missing `@Column(nullable=false)` lets bad rows in. A missing no-arg constructor fails at startup with `InstantiationException`.

#### Syntax and rules

```java
@Entity @Table(name = "books")
class Book {
  @Id @GeneratedValue(strategy = GenerationType.IDENTITY) Long id;
  @Column(nullable = false, length = 120) String title;
  @Enumerated(EnumType.STRING) Genre genre;
  protected Book() {}
}
```
Prefer `Long` wrappers for generated ids (null = not persisted yet). Avoid `user`, `order`, `group` as table names (reserved words).

#### Examples

**Example 1 — Unique column**

```java
@Column(nullable = false, unique = true, length = 20)
private String isbn;
```

**Example 2 — Money**

```java
@Column(nullable = false, precision = 10, scale = 2)
private BigDecimal price;
```

**Example 3 — Explicit column name**

```java
@Column(name = "created_at", nullable = false)
private LocalDateTime createdAt;
```

#### Quick checks

1. Why store enums as STRING?
2. What must every entity have?
3. Who implements JPA in Spring Boot?

### Spring Data JPA repositories and CRUD

#### What it is

A repository interface extending `JpaRepository<T, ID>` gets implementations of `save`, `findById`, `findAll`, `deleteById`, `existsById`, `count`, paging and sorting generated at startup as a proxy. `@Transactional` services wrap use cases; inside a transaction the **persistence context** tracks managed entities, so mutating one is flushed automatically (dirty checking). `save` performs `persist` for new entities and `merge` otherwise.

#### Why it exists / why it matters

CRUD is 80 percent of data access; generating it removes repetitive code and keeps data access consistent. Transaction boundaries ensure all-or-nothing business operations.

#### Pros and cons

**Pros**

- No hand-written DAO code for CRUD
- Optional-returning API fits modern Java
- Easy to test with `@DataJpaTest`
- Extensible with derived queries (Day 33)

**Cons / trade-offs**

- Generated proxies are opaque when debugging
- `save` on detached entities issues SELECT + UPDATE (merge)
- Exposing full repositories to the web layer bypasses rules

#### What happens without it / when misused

`deleteById` on a missing id does nothing silently (Spring Data 3). Calling repository methods outside a transaction gives each call its own transaction, so multi-step logic loses atomicity and lazy loading may fail.

#### Syntax and rules

```java
interface CustomerRepository extends JpaRepository<Customer, Long> {}

@Service @Transactional class CustomerService {
  Customer rename(long id, String name) {
    Customer c = repo.findById(id).orElseThrow();
    c.setName(name);      // dirty checking issues the UPDATE at flush/commit
    return c;
  }
}
```
`@Transactional(readOnly = true)` for queries.

#### Examples

**Example 1 — Optional handling**

```java
repo.findById(id).orElseThrow(() -> new NoSuchElementException("Customer " + id));
```

**Example 2 — Existence check before delete**

```java
if (!repo.existsById(id)) throw new NoSuchElementException();
repo.deleteById(id);
```

**Example 3 — Slice test**

```java
@DataJpaTest
@Import(CustomerService.class)
class CustomerServiceTest { ... }
```

#### Quick checks

1. What does dirty checking do?
2. Does deleteById throw for unknown ids?
3. Where should @Transactional go?

### DataSource configuration, ddl-auto versus SQL scripts

#### What it is

Boot auto-configures a `DataSource` (HikariCP) from `spring.datasource.*`. `spring.jpa.hibernate.ddl-auto` controls schema management: `none`, `validate`, `update`, `create`, `create-drop`. `schema.sql`/`data.sql` run with `spring.sql.init.mode`. Production teams use `validate` or `none` together with migrations (Flyway/Liquibase, Day 35). H2 in `MODE=PostgreSQL` mimics Postgres behavior in tests.

#### Why it exists / why it matters

Schema changes must be reviewable, repeatable and safe. Letting Hibernate alter production schemas is risky; tests, however, benefit from fast generated schemas.

#### Pros and cons

**Pros**

- `create-drop` gives fast isolated tests
- `validate` catches drift between entities and DB
- SQL scripts are explicit and reviewable
- H2 Postgres mode catches many dialect problems early

**Cons / trade-offs**

- `update` can produce surprising or destructive changes
- H2 is not Postgres: JSON, arrays, advisory locks and many functions differ
- Two sources of truth (entities and SQL) can drift

#### What happens without it / when misused

`ddl-auto=update` in production can silently add columns but never drops or fixes them, leaving unmanaged drift. `create` wipes data on every start. Not setting a URL makes Boot silently use an embedded DB.

#### Syntax and rules

```properties
spring.datasource.url=jdbc:h2:mem:testdb;MODE=PostgreSQL;DATABASE_TO_LOWER=TRUE;DEFAULT_NULL_ORDERING=HIGH;DB_CLOSE_DELAY=-1
spring.jpa.hibernate.ddl-auto=validate
spring.sql.init.mode=always
spring.jpa.open-in-view=false
```
Slice tests (`@DataJpaTest`) replace the datasource with an embedded DB unless `spring.test.database.replace=none`.

#### Examples

**Example 1 — Local dev**

```properties
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.show-sql=true
```

**Example 2 — Production-style**

```properties
spring.jpa.hibernate.ddl-auto=validate
spring.flyway.enabled=true
```

**Example 3 — Hikari tuning**

```properties
spring.datasource.hikari.maximum-pool-size=10
```

#### Quick checks

1. Which ddl-auto value verifies without changing the schema?
2. Why avoid `update` in production?
3. What does MODE=PostgreSQL do in H2?

## Interview corner

**Q1. JPA vs Hibernate vs Spring Data JPA?**

JPA is the spec, Hibernate an implementation, Spring Data JPA a repository abstraction on top.

**Q2. What is the persistence context?**

The first-level cache/identity map of managed entities in a transaction.

**Q3. save() vs persist/merge?**

`save` calls persist for new entities and merge for existing ones.

**Q4. ddl-auto options?**

none, validate, update, create, create-drop.

**Q5. Why is ORDINAL enum mapping dangerous?**

It stores positions that change when constants are reordered.

## Common mistakes & debugging

- Using default ordinal enums.
- Reserved words as table names.
- Relying on `update` in production.
- Calling repositories without a transaction for multi-step logic.

## Further reading

- Spring Data JPA Reference
- Hibernate ORM User Guide: Mapping
- Spring Boot Reference: SQL Databases

## Glossary

| Term | Meaning |
|------|---------|
| Entity | Class mapped to a table |
| Persistence context | Set of managed entities per transaction |
| Dirty checking | Automatic detection of changes |
| ddl-auto | Hibernate schema management mode |
| HikariCP | Default connection pool |

## Answers

### JPA entities and mapping annotations

1. Ordinals change when constants are reordered or inserted; names are stable.
2. An `@Id` and a no-arg constructor (at least protected).
3. Hibernate ORM.

### Spring Data JPA repositories and CRUD

1. It detects changes to managed entities and issues UPDATEs at flush time.
2. No, it silently does nothing in Spring Data 3.
3. On service methods representing a use case.

### DataSource configuration, ddl-auto versus SQL scripts

1. `validate`.
2. It cannot guarantee a correct schema and can cause drift; use migrations.
3. It emulates Postgres syntax/behavior to catch dialect issues in tests.
