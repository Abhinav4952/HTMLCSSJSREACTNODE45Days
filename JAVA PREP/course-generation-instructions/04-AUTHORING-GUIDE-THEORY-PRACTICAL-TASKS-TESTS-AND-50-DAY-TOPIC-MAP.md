# 04 — Authoring Guide: Theory, Practical Tasks, Tests, and 50-Day Topic Map

**Instruction set version:** `1.0.0`

This document tells agents **how to design exercises and tests** and provides the **default day-by-day topic map** for all 50 days. If the instructor publishes a revised map, follow that instead.

---

## Part A — Practical task design principles

### A.1 Task-type mix

Across any 7-day window aim for variety within the phase:

- **Core Java (01–24):** pure-logic tasks with JUnit; at least one task per day that **breaks** something on purpose (bug hunt, "why does this print X?") and requires an explanation in code comments or a test.
- **SQL/JDBC (25–27):** SQL script tasks verified through H2 (PostgreSQL mode) + JDBC tests; DAO tasks with `PreparedStatement`.
- **Spring Boot (28–42):** a mix of slice tests (`@WebMvcTest`, `@DataJpaTest`), service unit tests with Mockito, and one integration-style task per day from Day 35 onward.
- **Microservices (43–46):** resilience and messaging tasks with simulated downstream services and `EmbeddedKafka`.
- **Capstone (47–50):** multi-feature tasks, timed tasks, review.

### A.2 Difficulty curve within a day

| Slot | Purpose |
|------|---------|
| `task-01` | Warm-up (Level A): follows examples from theory; includes at least one "predict the output / explain" element |
| `task-02` | Core skill (Level B): independent implementation |
| `task-03` | Stretch within the day: combines 1–2 prior concepts |
| `task-04` | Challenge: integrates the day with earlier days; may be labeled **Challenge (requires research)** |

If only three tasks exist, merge `task-04` goals into `task-03` and label difficulty.

### A.3 Anti-patterns (do not generate)

- **Mystery tasks** — no acceptance criteria.
- **Huge boilerplate** — learners delete code instead of learning.
- **Brittle tests** — asserting log output, exact exception text, hash codes, iteration order of `HashMap`, or timing.
- **Hidden coupling** — requires knowledge from later days (label **Challenge** if unavoidable).
- **Tests that can be satisfied by hard-coded returns** — include varied inputs and property-style cases.
- **Framework magic early** — Spring or Lombok before Day 28 / ever, respectively.
- **Live infrastructure** — tests needing PostgreSQL, Kafka, network, or Docker.
- **Sleep-based concurrency tests** — use latches, `Awaitility`, or `@Timeout`.

### A.4 Academic integrity nudge

Vary domain nouns across tasks (library, parking lot, clinic, warehouse, ticketing, bookstore) and require small unique details (rename-able identifiers, domain-specific rules) so solutions diverge. Keep grading objective through tests + rubric.

### A.5 Realism

Tasks should resemble backend work: parse input, validate, transform collections, persist, expose APIs, secure endpoints, handle errors, write tests. Prefer small domain models (Order, Customer, Account, Product, Booking, Employee) that recur across phases so learners see them evolve.

---

## Part B — Java testing guidance

### B.1 Behavioral contracts

Good:

- Public methods return expected results for listed inputs, including edge cases (null, empty, boundary, overflow).
- Exceptions: `assertThatThrownBy(() -> ...).isInstanceOf(IllegalArgumentException.class)`.
- Immutability: attempting mutation throws (`UnsupportedOperationException`) or a defensive copy is observable.

Avoid:

- Asserting `HashMap`/`HashSet` iteration order; compare with `containsExactlyInAnyOrder`, `containsOnlyKeys`.
- Asserting `toString()` formats unless the task defines the format.
- Testing private methods (use reflection only in tasks whose goal is reflection).

### B.2 Stub behavior

All stubs throw `UnsupportedOperationException("TODO(DayXX-taskYY): ...")` (see `03` §6.2). Document the expected initial red count.

### B.3 Mockito usage

- Introduce Mockito mocks formally on **Day 23**; earlier days use hand-written fakes/stubs.
- Prefer constructor-injected collaborators so tests need no reflection.
- Verify interactions (`verify`) only when the interaction **is** the behavior (e.g. "email sent once"); otherwise assert state/results.
- Use `ArgumentCaptor` sparingly and teach it explicitly.

