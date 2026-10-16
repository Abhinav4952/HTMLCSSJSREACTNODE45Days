# 50-Day Java Backend Prep Course

A hands-on, graduate-level **Java backend** course: **50 days** of theory plus practical tasks, followed by **three capstone projects**. Each `Day XX` folder holds consolidated theory and four Maven-based practical tasks with automated JUnit tests.

**Stack:** Java 21 (LTS) · Spring Boot **3.4.x** (Spring Framework 6.2, Hibernate 6.6) · Maven · PostgreSQL 17 · Spring Data JPA (Hibernate) · JUnit 5 + Mockito + AssertJ · Kafka (KRaft) for messaging days.

> Spring Boot 4 / Spring 7 landed recently; this course pins **3.4.x** so every lab and the three projects share one stable BOM. Concepts transfer cleanly when you upgrade later.

Scope is **backend only**: no frontend and no Docker. IDE of choice: **IntelliJ IDEA Community**.

## Setup guides (do these first)

| Guide | Purpose |
|-------|---------|
| [`setup/JAVA_AND_MAVEN_SETUP.md`](setup/JAVA_AND_MAVEN_SETUP.md) | JDK 21 (Temurin), Maven, `JAVA_HOME`, IntelliJ |
| [`setup/POSTGRESQL_SETUP.md`](setup/POSTGRESQL_SETUP.md) | PostgreSQL 17, `psql`, GUI clients, `application-local.yml` |
| [`setup/KAFKA_SETUP.md`](setup/KAFKA_SETUP.md) | Apache Kafka in KRaft mode (needed for Days 45–46 labs and Project 03) |

You only need Java + Maven for the first days. PostgreSQL is needed for projects and manual runs; Kafka only for the Kafka labs.

## How to work day by day

1. Open `Day 01`, then `Day 02`, and so on in order (unless your instructor assigns a different path).
2. In each day folder, read `README.md` for objectives and the task table.
3. Read `DAY-XX-THEORY-AND-REFERENCE.md` before starting tasks.
4. Complete tasks in `practical-tasks/task-01-...` through `task-04-...` in order.
5. Edit only the places marked `TODO(DayXX-taskYY): ...`. Unfinished methods are stubs that throw `UnsupportedOperationException("TODO(DayXX-taskYY): ...")`; replace the stub with your implementation.
6. Do not modify `TASK_INSTRUCTIONS.md`, `EVALUATION_CRITERIA.md`, or test files unless a task explicitly allows it.
7. Run the tests, commit, and move on.

## Install, run, and verify

Prerequisites: JDK 21 and Maven 3.9+ (see the setup guide).

```bash
java -version      # should report 21.x
mvn -version       # should report Maven 3.9+ running on Java 21

cd "Day 01/practical-tasks/task-01-<name>"
mvn test           # fails until you complete the TODOs, passes when done
```

Useful variants:

| Command | Meaning |
|---------|---------|
| `mvn test` | Run all tests in the task (primary verification) |
| `mvn -q test` | Same, quieter output |
| `mvn -Dtest=ClassNameTest test` | Run a single test class |
| `mvn clean test` | Rebuild from scratch (useful after odd IDE/compile state) |
| `mvn spring-boot:run` | Start a Spring Boot task manually (Spring days) |

Notes:

- **Course tests use H2 in PostgreSQL mode** and `EmbeddedKafka`, so `mvn test` needs neither a local Postgres nor a local Kafka.
- Local PostgreSQL is for the capstone projects and manual runs. Copy `application-local.yml.example` to `application-local.yml` (git-ignored) as described in `setup/POSTGRESQL_SETUP.md`.
- Never commit `application-local.yml`, `.env`, or credentials.

## Git workflow (recommended)

1. `git clone <repo-url>` and `cd` into the repository.
2. **Branching:** create a personal branch such as `student/<your-id>/main`, or per-day branches like `student/<your-id>/day-07` if your instructor prefers that model.
3. **Daily loop:**
   `git pull` → complete `TODO`s → `mvn test` → `git add` only the files you changed → `git commit -m "Day 07: complete task-02 ..."` → `git push`.
4. Do not commit `target/`, `.idea/`, `*.iml`, logs, or local config (all covered by `.gitignore`).

## How evaluation works

- **`mvn test` is the primary correctness signal.** All tests in a task passing means the functional bar is met.
- Instructors (or AI-assisted review) also score code quality, naming, structure, and handling of edge cases using each task's `EVALUATION_CRITERIA.md`.
- Grading uses a **1–100 scale** with bands (needs work / passing / strong / excellent) and written feedback.
- Do not weaken, delete, or skip tests to get green; that is a failing submission.

## Getting help

Use office hours, the class forum, or the agreed chat channel. Include the exact failing command, the full error output, and the Java/Maven versions (`java -version`, `mvn -version`). Each day's theory file links to official documentation.

## Capstone projects (after Day 50)

