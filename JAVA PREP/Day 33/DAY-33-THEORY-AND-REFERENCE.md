# Day 33 — Spring Data JPA II: Derived Queries, JPQL, Native SQL, Paging and Projections

**Phase:** Spring Boot  
**Primary theme:** Querying with Spring Data: method-name queries, @Query, pagination and projections  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-derived-query-methods`, `task-02-jpql-query-annotation`, `task-03-native-and-pagination`, `task-04-projections-challenge`  
**Instruction alignment:** Maps to Day 33 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Querying with Spring Data: method-name queries, @Query, pagination and projections. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. Derived query methods
2. @Query: JPQL, native SQL, modifying queries
3. Pagination, sorting and projections
4. Interview corner, common mistakes, glossary

## Subtopics

### Derived query methods

#### What it is

Spring Data parses repository method names (`findBy`, `countBy`, `existsBy`, `deleteBy`, `Top`/`First`) into queries at startup. Keywords: `And`, `Or`, `Between`, `LessThan`, `GreaterThanEqual`, `Like`, `Containing`, `StartingWith`, `In`, `IsNull`, `True`, `IgnoreCase`, `OrderBy...Asc/Desc`. Property paths traverse relations (`findByAddressCity`).

#### Why it exists / why it matters

Most lookups are simple predicates; encoding them in the method name removes the need for JPQL strings and gives startup-time validation.

#### Pros and cons

**Pros**

- Zero query code for simple cases
- Compile-time visible API, verified at startup
- Readable for short predicates
- Supports sorting, limiting and projections

**Cons / trade-offs**

- Long names become unreadable (use `@Query`)
- Name typos fail only at startup/test time
- Renaming entity fields requires renaming methods

#### What happens without it / when misused

Hand-writing JPQL for every lookup is verbose. Conversely, 6-clause method names (`findByAAndBOrCAndD...`) are a maintenance trap and hide precedence rules.

#### Syntax and rules

```java
List<Employee> findByDepartmentAndActiveTrue(String d);
List<Employee> findBySalaryGreaterThanEqualOrderBySalaryDesc(BigDecimal min);
long countByDepartment(String d);
boolean existsByNameIgnoreCase(String n);
List<Employee> findTop2ByOrderBySalaryDesc();
long deleteByActiveFalse();   // needs a transaction
```

#### Examples

**Example 1 — Between**

```java
List<Employee> findByHiredOnBetween(LocalDate from, LocalDate to);   // inclusive
```

**Example 2 — Collection parameter**

```java
List<Employee> findByDepartmentIn(Collection<String> departments);
```

**Example 3 — Nested property**

```java
List<Order> findByCustomerAddressCity(String city);   // customer.address.city
```

#### Quick checks

1. Is Between inclusive?
2. What happens with a wrong property name?
3. How do you limit results?

### @Query: JPQL, native SQL, modifying queries

#### What it is

`@Query` supplies explicit JPQL (entity-based, portable) or native SQL (`nativeQuery = true`). Use named (`:name` + `@Param`) or positional parameters. `@Modifying` marks UPDATE/DELETE queries; use `clearAutomatically = true` so stale managed entities do not survive a bulk update. Aliases in select lists map to interface projection getters.

#### Why it exists / why it matters

Complex joins, aggregates, subqueries and database-specific features are clearer (and faster) as explicit queries than as method names.

#### Pros and cons

**Pros**

- Full expressive power of JPQL/SQL
- Validated at startup (JPQL)
- Named parameters are refactor-safe
- Bulk operations avoid loading entities

**Cons / trade-offs**

- Native SQL ties code to a database dialect
- Bulk updates bypass the persistence context, lifecycle callbacks and optimistic locking
- String queries have no compile-time checking

#### What happens without it / when misused

Forgetting `clearAutomatically` after a bulk update returns stale entities from the first-level cache. Concatenating user input into native strings invites SQL injection - always bind parameters.

#### Syntax and rules

```java
@Query("select e from Employee e where lower(e.name) like lower(concat('%', :q, '%'))")
List<Employee> search(@Param("q") String q);

@Modifying(clearAutomatically = true, flushAutomatically = true)
@Query("update Employee e set e.salary = e.salary * :f where e.department = :d")
int raise(@Param("d") String d, @Param("f") BigDecimal f);