### B.4 Time, randomness, concurrency

- Inject `java.time.Clock`; tests use `Clock.fixed(...)`.
- Inject `Random`/`Supplier<UUID>` or seed it.
- Concurrency tests: `@Timeout(5)`, `CountDownLatch`, `ExecutorService` with bounded pools, `Awaitility`; assert on invariants (final counter value, no deadlock), not on scheduling order.

### B.5 Spring test guidance

| Slice | Use for | Notes |
|-------|---------|-------|
| `@WebMvcTest` | controllers, validation, `ProblemDetail`, security rules | `@MockitoBean` for services (Boot 4 naming — verify) |
| `@DataJpaTest` | repositories, JPQL, relationships | H2 PostgreSQL mode via `application-test.yml`; `@AutoConfigureTestDatabase(replace = NONE)` when using explicit URL |
| `@SpringBootTest` | end-to-end wiring, security chain, Kafka | Use sparingly; random port; `@ActiveProfiles("test")` |
| Plain JUnit + Mockito | services, mappers, utilities | Fastest; default choice |

Rules:

- Seed data via test setup or `@Sql` scripts, never relying on test order.
- JWT tests use a fixed fake secret from `application-test.yml`.
- Kafka tests: `@EmbeddedKafka(partitions = 1, topics = {...})`, `spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}`; bounded waits only.

### B.6 Coverage

JaCoCo is introduced Day 23. **100% coverage is not required**; target meaningful tests. Coverage gates (if any) are discussed on Day 49 and are optional.

---

## Part C — Spring / REST / JPA task guidance

### C.1 What to include in boilerplate

- A bootable `@SpringBootApplication` class.
- Skeletons for controllers/services/repositories with throwing stubs.
- DTOs/entities provided when the day is not about writing them.
- `application.yml` with env-var placeholders; `application-test.yml` for H2.

### C.2 REST rubric expectations

Rubrics should reference concrete HTTP behavior:

- Status codes (201 + `Location` on create, 204 on delete, 400 validation, 404 missing, 409 conflict, 401 vs 403).
- Response body shape (DTO fields, `ProblemDetail` fields `type`, `title`, `status`, `detail`, `instance`, custom properties).
- Validation messages and field errors.

### C.3 JPA rubric expectations

- Entities have a protected/no-arg constructor, correct `equals/hashCode` strategy, and no Lombok.
- Relationships: owning side correct, `mappedBy`, cascade/orphanRemoval justified, `FetchType.LAZY` default for to-many and explicit for to-one.
- Include a task (Day 35) where N+1 is **measured** (e.g. via Hibernate `Statistics` or a query counter) and fixed with `JOIN FETCH` / entity graph.
- `@Transactional` boundaries placed in services; demonstrate `LazyInitializationException` and its correct fix (not `open-in-view` hacks).
- `@Version` optimistic-locking conflict reproduced in a test.

### C.4 Security rubric expectations

- BCrypt for passwords; no plaintext persistence.
- Stateless JWT with `Authorization: Bearer <token>`; verify signature, expiry, and claims.
- 401 (unauthenticated) vs 403 (authenticated, not allowed) asserted separately.
- `@PreAuthorize` method security verified with `spring-security-test`.
- Never log tokens or passwords.

### C.5 Microservices and Kafka expectations

- Resilience4j: tests demonstrate circuit-breaker open state, retry counts, and timeout with a fake downstream (no real network).
- Gateway routing tested with local stub targets on random ports.
- Kafka: producer/consumer round-trip with `EmbeddedKafka`; DLT test with poison message; idempotent consumer test with duplicate event IDs; outbox is a **concept + table-based simulation** (no CDC tooling).

---

## Part D — Mapping topics to theory sections (agent checklist)

When writing `DAY-XX-THEORY-AND-REFERENCE.md`:

- Every primary theme appears as an `##`/`###` heading.
- Every subtopic uses the per-subtopic template from `03` §4.4.
- Examples compile (verify by pasting into a scratch project when tools allow).
- Cross-link prior days ("Review Day 09 `equals/hashCode` before HashMap").
- Include the **Interview corner**.
- Call out Java 21 specifics (records, sealed, pattern matching, virtual threads) where relevant, and legacy forms only for reading old code.
- For each day, state in the theory header which tasks reinforce which subtopic.

---

## Part E — The 50-day topic map (default schedule)

