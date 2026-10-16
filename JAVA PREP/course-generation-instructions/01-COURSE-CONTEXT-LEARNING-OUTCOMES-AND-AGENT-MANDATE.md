# 01 — Course Context, Learning Outcomes, and Agent Mandate

**Instruction set version:** `1.0.0`

This document defines **who** the course is for, **what** “done” means for each topic, the **locked technical decisions**, and **non-negotiable rules** for any AI agent (or human author) that generates day-wise folders.

---

## 1. Audience and assumed prior training

### 1.1 Learner profile

- **Level:** Graduate student (or early-career engineer) preparing for **Java backend** roles and interviews.
- **Declared baseline:** Familiar with programming fundamentals and basic web concepts (HTTP, JSON). May have JavaScript/Node exposure from earlier coursework; **no Java mastery is assumed**.
- **Reality check:** Treat the baseline as *exposure*, not mastery. The 50-day plan must **teach Java from first principles**, **force deliberate practice**, and reach the point where the learner can build a secured, tested, database-backed Spring Boot service unsupervised.

### 1.2 What this course is optimizing for

1. **Interview readiness:** Core Java, collections, concurrency, JVM, SQL, Spring, JPA, security, and microservice basics are the usual backend interview surface.
2. **Retention through spaced repetition:** Revisit ideas (equality, immutability, collections, transactions, exceptions) in later, harder contexts.
3. **Transfer:** Every day connects theory to **hands-on** work in `practical-tasks/`.
4. **Self-assessment:** Every task ships **JUnit 5 tests** runnable with `mvn test`.
5. **Production awareness:** Layering, validation, error handling, logging, security, and testing are taught as habits, not afterthoughts.

---

## 2. Locked decisions (do not change without instructor approval)

| Area | Decision | Notes |
|------|----------|-------|
| JDK | **Java 21 LTS** | Use records, sealed types, switch/pattern matching, text blocks, virtual threads. Do **not** use preview features. |
| Framework | **Spring Boot 4** (Spring Framework 7) | Pin the exact Boot 4.x version in each `pom.xml` via the parent. |
| Build tool | **Maven** | Each task is a standalone Maven project. |
| IDE | **IntelliJ IDEA Community** | Instructions mention IntelliJ steps; must not require Ultimate-only features. |
| Database | **PostgreSQL 17** | Local installation; connection via environment variables. |
| ORM | **Spring Data JPA (Hibernate)** | |
| Test DB | **H2 in PostgreSQL compatibility mode** | `jdbc:h2:mem:...;MODE=PostgreSQL;DATABASE_TO_LOWER=TRUE;DEFAULT_NULL_ORDERING=HIGH` |
| Kafka tests | **`EmbeddedKafka`** (`spring-kafka-test`) | No external broker needed for tests. |
| Containers | **No Docker** | Never require Docker, Testcontainers, or docker-compose. |
| Frontend | **None** | Backend only. Use `curl`, HTTP client files, or tests. |
| Testing | **JUnit 5 + Mockito + AssertJ** | Verified with `mvn test`. |
| Package root | `com.javaprep` | Sub-packages per day/task (see `03`). |

---

## 3. Topic inventory (authoritative list)

Every bullet below must appear in **at least one day’s theory** and be **practiced in at least one task** before the course ends. Overlap is intentional; later days deepen earlier themes.

### 3.1 Core Java (Days 01–24)

