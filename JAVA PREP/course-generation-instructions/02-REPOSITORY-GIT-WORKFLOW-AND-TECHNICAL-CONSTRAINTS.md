# 02 — Repository, Git Workflow, and Technical Constraints

**Instruction set version:** `1.0.0`

This document defines **how the repository is organized**, **what must never be committed**, **how Java tasks are built and verified**, and the **baseline tooling** so multiple agents produce compatible output.

---

## 1. Repository layout (target end state)

The Java course lives inside the existing monorepo under `JAVA PREP/`:

```text
JAVA PREP/
  course-generation-instructions/     # This folder
  Day 01/
  Day 02/
  ...
  Day 50/
  README.md                           # Candidate-facing: prerequisites, setup, workflow
  .gitignore                          # Java-specific (see Section 3)
  setup/                              # Optional: installation notes (JDK, PostgreSQL, IntelliJ)
  scripts/                            # Optional: validation / generator scripts
```

**Day folder naming:** `Day 01` … `Day 50` (capital `D`, space, two digits). Do **not** use `day-1`, `Day1`, `day_01`.

Each task is a **standalone Maven project** (its own `pom.xml`). There is **no** multi-module parent at the course level; candidates open one task folder at a time in IntelliJ.

---

## 2. Git workflow for candidates (must be documented in `JAVA PREP/README.md`)

### 2.1 Clone and branch

1. `git clone <repo-url>` and `cd` to the repo.
2. Recommended: personal branch `student/<name-or-id>/main`, or per-day branches `student/<id>/day-07`. Instructor chooses; **document the policy** in the README.

### 2.2 Daily work loop

1. `git pull`.
2. Read `Day XX/DAY-XX-THEORY-AND-REFERENCE.md`.
3. `cd "JAVA PREP/Day XX/practical-tasks/task-0N-slug"`.
4. Run `mvn test` — expect **red** (stubs throw `UnsupportedOperationException`).
5. Implement the `TODO(DayXX-taskYY)` items; re-run `mvn test` until green.
6. `git add` only the intentionally changed files (never `target/`).
7. `git commit -m "Day 07: complete task-02 overloading lab"`.
8. `git push`.

### 2.3 Instructor evaluation loop

1. `git pull` the candidate branch.
2. Per task: `mvn -q test` (or `mvn test`) in the task folder; capture the Surefire summary.
3. Review code against `EVALUATION_CRITERIA.md` and `05`. Optionally use an AI agent with those files as rubric.

### 2.4 Conflict-avoidance rules

- Candidates must **not** edit `TASK_INSTRUCTIONS.md`, `EVALUATION_CRITERIA.md`, `pom.xml` (unless told), or files under `src/test/` **unless the task says so in bold**.
- Candidates edit only files containing `TODO(DayXX-taskYY)` markers (and glue files the task names).
- Commit messages follow `Day XX: <what was done>`.

---

## 3. `.gitignore` (required at `JAVA PREP/`)

```gitignore
# Maven / build output
target/
*.class
*.jar
*.war
!.mvn/wrapper/maven-wrapper.jar
dependency-reduced-pom.xml

# Logs
*.log
logs/

# IntelliJ / editors
.idea/
*.iml
*.iws
out/
.vscode/*
!.vscode/extensions.json

# OS
.DS_Store
Thumbs.db

# Environment and secrets (never commit)
.env
.env.*
!.env.example
application-local.yml
application-local.properties
*.pem
*.key
*.p12
*.jks

# Test / coverage output
jacoco.exec
```

---

## 4. Maven rules (every task)

### 4.1 Mandatory `pom.xml` properties

- `groupId`: `com.javaprep`
- `artifactId`: matches the task slug, e.g. `day07-task02-overloading-lab`
- `version`: `1.0.0-SNAPSHOT`
- `maven.compiler.release` = `21` (use `<release>21</release>`, not `source/target`)
- `project.build.sourceEncoding` = `UTF-8`

### 4.2 Plain-Java tasks (Days 01–27)

- **No Spring**. Packaging `jar`.
- Dependencies (test scope): `org.junit.jupiter:junit-jupiter`, `org.assertj:assertj-core`, `org.mockito:mockito-junit-jupiter` (only when mocking is taught or needed).
- Plugins: `maven-compiler-plugin`, `maven-surefire-plugin` (3.x, JUnit Platform). Pin versions explicitly.
- Use the **JUnit BOM** (`junit-bom`) and keep versions consistent across all tasks (record chosen versions in `JAVA PREP/setup/VERSIONS.md`).
- Day 27 (JDBC) adds `org.postgresql:postgresql` (runtime), `com.zaxxer:HikariCP`, and `com.h2database:h2` (test) — tests run against **H2 PostgreSQL mode**.
- Day 24 adds Maven-depth content (profiles, BOM, plugin execution); JaCoCo is introduced on Day 23 via `jacoco-maven-plugin` (report only; **no coverage gate** that fails the build by default).

