# 03 — Day Folder, Task Structure, and Naming Conventions

**Instruction set version:** `1.0.0`

This is the **mechanical specification** for directory trees, filenames, and required contents of Markdown and boilerplate files. Follow it **verbatim** unless the instructor publishes an amendment.

---

## 1. Day folder name and placement

- **Path:** `JAVA PREP/Day XX/`, `XX` = `01`–`50`.
- **Case:** Capital `D`, space, two-digit number.
- **Forbidden:** `Day-01`, `day01`, `Day1`, `Week1/Day1`.

---

## 2. Inside each `Day XX/` folder

```text
JAVA PREP/Day XX/
  README.md                          # Day index (Section 3)
  DAY-XX-THEORY-AND-REFERENCE.md     # Single consolidated theory file (Section 4)
  INSTRUCTOR_GRADING_1-100.md        # Optional, instructor/AI-only (see 05)
  practical-tasks/
    task-01-<slug>/
    task-02-<slug>/
    task-03-<slug>/
    task-04-<slug>/                  # Optional 4th task (target)
```

### 2.1 Task count

- **Minimum:** 3. **Target:** 4. **Maximum:** 4 (exceptions need instructor approval).

### 2.2 Task folder naming

```text
task-<two-digit-index>-<kebab-case-slug>/
```

Examples: `task-01-primitive-vs-reference`, `task-02-string-pool-lab`, `task-03-hashmap-word-count`.

Slug rules: lowercase, digits, hyphens only; no spaces/underscores; ≤ 40 characters.

---

## 3. `Day XX/README.md` (day index)

**Length:** 1–2 screens.

Required sections:

1. **Title (H1):** `Day 07 — Methods, Access Modifiers, static, and Overloading`
2. **Learning objectives** (4–7 bullets, aligned with theory headings)
3. **Prerequisites** (earlier days to review)
4. **How to use this folder**
   - Read the theory file first.
   - Open each task folder as its own Maven project in IntelliJ.
   - Run `mvn test` (red) → implement TODOs → `mvn test` (green).
5. **Task list**

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-...` | Plain Java (JUnit) | `mvn test` |
| 2 | `task-02-...` | Plain Java (JUnit + Mockito) | `mvn test` |
| 3 | `task-03-...` | Spring Boot (`@WebMvcTest`) | `mvn test` |
| 4 | `task-04-...` | Stretch / integration | `mvn test` + rubric |

The table must reflect the **actual** tasks. Allowed **Type** values: `Plain Java`, `Plain Java + JDBC (H2)`, `SQL script + JDBC test`, `Spring Boot`, `Spring Boot + JPA (H2)`, `Spring Boot + Security`, `Spring Boot + Kafka (EmbeddedKafka)`, `Microservice pair`, `Reading + code`.

6. **Estimated time** and **Phase** (Core Java / SQL-JDBC / Spring Boot / Microservices / Capstone).

---

## 4. `DAY-XX-THEORY-AND-REFERENCE.md`

### 4.1 Filename

`DAY-XX-THEORY-AND-REFERENCE.md`, `XX` identical to the parent folder.

### 4.2 Top matter (required)

```markdown
# Day XX — <Short Title>

**Phase:** <Core Java | SQL/JDBC | Spring Boot | Microservices | Capstone>
**Primary theme:** <one line>
**Estimated study time:** <e.g. 2–3 h theory + 3–5 h tasks>
**Related tasks:** `task-01-...`, `task-02-...`, ...
**Instruction alignment:** Maps to topics <list> from `01` §3.
**Java / Spring versions:** Java 21, Spring Boot 4.x (when applicable)
```

### 4.3 Document structure

1. **Overview** — what the learner gains; how it appears in real backend work and interviews.
2. **Day roadmap** — numbered reading order.
3. **Subtopic sections** — one per subtopic using Section 4.4.
4. **Interview corner** — 5–8 likely interview questions with concise model answers.
5. **Common mistakes & debugging** — grounded in the day’s content (real exception names, real symptoms).
6. **Further reading** — Oracle Java docs / JLS / Javadoc, Spring reference docs, PostgreSQL docs, Baeldung-class sources only as secondary.
7. **Glossary**
8. **Answers** — answers to all “Quick checks”.

### 4.4 Required template per subtopic (`### <Subtopic>`)