- JDK/JRE/JVM, `javac`, `java`, class structure, `main`, packages, first Maven project
- Primitives vs references, variables, scope, `var`, garbage-collection basics
- Operators, numeric promotion, casting, overflow
- Control flow: `if`, `switch`, switch expressions, loops, labeled break/continue
- `String`, string pool, `StringBuilder`, `equals`, text blocks
- Arrays, `Arrays.sort`/`binarySearch`, varargs
- Methods, access modifiers, `static`, pass-by-value, overloading
- Constructors, initialization order, `final`, immutability, records
- Inheritance, overriding, `super`, `equals`/`hashCode`/`toString`
- Abstract classes, interfaces, polymorphism, sealed types, SOLID (light)
- Exceptions, try-with-resources, custom exceptions
- Wrapper types, autoboxing, enums, nested/inner/anonymous classes
- Generics, bounds, wildcards, PECS
- Collections: `List`, `Iterator`, `Comparable`/`Comparator`, `Set`, `Map`, `HashMap` internals, `Queue`/`Deque`, immutable collections
- Lambdas, functional interfaces, method references, `Optional`
- Streams: filter/map/reduce, collectors, `groupingBy`, `flatMap`, primitive streams, parallel-stream cautions
- `java.time`, NIO.2 (`Path`, `Files`)
- Threads, `synchronized`, `volatile`, `wait`/`notify`, deadlock
- `ExecutorService`, `CompletableFuture`, atomics, locks, virtual threads
- JVM memory model overview, GC, classloading, troubleshooting tools
- JUnit 5, Mockito, TDD, JaCoCo
- Maven depth (lifecycle, scopes, BOMs, plugins), pattern matching, Core Java review

### 3.2 SQL and JDBC (Days 25–27)

- PostgreSQL DDL/DML, constraints, normalization, ACID
- Joins, aggregates, indexes, views, transactions, functions/procedures
- JDBC, `PreparedStatement`, DAO pattern, HikariCP, SQL injection

### 3.3 Spring Boot (Days 28–42)

- Spring Core IoC/DI; Boot starters, `application.yml`, profiles, `@ConfigurationProperties`
- REST controllers, `ResponseEntity`, Jackson, DTOs, Bean Validation, `ProblemDetail`, layered architecture
- Spring Data JPA: entities, repositories, CRUD, JPQL, `@Query`, pagination, projections
- JPA relationships, cascade, fetch types, N+1, `JOIN FETCH`, `@Transactional`, `@Version`, Flyway
- springdoc/OpenAPI, `RestClient`, CORS
- Spring Security: filter chain, `UserDetailsService`, BCrypt, roles, JWT, 401 vs 403, `@PreAuthorize`
- Spring testing: `@WebMvcTest`, `@DataJpaTest`, `@SpringBootTest`
- AOP, SLF4J/Logback, MDC, Actuator, health, metrics
- `@Async`, `@Scheduled`, caching, virtual threads in Boot

### 3.4 Microservices (Days 43–46)

- Microservice basics, `RestClient`, Resilience4j (circuit breaker, retry, timeout)
- Spring Cloud Gateway, config across services
- Kafka producer/consumer, JSON events, dead-letter topics, idempotent consumers, outbox concept

### 3.5 Capstone and readiness (Days 47–50)

- Capstone API slices (auth, entities, relationships, ownership, pagination, errors, tests)
- Production: profiles, secrets, executable JAR, GitHub Actions, Checkstyle, Git practices
- Interview review: Core Java + Spring, timed tasks

### 3.6 After Day 50 (named only)

Three portfolio projects: **StayEasy Hotel Booking**, **PayFlow Wallet Banking**, **PeopleHub HR Microservices**.

---

## 4. Proficiency model (what “learned” means)

For **each** topic taught on a day, the learner should reach both levels by the end of that day.

### 4.1 Level A — Theoretical + guided

- Can explain **what** it is and **why** it exists.
- Can trace **what breaks** when it is missing or misused.
- Can read and explain small code samples (including bytecode-level or runtime consequences where relevant, e.g. string pool, boxing).
- Can complete simple exercises with hints.

### 4.2 Level B — Independent “normal” tasks

- Can implement typical assignments without step-by-step supervision.
- Can debug common mistakes (NPE, `ConcurrentModificationException`, `LazyInitializationException`, 401 vs 403 confusion, wrong bean wiring).
- Knows where to look (Javadoc, Spring reference docs, PostgreSQL docs) when stuck.

**Agent instruction:** Task 1 leans Level A, Tasks 2–3 target Level B, Task 4 is a **stretch** combining the day’s topic with earlier days.