### 4.3 Spring Boot tasks (Days 28–50)

- Parent: `org.springframework.boot:spring-boot-starter-parent` at the **same Boot 4.x version** for all tasks (record in `VERSIONS.md`).
- Java: `<java.version>21</java.version>`.
- Only the starters the day has taught. Typical ones:

| Need | Dependency |
|------|-----------|
| Web | `spring-boot-starter-web` (or `spring-boot-starter-webmvc` if Boot 4 modular naming applies — verify against the pinned version) |
| Validation | `spring-boot-starter-validation` |
| JPA | `spring-boot-starter-data-jpa` |
| Security | `spring-boot-starter-security` |
| Actuator | `spring-boot-starter-actuator` |
| AOP | `spring-boot-starter-aop` |
| Cache | `spring-boot-starter-cache` |
| Kafka | `spring-kafka` |
| Test | `spring-boot-starter-test`, `spring-security-test`, `spring-kafka-test` |
| DB (runtime) | `org.postgresql:postgresql` |
| DB (test) | `com.h2database:h2` (scope `test`) |
| Migrations | `flyway-core` + `flyway-database-postgresql` |

**Boot 4 caveat for agents:** Boot 4 modularized auto-configuration and starters and changed some test-slice packages/artifacts. **Before generating Days 28+, resolve the real dependency coordinates and test-slice import packages against the pinned Boot 4.x release** (e.g. by building one reference task and checking imports for `@WebMvcTest`, `@DataJpaTest`, `TestRestTemplate`/`RestTestClient`, Jackson 3 vs 2 packages). Document findings in `JAVA PREP/setup/VERSIONS.md` and apply them uniformly. Do not guess.

### 4.4 Maven wrapper

- Include the Maven Wrapper (`mvnw`, `mvnw.cmd`, `.mvn/wrapper/maven-wrapper.properties`) in each task **or** require a system Maven 3.9+ and document that choice once in the root README. Pick **one** policy for the whole course.
- Default recommendation: **system Maven 3.9+**, no wrapper (smaller tasks). The verification command is always `mvn test`.

### 4.5 After cloning, these commands must work

| Task type | Minimum success criteria |
|-----------|---------------------------|
| Any task | `mvn -q test-compile` succeeds on the unmodified boilerplate. |
| Any task | `mvn test` runs and **fails (red)** only because of TODO stubs. |
| Spring Boot task | Context-loading tests pass or fail only through TODO work; the app must not fail at startup because of missing infrastructure (no mandatory live PostgreSQL/Kafka for `mvn test`). |
| Reference solution | `mvn test` fully green. |

---

## 5. Database constraints

### 5.1 PostgreSQL 17 (manual / runtime use)

- Local install (Homebrew, installer, or package manager) — **no Docker**. Document install steps in `JAVA PREP/setup/`.
- Connection values only through environment variables / Spring placeholders:

```yaml
spring:
  datasource:
    url: ${DB_URL:jdbc:postgresql://localhost:5432/javaprep}
    username: ${DB_USERNAME:javaprep}
    password: ${DB_PASSWORD:change-me-in-dev}
```

- Days 25–26 are **SQL-script** days: provide `.sql` files under `src/main/resources/sql/` or a task `sql/` folder for use in `psql`; automated tests execute equivalent scripts on **H2 in PostgreSQL mode** through JDBC where feasible, and use rubric review for PostgreSQL-only features.

### 5.2 H2 for tests

Use this base URL pattern in test config:

```text
jdbc:h2:mem:testdb;MODE=PostgreSQL;DATABASE_TO_LOWER=TRUE;DEFAULT_NULL_ORDERING=HIGH;DB_CLOSE_DELAY=-1
```

Rules:

- Tests **must not** need a running PostgreSQL.
- Prefer Flyway/`schema.sql` that works on both; if a migration uses PostgreSQL-only syntax (`jsonb`, `ILIKE`, partial indexes, `RETURNING` nuances, sequences with `nextval` casts), provide an H2-compatible alternative in a test-only location or avoid the syntax in tested paths, and note limitations in `TASK_INSTRUCTIONS.md`.
- Never use `spring.jpa.hibernate.ddl-auto=create-drop` in `main` profiles other than a clearly labeled `dev`/`test` profile. Prefer `validate` with Flyway from Day 35.

### 5.3 Kafka

- Tests use `@EmbeddedKafka` (from `spring-kafka-test`). Never require a locally running broker for `mvn test`.
- Runtime/manual Kafka instructions may describe running a local Kafka (KRaft) **without Docker**, but this is **optional** and must not block grading.
- Keep tests deterministic: use `Awaitility` or bounded `CountDownLatch`/`Consumer.poll` with explicit timeouts; never `Thread.sleep` for synchronization.