Each includes the following `####` headings, in order:

1. `#### What it is` — plain definition + mental model.
2. `#### Why it exists / why it matters` — real engineering problems.
3. `#### Pros and cons` — ≥ 3 pros, ≥ 2 cons/tradeoffs.
4. `#### What happens without it / when misused` — concrete failure modes (exceptions, bugs, performance, security).
5. `#### Syntax and rules` — canonical forms; gotchas (e.g. integer cache, `HashMap` mutable keys, `LazyInitializationException`).
6. `#### Examples` — **3–5** per major subtopic: ≥ 2 tiny (5–20 lines), ≥ 1 medium (a cohesive class set or multi-file reference). Java examples are compilable or state assumed context; Spring examples name the starters needed.
7. `#### Quick checks` — 3–5 questions, no answers inline.

**Java specifics:**

- Show **expected output** in comments for examples that print.
- For JVM/memory topics include small diagrams (ASCII/Mermaid) of stack/heap/pool.
- For Spring topics include **request → response flow** or **bean wiring** diagrams where useful.
- For SQL topics provide runnable `psql` snippets, noting PostgreSQL-specific behavior.

---

## 5. Task folder: required files and standard tree

Every task folder **must** contain:

1. `TASK_INSTRUCTIONS.md`
2. `EVALUATION_CRITERIA.md`
3. `pom.xml`
4. `src/main/java/com/javaprep/...` with stubs/TODOs
5. `src/test/java/com/javaprep/...` with tests

### 5.1 Package convention

```text
com.javaprep.day<XX>.task<YY>[.<subpackage>]
```

Examples: `com.javaprep.day07.task02`, `com.javaprep.day35.task01.repository`.

Test classes mirror the main package.

### 5.2 Plain Java task tree

```text
task-02-overloading-lab/
  TASK_INSTRUCTIONS.md
  EVALUATION_CRITERIA.md
  pom.xml
  src/
    main/java/com/javaprep/day07/task02/
      OverloadingLab.java            # stubs + TODOs
    test/java/com/javaprep/day07/task02/
      OverloadingLabTest.java
```

### 5.3 Spring Boot task tree

```text
task-03-student-rest-api/
  TASK_INSTRUCTIONS.md
  EVALUATION_CRITERIA.md
  pom.xml
  src/
    main/
      java/com/javaprep/day31/task03/
        Day31Task03Application.java
        controller/StudentController.java      # TODOs
        service/StudentService.java            # TODOs
        dto/StudentRequest.java
        dto/StudentResponse.java
        exception/GlobalExceptionHandler.java  # TODOs
      resources/
        application.yml                        # env-var placeholders only
    test/
      java/com/javaprep/day31/task03/
        controller/StudentControllerTest.java
      resources/
        application-test.yml                   # H2 PostgreSQL mode when JPA is used
```

### 5.4 JPA task additions

```text
  src/main/resources/db/migration/V1__init.sql     # from Day 35 (Flyway)
  src/test/resources/application-test.yml          # H2 PostgreSQL mode
```

### 5.5 Kafka task additions

```text
  src/main/java/.../event/OrderPlacedEvent.java
  src/main/java/.../producer/OrderProducer.java    # TODOs
  src/main/java/.../consumer/OrderConsumer.java    # TODOs
  src/test/java/.../OrderMessagingTest.java        # @EmbeddedKafka
```

### 5.6 SQL-script task tree (Days 25–26)

```text
task-02-joins-lab/
  TASK_INSTRUCTIONS.md
  EVALUATION_CRITERIA.md
  pom.xml
  sql/
    schema.sql
    seed.sql
    answers.sql                  # candidate fills (TODO markers as -- TODO(Day26-task02): ...)
  src/test/java/com/javaprep/day26/task02/
    JoinsLabTest.java            # runs answers.sql against H2 (PostgreSQL mode) via JDBC
```

In SQL files use: `-- TODO(Day26-task02): <instruction>`.

### 5.7 Microservice pair (Days 43–46)

