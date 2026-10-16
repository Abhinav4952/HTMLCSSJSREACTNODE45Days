# Day 34 — Spring Data JPA III: Relationships, Cascade and Fetching

**Phase:** Spring Boot  
**Primary theme:** Mapping associations between entities: ownership, join tables, cascading and lazy/eager loading  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-one-to-one-profile`, `task-02-one-to-many-orders`, `task-03-many-to-many-enrollment`, `task-04-library-model-challenge`  
**Instruction alignment:** Maps to Day 34 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Mapping associations between entities: ownership, join tables, cascading and lazy/eager loading. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. One-to-one, one-to-many and many-to-one
2. Many-to-many and join tables
3. Cascade, orphanRemoval and fetch types
4. Interview corner, common mistakes, glossary

## Subtopics

### One-to-one, one-to-many and many-to-one

#### What it is

Relationships are mapped with `@OneToOne`, `@OneToMany`, `@ManyToOne`. The **owning side** holds the foreign key (`@JoinColumn`); the **inverse side** uses `mappedBy`. A bidirectional one-to-many is owned by the `@ManyToOne` side. Convenience methods (`addOrder`, `removeOrder`) keep both in-memory sides consistent.

#### Why it exists / why it matters

Relational data is connected by keys; the object model needs references. Correct ownership decides which table gets the FK and whether Hibernate generates extra join tables.

#### Pros and cons

**Pros**

- Navigate relations as object references
- Cascade lifecycle operations along aggregates
- FK constraints enforced by the DB
- orphanRemoval models true composition

**Cons / trade-offs**

- Bidirectional associations require discipline
- Easy to create N+1 problems (Day 35)
- Mistaken ownership gives silent no-ops (no FK written)

#### What happens without it / when misused

Setting only the inverse side (`customer.getOrders().add(o)`) writes nothing because the owning side `o.customer` is still null. Without `mappedBy` a one-to-many creates an unwanted join table.

#### Syntax and rules

```java
@OneToMany(mappedBy = "customer", cascade = CascadeType.ALL, orphanRemoval = true)
private List<PurchaseOrder> orders = new ArrayList<>();

@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "customer_id", nullable = false)
private Customer customer;
```
Defaults: `@ManyToOne`/`@OneToOne` EAGER, `@OneToMany`/`@ManyToMany` LAZY.

#### Examples

**Example 1 — Helper**

```java
public void addOrder(PurchaseOrder o) { orders.add(o); o.setCustomer(this); }
```

**Example 2 — One-to-one**

```java
@OneToOne(fetch = LAZY, cascade = ALL, orphanRemoval = true)
@JoinColumn(name = "profile_id")
private Profile profile;
```

**Example 3 — Unidirectional one-to-many (avoid)**

```java
@OneToMany @JoinColumn(name = "customer_id") List<Order> orders;   // extra UPDATEs
```

#### Quick checks

1. Which side owns a bidirectional one-to-many?
2. What does mappedBy tell Hibernate?
3. Default fetch of @ManyToOne?

### Many-to-many and join tables

#### What it is

`@ManyToMany` maps a link table. The owning side declares `@JoinTable` with `joinColumns` and `inverseJoinColumns`; the other side uses `mappedBy`. Use `Set` to avoid re-inserting all rows on changes. When the link has attributes (enrolled_at, grade), model it as an explicit entity with two `@ManyToOne`.

#### Why it exists / why it matters

Many-to-many exists everywhere (students/courses, posts/tags, users/roles). Correct mapping prevents duplicate links and accidental deletes of shared data.

#### Pros and cons

**Pros**

- Concise for pure links
- Join table managed automatically
- Works naturally with Sets

**Cons / trade-offs**

- No place for link attributes
- Cascade REMOVE is dangerous
- Large collections load entirely when initialized

#### What happens without it / when misused

Cascading REMOVE across a many-to-many deletes entities other aggregates still reference. Using `List` can make Hibernate delete and re-insert every link row for one change. Mutable-field equals/hashCode breaks HashSet membership.

#### Syntax and rules

```java
@ManyToMany
@JoinTable(name = "enrollments",
    joinColumns = @JoinColumn(name = "student_id"),
    inverseJoinColumns = @JoinColumn(name = "course_id"))
