# Day 50 — Interview Review: Core Java, Spring, and Timed Rounds

**Phase:** Capstone  
**Primary theme:** Rapid review of Core Java, collections, concurrency, JVM, SQL, JPA, Spring and security, plus four timed mixed coding rounds  
**Estimated study time:** 3-4 h review + 4 timed rounds (45/60/90/60 min)  
**Related tasks:** `task-01-timed-collections-streams-45min`, `task-02-timed-spring-jpa-bug-hunt-60min`, `task-03-timed-concurrency-fix-90min`, `task-04-timed-sql-reasoning-60min`  
**Instruction alignment:** Maps to Day 50 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Rapid review of Core Java, collections, concurrency, JVM, SQL, JPA, Spring and security, plus four timed mixed coding rounds. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. Core Java and collections rapid review
2. Concurrency and JVM review
3. SQL, transactions, and JPA review
4. Spring, REST, and security review
5. System design talking points and how to run a timed round
6. Interview corner, common mistakes, glossary

## Subtopics

### Core Java and collections rapid review

#### What it is

Core Java interview staples: `equals`/`hashCode` contract, immutability (`String`, records), `HashMap` internals (buckets, treeification at 8, resize at 0.75 load), `ArrayList` vs `LinkedList`, `TreeMap` ordering, fail-fast iterators, generics (type erasure, PECS), `Optional`, exceptions (checked vs unchecked, try-with-resources), streams (lazy, short-circuit, collectors), `var`, records, sealed types, switch patterns (Java 21).

#### Why it exists / why it matters

Interviewers use these topics to test whether you understand the tools you use daily, not only their syntax.

#### Pros and cons

**Pros**

- Foundation for every framework
- Quick to rehearse with code snippets

**Cons / trade-offs**

- Easy to know the API but not the reasoning
- Trick questions reward precise vocabulary

#### What happens without it / when misused

Mutable keys in a HashMap, equals without hashCode, or modifying a list while iterating produce subtle bugs that interviewers love to probe.

#### Syntax and rules

Complexities: `HashMap` get/put O(1) avg, `TreeMap` O(log n), `ArrayList` get O(1) / insert middle O(n), `ArrayDeque` O(1) at both ends. `Comparator.comparing(A::x).thenComparing(A::y)`. Streams: `collect(groupingBy(f, counting()))`.

#### Examples

**Example 1 — equals/hashCode contract**

```java
// equal objects MUST have equal hash codes (not vice versa)
record Point(int x, int y) {}  // gets both for free
```

**Example 2 — PECS**

```java
void copy(List<? super Integer> dst, List<? extends Integer> src) { dst.addAll(src); }
```

#### Quick checks

1. Why must keys be effectively immutable?
2. Checked vs unchecked exceptions?

### Concurrency and JVM review

#### What it is

Threads, `Runnable`/`Callable`, executors, `synchronized` (monitor, reentrant), `volatile` (visibility, no atomicity), atomics (CAS), `ConcurrentHashMap`, `CompletableFuture`, virtual threads (Java 21). The **Java Memory Model**: happens-before. JVM: heap (young/old), GC basics, stack frames, class loading, JIT, `OutOfMemoryError` vs `StackOverflowError`.

#### Why it exists / why it matters

Concurrency bugs are rare in tests and common in production; interviewers check you can reason about visibility, atomicity and deadlocks.

#### Pros and cons

**Pros**

- Better throughput
- Virtual threads simplify blocking I/O code

**Cons / trade-offs**

- Races, deadlocks and visibility bugs are hard to reproduce
- Over-synchronization kills performance

#### What happens without it / when misused

`count++` on a shared field loses updates; double-checked locking without `volatile` can publish a half-constructed object; unbounded thread pools exhaust memory.

#### Syntax and rules

Rules: prefer immutability; confine state; use `java.util.concurrent` over wait/notify; always shut executors down; lock ordering prevents deadlocks.

#### Examples

**Example 1 — Atomic counter**

```java
AtomicLong n = new AtomicLong();
n.incrementAndGet();
```

