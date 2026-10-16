# Evaluation Criteria — Day 47 — Task 03 — Entity Relationships: User - Project - Task

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 47 Task 03 (`project-task-relationships`).

## Weighting (100 points)

| Category | Points |
|----------|-------:|
| Correctness (all tests green, requirements met) | 60 |
| Edge cases and error contracts | 20 |
| Code clarity (naming, simplicity, idiomatic Spring/SQL) | 15 |
| Git / hygiene (no `target/`, no secrets, only intended files changed) | 5 |

## Pass / fail gates (automatic fail if violated)

- Project does not compile or `mvn test` fails
- Tests, `pom.xml`, or provided helpers modified to force a pass
- Hard-coded answers that special-case test inputs
- Secrets or `target/` committed

## Detailed rubric

### Correctness

- Map `Project.owner` as a lazy mandatory `@ManyToOne` with `owner_id`.
- Map `Project.tasks` as `@OneToMany(mappedBy = "project", cascade = ALL, orphanRemoval = true)`.
- Map `TaskItem.project` as the owning `@ManyToOne` with `project_id`.
- Implement `addTask` / `removeTask` so both sides stay consistent.

### Edge cases

- Forgetting `mappedBy` creates a join table.
- Removing from the list without clearing the back reference.
- Lazy loading outside a transaction (not an issue inside `@DataJpaTest`).

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day47-task03)`

## AI grading prompt (paste into your grader)

```
You are grading Day 47 Task 03 (Entity Relationships: User - Project - Task) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