Prefer a **single Maven project per task** that contains **two embedded Spring contexts or a simulated downstream** (e.g. `MockRestServiceServer`, WireMock-free stub controller on a random port). If two real services are needed, use a task folder with two sibling Maven projects:

```text
task-01-order-and-inventory/
  TASK_INSTRUCTIONS.md
  EVALUATION_CRITERIA.md
  order-service/        (pom.xml, src/...)
  inventory-service/    (pom.xml, src/...)
```

`mvn test` is run in each sub-project; document both commands. Tests must still run without Docker or external brokers.

---

## 6. TODO and stub conventions

### 6.1 TODO tag format

```text
TODO(DayXX-taskYY): <actionable instruction>
```

- Java: `// TODO(Day07-task02): ...` or `/** TODO(Day07-task02): ... */` above the member.
- SQL: `-- TODO(Day26-task02): ...`
- YAML/properties: `# TODO(Day29-task01): ...`
- `XX` and `YY` are two-digit and match the folder numbers.

### 6.2 Stub format (required)

Every unimplemented method **throws**:

```java
// TODO(Day07-task02): return the rectangle area; throw IllegalArgumentException if width or height is negative
public static int area(int width, int height) {
    throw new UnsupportedOperationException("TODO(Day07-task02): implement area(int, int)");
}
```

Rules:

- The exception message **starts with** `TODO(DayXX-taskYY):` and names the method/behavior.
- Do **not** return placeholder values (`0`, `null`, `""`) — tests could pass by accident.
- Constructors/fields that need work follow the same pattern; if a class must compile with fields only, leave a TODO comment and make the dependent method throw.
- TODO text is **actionable** and lists edge cases/exceptions expected.
- One TODO per missing behavior where practical.
- Spring `@Bean`/controller stubs also throw `UnsupportedOperationException`, so the context still loads unless the task is about wiring failures.

---

## 7. `TASK_INSTRUCTIONS.md` template (required headings)

```markdown
# Task <index> — <Title>

**Day:** XX · **Task ID:** DayXX-taskYY · **Type:** <Plain Java | Spring Boot | ...> · **Difficulty:** <Warm-up | Core | Stretch | Challenge>

## Summary
<2–4 sentences>

## Learning goals
- ...

## Provided files
| Path | Purpose |
|------|---------|

## Prerequisites
- Days / concepts to review

## What you will implement
Numbered, observable outcomes (each maps to at least one test).

## Constraints
- Allowed / forbidden APIs (e.g. "do not use streams", "do not use Lombok")
- Java 21; no Docker; no external services

## Step-by-step guidance
1. ...

## How to run and verify

### Prerequisites check
`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)
`mvn test`

### Run one test class
`mvn -Dtest=<ClassName>Test test`

### Run the app (Spring Boot tasks, optional)
`mvn spring-boot:run` — plus required env vars

### Manual checks
Checklist (e.g. `curl` commands with expected status/body)

## `TODO` map
| Location | TODO tag | "Done" means |
|----------|----------|--------------|

## Test map
| Requirement # | Test method(s) |
|--------------:|----------------|

## Edge cases to handle
- ...

## Submission checklist (Git)
- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day XX: ...`

## Hints (optional)
<details><summary>Hint 1</summary> ... </details>
```

Rules:

- Every requirement has a **Test map** entry or is explicitly marked **manual/rubric-only**.
- Every `TODO(DayXX-taskYY)` in code appears in the `TODO` map.
- State the initial **red** expectation (e.g. "`N` tests fail with `UnsupportedOperationException`").
- Tasks needing knowledge not yet taught must be labeled **Challenge (requires research)**.

---

## 8. `EVALUATION_CRITERIA.md` template (required headings)

```markdown
# Evaluation Criteria — Day XX — Task YY — <Title>

## Scope
What is graded vs out of scope.

## Weighting (100 points unless the instructor overrides)
| Category | Points | Description |
|----------|-------:|-------------|
| Automated tests (`mvn test`) | 40 | Fraction of tests passing; no skipped/@Disabled tests |
| Requirements coverage | 25 | Each "What you will implement" bullet satisfied |
| Code quality | 20 | Naming, structure, idiomatic Java 21, no duplication, correct use of the day's concepts |
| Robustness & safety | 10 | Edge cases, null/validation handling, exceptions, thread-safety/security where relevant |
| Readability & process | 5 | Clear commits, formatting, sensible comments |

## Pass / fail gates (automatic fail if violated)
- Tests modified/disabled to force a pass
- Hard-coded secrets
- Forbidden APIs from Constraints used
- Project does not compile

## Detailed rubric
### Automated tests
### Requirements coverage
### Code quality
### Robustness & safety
### Day-specific checks (e.g. "uses `equals`, not `==`, for Strings")

## Evidence the grader should collect
- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`, JaCoCo summary (Day 23+)

