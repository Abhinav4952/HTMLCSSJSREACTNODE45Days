# Java Backend Prep Course — Generation Instructions Index

This folder contains the **authoritative specifications** for generating a **50-day**, hands-on **Java backend preparation course**: Core Java 21, SQL/JDBC with PostgreSQL, Spring Boot 4, Spring Data JPA, Spring Security (JWT), testing, microservices (Gateway, Resilience4j, Kafka), and a capstone.

The documents are written for **human instructors** and **AI coding agents** that will create `JAVA PREP/Day 01` … `JAVA PREP/Day 50` in later phases.

## How to use this folder

1. Read the files **in numerical order** (`01` → `05`).
2. Do **not** skip `02` (repository, Git, technical constraints) or `03` (folder structure). Agents that skip them produce inconsistent repositories.
3. Treat the topic map in `04` as the **default schedule** unless the instructor publishes an override.
4. Use `05` when grading or when building grading aids.

## Files in this set

| File | Purpose |
|------|---------|
| [`01-COURSE-CONTEXT-LEARNING-OUTCOMES-AND-AGENT-MANDATE.md`](./01-COURSE-CONTEXT-LEARNING-OUTCOMES-AND-AGENT-MANDATE.md) | Audience, locked decisions, proficiency targets, pedagogy, topic inventory, agent mandate, quality bar. |
| [`02-REPOSITORY-GIT-WORKFLOW-AND-TECHNICAL-CONSTRAINTS.md`](./02-REPOSITORY-GIT-WORKFLOW-AND-TECHNICAL-CONSTRAINTS.md) | Repo layout, Git workflow, `.gitignore`, Maven rules, Java/Spring/DB/Kafka/test constraints, security checklist. |
| [`03-DAY-FOLDER-TASK-STRUCTURE-AND-NAMING-CONVENTIONS.md`](./03-DAY-FOLDER-TASK-STRUCTURE-AND-NAMING-CONVENTIONS.md) | Exact directory tree, file names, templates, TODO and stub conventions, Maven task skeletons. |
| [`04-AUTHORING-GUIDE-THEORY-PRACTICAL-TASKS-TESTS-AND-50-DAY-TOPIC-MAP.md`](./04-AUTHORING-GUIDE-THEORY-PRACTICAL-TASKS-TESTS-AND-50-DAY-TOPIC-MAP.md) | Task design principles, testing guidance, Spring/JPA/Kafka patterns, full **50-day topic map**, post-course projects. |
| [`05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`](./05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md) | 1–100 grading model, bands, feedback style, AI grading workflow and prompt. |

## Locked decisions (summary)

| Area | Decision |
|------|----------|
| Language / JDK | Java 21 LTS |
| Framework | Spring Boot 4 (Spring Framework 7) |
| Build | Maven |
| IDE | IntelliJ IDEA Community |
| Database | PostgreSQL 17 (local install, no Docker) |
| Persistence | Spring Data JPA (Hibernate) |
| Test DB | H2 in PostgreSQL mode |
| Messaging tests | `EmbeddedKafka` |
| Scope | Backend only: no frontend, no Docker |
| Tests | JUnit 5 + Mockito + AssertJ; verify with `mvn test` |
| Paths | `JAVA PREP/Day XX/` (`XX` = 01–50) |
| TODO format | `TODO(DayXX-taskYY): description` |
| Stubs | `throw new UnsupportedOperationException("TODO(DayXX-taskYY): ...")` |

## Out of scope for this folder

- The actual `Day XX` folders and task implementations are **not** created here.
- Post-course projects (StayEasy, PayFlow, PeopleHub) are only named here; their specs are a separate effort.

## Versioning

When these instructions change, bump **“Instruction set version”** at the top of `01` and add a row to the changelog at the bottom of `01`.

**Instruction set version:** `1.0.0` (initial)