**Legend — Task type:** **PJ** = Plain Java + JUnit; **PJM** = Plain Java + Mockito; **SQL** = SQL script + JDBC/H2 test; **JDBC** = JDBC + H2; **SB** = Spring Boot slice/unit tests; **JPA** = Spring Boot + JPA on H2; **SEC** = Spring Security; **KAF** = EmbeddedKafka; **MS** = microservice pair/simulation.

### Phase 1 — Core Java (Days 01–24)

| Day | Primary theme and subtopics | Suggested task ideas (3–4 tasks) | Types |
|----:|-----------------------------|-----------------------------------|-------|
| **01** | **JDK/JRE/JVM, `javac`, class structure, `main`, packages, first Maven.** Compile/run lifecycle, bytecode, `java` launcher, source layout, package/import rules, Maven coordinates, `mvn compile/test`, IntelliJ import. | Predict compile/run outputs; fix package/directory mismatches; implement `Greeter` utilities; Maven project health check class (reads `System.getProperty("java.version")` via injectable supplier). | PJ |
| **02** | **Primitives vs references, variables, scope, `var`, GC basics.** 8 primitives, defaults, reference semantics, aliasing, scope/shadowing, `var` rules, reachability, `finalize` is dead, `WeakReference` glimpse. | Alias vs copy lab; scope/shadowing puzzle; `var` inference table; reachability quiz with `WeakReference` (deterministic assertions only). | PJ |
| **03** | **Operators, promotion, casting, overflow.** Arithmetic/bitwise/logical, short-circuit, precedence, binary numeric promotion, widening/narrowing, `Math.*Exact`, floating-point pitfalls, `BigDecimal` intro. | Overflow-safe add/multiply; bit flags; casting traps; money rounding with `BigDecimal`. | PJ |
| **04** | **Control flow: `if`, `switch`, switch expressions, loops, labels.** Old vs arrow `switch`, `yield`, exhaustiveness, enhanced `for`, `break`/`continue` with labels, loop invariants. | Grade/day-type switch expressions; FizzBuzz variants; nested-loop search with labels; state-machine dispatcher. | PJ |
| **05** | **`String`, pool, `StringBuilder`, `equals`, text blocks.** Immutability, `intern`, `==` vs `equals`, `String.format`/`formatted`, `strip`, `repeat`, `chars`, text blocks, builder performance. | String pool predictions; palindrome/anagram utilities; CSV line parser; template renderer with text blocks. | PJ |
| **06** | **Arrays, `Arrays.sort`/`binarySearch`, varargs.** Arrays as objects, multi-dim, `Arrays.*` utilities, `System.arraycopy`, defensive copies, varargs pitfalls. | Rotate/merge arrays; binary search contract (insertion point); matrix utilities; varargs statistics. | PJ |
| **07** | **Methods, access modifiers, `static`, pass-by-value, overloading.** Pass-by-value of references, overload resolution (widening/boxing/varargs order), `static` state, encapsulation, `private/package/protected/public`. | Swap-that-doesn't-swap; overload resolution quiz; utility class design (private ctor); counter with static state and reset hook. | PJ |
| **08** | **Constructors, init order, `final`, immutable classes, records.** Constructor chaining, instance/static init blocks, order of initialization, `final` fields/vars, defensive copies, records (compact ctor), immutability checklist. | Init-order tracer (records execution log); immutable `Money`/`DateRange`; record with validation; builder vs record comparison. | PJ |
| **09** | **Inheritance, overriding, `super`, `equals`/`hashCode`/`toString`.** Method dispatch, field hiding, `super` calls, `@Override`, equals contract, hashCode consistency, `Objects.equals/hash`, `toString`. | Override vs hiding puzzles; implement `equals/hashCode` for `Point`/`Employee`; symmetry break with subclass; use mutable key in `HashSet` bug. | PJ |
| **10** | **Abstract classes, interfaces, polymorphism, `sealed`, SOLID light.** Abstract vs interface, default/static/private interface methods, sealed hierarchies, composition over inheritance, SRP/OCP/LSP/DIP intro. | Shape/Payment hierarchy; sealed `Result` with exhaustive switch; LSP violation fix; strategy via interface. | PJ |
| **11** | **Exceptions, try-with-resources, custom exceptions.** Checked vs unchecked, `finally`, suppressed exceptions, `AutoCloseable`, chaining (`cause`), custom domain exceptions, rethrow rules, exception-safe design. | Resource closing order tracker; custom `InsufficientFundsException`; retry-with-cause; parse-and-validate with meaningful exceptions. | PJ |
| **12** | **Wrappers, autoboxing, enums, nested classes.** `Integer` cache, boxing NPE, `==` on wrappers, enums with fields/methods/abstract methods, `EnumMap/EnumSet`, static nested/inner/local/anonymous classes. | Boxing traps; enum state machine; `EnumMap` counters; inner-class access to outer state. | PJ |
| **13** | **Generics, bounds, wildcards, PECS.** Type erasure, generic methods/classes, bounded types, `? extends` / `? super`, raw types, heap pollution, generic arrays limitation. | `Pair<A,B>`; `max(T extends Comparable<T>)`; copy with PECS; typed `Repository<T, ID>` in-memory. | PJ |
| **14** | **Collections I: `List`, `Iterator`, `Comparable`/`Comparator`.** `ArrayList` vs `LinkedList`, `Iterator`/`ListIterator`, `ConcurrentModificationException`, sorting, comparator chaining, `List.of` vs `Arrays.asList`. | Safe removal while iterating; multi-key sorting; stable sort demo; custom `Comparable` domain object. | PJ |
| **15** | **Collections II: `Set`/`Map`, `HashMap` internals, `Queue`, immutable collections.** `HashSet/LinkedHashSet/TreeSet`, `HashMap` buckets/resize/treeify (conceptual), `LinkedHashMap` LRU, `PriorityQueue`, `ArrayDeque`, `Map.of`, `Collections.unmodifiable*`, `copyOf`. | Word frequency; LRU cache via `LinkedHashMap`; bad `hashCode` key experiment; task scheduler with `PriorityQueue`. | PJ |
| **16** | **Lambdas, functional interfaces, method refs, `Optional`.** `Function/Predicate/Consumer/Supplier/BiFunction/UnaryOperator`, capturing/effectively final, method reference kinds, `Optional` API and misuse. | Build predicate combinators; compose functions; refactor null-checks to `Optional`; custom functional interface. | PJ |
| **17** | **Streams I: `filter`/`map`/`reduce`, collectors.** Pipeline model, lazy evaluation, intermediate vs terminal, `collect`, `toList`, `toMap`, `joining`, `reduce` identity/combiner, side-effect pitfalls. | Order total pipeline; text analytics; `toMap` duplicate-key handling; stream vs loop comparison. | PJ |
| **18** | **Streams II: `groupingBy`, `flatMap`, primitive streams, parallel cautions.** Downstream collectors, `partitioningBy`, `flatMap`, `IntStream/LongStream/DoubleStream`, summary statistics, `parallel()` pitfalls. | Group orders by status/customer; flatten nested data; statistics report; show parallel unsafe accumulation bug and fix. | PJ |
| **19** | **Date/Time, NIO.2 `Files`/`Path`.** `LocalDate/LocalDateTime/ZonedDateTime/Instant/Duration/Period`, formatters, time zones/DST, `Clock`, `Path`, `Files.*`, walking, temp dirs, charset. | Business-day calculator with `Clock`; timezone converter; log-file summarizer with `@TempDir`; safe path resolver (path traversal guard). | PJ |
| **20** | **Threads I: `Thread`/`Runnable`, `synchronized`, `volatile`, `wait`/`notify`, deadlock.** Thread lifecycle, race conditions, visibility, happens-before intro, monitors, producer/consumer with `wait/notify`, deadlock detection/avoidance. | Race-condition demo and fix; volatile flag stop; bounded buffer with wait/notify; lock-ordering deadlock fix. | PJ |
| **21** | **Concurrency II: `ExecutorService`, `CompletableFuture`, atomics, locks.** Thread pools, `Future`, `CompletableFuture` composition, `Atomic*`, `ReentrantLock`, `ReadWriteLock`, `ConcurrentHashMap`, `CountDownLatch`, shutdown patterns. | Parallel sum with executor; async aggregation with `CompletableFuture`; thread-safe counter/cache; rate-limiter with lock. | PJ |
| **22** | **Virtual threads, JVM memory/GC, classloading, troubleshooting.** Virtual threads vs platform threads, `Executors.newVirtualThreadPerTaskExecutor`, pinning, heap/stack/metaspace, GC families (G1/ZGC overview), class loader delegation, `jps/jstack/jmap/jcmd/jfr` basics, OOM types. | Virtual-thread fan-out; memory-leak pattern (static map) detection test; class-loading experiment; `Runtime` memory report utility. | PJ |
| **23** | **JUnit 5, Mockito, TDD, JaCoCo.** Lifecycle annotations, parameterized tests, `assertThrows`/AssertJ, mocks/stubs/spies, `ArgumentCaptor`, TDD red-green-refactor, JaCoCo report. | TDD a `PasswordPolicy`; mock a `PaymentGateway`; parameterized tests for a parser; write tests for provided code to reach target branches. | PJ, PJM |
| **24** | **Maven depth, pattern matching, Core Java review.** Lifecycle/phases, scopes, dependency management/BOM, plugins, profiles, multi-module overview, `instanceof`/`switch` pattern matching, record patterns, review integration. | Pattern-matching evaluator; Maven config reading quiz via tests on POM parsing helper; integrated Library domain task; mini "interview round" mixing Days 01–23. | PJ, PJM |

