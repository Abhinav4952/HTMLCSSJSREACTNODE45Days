# Task 3 — Many-to-Many: Students and Courses

**Day:** 34 · **Task ID:** Day34-task03 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Model many-to-many with an explicit join table, helper methods, no accidental cascade, and business-key equals/hashCode.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day34/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day34/task03/Student.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day34/task03/Course.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day34/task03/ManyToManyTest.java` | Provided helper or test (do not edit) |
| `src/test/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 34 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Map `Student.courses` (owning, join table `enrollments`) and `Course.students` (inverse).
2. Implement `enroll`/`drop` and `Course.equals/hashCode` on the business key `code`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day34-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day34-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 34: complete task-03-many-to-many-enrollment`.

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
| `Student.java` | `Day34-task03` | owning side of the many-to-many: join table enrollments(student_id, course_id); NO cascade |
| `Student.java` | `Day34-task03` | add to both sides |
| `Student.java` | `Day34-task03` | remove from both sides |
| `Course.java` | `Day34-task03` | inverse side: mappedBy courses |
| `Course.java` | `Day34-task03` | equal when same class and equal code |
| `Course.java` | `Day34-task03` | consistent with equals (use the code |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `enrollWritesJoinTableRows` |
| 2 | `dropRemovesOnlyTheLink` |
| 3 | `deletingStudentKeepsCoursesButClearsLinks` |
| 4 | `noCascadeFromStudentToCourse` |
| 5 | `courseEqualityUsesBusinessKey` |

## Edge cases to handle

- Never cascade REMOVE on many-to-many: it deletes shared rows.
- Use `Set`, not `List`, to avoid delete-all/re-insert of join rows.
- Two courses with null codes are not equal.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 34: Many-to-Many: Students and Courses`

## Hints (optional)

<details><summary>Hint 1</summary>
`mappedBy` points at the field name on the owning side.
</details>

<details><summary>Hint 2</summary>
`Objects.hashCode(code)` is null-safe.
</details>