---

## 5. Pedagogical rules for content generation

### 5.1 One primary theme per day

Each `Day XX` has **one primary theme** with a bounded list of subtopics. Avoid kitchen-sink days unless labeled **Review / integration** (Days 24, 49, 50).

### 5.2 Spiral curriculum

- Equality (`==` vs `equals`) → `hashCode` → `HashMap` → JPA entity equality.
- Exceptions → custom exceptions → `@ControllerAdvice` / `ProblemDetail`.
- Immutability → records → DTOs.
- Threads → executors → `@Async` → virtual threads in Boot.
- SQL transactions → JDBC transactions → `@Transactional`.
- Lambdas → streams → Spring functional configuration and `Specification`-style code.

### 5.3 Java-first, framework-second

Days 01–27 use **plain Java** (no Spring). Spring appears only from Day 28. Do not smuggle Spring annotations into Core Java tasks.

### 5.4 Honesty about security and production

For JWT, passwords, CORS, SQL, and secrets:

- Teach **threat awareness** (SQL injection, leaked secrets, weak hashing, token misuse, mass assignment, over-exposed entities).
- **Never** embed real credentials; use placeholders and environment variables.
- Always hash passwords with BCrypt in examples.

### 5.5 Idiomatic modern Java

Prefer Java 21 idioms (records, `var` where readable, switch expressions, `Stream.toList()`, `Optional`, text blocks, pattern matching). Mention legacy forms (anonymous classes, raw types, `Date`, `Vector`) **only** so learners can read old code.

### 5.6 Testing as a habit

Every task includes tests. From Day 23 onward, theory teaches how to write tests; before Day 23, tests are provided and learners read them as specifications.

---

## 6. Agent mandate (non-negotiable deliverables)

Any agent generating `Day XX` content **must**:

1. Create the exact structure in `03`.
2. Cover every topic in Section 3 per the schedule in `04` (unless the instructor publishes an update).
3. Write theory in Markdown using the per-subtopic template in `03`.
4. Ship **3–4 practical tasks per day**, each its own standalone Maven project.
5. Provide runnable boilerplate: `mvn test` must **compile** and run; tests must **fail (red)** because of stubs (`UnsupportedOperationException("TODO(DayXX-taskYY): ...")`) until candidates implement TODOs.
6. Include `TASK_INSTRUCTIONS.md` and `EVALUATION_CRITERIA.md` for every task.
7. **Validate locally** when tools allow: `mvn -q test-compile` must succeed for every task; also verify a reference solution makes `mvn test` green (kept **outside** the candidate-facing tree or in an instructor-only location).
8. Never commit `target/`, IDE files, or secrets.
9. Respect the locked decisions in Section 2. If a topic seems to demand Docker, a frontend, or a different stack, find a no-Docker/backend-only alternative (H2, `EmbeddedKafka`, `curl`).

---

## 7. Quality bar and rejection criteria

Reject (revise) a generated day if any of the following are true:

- Theory has no examples, or fewer than **three** examples per major subtopic.
- Tasks do not reference the day’s learning objectives explicitly.
- `mvn test-compile` fails on boilerplate.
- Tests do not map to requirements in `TASK_INSTRUCTIONS.md`.
- A stub returns a plausible value instead of throwing (so tests could pass by accident) — unless the task says tests start green.
- Evaluation criteria are vague (“code should be good”) instead of observable checkpoints.
- Tests depend on Docker, a real PostgreSQL server, network access, system time, or randomness without control.
- Secrets or real credentials appear anywhere.
- Spring annotations appear in Days 01–27 tasks (except Day 27 using plain JDBC + HikariCP without Spring).
- Day uses APIs removed or deprecated for removal in Java 21 / Boot 4 without a note.

---

## 8. Changelog

| Version | Date | Notes |
|---------|------|-------|
| `1.0.0` | 2026-10-16 | Initial Java 50-day instruction set. |