### Phase 2 — SQL and JDBC (Days 25–27)

| Day | Primary theme and subtopics | Suggested task ideas | Types |
|----:|-----------------------------|----------------------|-------|
| **25** | **PostgreSQL DDL/DML, constraints, normalization, ACID.** Data types, `CREATE/ALTER/DROP`, PK/FK/UNIQUE/CHECK/NOT NULL, `INSERT/UPDATE/DELETE`, `RETURNING`, 1NF–3NF, ACID properties, `psql` basics. | Design `bookstore` schema; add constraints and prove violations; normalize a flat table; ACID scenario write-up + scripted test. | SQL |
| **26** | **Joins, aggregates, indexes, views, transactions, functions/procedures.** Inner/left/right/full/cross joins, `GROUP BY/HAVING`, subqueries/CTEs, window functions intro, indexes and `EXPLAIN`, views, `BEGIN/COMMIT/ROLLBACK`, isolation levels, PL/pgSQL basics. | Multi-table reports; top-N per group; index choice reasoning; transaction rollback script; (PostgreSQL-only parts via rubric). | SQL |
| **27** | **JDBC, `PreparedStatement`, DAO, HikariCP, SQL injection.** Driver/URL, `Connection/Statement/ResultSet`, try-with-resources, batch, transactions in JDBC, DAO/repository pattern, pooling, injection demo and fix. | `ProductDao` CRUD on H2; transfer with manual transaction/rollback; vulnerable-vs-safe query test; Hikari config wrapper. | JDBC |