---

## 6. Testing standard

| Concern | Rule |
|---------|------|
| Framework | JUnit 5 (`org.junit.jupiter.api`) |
| Assertions | **AssertJ** (`assertThat`, `assertThatThrownBy`, `assertThatCode`) |
| Mocking | Mockito (`@ExtendWith(MockitoExtension.class)`); no PowerMock |
| Naming | `<ClassUnderTest>Test` in the **same package** under `src/test/java` |
| Method names | descriptive, e.g. `shouldReturnZeroWhenListIsEmpty` |
| Determinism | No real clocks (inject `Clock`), no random without seed, no network |
| Spring slices | `@WebMvcTest`, `@DataJpaTest`, `@SpringBootTest` (use sparingly; slow) |
| Timeouts | Concurrency tests use `@Timeout` |
| Command | `mvn test` (single class: `mvn -Dtest=ClassNameTest test`) |

### 6.1 Red–green workflow

Boilerplate **compiles** and tests **fail** because stubs throw:

```java
// TODO(Day07-task02): implement area(int, int) — rectangle area
public static int area(int width, int height) {
    throw new UnsupportedOperationException("TODO(Day07-task02): implement area(int, int)");
}
```

If a task is *intentionally* green at start (e.g., a read-and-explain task), say so at the top of `TASK_INSTRUCTIONS.md`.

### 6.2 Test integrity

- Tests assert **public behavior**, not private internals (unless the learning goal is internals, e.g. HashMap behavior demos).
- Do not assert exact exception message text unless the task teaches it; prefer exception type + `hasMessageContaining` for key tokens.
- Tests must not make correctness depend on stub *messages*.

---

## 7. Java language constraints for generated code

- Java 21 only; **no `--enable-preview`**.
- No Lombok (teach plain Java and records first; avoids annotation-processor setup issues in IntelliJ Community).
- No MapStruct. Write mappers manually.
- Prefer constructor injection in Spring code; field injection (`@Autowired` on fields) only in an explicitly labeled “anti-pattern” example.
- No `System.exit` in library code; no `printStackTrace()` in committed solutions (use SLF4J from Day 41; before that, return/throw).
- Sources under `src/main/java/com/javaprep/dayXX/taskYY/...` (see `03`).

---

## 8. Security checklist for agents (mandatory review)

- [ ] No real credentials, tokens, JWT secrets, or connection strings in the repo.
- [ ] Passwords in examples are hashed with BCrypt; plaintext passwords appear only as obvious test fixtures.
- [ ] JWT secrets come from properties/environment; test secrets are obviously fake (≥ 32 bytes for HS256, e.g. `test-only-secret-key-change-me-0123456789`).
- [ ] No SQL built by string concatenation with user input except in a clearly labeled **vulnerable demo** paired with the fixed version (Day 27).
- [ ] JPA entities are not returned directly from controllers after Day 31.
- [ ] `.env`/`application-local.*` are gitignored; `.env.example` has placeholders only.
- [ ] Actuator exposure is limited by config (`management.endpoints.web.exposure.include`).
- [ ] Dependencies are pinned through the Boot BOM / explicit versions; no known-critical CVE versions without a note.

---

## 9. Environment prerequisites to document (in `JAVA PREP/setup/`)

1. **JDK 21** (Temurin/OpenJDK), `JAVA_HOME`, `java -version` check.
2. **Maven 3.9+**, `mvn -v` check.
3. **IntelliJ IDEA Community**: open task folder → import as Maven project; set Project SDK to 21; run tests via gutter icons.
4. **PostgreSQL 17**: install, create role/database `javaprep`, `psql` smoke check.
5. **Git** and optional `curl`/HTTPie/`.http` files for manual API checks (IntelliJ Community does not run `.http` files natively — prefer `curl` examples).
6. Optional local Kafka (KRaft) for manual experiments; **not required** for tests.

---

## 10. Root `JAVA PREP/README.md` — required sections

1. Purpose and 50-day structure with phases.
2. Environment setup summary (links to `setup/`).
3. How to work day by day (navigate, `mvn test`, red→green).
4. Git workflow and branch policy.
5. How evaluation works (tests + rubric).
6. Troubleshooting (JAVA_HOME, wrong JDK, port in use, PostgreSQL auth).
7. Getting help policy (placeholder OK).
8. Post-Day-50 projects overview.

---

## 11. Handoff note for AI agents

Before generating any `Day XX` folder, re-read this file (`02`), then `03` (structure) and `04` (templates + schedule).

Precedence on conflict:

1. Security constraints in `02`
2. Locked decisions in `01` §2 and technical constraints in `02`
3. Folder structure in `03`
4. Schedule in `04`
5. Pedagogical goals in `01`

If `01` and `04` disagree on scheduling, **stop and ask the instructor**; do not silently drop topics.