**Example 2 — Executor lifecycle**

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
try { /* submit */ } finally { pool.shutdown(); }
```

#### Quick checks

1. volatile vs synchronized?
2. What causes a deadlock?

### SQL, transactions, and JPA review

#### What it is

SQL: joins, aggregation, `GROUP BY/HAVING`, subqueries, anti-joins (`NOT EXISTS`), window functions, indexes (B-tree, composite order, covering), `EXPLAIN`. Transactions: ACID, isolation levels (read committed, repeatable read, serializable), locks, optimistic (`@Version`) vs pessimistic locking. JPA: entity states, lazy vs eager, N+1 problem and `JOIN FETCH`, `@Transactional` boundaries and proxy limits (self-invocation), dirty checking.

#### Why it exists / why it matters

Persistence mistakes are the dominant cause of production slowness and data corruption.

#### Pros and cons

**Pros**

- High interview signal
- Directly applies to Projects 01-03

**Cons / trade-offs**

- Database-specific behavior
- ORM hides SQL until it hurts

#### What happens without it / when misused

N+1 queries from lazy collections in a loop; `@Transactional` ignored on `private` or self-invoked methods; missing index on a foreign key; `NOT IN` with NULLs returning no rows.

#### Syntax and rules

Composite index `(a, b)` helps filters on `a` and `a,b` but not `b` alone (left-most prefix). Use `@Version` for optimistic locking, retry on `OptimisticLockException`. Fix N+1 with `join fetch` or `@EntityGraph`.

#### Examples

**Example 1 — Anti-join**

```sql
select c.name from customers c where not exists (select 1 from orders o where o.customer_id = c.id)
```

**Example 2 — Optimistic lock**

```java
@Version private long version;
```

#### Quick checks

1. What is the N+1 problem?
2. Why can @Transactional fail on self-invocation?

### Spring, REST, and security review

#### What it is

Spring: IoC/DI, bean scopes and life cycle, auto-configuration, `@Configuration` vs `@Component`, constructor injection, profiles, `@ConfigurationProperties`. Web: request mapping, validation, `@RestControllerAdvice`, `ProblemDetail`, idempotent methods, status codes. Security: authentication vs authorization, BCrypt, JWT pitfalls, CSRF, CORS, BOLA. Testing: pyramid, `@WebMvcTest`, `@DataJpaTest`, Mockito.

#### Why it exists / why it matters

Most backend interviews are Spring-heavy; clear definitions plus a concrete example set strong candidates apart.

#### Pros and cons

**Pros**

- Reusable answers across companies

**Cons / trade-offs**

- Frameworks change; focus on principles

#### What happens without it / when misused

Field injection hides dependencies and hurts tests; exposing entities from controllers leaks internals; catching `Exception` broadly hides bugs.

#### Syntax and rules

Be ready to draw: request -> filter chain -> DispatcherServlet -> controller -> service -> repository -> DB, and explain where transactions and security apply.

#### Examples

**Example 1 — Constructor injection**

```java
@Service class A { private final B b; A(B b) { this.b = b; } }
```

#### Quick checks

1. Singleton scope and thread-safety?
2. PUT vs PATCH vs POST?

### System design talking points and how to run a timed round

#### What it is

Design discussions: clarify requirements, estimate scale, draw components (API, DB, cache, queue), choose data model and consistency, discuss failure modes (retries, circuit breakers, idempotency, outbox), security and observability, then trade-offs. For timed coding: read all requirements, plan 5 minutes, get tests green incrementally, narrate trade-offs, leave 5 minutes for review.

#### Why it exists / why it matters

Interviews evaluate communication and judgment as much as code.

#### Pros and cons

**Pros**

- Structure reduces panic
- Reusable template for any design question

**Cons / trade-offs**

- Over-engineering in a short slot
- Talking without writing tests

#### What happens without it / when misused

Jumping into code without clarifying edge cases or silently choosing a design wastes time and loses points.

#### Syntax and rules

Template: requirements -> API -> data model -> high-level design -> deep dive (one hard part) -> failure modes -> scaling -> security -> monitoring. Examples to prepare: URL shortener, wallet transfer (idempotency + locking), hotel booking (date overlap), HR notifications with Kafka.

#### Examples

**Example 1 — Wallet transfer talking points**

```text
debit+credit in one DB transaction; @Version or SELECT FOR UPDATE; idempotency key; ledger rows immutable; reconcile job
```

#### Quick checks

1. How do you handle a question you do not know?
2. What do you do when time is almost out?

## Interview corner

**Q1. Explain the equals/hashCode contract.**

Equal objects must return equal hash codes; hashCode must be consistent; equals must be reflexive, symmetric, transitive, consistent and false for null.

**Q2. Why is String immutable?**

Security, caching of hash codes, safe sharing across threads, and string-pool interning.

**Q3. ArrayList vs LinkedList?**

ArrayList: contiguous array, O(1) index access, amortized O(1) append. LinkedList: O(1) at ends via references but O(n) index; rarely better in practice - use ArrayDeque for queues.

**Q4. How does HashMap work?**

Array of buckets; index from hash; collisions are chained and treeified at 8 entries per bucket; resizes at load factor 0.75; allows one null key.

**Q5. HashMap vs ConcurrentHashMap?**

ConcurrentHashMap is thread-safe with fine-grained locking/CAS, no null keys/values, and weakly consistent iterators.

**Q6. What are generics' type erasure consequences?**

No runtime type info: no `new T()`, no `instanceof List<String>`, overloads that differ only by type args clash.

**Q7. Checked vs unchecked exceptions?**

Checked extend Exception (not RuntimeException) and must be declared/handled; unchecked are programming errors or unrecoverable conditions.

**Q8. What does try-with-resources do?**

Automatically closes AutoCloseable resources in reverse order, suppressing secondary exceptions.

**Q9. Stream laziness?**

Intermediate operations build a pipeline; nothing runs until a terminal operation; short-circuiting ops can stop early.

**Q10. map vs flatMap?**

map transforms one element to one; flatMap transforms each element to a stream and flattens.

**Q11. What are records and sealed types?**

Records: concise immutable data carriers with generated accessors/equals/hashCode. Sealed types restrict which classes may extend/implement, enabling exhaustive switches.

**Q12. What are virtual threads?**

Lightweight JVM-managed threads (Java 21) that make blocking code scale; do not pool them and avoid pinning with synchronized around blocking I/O.

**Q13. volatile vs synchronized vs atomic?**

volatile: visibility; synchronized: visibility + mutual exclusion; atomic: lock-free atomic read-modify-write via CAS.

**Q14. What is a deadlock and how do you avoid it?**

Circular waiting for locks; use lock ordering, timeouts (tryLock) or fewer locks.

**Q15. How does garbage collection decide what to free?**

Objects unreachable from GC roots (stacks, statics, JNI) are collectable; generational collectors optimize for short-lived objects.

**Q16. OutOfMemoryError vs StackOverflowError?**

Heap exhaustion (leak, huge data) vs too-deep recursion exhausting thread stack.

**Q17. Inner join vs left join?**

Inner keeps matching rows only; left keeps all left rows with NULLs where no match.

**Q18. Why NOT EXISTS over NOT IN?**

NOT IN returns no rows if the subquery yields NULL; NOT EXISTS is NULL-safe and often better optimized.

**Q19. What is an index and its cost?**

A sorted structure (B-tree) that speeds lookups; costs storage and slows writes.

**Q20. Composite index column order?**

Left-most prefix rule: put equality columns first; the index serves queries using a prefix of its columns.

**Q21. Explain ACID.**

Atomicity, Consistency, Isolation, Durability.

**Q22. Isolation levels and anomalies?**

Read uncommitted (dirty reads), read committed (non-repeatable reads), repeatable read (phantoms in some DBs), serializable (none).

**Q23. Optimistic vs pessimistic locking?**

Optimistic uses a version column and fails on conflict (good for low contention); pessimistic locks rows (SELECT FOR UPDATE) up front.

**Q24. What is the N+1 select problem?**

Loading N children with N extra queries; fix with join fetch, entity graphs or batch fetching.

**Q25. JPA entity states?**

Transient, managed, detached, removed.

**Q26. Why might @Transactional not work?**

Self-invocation, private/final methods, wrong proxy type, exception types not rolled back (checked by default).

**Q27. Bean scopes?**

singleton (default), prototype, request, session, application.

**Q28. Constructor vs field injection?**

Constructor: immutability, required dependencies, easy tests; field injection hides dependencies.

**Q29. How does Spring Boot auto-configuration work?**

Conditional configuration classes listed in AutoConfiguration.imports activate based on classpath, beans and properties.

**Q30. REST idempotency?**

GET, PUT, DELETE are idempotent; POST is not unless an idempotency key is used.

**Q31. Which status codes do you use for validation vs conflict vs auth errors?**

400 validation, 401 unauthenticated, 403 forbidden, 404 not found, 409 conflict, 422 semantic validation (team policy), 429 rate limit.

**Q32. What is CSRF and when does it matter?**

Forged cross-site requests using automatic browser credentials (cookies); irrelevant for pure bearer-token APIs.

**Q33. JWT pitfalls?**

alg=none, weak secrets, no expiry check, sensitive data in payload, hard revocation.

**Q34. What is BOLA?**

Broken object-level authorization: accessing other users' objects by id.

**Q35. Test pyramid in Spring?**

Many unit tests, fewer slice tests (@WebMvcTest, @DataJpaTest), few @SpringBootTest integration tests.

**Q36. Mockito: mock vs spy?**

A mock replaces behavior entirely; a spy wraps a real object and lets you stub selectively.

**Q37. Circuit breaker states?**

CLOSED, OPEN, HALF_OPEN.

**Q38. Why use Kafka keys?**

Per-key ordering via partitioning.

**Q39. How do you make a Kafka consumer idempotent?**

Store processed event ids (unique key) in the same transaction as the side effect.

**Q40. What is the outbox pattern?**

Write business data and event row in one DB transaction; relay events to the broker afterwards.

**Q41. How would you design a wallet transfer?**

One transaction debits and credits, optimistic version or row locks, idempotency key, immutable ledger entries, reconciliation.

**Q42. How would you prevent double bookings in a hotel system?**

Date-overlap check plus a DB constraint (exclusion constraint in PostgreSQL) or locking the room row inside the transaction.

**Q43. What do you put in CI for a Spring project?**

Build, unit/integration tests, style checks, dependency/security scan; run on every PR.

**Q44. Where do secrets live in production?**

Environment variables/secret manager; never in the repository.

## Common mistakes & debugging

- Optimizing before correctness.
- Silent coding: not narrating assumptions.
- Ignoring edge cases (null, empty, boundaries).
- Unbounded executors and unclosed resources.
- Over-reliance on memorized answers.

## Further reading

- Effective Java (Bloch), items on equals/hashCode, immutability, generics
- Java Concurrency in Practice (Goetz)
- Use The Index, Luke (SQL indexing)
- Spring Framework and Spring Boot reference documentation

## Glossary

| Term | Meaning |
|------|---------|
| PECS | Producer extends, consumer super |
| CAS | Compare-and-swap atomic primitive |
| N+1 | One query plus one per row |
| BOLA | Broken object-level authorization |
| Happens-before | JMM ordering guarantee |
| Anti-join | Rows with no match, via NOT EXISTS |

## Answers

### Core Java and collections rapid review

1. Changing a key after insertion changes its hash bucket, so the entry becomes unreachable.
2. Checked must be handled/declared (recoverable conditions); unchecked signal programming errors.

### Concurrency and JVM review

1. volatile gives visibility only; synchronized gives visibility plus mutual exclusion.
2. Circular wait on locks held by each other; avoid by consistent lock ordering or timeouts.

### SQL, transactions, and JPA review

1. One query for the parents plus one per parent for lazy children; fix with fetch joins or batching.
2. The proxy is bypassed when a bean calls its own method.

### Spring, REST, and security review

1. Singleton beans are shared across threads, so they must be stateless or properly synchronized.
2. PUT replaces and is idempotent, PATCH partially updates, POST creates/processes and is not idempotent by default.

### System design talking points and how to run a timed round

1. State assumptions, reason from first principles, ask clarifying questions, and say what you would verify.
2. Make the tests for the core path pass, document what is unfinished and why.