### Phase 3 — Spring Boot (Days 28–42)

| Day | Primary theme and subtopics | Suggested task ideas | Types |
|----:|-----------------------------|----------------------|-------|
| **28** | **Spring Core IoC/DI.** Container, beans, `@Component/@Service/@Repository`, `@Configuration/@Bean`, constructor injection, scopes, lifecycle callbacks, qualifiers, `ApplicationContext`. | Wire service graph; replace implementation via `@Qualifier`/`@Primary`; bean lifecycle logger; fix circular dependency. | SB |
| **29** | **Boot starters, `application.yml`, profiles, `@ConfigurationProperties`.** Auto-configuration, starters, property binding/relaxed names, profile-specific config, validation of properties, `@Value` vs properties classes. | Typed config with validation; profile-switching beans; custom auto-config-lite; config precedence tests. | SB |
| **30** | **REST I: controllers, `ResponseEntity`, Jackson.** `@RestController`, mappings, `@PathVariable/@RequestParam/@RequestBody`, status codes, headers, Jackson (de)serialization, `@JsonProperty/@JsonIgnore`, content negotiation. | CRUD controller on in-memory store; `Location` header on create; Jackson customization; query-param filtering. | SB |
| **31** | **REST II: DTOs, Validation, `ProblemDetail`, layered architecture.** Controller/service/repository layering, DTO mapping, Bean Validation (`@Valid`, constraints, groups), `@RestControllerAdvice`, RFC 9457 `ProblemDetail`. | Request/response DTOs; custom validator; global handler with field errors; layered refactor. | SB |
| **32** | **Spring Data JPA I: entities, repositories, CRUD.** `@Entity`, ids/generation, `JpaRepository`, derived queries, `save/find/delete`, entity lifecycle states, H2 test setup. | `Customer` entity + repository tests; derived query methods; id strategies; auditing fields. | JPA |
| **33** | **JPA II: JPQL, `@Query`, pagination, projections.** JPQL syntax, named/positional params, native queries (PostgreSQL-compatible subset), `Pageable/Page/Slice`, `Sort`, interface/class projections, `Specification` intro. | Search endpoint with pagination; projection DTOs; dynamic filtering; JPQL aggregates. | JPA |
| **34** | **JPA III: relationships, cascade, fetch.** `@OneToMany/@ManyToOne/@ManyToMany`, owning side, `mappedBy`, cascade types, `orphanRemoval`, `FetchType`, bidirectional helpers, `equals/hashCode` on entities. | Order–OrderItem model; Student–Course many-to-many with join entity; cascade/orphan removal tests. | JPA |
| **35** | **JPA IV: N+1, `JOIN FETCH`, `@Transactional`, `@Version`, Flyway.** Detecting/fixing N+1, `@EntityGraph`, transaction propagation/isolation/rollback rules, `LazyInitializationException`, optimistic locking, Flyway migrations. | Measure and fix N+1; rollback-on-checked-exception test; optimistic-lock conflict test; V1/V2 migrations with `validate`. | JPA |
| **36** | **OpenAPI/springdoc, `RestClient`, CORS.** springdoc annotations, grouping, schema docs, `RestClient` builder/error handling/timeouts, `MockRestServiceServer`, CORS config and pitfalls. | Document API with examples; client wrapper with error mapping; CORS config tests. | SB |
| **37** | **Security I: filter chain, `UserDetailsService`, BCrypt, roles.** `SecurityFilterChain`, authentication vs authorization, `UserDetailsService`, `PasswordEncoder`, roles/authorities, CSRF stance for stateless APIs, `spring-security-test`. | Registration with BCrypt; basic-auth protected endpoints; role-based access tests; custom `UserDetailsService`. | SEC |
| **38** | **Security II: JWT, 401 vs 403, `@PreAuthorize`.** JWT structure/claims, signing/verification, filter or resource-server style, `AuthenticationEntryPoint` vs `AccessDeniedHandler`, method security, expiry/refresh concepts. | Login → token → protected call; 401/403 handlers returning `ProblemDetail`; `@PreAuthorize` ownership rule; expired/tampered token tests. | SEC |
| **39** | **Spring testing: `@WebMvcTest`, `@DataJpaTest`, `@SpringBootTest`.** Slice philosophy, mocking beans, MockMvc assertions, JPA slice, full-context tests, test profiles, `@Sql`, test performance. | Convert slow tests to slices; controller contract tests; repository tests with constraints; one end-to-end flow. | SB, JPA, SEC |
| **40** | **AOP: aspects, pointcuts, advice.** Proxy model (JDK vs CGLIB), `@Aspect`, pointcut expressions, `@Before/@After/@Around`, self-invocation pitfall, cross-cutting use cases. | Timing aspect; audit-log aspect; retry aspect; self-invocation failure demo. | SB |
| **41** | **SLF4J/Logback, MDC, Actuator, health, metrics.** Log levels/appenders/patterns, parameterized logging, MDC correlation id filter, Actuator exposure/security, custom `HealthIndicator`, Micrometer counters/timers. | Correlation-id filter; custom health indicator; metrics on service calls; assert log capture with `OutputCaptureExtension`. | SB |
| **42** | **Async, Scheduled, Cache, virtual threads in Boot.** `@EnableAsync/@Async`, executors, `@Scheduled` (cron/fixed), `@Cacheable/@CacheEvict`, cache pitfalls, `spring.threads.virtual.enabled`, blocking I/O guidance. | Async report generation; scheduler with injected `Clock`/trigger test; cache hit/miss counters; virtual-thread config check. | SB |