private Set<Course> courses = new HashSet<>();
```
Equality: prefer a business key (`code`) or a stable id strategy; never include lazy collections in equals/hashCode.

#### Examples

**Example 1 — Inverse side**

```java
@ManyToMany(mappedBy = "courses")
private Set<Student> students = new HashSet<>();
```

**Example 2 — Link entity**

```java
@Entity class Enrollment {
  @ManyToOne Student student; @ManyToOne Course course; LocalDate enrolledAt; int grade; }
```

**Example 3 — Business-key equals**

```java
public boolean equals(Object o) { return o instanceof Course c && code != null && code.equals(c.code); }
```

#### Quick checks

1. Set or List for many-to-many?
2. What if the link needs attributes?
3. Should many-to-many cascade REMOVE?

### Cascade, orphanRemoval and fetch types

#### What it is

**Cascade** propagates persist/merge/remove/refresh/detach from parent to children (`CascadeType.ALL`). **orphanRemoval** deletes a child removed from the parent's collection or replaced. **FetchType** LAZY loads on first access via proxies/uninitialized collections; EAGER loads together with the owner. Lazy access outside a session throws `LazyInitializationException`.

#### Why it exists / why it matters

Aggregates (order + lines) share a lifecycle: cascade avoids saving each child manually. Fetch strategy controls performance: eager associations multiply queries and joins.

#### Pros and cons

**Pros**

- Simplifies aggregate persistence
- orphanRemoval models composition cleanly
- LAZY avoids loading unused graphs

**Cons / trade-offs**

- Cascade across shared references deletes too much
- LAZY requires fetching strategy awareness (join fetch, entity graphs)
- orphanRemoval + replacing a collection instance breaks (mutate it instead)

#### What happens without it / when misused

EAGER everywhere loads half the database per query. Cascade ALL on a shared reference deletes data other rows still need. Replacing (`setOrders(new ArrayList<>())`) a collection with orphanRemoval throws `HibernateException: A collection with cascade=all-delete-orphan was no longer referenced`.

#### Syntax and rules

```java
@OneToMany(mappedBy = "author", cascade = CascadeType.ALL, orphanRemoval = true) // aggregate children
@ManyToMany                                                                      // shared: no cascade
```
Check loading state in tests: `PersistenceUnitUtil.isLoaded(entity, "attribute")`.

#### Examples

**Example 1 — Aggregate**

```text
Author -> Books -> BookDetail   (cascade ALL + orphanRemoval)
Book <-> Tag                    (no cascade, shared)
```

**Example 2 — Lazy check**

```java
emf.getPersistenceUnitUtil().isLoaded(book, "author")
```

**Example 3 — Safe collection update**

```java
author.getBooks().clear(); author.getBooks().addAll(newBooks);
```

#### Quick checks

1. What does orphanRemoval do?
2. Why LAZY by default?
3. When must you not use CascadeType.REMOVE?

## Interview corner

**Q1. Owning vs inverse side?**

Owning side has the FK/join table; inverse uses mappedBy.

**Q2. Why helper methods?**

To keep both in-memory sides in sync.

**Q3. Cascade vs orphanRemoval?**

Cascade propagates operations; orphanRemoval deletes removed children.

**Q4. Default fetch types?**

To-one EAGER, to-many LAZY.

**Q5. LazyInitializationException?**

Accessing a lazy association after the session closed.

## Common mistakes & debugging

- Setting only the inverse side.
- Cascade REMOVE on shared entities.
- List instead of Set for many-to-many.
- Replacing an orphanRemoval collection instance.

## Further reading

- Hibernate ORM User Guide: Associations
- Spring Data JPA Reference

## Glossary

| Term | Meaning |
|------|---------|
| Owning side | Side whose table holds the FK |
| mappedBy | Marks the inverse side |
| Cascade | Propagating operations |
| orphanRemoval | Delete removed children |
| Join table | Link table for N:M |

## Answers

### One-to-one, one-to-many and many-to-one

1. The many-to-one side (it has the FK).
2. That the other side owns the relationship and no join table is needed.
3. EAGER - usually override to LAZY.

### Many-to-many and join tables

1. Set, to avoid delete-all/insert-all of link rows.
2. Make an explicit link entity.
3. No.

### Cascade, orphanRemoval and fetch types

1. Deletes children removed from the parent collection or replaced.
2. To avoid loading unnecessary graphs and N+1 explosions with eager joins.
3. On references shared with other aggregates (e.g. tags).