| Project | Focus |
|---------|-------|
| **Project 01: StayEasy** | Booking/hospitality REST API: JPA entities, relationships, validation, Spring Security (JWT), PostgreSQL |
| **Project 02: PayFlow** | Payments/wallet service: transactions, idempotency, resilience patterns, testing strategy |
| **Project 03: PeopleHub** | Event-driven HR/people platform: microservices pieces, Gateway, Resilience4j, Kafka (needs local Kafka) |

Full specifications are authored as a separate effort and will live in each project's folder.

## Repository layout

```text
JAVA PREP/
├── README.md                       # this file
├── .gitignore
├── setup/
│   ├── JAVA_AND_MAVEN_SETUP.md
│   ├── POSTGRESQL_SETUP.md
│   └── KAFKA_SETUP.md
├── course-generation-instructions/ # authoring specs for instructors / agents
├── scripts/                        # helper scripts
├── DOCS/                           # reference material
├── Day 01/ ... Day 50/
│   ├── README.md
│   ├── DAY-XX-THEORY-AND-REFERENCE.md
│   └── practical-tasks/
│       ├── task-01-<name>/         # pom.xml, src/main, src/test,
│       ├── task-02-<name>/         # TASK_INSTRUCTIONS.md,
│       ├── task-03-<name>/         # EVALUATION_CRITERIA.md
│       └── task-04-<name>/
└── Project 01 - StayEasy/ · Project 02 - PayFlow/ · Project 03 - PeopleHub/
```

## 50-day phase summary

Day titles below are the planned schedule; the instructor may publish overrides. Check each `Day XX/README.md` for the authoritative title.

| Phase | Days | Theme | Brief titles |
|-------|------|-------|--------------|
| 1. Core Java | 01–10 | Language foundations | 01 Setup, JVM, first program · 02 Types, variables, operators · 03 Control flow · 04 Methods and arrays · 05 Classes and objects · 06 Encapsulation, constructors, `static` · 07 Inheritance and polymorphism · 08 Interfaces, abstract classes, records · 09 Enums, `Object` methods, immutability · 10 Strings, `StringBuilder`, text blocks |
| 2. Java in depth | 11–20 | Collections, functional, I/O | 11 Exceptions · 12 Generics · 13 Collections: List/Set · 14 Collections: Map, ordering · 15 Lambdas and functional interfaces · 16 Streams I · 17 Streams II, `Optional` · 18 Date/time API · 19 File I/O (NIO.2) · 20 Concurrency basics: threads, executors |
| 3. SQL and JDBC | 21–25 | Relational foundations | 21 Relational modeling, PostgreSQL DDL · 22 SELECT, WHERE, ORDER BY · 23 Joins and aggregates · 24 JDBC: connections, `PreparedStatement` · 25 Transactions, isolation, connection pooling |
| 4. Spring core | 26–30 | Spring Boot basics | 26 Spring Boot project anatomy · 27 IoC and dependency injection · 28 Configuration, profiles, properties · 29 REST controllers · 30 Validation and error handling |
| 5. Persistence | 31–36 | Spring Data JPA | 31 JPA entities and mapping · 32 Repositories, derived queries · 33 Relationships (1:N, N:M) · 34 JPQL, pagination, N+1 · 35 Transactions in Spring · 36 DTOs, mapping, service layer design |
| 6. Security | 37–40 | Spring Security | 37 Authentication basics · 38 Password hashing, user store · 39 JWT issuing and validation · 40 Authorization, roles, method security |
| 7. Testing | 41–43 | Quality | 41 Unit testing with Mockito · 42 Web and slice tests (`@WebMvcTest`, `@DataJpaTest`) · 43 Integration tests with H2 (PostgreSQL mode) |
| 8. Microservices | 44–48 | Distributed systems | 44 Service boundaries, REST clients · 45 Kafka fundamentals (KRaft, topics, producers) · 46 Kafka consumers, `EmbeddedKafka` tests · 47 API Gateway · 48 Resilience4j: retry, circuit breaker |
| 9. Wrap-up | 49–50 | Production readiness, capstone | 49 Observability, Actuator, logging, build packaging · 50 Capstone rehearsal and review |

Days 45–46 include manual labs against a local Kafka broker (see `setup/KAFKA_SETUP.md`); their unit tests still use `EmbeddedKafka`.

## Quick reference

| Topic | Decision |
|-------|----------|
| Java | 21 LTS (Temurin recommended) |
| Framework | Spring Boot 4 / Spring Framework 7 |
| Build | Maven 3.9+ |
| Database | PostgreSQL 17 (local install, no Docker) |
| Persistence | Spring Data JPA (Hibernate) |
| Test DB | H2 in PostgreSQL mode |
| Messaging tests | `EmbeddedKafka` |
| Test libs | JUnit 5, Mockito, AssertJ |
| TODO format | `TODO(DayXX-taskYY): description` |