### Phase 4 — Microservices (Days 43–46)

| Day | Primary theme and subtopics | Suggested task ideas | Types |
|----:|-----------------------------|----------------------|-------|
| **43** | **Microservices, `RestClient`, Resilience4j.** Service boundaries, sync communication, failure modes, timeouts, retry, circuit breaker, bulkhead, fallbacks, observability basics. | Order→Inventory client with fallback; circuit-breaker state test; retry with backoff; timeout test with slow stub. | MS |
| **44** | **Spring Cloud Gateway, config across services.** Routes/predicates/filters, path rewriting, auth at the edge, externalized config concepts, per-service config and profiles (Config Server concept only, local files in practice), service-to-service config contracts. | Gateway routes to two stubs; header-injection filter; shared properties pattern; rate-limit/filter test. | MS |
| **45** | **Kafka I: producer/consumer.** Topics, partitions, keys, offsets, consumer groups, `KafkaTemplate`, `@KafkaListener`, serializers, acks, ordering guarantees, `EmbeddedKafka`. | Publish/consume string events; keyed partition ordering test; consumer-group behavior; error handler basics. | KAF |
| **46** | **Kafka II: JSON events, DLT, idempotent consumers, outbox concept.** JSON (de)serialization with versioned events, `DefaultErrorHandler` + `DeadLetterPublishingRecoverer`, retry/backoff, idempotent processing with processed-event table, transactional outbox pattern (simulated). | Order event JSON contract; poison message → DLT; duplicate-event idempotency; outbox poller simulation. | KAF |