## AI-assisted grading prompt (optional)
Short paste-ready block.
```

Rules:

- Rubric items are **observable** and **file-scoped** (e.g. "`StudentService.create` rejects duplicate emails with `DuplicateEmailException`").
- Tests are the primary correctness signal but **never the only one**; include manual review items because tests can be gamed (hard-coded return values).
- Leftover `TODO` comments are **never** penalized when behavior is implemented (see `05`).

---

## 9. Boilerplate rules (all tasks)

1. `mvn -q test-compile` succeeds on boilerplate.
2. Stubs throw `UnsupportedOperationException("TODO(DayXX-taskYY): ...")`.
3. Tests are complete, readable, and deterministic; they serve as the specification.
4. Minimal surface: no unrelated starter code.
5. No secrets; config uses placeholders/env vars.
6. No committed `target/`, `.idea/`, `*.iml`.
7. Cross-platform: no shell scripts required; path handling via `Path`/`Files`.
8. Sources UTF-8; line endings LF.
9. Tests must not need network, Docker, a live PostgreSQL, or a live Kafka broker.

---

## 10. Consistency checklist (run before declaring a day complete)

- [ ] Folder number matches `DAY-XX-THEORY-AND-REFERENCE.md`
- [ ] Day `README.md` table matches actual tasks
- [ ] Each task has `TASK_INSTRUCTIONS.md`, `EVALUATION_CRITERIA.md`, `pom.xml`, `src/main/java`, `src/test/java`
- [ ] Package names follow `com.javaprep.dayXX.taskYY`
- [ ] Every `TODO(DayXX-taskYY)` appears in the `TODO` map and uses the correct IDs
- [ ] Every stub throws `UnsupportedOperationException("TODO(DayXX-taskYY): ...")`
- [ ] `mvn -q test-compile` passes for every task
- [ ] Reference solution (kept out of candidate tree) makes `mvn test` green
- [ ] No Spring in Days 01–27; no Docker/frontend anywhere
- [ ] Theory covers all required subtopic sections with ≥ 3 examples per major subtopic and includes Interview corner + Answers

---

## 11. Minimal `pom.xml` skeleton (plain Java)

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.javaprep</groupId>
  <artifactId>day07-task02-overloading-lab</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <packaging>jar</packaging>

  <properties>
    <maven.compiler.release>21</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <junit.version><!-- pinned in setup/VERSIONS.md --></junit.version>
    <assertj.version><!-- pinned --></assertj.version>
  </properties>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>org.junit</groupId>
        <artifactId>junit-bom</artifactId>
        <version>${junit.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependencies>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.assertj</groupId>
      <artifactId>assertj-core</artifactId>
      <version>${assertj.version}</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version><!-- pinned 3.x --></version>
      </plugin>
    </plugins>
  </build>
</project>
```

Agents replace comment placeholders with the concrete pinned versions from `setup/VERSIONS.md`.

---

## 12. Minimal Spring Boot `pom.xml` notes

- `<parent>` = `spring-boot-starter-parent` (pinned Boot 4.x), `<java.version>21</java.version>`.
- Include `spring-boot-maven-plugin`.
- `application.yml` uses `${ENV_VAR:default}` placeholders; defaults are obviously fake.
- Test profile config in `src/test/resources/application-test.yml` (H2 PostgreSQL mode).
- Verify actual starter artifact names for Boot 4 before use (see `02` §4.3).

---

## 13. Handoff note for AI agents

Treat this file as a **lintable spec**. When unsure, prefer **more explicit** `TASK_INSTRUCTIONS.md` text over assumptions, and keep tests the single source of truth for behavior.
