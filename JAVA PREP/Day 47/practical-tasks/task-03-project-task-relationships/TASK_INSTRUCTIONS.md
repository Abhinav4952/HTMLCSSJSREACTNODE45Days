# Task 3 — Entity Relationships: User - Project - Task

**Day:** 47 · **Task ID:** Day47-task03 · **Type:** Spring Boot (JPA) · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Map the capstone's core relationships (many projects per user, many tasks per project) correctly: owning side, mappedBy, cascade, orphan removal and helper methods that keep both sides in sync.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day47/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task03/User.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task03/Project.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day47/task03/TaskItem.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day47/task03/ProjectRepository.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day47/task03/ProjectMappingTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 47 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Map `Project.owner` as a lazy mandatory `@ManyToOne` with `owner_id`.
2. Map `Project.tasks` as `@OneToMany(mappedBy = "project", cascade = ALL, orphanRemoval = true)`.
3. Map `TaskItem.project` as the owning `@ManyToOne` with `project_id`.
4. Implement `addTask` / `removeTask` so both sides stay consistent.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day47-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day47-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 47: complete task-03-project-task-relationships`.

## How to run and verify

```bash
java -version   # 21.x
mvn -v          # 3.9+
mvn test        # expected RED at the start
mvn -Dtest=<TestClass> test
```

## TODO map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `Project.java` | `Day47-task03` | map the owner: many projects belong to one User -> @ManyToOne(fetch = LAZY, optional = false) + @JoinColumn(name = "owner_id |
| `Project.java` | `Day47-task03` | one project has many tasks -> @OneToMany(mappedBy = "project", cascade = ALL, orphanRemoval = true |
| `Project.java` | `Day47-task03` | tasks.add(task); task.setProject(this |
| `Project.java` | `Day47-task03` | tasks.remove(task); task.setProject(null |
| `TaskItem.java` | `Day47-task03` | owning side of the relationship -> @ManyToOne(fetch = LAZY, optional = false) + @JoinColumn(name = "project_id |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `tasksArePersistedWithTheProjectAndReloaded` |
| 2 | `removingATaskDeletesItsRow` |
| 3 | `deletingTheProjectDeletesItsTasks` |
| 4 | `projectsCanBeFoundByOwner` |

## Edge cases to handle

- Forgetting `mappedBy` creates a join table.
- Removing from the list without clearing the back reference.
- Lazy loading outside a transaction (not an issue inside `@DataJpaTest`).

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 47: Entity Relationships: User - Project - Task`

## Hints (optional)

<details><summary>Hint 1</summary>
Annotations come from `jakarta.persistence`.
</details>

<details><summary>Hint 2</summary>
The `User` entity is provided and persisted by the test.
</details>