### Phase 5 — Capstone and readiness (Days 47–50)

| Day | Primary theme and subtopics | Suggested task ideas | Types |
|----:|-----------------------------|----------------------|-------|
| **47** | **Capstone API slice I: auth + entity + relationships.** Register/login, JWT, `User`–`Resource` relationships, DTO layering, validation, Flyway schema. | Auth module; core entity CRUD with relationships; migrations + tests; security rules matrix. | SEC, JPA |
| **48** | **Capstone API slice II: ownership, pagination, errors, tests.** Owner-only access, pagination/sorting/filtering, consistent error model, test pyramid, edge-case hardening. | Ownership enforcement (403 vs 404 policy); paged search; global error contract; full test suite pass. | SEC, JPA |
| **49** | **Production: profiles, secrets, JAR, GitHub Actions, Checkstyle, Git.** Profiles per env, secrets via env/secret stores, `spring-boot:repackage`, running the JAR, GitHub Actions workflow (Maven build + test), Checkstyle config, Git branching/PR hygiene, release checklist. | Prepare prod profile + externalized secrets; write `.github/workflows/ci.yml`; Checkstyle fix pass; assess a PR checklist test (config validation unit tests). | SB, Reading + code |
| **50** | **Interview review: Core Java + Spring, timed tasks.** Rapid review of Core Java, collections, concurrency, JVM, SQL, Spring, JPA, security; timed coding rounds; system design talking points. | 3–4 timed tasks (e.g. 45/60/90 minutes) mixing collections/streams, Spring REST+JPA bug hunt, concurrency fix, SQL optimization reasoning. | PJ, SB, JPA |

### Post-course projects (named only; separate specs)

1. **StayEasy Hotel Booking** — monolith: auth, rooms, availability, bookings, payments simulation, pagination, ownership.
2. **PayFlow Wallet Banking** — transactional integrity, idempotency, optimistic locking, ledger, Kafka events.
3. **PeopleHub HR Microservices** — gateway, employee/department/leave services, resilience, Kafka events, centralized config.

---

## Part F — Coverage and spiral checklist

Before finalizing the course, verify:

- [ ] Every item in `01` §3 appears in a theory file and a task.
- [ ] `equals/hashCode` is revisited on Days 09, 15, 34 (JPA entities).
- [ ] Exceptions appear on Days 11, 31, 38 (`ProblemDetail`, 401/403), 43 (resilience).
- [ ] Immutability appears on Days 08, 15, 31 (DTO records), 46 (events).
- [ ] Transactions appear on Days 25–27, 35, 46 (outbox).
- [ ] Concurrency appears on Days 20–22, 42, 43.
- [ ] Testing appears every day, formally taught Days 23 and 39.
- [ ] Day 24 and Day 50 act as integration/review days with mixed-prior-day tasks.
- [ ] No Spring before Day 28; no Docker or frontend anywhere.

---

## Part G — Reference-solution policy

- For every task, authors produce a **reference solution** to prove `mvn test` can pass.
- Reference solutions are **not** committed in the candidate-facing tree. Store them instructor-side (e.g. a private branch or local `solutions/` directory that is gitignored) or in a separate private repository.
- Before publishing a day, run: boilerplate → expect red; solution → expect green.

---

## Part H — Handoff note

Agents generating days must follow: `02` constraints → `03` structure → this schedule → `01` pedagogy. If a topic cannot be taught within the locked decisions (e.g. needs Docker), choose the closest no-Docker alternative and note it in the day's theory.
