# Day 24 — Maven Lifecycle, Scopes & Plugins; Pattern Matching Recap; Core Java Review Challenge

## Learning objectives

- Explain Maven's three built-in lifecycles (clean, default, site), phases vs goals, and how plugin goals bind to phases for `jar` packaging
- Choose the right dependency scope (`compile`, `provided`, `runtime`, `test`, `system`/`import`) and predict which classpath each lands on
- Explain transitive dependencies, nearest-wins mediation, version ranges, exclusions, `dependencyManagement`, and BOM imports; inspect with `dependency:tree`
- Configure core plugins (compiler, surefire, failsafe, jar/shade, JaCoCo, enforcer) and profiles
- Use `instanceof` patterns, switch patterns with guards, record deconstruction patterns, and exhaustive switches over sealed hierarchies
- Combine records, streams, collections, generics, exceptions, `Optional`, and virtual threads in one coherent program

## Prerequisites

- Day 13-21 — exceptions, collections, generics, streams, concurrency
- Day 22 — virtual threads
- Day 23 — JUnit 5 and JaCoCo
- Days 4-5 — records and sealed types (Core Java)

## How to use this folder

1. Read [`DAY-24-THEORY-AND-REFERENCE.md`](DAY-24-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day24-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-maven-lifecycle-and-scopes` | Plain Java | `mvn test` |
| 2 | `task-02-maven-version-mediation` | Plain Java | `mvn test` |
| 3 | `task-03-pattern-matching-expressions` | Plain Java | `mvn test` |
| 4 | `task-04-core-java-inventory-challenge` | Plain Java | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Core Java