@Query(value = "select department, count(*) as headcount from employees group by department", nativeQuery = true)
List<DeptCount> headcounts();
```

#### Examples

**Example 1 — Subquery**

```java
@Query("select e from Employee e where e.salary > (select avg(x.salary) from Employee x)")
```

**Example 2 — Aggregate projection**

```java
@Query("select e.department as department, sum(e.salary) as total from Employee e group by e.department")
List<DeptTotal> payroll();
```

**Example 3 — Native with count**

```java
@Query(value = "select * from employees where salary >= :min",
       countQuery = "select count(*) from employees where salary >= :min", nativeQuery = true)
Page<Employee> wellPaid(@Param("min") BigDecimal min, Pageable p);
```

#### Quick checks

1. What does clearAutomatically do?
2. JPQL vs SQL names?
3. How do you avoid SQL injection?

### Pagination, sorting and projections

#### What it is

`Pageable` (`PageRequest.of(page, size, Sort)`) turns list methods into `Page<T>` (content + total count + page metadata) or `Slice<T>` (content + has-next, no count query) or `List<T>`. **Projections** limit what is fetched: closed interface projections (getter names), open projections (`@Value` SpEL), class/record DTOs, and dynamic projections (`Class<T>` parameter).

#### Why it exists / why it matters

Returning unbounded lists does not scale, and loading entire entities to show two columns wastes memory and I/O. Pagination and projections make APIs predictable and efficient.

#### Pros and cons

**Pros**

- Bounded memory and response size
- `Slice` avoids expensive counts
- Projections reduce selected columns
- Dynamic projection reuses one query for several views

**Cons / trade-offs**

- Offset pagination gets slow on deep pages (use keyset/Scroll for huge tables)
- Count queries can be expensive
- Open projections load the full entity

#### What happens without it / when misused

Without paging, one request can load millions of rows (OOM, slow responses). Sorting by a non-indexed or unstable column yields duplicate/missing rows across pages: always add a unique tiebreaker such as the id.

#### Syntax and rules

```java
Page<Employee> findByDepartment(String dept, Pageable pageable);
PageRequest.of(0, 20, Sort.by("salary").descending().and(Sort.by("id")));

interface EmployeeSummary { String getName(); String getDepartment(); }
record EmployeeRow(String name, BigDecimal salary) {}
<T> List<T> findByDepartment(String d, Class<T> type);
```
`Page` getters: `getContent`, `getTotalElements`, `getTotalPages`, `getNumber`, `hasNext`.

#### Examples

**Example 1 — Controller usage**

```java
@GetMapping Page<EmployeeSummary> list(@PageableDefault(size = 20) Pageable p) { return repo.findAllBy(p); }
```

**Example 2 — Slice**

```java
Slice<Employee> findByActiveTrue(Pageable p);   // no count query
```

**Example 3 — Constructor expression**

```java
@Query("select new com.acme.EmployeeRow(e.name, e.salary) from Employee e")
```

#### Quick checks

1. Page vs Slice?
2. Why add a tiebreaker to sorting?
3. What is a dynamic projection?

## Interview corner

**Q1. Derived queries vs @Query?**

Derived for short predicates; @Query when joins, aggregates or readability need explicit control.

**Q2. Page vs Slice?**

Page includes totals via a count query; Slice does not.

**Q3. Why use projections?**

To select only the required columns and decouple API shapes from entities.

**Q4. What is the danger of @Modifying queries?**

They bypass the persistence context; clear it to avoid stale reads.

**Q5. Offset pagination drawbacks?**

Deep pages are slow; consider keyset pagination.

## Common mistakes & debugging

- Misspelled property in a derived method.
- Forgetting `countQuery` for native paged queries.
- Using entity names in native SQL.
- Missing alias for projections.

## Further reading

- Spring Data JPA Reference: Query Methods, Projections
- Hibernate: HQL guide

## Glossary

| Term | Meaning |
|------|---------|
| Derived query | Query generated from a method name |
| JPQL | Object query language of JPA |
| Pageable | Page request abstraction |
| Projection | Reduced view of entity data |
| Slice | Page without total count |

## Answers

### Derived query methods

1. Yes, both bounds are inclusive.
2. The application context fails to start with a PropertyReferenceException.
3. `Top`/`First` in the name or a `Pageable` parameter.

### @Query: JPQL, native SQL, modifying queries

1. Clears the persistence context after the bulk query so later reads hit the database.
2. JPQL uses entity and field names; SQL uses table and column names.
3. Bind parameters; never concatenate user input.

### Pagination, sorting and projections

1. `Page` runs a count query and knows totals; `Slice` only knows whether another slice exists.
2. Stable ordering across pages prevents duplicates and gaps.
3. A repository method taking `Class<T>` so the caller chooses the return type.
